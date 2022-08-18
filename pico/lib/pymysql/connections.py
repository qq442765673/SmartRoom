# Python implementation of the MySQL client-server protocol
# http://dev.mysql.com/doc/internals/en/client-server-protocol.html
# Error codes:
# https://dev.mysql.com/doc/refman/5.5/en/error-handling.html
import errno
import os
import socket
import struct
import sys
import traceback
import warnings

from . import _auth

from .charset import charset_by_name, charset_by_id
from .constants import CLIENT, COMMAND, CR, FIELD_TYPE, SERVER_STATUS
from . import converters
from .cursors import Cursor
from .optionfile import Parser
from .protocol import (
    dump_packet,
    MysqlPacket,
    FieldDescriptorPacket,
    OKPacketWrapper,
    EOFPacketWrapper,
    LoadLocalPacketWrapper,
)
from . import err, VERSION_STRING

try:
    import ssl

    SSL_ENABLED = True
except ImportError:
    ssl = None
    SSL_ENABLED = False

try:
    import getpass

    DEFAULT_USER = getpass.getuser()
    del getpass
except (ImportError, KeyError):
    # KeyError occurs when there's no entry in OS database for a current user.
    DEFAULT_USER = None

DEBUG = False

TEXT_TYPES = {
    FIELD_TYPE.BIT,
    FIELD_TYPE.BLOB,
    FIELD_TYPE.LONG_BLOB,
    FIELD_TYPE.MEDIUM_BLOB,
    FIELD_TYPE.STRING,
    FIELD_TYPE.TINY_BLOB,
    FIELD_TYPE.VAR_STRING,
    FIELD_TYPE.VARCHAR,
    FIELD_TYPE.GEOMETRY,
}


DEFAULT_CHARSET = "utf8mb4"

MAX_PACKET_LEN = 2 ** 24 - 1


def _pack_int24(n):
    return struct.pack("<I", n)[:3]


# https://dev.mysql.com/doc/internals/en/integer.html#packet-Protocol::LengthEncodedInteger
def _lenenc_int(i):
    if i < 0:
        raise ValueError(
            "Encoding %d is less than 0 - no representation in LengthEncodedInteger" % i
        )
    elif i < 0xFB:
        return bytes([i])
    elif i < (1 << 16):
        return b"\xfc" + struct.pack("<H", i)
    elif i < (1 << 24):
        return b"\xfd" + struct.pack("<I", i)[:3]
    elif i < (1 << 64):
        return b"\xfe" + struct.pack("<Q", i)
    else:
        raise ValueError(
            "Encoding %x is larger than %x - no representation in LengthEncodedInteger"
            % (i, (1 << 64))
        )


class Connection:
    """
    Representation of a socket with a mysql server.

    The proper way to get an instance of this class is to call
    connect().

    Establish a connection to the MySQL database. Accepts several
    arguments:

    :param host: Host where the database server is located
    :param user: Username to log in as
    :param password: Password to use.
    :param database: Database to use, None to not use a particular one.
    :param port: MySQL port to use, default is usually OK. (default: 3306)
    :param bind_address: When the client has multiple network interfaces, specify
        the interface from which to connect to the host. Argument can be
        a hostname or an IP address.
    :param unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
    :param read_timeout: The timeout for reading from the connection in seconds (default: None - no timeout)
    :param write_timeout: The timeout for writing to the connection in seconds (default: None - no timeout)
    :param charset: Charset you want to use.
    :param sql_mode: Default SQL_MODE to use.
    :param read_default_file:
        Specifies  my.cnf file to read these parameters from under the [client] section.
    :param conv:
        Conversion dictionary to use instead of the default one.
        This is used to provide custom marshalling and unmarshalling of types.
        See converters.
    :param use_unicode:
        Whether or not to default to unicode strings.
        This option defaults to true.
    :param client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
    :param cursorclass: Custom cursor class to use.
    :param init_command: Initial SQL statement to run when connection is established.
    :param connect_timeout: Timeout before throwing an exception when connecting.
        (default: 10, min: 1, max: 31536000)
    :param ssl:
        A dict of arguments similar to mysql_ssl_set()'s parameters.
    :param ssl_ca: Path to the file that contains a PEM-formatted CA certificate
    :param ssl_cert: Path to the file that contains a PEM-formatted client certificate
    :param ssl_disabled: A boolean value that disables usage of TLS
    :param ssl_key: Path to the file that contains a PEM-formatted private key for the client certificate
    :param ssl_verify_cert: Set to true to check the validity of server certificates
    :param ssl_verify_identity: Set to true to check the server's identity
    :param read_default_group: Group to read from in the configuration file.
    :param autocommit: Autocommit mode. None means use server default. (default: False)
    :param local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)
    :param max_allowed_packet: Max size of packet sent to server in bytes. (default: 16MB)
        Only used to limit size of "LOAD LOCAL INFILE" data packet smaller than default (16KB).
    :param defer_connect: Don't explicitly connect on construction - wait for connect call.
        (default: False)
    :param auth_plugin_map: A dict of plugin names to a class that processes that plugin.
        The class will take the Connection object as the argument to the constructor.
        The class needs an authenticate method taking an authentication packet as
        an argument.  For the dialog plugin, a prompt(echo, prompt) method can be used
        (if no authenticate method) for returning a string from the user. (experimental)
    :param server_public_key: SHA256 authentication plugin public key value. (default: None)
    :param binary_prefix: Add _binary prefix on bytes and bytearray. (default: False)
    :param compress: Not supported
    :param named_pipe: Not supported
    :param db: **DEPRECATED** Alias for database.
    :param passwd: **DEPRECATED** Alias for password.

    See `Connection <https://www.python.org/dev/peps/pep-0249/#connection-objects>`_ in the
    specification.
    """

    _sock = None
    _auth_plugin_name = ""
    _closed = False
    _secure = False

    def __init__(
        self,
        *,
        user=None,  # The first four arguments is based on DB-API 2.0 recommendation.
        password="",
        host=None,
        database=None,
        unix_socket=None,
        port=0,
        charset="",
        sql_mode=None,
        read_default_file=None,
        conv=None,
        use_unicode=True,
        client_flag=0,
        cursorclass=Cursor,
        init_command=None,
        connect_timeout=10,
        read_default_group=None,
        autocommit=False,
        local_infile=False,
        max_allowed_packet=16 * 1024 * 1024,
        defer_connect=False,
        auth_plugin_map=None,
        read_timeout=None,
        write_timeout=None,
        bind_address=None,
        binary_prefix=False,
        program_name=None,
        server_public_key=None,
        ssl=None,
        ssl_ca=None,
        ssl_cert=None,
        ssl_disabled=None,
        ssl_key=None,
        ssl_verify_cert=None,
        ssl_verify_identity=None,
        compress=None,  # not supported
        named_pipe=None,  # not supported
        passwd=None,  # deprecated
        db=None,  # deprecated
    ):
        if db is not None and database is None:
            # We will raise warining in 2022 or later.
            # See https://github.com/PyMySQL/PyMySQL/issues/939
            # warnings.warn("'db' is deprecated, use 'database'", DeprecationWarning, 3)
            database = db
        if passwd is not None and not password:
            # We will raise warining in 2022 or later.
            # See https://github.com/PyMySQL/PyMySQL/issues/939
            # warnings.warn(
            #    "'passwd' is deprecated, use 'password'", DeprecationWarning, 3
            # )
            password = passwd

        if compress or named_pipe:
            raise NotImplementedError(
                "compress and named_pipe arguments are not supported"
            )

        self._local_infile = bool(local_infile)
        if self._local_infile:
            client_flag |= CLIENT.LOCAL_FILES

        if read_default_group and not read_default_file:
            if sys.platform.startswith("win"):
                read_default_file = "c:\\my.ini"
            else:
                read_default_file = "/etc/my.cnf"

        if read_default_file:
            if not read_default_group:
                read_default_group = "client"

            cfg = Parser()
            cfg.read(os.path.expanduser(read_default_file))

            def _config(key, arg):
                if arg:
                    return arg
                try:
                    return cfg.get(read_default_group, key)
                except Exception:
                    return arg

            user = _config("user", user)
            password = _config("password", password)
            host = _config("host", host)
            database = _config("database", database)
            unix_socket = _config("socket", unix_socket)
            port = int(_config("port", port))
            bind_address = _config("bind-address", bind_address)
            charset = _config("default-character-set", charset)
            if not ssl:
                ssl = {}
            if isinstance(ssl, dict):
                for key in ["ca", "capath", "cert", "key", "cipher"]:
                    value = _config("ssl-" + key, ssl.get(key))
                    if value:
                        ssl[key] = value

        self.ssl = False
        if not ssl_disabled:
            if ssl_ca or ssl_cert or ssl_key or ssl_verify_cert or ssl_verify_identity:
                ssl = {
                    "ca": ssl_ca,
                    "check_hostname": bool(ssl_verify_identity),
                    "verify_mode": ssl_verify_cert
                    if ssl_verify_cert is not None
                    else False,
                }
                if ssl_cert is not None:
                    ssl["cert"] = ssl_cert
                if ssl_key is not None:
                    ssl["key"] = ssl_key
            if ssl:
                if not SSL_ENABLED:
                    raise NotImplementedError("ssl module not found")
                self.ssl = True
                client_flag |= CLIENT.SSL
                self.ctx = self._create_ssl_ctx(ssl)

        self.host = host or "localhost"
        self.port = port or 3306
        if type(self.port) is not int:
            raise ValueError("port should be of type int")
        self.user = user or DEFAULT_USER
        self.password = password or b""
        if isinstance(self.password, str):
            self.password = self.password.encode("latin1")
        self.db = database
        self.unix_socket = unix_socket
        self.bind_address = bind_address
        if not (0 < connect_timeout <= 31536000):
            raise ValueError("connect_timeout should be >0 and <=31536000")
        self.connect_timeout = connect_timeout or None
        if read_timeout is not None and read_timeout <= 0:
            raise ValueError("read_timeout should be > 0")
        self._read_timeout = read_timeout
        if write_timeout is not None and write_timeout <= 0:
            raise ValueError("write_timeout should be > 0")
        self._write_timeout = write_timeout

        self.charset = charset or DEFAULT_CHARSET
        self.use_unicode = use_unicode

        self.encoding = charset_by_name(self.charset).encoding

        client_flag |= CLIENT.CAPABILITIES
        if self.db:
            client_flag |= CLIENT.CONNECT_WITH_DB

        self.client_flag = client_flag

        self.cursorclass = cursorclass

        self._result = None
        self._affected_rows = 0
        self.host_info = "Not connected"

        # specified autocommit mode. None means use server default.
        self.autocommit_mode = autocommit

        if conv is None:
            conv = converters.conversions

        # Need for MySQLdb compatibility.
        self.encoders = {k: v for (k, v) in conv.items() if type(k) is not int}
        self.decoders = {k: v for (k, v) in conv.items() if type(k) is int}
        self.sql_mode = sql_mode
        self.init_command = init_command
        self.max_allowed_packet = max_allowed_packet
        self._auth_plugin_map = auth_plugin_map or {}
        self._binary_prefix = binary_prefix
        self.server_public_key = server_public_key

        self._connect_attrs = {
            "_client_name": "pymysql",
            "_pid": str(os.getpid()),
            "_client_version": VERSION_STRING,
        }

        if program_name:
            self._connect_attrs["program_name"] = program_name

        if defer_connect:
            self._sock = None
        else:
            self.connect()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()

    def _create_ssl_ctx(self, sslp):
        if isinstance(sslp, ssl.SSLContext):
            return sslp
        ca = sslp.get("ca")
        capath = sslp.get("capath")
        hasnoca = ca is None and capath is None
        ctx = ssl.create_default_context(cafile=ca, capath=capath)
        ctx.check_hostname = not hasnoca and sslp.get("check_hostname", True)
        verify_mode_value = sslp.get("verify_mode")
        if verify_mode_value is None:
            ctx.verify_mode = ssl.CERT_NONE if hasnoca else ssl.CERT_REQUIRED
        elif isinstance(verify_mode_value, bool):
            ctx.verify_mode = ssl.CERT_REQUIRED if verify_mode_value else ssl.CERT_NONE
        else:
            if isinstance(verify_mode_value, str):
                verify_mode_value = verify_mode_value.lower()
            if verify_mode_value in ("none", "0", "false", "no"):
                ctx.verify_mode = ssl.CERT_NONE
            elif verify_mode_value == "optional":
                ctx.verify_mode = ssl.CERT_OPTIONAL
            elif verify_mode_value in ("required", "1", "true", "yes"):
                ctx.verify_mode = ssl.CERT_REQUIRED
            else:
                ctx.verify_mode = ssl.CERT_NONE if hasnoca else ssl.CERT_REQUIRED
        if "cert" in sslp:
            ctx.load_cert_chain(sslp["cert"], keyfile=sslp.get("key"))
        if "cipher" in sslp:
            ctx.set_ciphers(sslp["cipher"])
        ctx.options |= ssl.OP_NO_SSLv2
        ctx.options |= ssl.OP_NO_SSLv3
        return ctx

    def close(self):
        """
        Send the quit message and close the socket.

        See `Connection.close() <https://www.python.org/dev/peps/pep-0249/#Connection.close>`_
        in the specification.

        :raise Error: If the connection is already closed.
        """
        if self._closed:
            raise err.Error("Already closed")
        self._closed = True
        if self._sock is None:
            return
        send_data = struct.pack("<iB", 1, COMMAND.COM_QUIT)
        try:
            self._write_bytes(send_data)
        except Exception:
            pass
        finally:
            self._force_close()

    @property
    def open(self):
        """Return True if the connection is open"""
        return self._sock is not None

    def _force_close(self):
        """Close connection without QUIT message"""
        if self._sock:
            try:
                self._sock.close()
            except:  # noqa
                pass
        self._sock = None
        self._rfile = None

    __del__ = _force_close

    def autocommit(self, value):
        self.autocommit_mode = bool(value)
        current = self.get_autocommit()
        if value != current:
            self._send_autocommit_mode()

    def get_autocommit(self):
        return bool(self.server_status & SERVER_STATUS.SERVER_STATUS_AUTOCOMMIT)

    def _read_ok_packet(self):
        pkt = self._read_packet()
        if not pkt.is_ok_packet():
            raise err.OperationalError(2014, "Command Out of Sync")
        ok = OKPacketWrapper(pkt)
        self.server_status = ok.server_status
        return ok

    def _send_autocommit_mode(self):
        """Set whether or not to commit after every execute()"""
        self._execute_command(
            COMMAND.COM_QUERY, "SET AUTOCOMMIT = %s" % self.escape(self.autocommit_mode)
        )
        self._read_ok_packet()

    def begin(self):
        """Begin transaction."""
        self._execute_command(COMMAND.COM_QUERY, "BEGIN")
        self._read_ok_packet()

    def commit(self):
        """
        Commit changes to stable storage.

        See `Connection.commit() <https://www.python.org/dev/peps/pep-0249/#commit>`_
        in the specification.
        """
        self._execute_command(COMMAND.COM_QUERY, "COMMIT")
        self._read_ok_packet()

    def rollback(self):
        """
        Roll back the current transaction.

        See `Connection.rollback() <https://www.python.org/dev/peps/pep-0249/#rollback>`_
        in the specification.
        """
        self._execute_command(COMMAND.COM_QUERY, "ROLLBACK")
        self._read_ok_packet()

    def show_warnings(self):
        """Send the "SHOW WARNINGS" SQL command."""
        self._execute_command(COMMAND.COM_QUERY, "SHOW WARNINGS")
        result = MySQLResult(self)
        result.read()
        return result.rows

    def select_db(self, db):
        """
        Set current db.

        :param db: The name of the db.
        """
        self._execute_command(COMMAND.COM_INIT_DB, db)
        self._read_ok_packet()

    def escape(self, obj, mapping=None):
        """Escape whatever value you pass to it.

        Non-standard, for internal use; do not use this in your applications.
        """
        if isinstance(obj, str):
            return "'" + self.escape_string(obj) + "'"
        if isinstance(obj, (bytes, bytearray)):
            ret = self._quote_bytes(obj)
            if self._binary_prefix:
                ret = "_binary" + ret
            return ret
        return converters.escape_item(obj, self.charset, mapping=mapping)

    def literal(self, obj):
        """Alias for escape()

        Non-standard, for internal use; do not use this in your applications.
        """
        return self.escape(obj, self.encoders)

    def escape_string(self, s):
        if self.server_status & SERVER_STATUS.SERVER_STATUS_NO_BACKSLASH_ESCAPES:
            return s.replace("'", "''")
        return converters.escape_string(s)

    def _quote_bytes(self, s):
        if self.server_status & SERVER_STATUS.SERVER_STATUS_NO_BACKSLASH_ESCAPES:
            return "'%s'" % (s.replace(b"'", b"''").decode("ascii", "surrogateescape"),)
        return converters.escape_bytes(s)

    def cursor(self, cursor=None):
        """
        Create a new cursor to execute queries with.

        :param cursor: The type of cursor to create; one of :py:class:`Cursor`,
            :py:class:`SSCursor`, :py:class:`DictCursor`, or :py:class:`SSDictCursor`.
            None means use Cursor.
        """
        if cursor:
            return cursor(self)
        return self.cursorclass(self)

    # The following methods are INTERNAL USE ONLY (called from Cursor)
    def query(self, sql, unbuffered=False):
        # if DEBUG:
        #     print("DEBUG: sending query:", sql)
        if isinstance(sql, str):
            sql = sql.encode(self.encoding, "surrogateescape")
        self._execute_command(COMMAND.COM_QUERY, sql)
        self._affected_rows = self._read_query_result(unbuffered=unbuffered)
        return self._affected_rows

    def next_result(self, unbuffered=False):
        self._affected_rows = self._read_query_result(unbuffered=unbuffered)
        return self._affected_rows

    def affected_rows(self):
        return self._affected_rows

    def kill(self, thread_id):
        arg = struct.pack("<I", thread_id)
        self._execute_command(COMMAND.COM_PROCESS_KILL, arg)
        return self._read_ok_packet()

    def ping(self, reconnect=True):
        """
        Check if the server is alive.

        :param reconnect: If the connection is closed, reconnect.
        :raise Error: If the connection is closed and reconnect=False.
        """
        if self._sock is None:
            if reconnect:
                self.connect()
                reconnect = False
            else:
                raise err.Error("Already closed")
        try:
            self._execute_command(COMMAND.COM_PING, "")
            self._read_ok_packet()
        except Exception:
            if reconnect:
                self.connect()
                self.ping(False)
            else:
                raise

    def set_charset(self, charset):
        # Make sure charset is supported.
        encoding = charset_by_name(charset).encoding

        self._execute_command(COMMAND.COM_QUERY, "SET NAMES %s" % self.escape(charset))
        self._read_packet()
        self.charset = charset
        self.encoding = encoding

    def connect(self, sock=None):
        self._closed = False
        try:
            if sock is None:
                if self.unix_socket:
                    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    sock.settimeout(self.connect_timeout)
                    sock.connect(self.unix_socket)
                    self.host_info = "Localhost via UNIX socket"
                    self._secure = True
                    if DEBUG:
                        print("connected using unix_socket")
                else:
                    kwargs = {}
                    if self.bind_address is not None:
                        kwargs["source_address"] = (self.bind_address, 0)
                    while True:
                        try:
                            sock = socket.create_connection(
                                (self.host, self.port), self.connect_timeout, **kwargs
                            )
                            break
                        except (OSError, IOError) as e:
                            if e.errno == errno.EINTR:
                                continue
                            raise
                    self.host_info = "socket %s:%d" % (self.host, self.port)
                    if DEBUG:
                        print("connected using socket")
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                sock.settimeout(None)

            self._sock = sock
            self._rfile = sock.makefile("rb")
            self._next_seq_id = 0

            self._get_server_information()
            self._request_authentication()

            if self.sql_mode is not None:
                c = self.cursor()
                c.execute("SET sql_mode=%s", (self.sql_mode,))

            if self.init_command is not None:
                c = self.cursor()
                c.execute(self.init_command)
                c.close()
                self.commit()

            if self.autocommit_mode is not None:
                self.autocommit(self.autocommit_mode)
        except BaseException as e:
            self._rfile = None
            if sock is not None:
                try:
                    sock.close()
                except:  # noqa
                    pass

            if isinstance(e, (OSError, IOError, socket.error)):
                exc = err.OperationalError(
                    2003, "Can't connect to MySQL server on %r (%s)" % (self.host, e)
                )
                # Keep original exception and traceback to investigate error.
                exc.original_exception = e
                exc.traceback = traceback.format_exc()
                if DEBUG:
                    print(exc.traceback)
                raise exc

            # If e is neither DatabaseError or IOError, It's a bug.
            # But raising AssertionError hides original error.
            # So just reraise it.
            raise

    def write_packet(self, payload):
        """Writes an entire "mysql packet" in its entirety to the network
        adding its length and sequence number.
        """
        # Internal note: when you build packet manually and calls _write_bytes()
        # directly, you should set self._next_seq_id properly.
        data = _pack_int24(len(payload)) + bytes([self._next_seq_id]) + payload
        if DEBUG:
            dump_packet(data)
        self._write_bytes(data)
        self._next_seq_id = (self._next_seq_id + 1) % 256

    def _read_packet(self, packet_type=MysqlPacket):
        """Read an entire "mysql packet" in its entirety from the network
        and return a MysqlPacket type that represents the results.

        :raise OperationalError: If the connection to the MySQL server is lost.
        :raise InternalError: If the packet sequence number is wrong.
        """
        buff = bytearray()
        while True:
            packet_header = self._read_bytes(4)
            # if DEBUG: dump_packet(packet_header)

            btrl, btrh, packet_number = struct.unpack("<HBB", packet_header)
            bytes_to_read = btrl + (btrh << 16)
            if packet_number != self._next_seq_id:
                self._force_close()
                if packet_number == 0:
                    # MariaDB sends error packet with seqno==0 when shutdown
                    raise err.OperationalError(
                        CR.CR_SERVER_LOST,
                        "Lost connection to MySQL server during query",
                    )
                raise err.InternalError(
                    "Packet sequence number wrong - got %d expected %d"
                    % (packet_number, self._next_seq_id)
                )
            self._next_seq_id = (self._next_seq_id + 1) % 256

            recv_data = self._read_bytes(bytes_to_read)
            if DEBUG:
                dump_packet(recv_data)
            buff += recv_data
            # https://dev.mysql.com/doc/internals/en/sending-more-than-16mbyte.html
            if bytes_to_read == 0xFFFFFF:
                continue
            if bytes_to_read < MAX_PACKET_LEN:
                break

        packet = packet_type(bytes(buff), self.encoding)
        if packet.is_error_packet():
            if self._result is not None and self._result.unbuffered_active is True:
                self._result.unbuffered_active = False
            packet.raise_for_error()
        return packet

    def _read_bytes(self, num_bytes):
        self._sock.settimeout(self._read_timeout)
        while True:
            try:
                data = self._rfile.read(num_bytes)
                break
            except (IOError, OSError) as e:
                if e.errno == errno.EINTR:
                    continue
                self._force_close()
                raise err.OperationalError(
                    CR.CR_SERVER_LOST,
                    "Lost connection to MySQL server during query (%s)" % (e,),
                )
            except BaseException:
                # Don't convert unknown exception to MySQLError.
                self._force_close()
                raise
        if len(data) < num_bytes:
            self._force_close()
            raise err.OperationalError(
                CR.CR_SERVER_LOST, "Lost connection to MySQL server during query"
            )
        return data

    def _write_bytes(self, data):
        self._sock.settimeout(self._write_timeout)
        try:
            self._sock.sendall(data)
        except IOError as e:
            self._force_close()
            raise err.OperationalError(
                CR.CR_SERVER_GONE_ERROR, "MySQL server has gone away (%r)" % (e,)
            )

    de