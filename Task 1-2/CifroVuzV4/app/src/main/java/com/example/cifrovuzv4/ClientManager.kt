package com.example.cifrovuzv4

import java.net.HttpURLConnection
import java.net.URL

class ClientManager {
    companion object {
        public val url = URL("http://127.0.0.1:8000/")

        @JvmStatic
        public fun logIn(username: String, password: String) {
            with(url.openConnection() as HttpURLConnection) {
                requestMethod = "GET"  // optional default is GET

                println("\nSent 'GET' request to URL : $url; Response Code : $responseCode")

                inputStream.bufferedReader().use {
                    it.lines().forEach { line ->
                        println(line)
                    }
                }
            }
        }
    }
}