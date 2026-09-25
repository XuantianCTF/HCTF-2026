package com.example.unrooted

import android.content.Context

object NativeCheck {

    init {
        System.loadLibrary("unrooted")
    }

    external fun checkEnvironment(context: Context): Int

    external fun verifyFlag(input: String): Boolean
}
