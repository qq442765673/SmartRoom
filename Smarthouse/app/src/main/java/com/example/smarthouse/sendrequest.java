package com.example.smarthouse;

import static android.content.ContentValues.TAG;

import android.content.Context;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;


public class sendrequest extends AppCompatActivity {
    public RequestQueue mRequestQueue;
    public StringRequest stringRequest;
    public String url = "https://industrial.ubidots.com/api/v1.6/devices/raspberrypi/?token=BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk&_method=post&";
    ;

    public void send(Context context, String control, int value) {
        String urlfin = url + control + "=" + value;

        Log.i(TAG, "urlfin : " + urlfin.toString());

        mRequestQueue = Volley.newRequestQueue(context);
        stringRequest = new StringRequest(Request.Method.GET, urlfin, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Log.i(TAG, "Response : " + response.toString());


            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.i(TAG, "Error" + error.toString());
            }
        });
        mRequestQueue.add(stringRequest);

    }
}

