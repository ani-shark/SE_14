<template>
    <div class="sign-in-body">
        <div class="sign-in-header">
            <img src="@/assets/iitm-logo.png" alt="IITM Logo" />
            <div class="iit-title">
                <div>Indian Institute of Technology Madras</div>
                <div style="font-size: 1.1rem">Online Course Portal</div>
            </div>
        </div>

        <div class="sign-in-form-box">
            <div class="sign-in">
                <h2>Sign In</h2>
                <p>
                    Sign-in using the Google account you registered with to access your course dashboard.
                </p>
                <button @click="signIn">Sign in with Google</button>
                <span style="margin-top: 1rem;">
                    Not registered?
                    <router-link to="/Register" style="color: aqua">Register now</router-link>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
    name: "SignIn",
    methods: {
        ...mapActions(["signIn"]),
    },
};
</script>