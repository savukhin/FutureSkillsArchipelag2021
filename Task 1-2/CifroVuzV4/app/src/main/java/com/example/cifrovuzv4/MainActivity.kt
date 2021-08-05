package com.example.cifrovuzv4

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.method.LinkMovementMethod.*
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setupHyperlink();

        val button: Button = findViewById(R.id.button_login)
        button.setOnClickListener(View.OnClickListener { view ->
            val username = findViewById<TextView>(R.id.editTextTextPersonName).text.toString()
            val password = findViewById<TextView>(R.id.editTextTextPassword).text.toString()
            println("DATA = " + username + " " + password)
            val url = URL("http://127.0.0.1:8000/")
            println("Connecting...")
            with(ClientManager.url.openConnection() as HttpURLConnection) {
                println("Connecting 2...")
                requestMethod = "GET"  // optional default is GET

                println("\nSent 'GET' request to URL : $url; Response Code : $responseCode")

                inputStream.bufferedReader().use {
                    it.lines().forEach { line ->
                        println(line)
                    }
                }
            }
            val result = ClientManager.logIn(username, password)
            Toast.makeText(baseContext, result.toString(), Toast.LENGTH_LONG).show()
        })
    }
    fun setupHyperlink() {
        val linkTextView = findViewById<TextView>(R.id.textView4)
        linkTextView.setMovementMethod(getInstance());
    }

}