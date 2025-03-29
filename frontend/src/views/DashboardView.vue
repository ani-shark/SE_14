<template>
    <div class="my-courses">
        <seek-nav type="student dashboard" title="BS Degree in Data Science and Applications"></seek-nav>

        <div class="container meta-info">
            <div>
                <h3>My Current Courses</h3>
                <p>
                    Cumulative Grade Point Average (CGPA) till this term - <b>9</b><br />
                    Project Cumulative Grade Point Average (Project CGPA) till this term -
                    <b>10</b>
                </p>
            </div>
            <div>
                <h4>{{ currentDate }}</h4>
                <h4>JANUARY 2025 TERM</h4>
            </div>
        </div>

        <div class="container flash-cards-container">
            <div v-for="course in courses" :key="course.id" class="card">
                <div class="course-info">
                    <h4>{{ course.intro }}</h4> 
                    <h6>NEW COURSE</h6>
                    <ul>
                        <li v-for="(score, index) in course.scores" :key="index">
                            Week {{ index + 1 }} Assignment - {{ score }}
                        </li>
                    </ul>
                </div>
                <router-link to="/Seek" class="btn-primary">
                    Go to Course Page <i class="fa-solid fa-arrow-right"></i>
                </router-link>
            </div>
        </div>

        <footer class="footer">
            <b>SE Project | JAN 2025 Term</b>
        </footer>
    </div>
</template>

<script>
import SeekNavbar from "@/components/SeekNavbar.vue";
import { getUserCourses } from "@/api/user";
import axios from "@/api/api";


export default {
    name: "MyCourses",
    components: { "seek-nav": SeekNavbar },
    data() {
        return {
            courses: [], 
            currentDate: new Date().toLocaleDateString("en-US", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
            }),
            themeIcon: localStorage.getItem("theme") === "dark" ? "☀️" : "🌙",
        };
    },
    mounted() {
        this.fetchUserCourses();
        this.applyTheme();
    },
    methods: {
        async fetchUserCourses() {
            try {
                const userId = localStorage.getItem("user_id"); 
                if (!userId) {
                    console.error("User ID is missing. Redirecting to Sign In.");
                    this.$router.push("/SignIn");
                    return;
                }

                console.log("Fetching courses for User ID:", userId);
                const fetchedCourses = await getUserCourses(userId); 

                
                this.courses = fetchedCourses.map(course => ({
                    id: course.id,
                    intro: course.intro, 
                    scores: [100, 100, 100], 
                }));

            } catch (error) {
                console.error("Error fetching user courses:", error);
            }
        },
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
            }
        },
        signOut() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_role");
    localStorage.removeItem("user_email");

    delete axios.defaults.headers.common["Authorization"];

    console.log("User signed out. Redirecting to Sign In.");
    
    this.$router.push("/SignIn").then(() => {
        window.location.reload(); 
    });
},
    },
};
</script>
