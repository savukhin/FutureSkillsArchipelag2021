package com.example.cifrovuzv4

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.method.LinkMovementMethod
import android.text.method.LinkMovementMethod.*
import android.widget.TextView

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setupHyperlink();
    }
    fun setupHyperlink() {
        val linkTextView = findViewById<TextView>(R.id.textView4)
        linkTextView.setMovementMethod(getInstance());
    }
}