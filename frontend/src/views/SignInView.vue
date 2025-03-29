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
                <p>Enter your email to log in.</p>
                <input v-model="email" type="email" placeholder="Enter your email" required />
                <button @click="signInUser">Sign In</button>
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
import { signIn } from "@/api/auth"; 

export default {
    setup() {
        const router = useRouter();
        const email = ref("");

        const signInUser = async () => {
            try {
                const response = await signIn(email.value);
                console.log("API Response:", response);

                if (!response.id || !response.role || !response.access_token) {
                    console.error("Invalid response structure:", response);
                    alert("Login failed. Please try again.");
                    return;
                }

                localStorage.setItem("access_token", response.access_token);
                localStorage.setItem("user_id", response.id);
                localStorage.setItem("user_role", response.role);
                localStorage.setItem("user_email", response.email);

                if (response.role === "admin") {
                    router.push("/Admin");
                } else {
                    router.push("/Dashboard");
                }
            } catch (error) {
                console.error("Login error:", error);
                alert("Invalid login. Please try again.");
            }
        };

        return { email, signInUser };
    },
};
</script>