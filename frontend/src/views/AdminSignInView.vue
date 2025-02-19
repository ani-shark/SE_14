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
                <h2>Admin Sign In</h2>
                <p>
                    Sign-in using the Google account you have been authorized.
                </p>
                <button @click="this.$router.push('/Admin')">Sign in with Google</button>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    methods: {
        
    },
};
</script>