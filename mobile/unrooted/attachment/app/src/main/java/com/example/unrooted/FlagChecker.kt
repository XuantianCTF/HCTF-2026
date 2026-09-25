package com.example.unrooted

import android.content.Context

object FlagChecker {

    fun verify(context: Context, input: String): Boolean {
        if (NativeCheck.checkEnvironment(context) != 0) {
            return false
        }
        return NativeCheck.verifyFlag(input)
    }
}
