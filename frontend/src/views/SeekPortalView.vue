<template>
    <div v-if="course !== null">
        <seek-nav type="seek portal" :title="course.name"></seek-nav>

        <button class="accordion-toggle" id="accordion-toggle">☰</button>

        <div class="course-content">
            <div class="accordion" id="accordion">
                <button id="close-accordion" class="accordion-close">✖</button>

                <!-- Iterate through Weeks -->
                <div class="accordion-item" v-for="week in course.weeks" :key="week.id">
                    <div class="accordion-header">
                        <div class="text-truncate" style="width: 80%;">{{ week.name }}</div>
                        <i class="fa-solid fa-caret-down"></i>
                    </div>
                    <div class="accordion-content">
                        <!-- Course Intro (if exists) -->
                        <div v-if="week.course_intro && week.course_intro.length > 0" class="content-category">
                            <h5 class="category-title">Introduction</h5>
                            <div v-for="intro in week.course_intro" :key="intro.id" class="content-item">
                                <div class="text-truncate">
                                    <i class="fa-solid fa-book-open"></i> {{ intro.name }}
                                </div>
                                <input type="radio" name="main-content" :value="intro" 
                                      @change="changeContent(intro)"
                                      :checked="intro.id === content?.id" />
                            </div>
                        </div>

                        <!-- Lectures -->
                        <div v-if="week.lectures && week.lectures.length > 0" class="content-category">
                            <h5 class="category-title">Lectures</h5>
                            <div v-for="lecture in week.lectures" :key="lecture.id" class="content-item">
                                <div class="text-truncate">
                                    <i class="fa-solid fa-video"></i> {{ lecture.name }}
                                </div>
                                <input type="radio" name="main-content" :value="lecture" 
                                      @change="changeContent(lecture)"
                                      :checked="lecture.id === content?.id" />
                            </div>
                        </div>

                        <!-- MCQ Assignments -->
                        <div v-if="week.mcq && week.mcq.length > 0" class="content-category">
                            <h5 class="category-title">Quizzes</h5>
                            <div v-for="quiz in week.mcq" :key="quiz.id" class="content-item">
                                <div class="text-truncate">
                                    <i class="fa-solid fa-question-circle"></i> {{ quiz.name }}
                                </div>
                                <input type="radio" name="main-content" :value="quiz" 
                                      @change="changeContent(quiz)"
                                      :checked="quiz.id === content?.id" />
                            </div>
                        </div>

                        <!-- Programming Assignments -->
                        <div v-if="week.programming && week.programming.length > 0" class="content-category">
                            <h5 class="category-title">Programming Assignments</h5>
                            <div v-for="assignment in week.programming" :key="assignment.id" class="content-item">
                                <div class="text-truncate">
                                    <i class="fa-solid fa-code"></i> {{ assignment.name }}
                                </div>
                                <input type="radio" name="main-content" :value="assignment" 
                                      @change="changeContent(assignment)"
                                      :checked="assignment.id === content?.id" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Display Content -->
            <div class="main-content-area">
                <div v-if="content_type === 'programming'" class="content-display">
                    <prog-assgmt :details="content"></prog-assgmt>
                </div>
                <div v-else-if="content_type === 'lectures'" class="content-display">
                    <lectures :details="content"></lectures>
                </div>
                <div v-else-if="content_type === 'mcq'" class="content-display">
                    <mcq :details="content"></mcq>
                </div>
                <div v-else-if="content_type === 'intro'" class="content-display">
                    <div class="intro-content">
                        <h2>{{ content ? content.name : 'Course Introduction' }}</h2>
                        <div v-if="content" v-html="content.intro"></div>
                        <div v-else>No content available</div>
                    </div>
                </div>
                <div v-else class="content-display loading">
                    <div class="spinner"></div>
                </div>
            </div>
        </div>

        <button class="ai-agent-button" @click="this.$router.push({ path: '/Agent', query: {} })">
            <i class="fa-regular fa-message"></i>
        </button>
    </div>
    <div v-else class="spinner-container">
        <div class="spinner"></div>
    </div>
</template>

<script>
import SeekNavbar from "@/components/SeekNavbar.vue";
import ProgAssignment from "@/components/ProgAssignment.vue";
import LectureVideo from "@/components/LectureVideo.vue";
import McqAssignment from "@/components/McqAssignment.vue";
import { mapActions } from "vuex";
import { mapState } from "vuex";
export default {
    components: { 
        "seek-nav": SeekNavbar, 
        "prog-assgmt": ProgAssignment, 
        "lectures": LectureVideo, 
        "mcq": McqAssignment 
    },
    data() {
        return {
            accordionVisible: false,
            
            // This will contain type of content we're on currently lectures, programming, mcq or intro
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
        
        changeContent(item) {
            // Set the current content and its type
            this.content = item;
            this.content_type = item.content_type;
            
            // // Update the URL to reflect the current state
            // this.$router.push({
            //     path: '/Seek',
            //     query: {
            //         course_id: this.course.id,
            //         content_type: item.content_type,
            //         id: item.id,
            //         name: item.name
            //     }
            // });
            const newParams = {
                    course_id: this.course.id,
                    content_type: item.content_type,
                    id: item.id,
                    name: item.name
                }
            const url = new URL(window.location.href);

            // Update query params
            Object.keys(newParams).forEach((key) => {
                if (newParams[key] !== undefined && newParams[key] !== null) {
                    url.searchParams.set(key, newParams[key]);
                } else {
                    url.searchParams.delete(key); // Remove if value is null/undefined
                }
            });

            // Update the URL without reloading or triggering Vue Router
            window.history.replaceState({}, '', url);
        },
        
        toggleSidebar() {
            this.accordionVisible = !this.accordionVisible;
            const sidebar = document.getElementById("accordion");
            if (sidebar) {
                if (this.accordionVisible) {
                    sidebar.style.display = 'block';
                    const toggleBtn = document.getElementById("accordion-toggle");
                    if (toggleBtn) toggleBtn.style.display = "none";
                } else {
                    sidebar.style.display = 'none';
                    const toggleBtn = document.getElementById("accordion-toggle");
                    if (toggleBtn) toggleBtn.style.display = "block";
                }
            }
        },
        
        closeSidebar() {
            this.accordionVisible = false;
            const sidebar = document.getElementById("accordion");
            const toggleBtn = document.getElementById("accordion-toggle");
            if (sidebar) sidebar.style.display = 'none';
            if (toggleBtn) toggleBtn.style.display = "block";
        },
        
        adjustSidebar() {
            const sidebar = document.getElementById("accordion");
            const toggleButton = document.getElementById("accordion-toggle");
            const closeButton = document.getElementById("close-accordion");
            
            if (!sidebar || !toggleButton || !closeButton) return;
            
            if (window.innerWidth <= 868) {
                sidebar.style.left = "0";
                sidebar.style.width = "250px";
                sidebar.style.height = "100%";
                sidebar.style.position = "fixed";
                sidebar.style.top = "0";
                sidebar.style.transition = "left 0.3s ease-in-out";
                toggleButton.style.display = "block";
                sidebar.style.display = this.accordionVisible ? 'block' : 'none';
                closeButton.style.display = 'block';
                sidebar.style.zIndex = 1000;
            } else {
                sidebar.style.height = "100%";
                sidebar.style.position = "";
                sidebar.style.width = "25%";
                toggleButton.style.display = "none";
                sidebar.style.display = 'block';
                closeButton.style.display = 'none';
                this.accordionVisible = true;
            }
        },
        
        setupEventListeners() {
            const toggleButton = document.getElementById("accordion-toggle");
            const closeButton = document.getElementById("close-accordion");
            
            if (toggleButton) {
                toggleButton.addEventListener("click", this.toggleSidebar);
            }
            
            if (closeButton) {
                closeButton.addEventListener("click", this.closeSidebar);
            }
            
            document.querySelectorAll(".accordion-header").forEach((item) => {
                item.addEventListener("click", this.toggleAccordionItem);
            });
        },

        async fetchCourseDetails(course_id) {
            try {
                const csrf_access_token = await this.getToken();
                console.log("Fetching course details for ID:", course_id);
                console.log("CSRF token:", csrf_access_token);
                
                const response = await fetch(`http://localhost:5000/course/${course_id}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRF-TOKEN": csrf_access_token,
                    },
                    credentials: "include",
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error("Error fetching course:", errorText);
                    alert("Failed to load course content: " + errorText);
                    this.$router.replace('/SignIn');
                    return null;
                }
                
                try {
                    const data = await response.json();
                    this.course = data;
                    return data;
                } catch (jsonError) {
                    console.error("Error parsing JSON response:", jsonError);
                    alert("Invalid response from server. Please try again later.");
                    return null;
                }
            } catch (err) {
                console.error("Exception while fetching course:", err);
                alert("Failed to connect to server. Please try again later.");
                return null;
            }
        },

        // Use this function to find an object by id and content type from given weeks of a course
        findObjectByIdAndType(id, contentType) {
            if (!this.course || !this.course.weeks) return null;
            
            id = parseInt(id);
            
            for (const week of this.course.weeks) {
                // Check course intro
                if (week.course_intro && week.course_intro.length > 0 && contentType === 'intro') {
                    const found = week.course_intro.find(item => item.id === id);
                    if (found) return found;
                }
                
                // Check lectures
                if (week.lectures && week.lectures.length > 0 && contentType === 'lectures') {
                    const found = week.lectures.find(item => item.id === id);
                    if (found) return found;
                }
                
                // Check MCQ assignments
                if (week.mcq && week.mcq.length > 0 && contentType === 'mcq') {
                    const found = week.mcq.find(item => item.id === id);
                    if (found) return found;
                }
                
                // Check programming assignments
                if (week.programming && week.programming.length > 0 && contentType === 'programming') {
                    const found = week.programming.find(item => item.id === id);
                    if (found) return found;
                }
            }
            
            return null;
        },
        
        setDefaultContent() {
            if (!this.course || !this.course.weeks || this.course.weeks.length === 0) return;
            
            // Try to find the first available content item
            for (const week of this.course.weeks) {
                // Check course intro first
                if (week.course_intro && week.course_intro.length > 0) {
                    this.changeContent(week.course_intro[0]);
                    return;
                }
                
                // Then check lectures
                if (week.lectures && week.lectures.length > 0) {
                    this.changeContent(week.lectures[0]);
                    return;
                }
                
                // Then check MCQ assignments
                if (week.mcq && week.mcq.length > 0) {
                    this.changeContent(week.mcq[0]);
                    return;
                }
                
                // Then check programming assignments
                if (week.programming && week.programming.length > 0) {
                    this.changeContent(week.programming[0]);
                    return;
                }
            }
        },
        
        toggleAccordionItem(event) {
            const header = event.currentTarget;
            header.classList.toggle("active");
            
            const content = header.nextElementSibling;
            if (content) {
                content.style.display = content.style.display === "block" ? "none" : "block";
                
                const icon = header.querySelector("i.fa-caret-down");
                if (icon) {
                    icon.style.transform = content.style.display === "block" ? "rotate(180deg)" : "rotate(0deg)";
                    icon.style.transition = "transform 0.3s ease-in-out";
                }
            }
        }
    },
    computed: {
        ...mapState(["user"]),
    },
    async mounted() {
        if (this.user.id === null) {
         this.$router.push({ path: "/SignIn" });
        }
        // To set content on Load
        const query = this.$route.query;
        console.log("Route query:", query);

        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark-mode");
        }

        // Load course first, then set up UI
        if (query.course_id) {
            const courseData = await this.fetchCourseDetails(query.course_id);
            
            if (courseData) {
                // Set up UI after course data is loaded
                this.$nextTick(() => {
                    // Set up event listeners
                    window.addEventListener("resize", this.adjustSidebar);
                    this.setupEventListeners();
                    this.adjustSidebar();
                    
                    // Now try to set content
                    if (query.content_type && query.id) {
                        // Try to load specified content
                        const foundItem = this.findObjectByIdAndType(query.id, query.content_type);
                        if (foundItem) {
                            this.changeContent(foundItem);
                        } else {
                            this.setDefaultContent();
                        }
                    } else {
                        // Load default content
                        this.setDefaultContent();
                    }
                });
            }
        } else {
            // Redirect to course selection if no course_id
            this.$router.replace('/Dashboard');
        }
    },
    
    beforeUnmount() {
        window.removeEventListener("resize", this.adjustSidebar);
        
        const toggleButton = document.getElementById("accordion-toggle");
        const closeButton = document.getElementById("close-accordion");
        
        if (toggleButton) {
            toggleButton.removeEventListener("click", this.toggleSidebar);
        }
        
        if (closeButton) {
            closeButton.removeEventListener("click", this.closeSidebar);
        }
        
        document.querySelectorAll(".accordion-header").forEach((item) => {
            item.removeEventListener("click", this.toggleAccordionItem);
        });
    }
}
</script>

<style scoped>

.text-truncate {
    word-wrap: break-word;     /* Breaks long words if necessary */
  overflow-wrap: break-word; /* Modern equivalent of word-wrap */
  white-space: normal;  
}
.spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.spinner {
    width: 50px;
    height: 50px;
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