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
                <div style="color: red;">{{ errorMessage }}</div>
                <input v-model="email" type="email" placeholder="Enter your email to sign in" required />
                <button @click="handleSignIn">Sign In</button>
                <span style="margin-top: 1rem;">
                    Not registered? <router-link to="/Register" style="color: aqua">Register now</router-link>
                </span>
            </div>
        </div>
    </div>
</template>


<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { mapActions } from 'vuex';
export default {
   data() {
      return {
         email: "",
        errorMessage: "",
      };
   },
   methods:{
    ...mapActions(['signIn']),
    async handleSignIn(){
        if(this.email === ""){
            this.errorMessage = "Please enter your email.";
            setTimeout(() => {
                this.errorMessage = "";
            }, 2000);
            return;
        }
        const response = await this.signIn({ email: this.email });
        if (response !== true) {
            this.errorMessage = response || "Sign-in failed. Please try again.";
        } else {
            this.$router.push("/Dashboard");
        }
    }
   }
};
</script>