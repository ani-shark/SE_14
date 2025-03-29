<template>
    <div v-if = "course!==null">
        <seek-nav type="seek portal" :title="course.details.name"></seek-nav>

        <button class="accordion-toggle" id="accordion-toggle">☰</button>

        <div class="course-content">
            <div class="accordion" id="accordion">
                <button id="close-accordion" class="accordion-close">✖</button>
                <div class="accordion-item">
                    <div class="accordion-header" style="cursor:default;">
                        <div class="text-truncate" style="width: 80%;">Lectures</div>
                    </div>
                </div>
                <div class="accordion-item" v-for="week in course.details.weeks" :key="week.id">
                    <div class="accordion-header">
                        <div class="text-truncate" style="width: 80%">{{ week.name }}</div>
                        <i class="fa-solid fa-caret-down"></i>
                    </div>
                    <div class="accordion-content">
                        <div v-for="item in week.lectures" :key="week.id + '-' + item.id" class="content-item">
                            <div class="text-truncate" style="padding-left: 0.8em">
                                {{ item.name }}
                            </div>
                            <input type="radio" name="main-content" :value="item" @change="change_content(item)"
                                :checked="item === content" />
                        </div>
                        <div v-for="item in week.mcq" :key="week.id + '-' + item.id" class="content-item">
                            <div class="text-truncate" style="padding-left: 0.8em">
                                {{ item.name }}
                            </div>
                            <input type="radio" name="main-content" :value="item" @change="change_content(item)"
                                :checked="item === content" />
                        </div>
                        <div v-for="item in week.programming" :key="week.id + '-' + item.id" class="content-item">
                            <div class="text-truncate" style="padding-left: 0.8em">
                                {{ item.name }}
                            </div>
                            <input type="radio" name="main-content" :value="item" @change="change_content(item)"
                                :checked="item === content" />
                        </div>

                    </div>
                </div>
            </div>
            <div v-if="content_type === 'programming'">
                <prog-assgmt :details="content"></prog-assgmt>
            </div>
            <div v-else-if="content_type === 'lectures'">
                <lectures :details="content"></lectures>
            </div>
            <div v-else-if="content_type === 'mcq'">
                <mcq :details="content"></mcq>
            </div>
            <div v-else-if="content_type === 'intro'">
                <h6>{{ content ? content.intro : 'No content available' }}</h6>
            </div>
            <div v-else class="content">
                <div class="spinner"></div>
            </div>
        </div>

        <button class="ai-agent-button" @click="this.$router.push({ path: '/Agent', query: {} })">

            <i class="fa-regular fa-message"></i>
        </button>
    </div>
    <div v-else style="width: 100%;display: flex;align-items: center;justify-content: center;">
        <div class="spinner"></div>
    </div>
</template>

<script>
import SeekNavbar from "@/components/SeekNavbar.vue";
import ProgAssignment from "@/components/ProgAssignment.vue";
import LectureVideo from "@/components/LectureVideo.vue";
import McqAssignment from "@/components/McqAssignment.vue";
import { mapActions } from "vuex";
import router from "@/router";
export default {
    components: { "seek-nav": SeekNavbar, "prog-assgmt": ProgAssignment, "lectures": LectureVideo, "mcq": McqAssignment },
    data() {
        return {
            accordionVisible: false,
            
            // This will contain type of content we're on currently lectures,programming, mcq or intro
            content_type: null,
            
            // This will have response of the request to /user/courses/<course_id> from backend
            course: null,

            // This will have the content of the current item we're on eg. lecture, mcq, programming or intro
            content: null,

            // This will have the id of the current item we're on eg. lecture, mcq, programming or intro
            id: null,

            //  This is query structure for the URL /Seek?course_id=num1&content_type=string1&id=num2&name=string2
        };
    },
    methods: {
        ...mapActions(["getToken"]),
        change_content(item) {
            // Change the content of our main pane
        },
        toggleSidebar() {
            this.accordionVisible = !this.accordionVisible;
        },
        closeSidebar() {
            this.accordionVisible = false;
        },
        adjustSidebar() {
            const sidebar = document.getElementById("accordion");
            const toggleButton = document.getElementById("accordion-toggle");
            const closeButton = document.getElementById("close-accordion");
            if (window.innerWidth <= 868) {
                sidebar.style.left = "0";
                sidebar.style.width = "250px";
                sidebar.style.height = "100%";
                sidebar.style.position = "fixed";
                sidebar.style.top = "0";
                sidebar.style.transition = "left 0.3s ease-in-out";
                toggleButton.style.display = "block";
                sidebar.style.display = 'none'
                closeButton.style.display = 'block';
                sidebar.style['z-index'] = 1000;
            } else {
                sidebar.style.height = "100%";
                sidebar.style.position = "";
                sidebar.style.width = "25%";
                toggleButton.style.display = "none";
                sidebar.style.display = 'block';
                closeButton.style.display = 'none';
            }

            toggleButton.addEventListener("click", function () {
                sidebar.style.display = 'block';
                this.style.display = "none";
            });

            closeButton.addEventListener("click", function () {
                sidebar.style.display = "none";
                toggleButton.style.display = "block";
            });
        },

        async fetchCourseDetails(course_id) {
            try {
                const csrf_access_token = await this.getToken();
                console.log(csrf_access_token);
                const response = await fetch(`http://localhost:8000/user/courses/${course_id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRF-TOKEN": csrf_access_token,
                    },
                    credentials: "include",
                });

                const data = await response.json();
                if (response.ok) {
                }
                else {
                    alert(data.error);
                    this.$router.replace('/SignIn');
                }
            }
            catch (err) {
                console.error(err);
            }
        },

        // Use this function to find an object by id and content type from given weeks of a course
        findObjectByIdAndType(id, contentType) {
            for (const week of this.course.details.weeks) {
                if(week.id === 0) {
                    const found = week['course_intro'].find(item => item.id === id && item.content_type === contentType);
                    if (found) {
                        return found;
                    }
                }
                for (const category of ['lectures', 'mcq', 'programming']) {
                    const found = week[category].find(item => item.id === id && item.content_type === contentType);
                    if (found) {
                        return found;
                    }
                }
            }
            return null;
        }
    },
    async mounted() {
        // To set content on Load
        const query = this.$route.query;
        console.log(query);

        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark-mode");
        }

        // Sidebar Responsiveness
        window.addEventListener("load", this.adjustSidebar);
        window.addEventListener("resize", this.adjustSidebar);
        this.adjustSidebar()

        // Animation 
        document.querySelectorAll(".accordion-header").forEach((item) => {
            item.addEventListener("click", function () {
                this.classList.toggle("active");
                let content = this.nextElementSibling;

                content.style.display = content.style.display === "block" ? "none" : "block";

                let secondChild = this.children[1];
                if (secondChild) {
                    let currentRotation = secondChild.style.transform.includes("180deg") ? "0deg" : "180deg";
                    secondChild.style.transform = `rotate(${currentRotation})`;
                    secondChild.style.transition = "transform 0.3s ease-in-out"; // Smooth rotation
                }
            });
        });


    },
    watch: {
    }
}
</script>

<style scoped>
.spinner {
    width: 20%;
    height: 20%;
    border: 5px solid rgba(0, 0, 0, 0.1);
    border-top-color: #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}
</style>