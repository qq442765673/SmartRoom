package com.example.smarthouse;

import static android.content.ContentValues.TAG;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;


import java.text.SimpleDateFormat;


public class MainActivity extends AppCompatActivity {

    public static final String EXTRA_MESSAGE = "com.example.myfirstapp.MESSAGE";
    private String API_KEY = "BBFF-VFK6z72XVCSg4ioLSyqbPz3u67UzKk";
    private String tempVarId = "temperature";
    private String humVarId = "humidity";
    private String LightId = "light";
    private String MotionId = "motion";
    private String LightswtichId = "lightswitch";
    private String fanswtichId = "fanswitch";
    private String autofanId = "autofan";
    private String autolightId = "autolight";
    private static final SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
    public String temperature = "0";
    public String Humidity = "0";
    public String Lightsens = "0";
    public Float Motion = 0f;
    public Float Lightswtich = 0f;
    public Float fanswtich = 0f;
    public Float autofan = 0f;
    public Float autolight = 0f;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Update();

        Button button = (Button) findViewById(R.id.update);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Update();
            }
        });

    }

    public void Update()
    {
        (new UbidotsClient()).handleUbidots( API_KEY,tempVarId, result -> {
            Log.d("tempVarId", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            temperature = String.valueOf(ccc);
        });
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView tempureturetext = (TextView) findViewById(R.id.textView5);
                Log.d("tempure", temperature);
                tempureturetext.setText(temperature);
            }

        }, 2000);

        (new UbidotsClient()).handleUbidots( API_KEY,humVarId, result -> {
            Log.d("humVarId", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Humidity = String.valueOf(ccc);
        });
        Handler handler1 = new Handler();
        handler1.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Humiditytext = (TextView) findViewById(R.id.textView6);
                Log.d("Humidity", Humidity);
                Humiditytext.setText(Humidity);
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots( API_KEY,LightId, result -> {
            Log.d("LightId", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Lightsens = String.valueOf(ccc);
        });
        Handler handler2 = new Handler();
        handler2.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Lightsenstext = (TextView) findViewById(R.id.textView7);
                Log.d("Lightsens", Lightsens);
                Lightsenstext.setText(Lightsens);
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots( API_KEY, LightswtichId,result -> {
            Log.d("LightswtichId", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Lightswtich = ccc;
        });
        Handler handler3 = new Handler();
        handler3.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Lightswtichtext = (TextView) findViewById(R.id.textView8);
                Log.d("Lightswtich", Lightswtich.toString());
                if(Lightswtich==1){
                    Lightswtichtext.setText("on");
                }
                else if (Lightswtich==0){
                    Lightswtichtext.setText("off");
                }
                else {
                    Lightswtichtext.setText("error");
                }
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots( API_KEY,fanswtichId, result -> {
            Log.d("fanswtichId", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            fanswtich = ccc;
        });
        Handler handler4 = new Handler();
        handler4.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView fanswtichtext = (TextView) findViewById(R.id.textView9);
                Log.d("fanswtich", fanswtich.toString());
                if(fanswtich==1){
                    fanswtichtext.setText("on");
                }
                else if (fanswtich==0){
                    fanswtichtext.setText("off");
                }
                else {
                    fanswtichtext.setText("error");
                }
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots( API_KEY,MotionId, result -> {
            Log.d("MotionId", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            Motion = ccc;
        });
        Handler handler5 = new Handler();
        handler5.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView Motiontext = (TextView) findViewById(R.id.textView11);
                Log.d("Motion", Motion.toString());
                if(Motion==1){
                    Motiontext.setText("Occupied");
                }
                else if (Motion==0){
                    Motiontext.setText("Empty");
                }
                else {
                    Motiontext.setText("error");
                }
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(API_KEY, autofanId, result -> {
            Log.d("autofanId", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            autofan = ccc;
        });
        Handler handler6 = new Handler();
        handler6.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView autofantext = (TextView) findViewById(R.id.textView19);
                Log.d("autofan", autofan.toString());
                if(autofan==1){
                    autofantext.setText("on");
                }
                else if (autofan==0){
                    autofantext.setText("off");
                }
                else {
                    autofantext.setText("error");
                }
            }
        }, 2000);

        (new UbidotsClient()).handleUbidots(API_KEY,autolightId,  result -> {
            Log.d("autolightId", "======== On data Ready ===========");
            float ccc = result.get(0).value;
            autolight = ccc;
        });
        Handler handler7 = new Handler();
        handler7.postDelayed(new Runnable() {
            @Override
            public void run() {
                TextView autolighttext = (TextView) findViewById(R.id.textView18);
                Log.d("autolightId", autolight.toString());
                if(autolight==1){
                    autolighttext.setText("on");
                }
                else if (autolight==0){
                    autolighttext.setText("off");
                }
                else {
                    autolighttext.setText("error");
                }

            }

        }, 2000);

        Toast.makeText(this,"Updating",Toast.LENGTH_SHORT).show();
    }

    public void lighswitch (View view) throws InterruptedException {
        String respcodes = null;
        TextView Lightswtichtext = (TextView) findViewById(R.id.textView8);
        sendrequest sendrequest1= new  sendrequest();
        Log.d(TAG, "sendrequest1: " +Lightswtichtext.getText());
        if (Lightswtichtext.getText()=="on")
        {
            sendrequest1.send(this,"lightswitch",0);
            }
        else {
            sendrequest1.send(this,"lightswitch",1);
            }

        Toast.makeText(this,"Send Success ",Toast.LENGTH_SHORT).show();
        Thread.sleep(2000);
        Update();
    }

    public void fanswitch (View view) throws InterruptedException {
        TextView fanswtichtext = (TextView) findViewById(R.id.textView9);
        sendrequest sendrequest1= new  sendrequest();
        Log.d(TAG, "sendrequest1: " +fanswtichtext.getText());
        if (fanswtichtext.getText()=="on")
        {
            sendrequest1.send(this,"fanswitch",0);}
        else {
            sendrequest1.send(this,"fanswitch",1);}
        Toast.makeText(this,"Send Success ",Toast.LENGTH_SHORT).show();
        Thread.sleep(2000);
        Update();

    }

    public void AutoLight (View view) throws InterruptedException {
        TextView AutoLightswtichtext = (TextView) findViewById(R.id.textView18);
        sendrequest sendrequest1= new  sendrequest();
        Log.d(TAG, "sendrequest1: " +AutoLightswtichtext.getText());
        if (AutoLightswtichtext.getText()=="on")
        {
            sendrequest1.send(this,"AutoLight",0);}
        else {
            sendrequest1.send(this,"AutoLight",1);}

        Toast.makeText(this,"Send Success ",Toast.LENGTH_SHORT).show();
        Thread.sleep(2000);
        Update();
    }


    public void Autofan (View view) throws InterruptedException {
        TextView Autofanswtichtext = (TextView) findViewById(R.id.textView19);
        sendrequest sendrequest1= new  sendrequest();
        Log.d(TAG, "sendrequest2: " +Autofanswtichtext.getText());
        if (Autofanswtichtext.getText()=="on")
        {sendrequest1.send(this,"Autofan",0);}
        else {
            sendrequest1.send(this,"Autofan",1);}

        Toast.makeText(this,"Send Success ",Toast.LENGTH_SHORT).show();
        Thread.sleep(2000);
        Update();

    }

}