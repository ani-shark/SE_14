<template>
    <nav class="seek-navbar">
        <div class="course-detail">
            <div class="fs-5 text-truncate">
                <img src="@/assets/iitm-logo.png" alt="IITM Logo" />
                {{ title }}
            </div>
        </div>
        <div class="navigation">
            <button v-if="type == 'seek portal'" title="Go back" @click="this.$router.push('/Dashboard')">
                <i class="fa fa-arrow-left" aria-hidden="true"></i>
            </button>
            <button v-else-if="type == 'ai agent'" title="Close Agent">
                <router-link :to="this.$router.options.history.state.back || '/Dashboard'">
                    <i class="fa fa-arrow-left" aria-hidden="true"></i>
                </router-link>
            </button>
            <button v-else-if="type == 'admin'" title="Signout" @click="this.signOut()">
                <i class="fa fa-sign-out" aria-hidden="true"></i>
            </button>
            <button v-else title="Signout" @click="this.signOut()">
                <i class="fa fa-sign-out" aria-hidden="true"></i>

            </button>

            <button title="Change Theme" @click="toggleTheme" class="theme-btn">
                {{ themeIcon }}
            </button>
        </div>
    </nav>
</template>

<script>
import { mapActions } from 'vuex';
export default {
    props: {
        title: {
            type: String,
            required: true,
        },
        type: {
            type: String,
            required: true,
        },
    },
    data() {
        return {
            themeIcon: null
        }
    },
    methods: {
        ...mapActions(['signOut']),
        toggleTheme() {
            const body = document.body;
            body.classList.toggle("dark-mode");
            const newTheme = body.classList.contains("dark-mode") ? "dark" : "light";
            localStorage.setItem("theme", newTheme);
            this.themeIcon = newTheme === "dark" ? "☀️" : "🌙";
        },
        applyTheme() {
            if (localStorage.getItem("theme") === "dark") {
                document.body.classList.add("dark-mode");
                this.themeIcon = "☀️"; 
            }
            else {
                document.body.classList.remove("dark-mode");
                this.themeIcon = "🌙"; 
            }
        }
    },
    mounted() {
        this.applyTheme();
    },
    beforeUnmount() {
        if (document.body.classList.contains('dark-mode')) {
            document.body.classList.remove('dark-mode');
        }
    }
};
</script>