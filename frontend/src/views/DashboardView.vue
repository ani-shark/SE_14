<template>
    <div v-if="user.id !== null" class="my-courses">
        <seek-nav type="student dashboard" title="BS Degree in Data Science and Applications"></seek-nav>

        <div class="container meta-info">
            <div>
                <h3>My Current Courses</h3>
            </div>
            <div>
                <h4>{{ currentDate }}</h4>
                <h4>JANUARY 2025 TERM</h4>
            </div>
        </div>

        <div class="container flash-cards-container">
            <div v-for="course in user.course_details" :key="course.id" class="card">
                <div class="course-info">
                    <h4>{{ course.name }}</h4>
                    <h6>NEW COURSE</h6>
                    <ul>
                        <li v-for="(mcq, index) in course.mcq_scores" :key="index">
                            {{ mcq.week_name }} {{ mcq.assignment_title }} - {{ mcq.score }}
                        </li>
                        <li v-for="(prog, index) in course.programming_scores" :key="index">
                            {{ prog.week_name }} {{ prog.assignment_title }} - {{ prog.score }}
                        </li>
                    </ul>
                </div>
                <router-link :to="{
                    path: '/Seek',
                    query: { course_id: course.id, content_type: 'intro', id: 0, name: 'Course Intro' }
                }" class="btn-primary">
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
import { mapState } from "vuex";
export default {
    name: "MyCourses",
    components: { "seek-nav": SeekNavbar },
    data() {
        return {
            courses: [
                { id: 1, name: "Course 1", scores: [100, 100, 100] },
                { id: 2, name: "Course 2", scores: [100, 100, 100] },
                { id: 3, name: "Course 3", scores: [100, 100, 100] },
                { id: 4, name: "Course 4", scores: [100, 100, 100] },
            ],
            currentDate: new Date().toLocaleDateString("en-US", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
            }),
            themeIcon: localStorage.getItem("theme") === "dark" ? "☀️" : "🌙",
        };
    },
    computed: {
        ...mapState(["user"]),
    },
    mounted() {
        this.applyTheme();
    },
    methods: {
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
        }
    },
};
</script>