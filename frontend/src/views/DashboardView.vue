<template>
    <div v-if="user.id !== null" class="my-courses" style="position: relative;min-height:100vh;">
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
        <footer class="footer" style="position:absolute; bottom: 0;width: 100%;">
            <b>SE Project | JAN 2025 Term</b>
        </footer>
    </div>
</template>

<script>
import SeekNavbar from "@/components/SeekNavbar.vue";
import { mapState } from "vuex";
import { mapActions } from "vuex";
export default {
    name: "MyCourses",
    components: { "seek-nav": SeekNavbar },
    data() {
        return {
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
        if (this.user.id === null) {
         this.$router.push({ path: "/SignIn" });
        }
    }
    }
</script>