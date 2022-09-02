package com.example.smarthouse;





import android.util.Log;

import com.squareup.okhttp.Callback;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.Response;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class UbidotsClient {

    private com.example.smarthouse.UbidotsClient.UbiListener listener;

    public com.example.smarthouse.UbidotsClient.UbiListener getListener() {
        return listener;
    }

    public void setListener(com.example.smarthouse.UbidotsClient.UbiListener listener) {
        this.listener = listener;
    }

    public void handleUbidots( String apiKey, String rariable, final com.example.smarthouse.UbidotsClient.UbiListener listener) {

        final List<com.example.smarthouse.UbidotsClient.Value> results = new ArrayList<>();

        OkHttpClient client = new OkHttpClient();
        Request req = new Request.Builder().addHeader("X-Auth-Token", apiKey)
                .url("http://things.ubidots.com/api/v1.6/devices/RaspberryPi/" + rariable)
                .build();

        client.newCall(req).enqueue(new Callback() {
            @Override
            public void onFailure(Request request, IOException e) {
                Log.d("ubidots", "Network error");
                e.printStackTrace();
            }

            @Override
            public void onResponse(Response response) throws IOException {
                String body = response.body().string();
                Log.d("ubidots", body);

                try {
                    JSONObject jObj = new JSONObject(body);
                    JSONObject jObj1=jObj.getJSONObject("last_value");
                    String val=jObj1.getString("value");
                    Value val1= new Value();
                    val1.value=Float.parseFloat(val);
                    results.add(val1);
                    listener.onDataReady(results);

                }
                catch(JSONException jse) {
                    jse.printStackTrace();
                }
            }
        });

    }
    protected static class Value {
        float value;
    }

    protected interface  UbiListener {
        public void onDataReady(List<com.example.smarthouse.UbidotsClient.Value> result);
    }
}
