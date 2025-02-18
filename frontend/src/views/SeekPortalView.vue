<template>
    <div>
        <seek-nav type="seek portal" title="Course Name"></seek-nav>

        <button class="accordion-toggle" id="accordion-toggle">☰</button>

        <div class="course-content">
            <div class="accordion" id="accordion">
                <button id="close-accordion" class="accordion-close">✖</button>
                <div class="accordion-item">
                    <div class="accordion-header" style="cursor:default;">
                        <div class="text-truncate" style="width: 80%;">Lectures</div>
                    </div>
                </div>
                <div class="accordion-item" v-for="week in weeks" :key="week.id">
                    <div class="accordion-header">
                        <div class="text-truncate" style="width: 80%">{{ week.name }}</div>
                        <i class="fa-solid fa-caret-down"></i>
                    </div>
                    <div class="accordion-content">
                        <div v-for="item in week.content" :key="week.id + '-' + item.item_id" class="content-item">
                            <div class="text-truncate" style="padding-left: 0.8em">
                                {{ item.name }}
                            </div>
                            <input type="radio" name="main-content" :value="item" @change="change_content(item)"
                                :checked="item === content" />
                        </div>

                    </div>
                </div>
            </div>
            <div v-if="content && content.name && content.name.includes('Programming Assgmt')" class="content">
                <prog-assgmt :details="content"></prog-assgmt>
            </div>
            <div v-else-if="content && content.name && content.name.includes('Lecture')" class="content">
                <lectures :details="content"></lectures>
            </div>
            <div v-else-if="content && content.name && content.name.includes('Mcq')" class="content">
                <mcq :details="content"></mcq>
            </div>
            <div v-else class="content">
                <h3>{{ content ? content.name : 'No content available' }}</h3>
            </div>
        </div>

        <button class="ai-agent-button">
            <a href="ai_agent.html"><i class="fa-regular fa-message"></i></a>
        </button>
    </div>
</template>

<script>
import SeekNavbar from "@/components/SeekNavbar.vue";
import ProgAssignment from "@/components/ProgAssignment.vue";
import LectureVideo from "@/components/LectureVideo.vue";
import McqAssignment from "@/components/McqAssignment.vue";
export default {
    components: { "seek-nav": SeekNavbar, "prog-assgmt": ProgAssignment , "lectures":LectureVideo,"mcq":McqAssignment},
    data() {
        return {
            accordionVisible: false,
            content: null,
            weeks: [
                { id: 1, name: 'About Course', content: [{ item_id: 1, id: 1, name: "Course Intro" }] },
                {
                    id: 1, name: "Week 1", content: [{ item_id: 1, id: 1, name: "Week 1 Lecture 1" },
                    { item_id: 2, id: 2, name: "Week 1 Lecture 2" }, { item_id: 3, id: 1, name: 'Week 1 Mcq Assignment 1' },
                    { item_id: 4, id: 2, name: 'Week 1 Mcq Assignment 2' }]
                },
                {
                    id: 2, name: "Week 2", content: [{ item_id: 1, id: 3, name: "Week 2 Lecture 1" },
                    { item_id: 2, id: 4, name: "Week 2 Lecture 2" }, { item_id: 3, id: 3, name: 'Week 2 Mcq Assignment 1' },
                    { item_id: 4, id: 4, name: 'Week 2 Mcq Assignment 2' }, { item_id: 5, id: 1, name: 'Week 2 Programming Assgmt 1' },
                    { item_id: 6, id: 2, name: 'Week 2 Programming Assgmt 2' }]
                },
                {
                    id: 3, name: "Week 3", content: [{ item_id: 1, id: 5, name: "Week 3 Lecture 1" },
                    { item_id: 2, id: 6, name: "Week 3 Lecture 2" }, { item_id: 3, id: 7, name: "Week 3 Lecture 3" },
                    { item_id: 4, id: 8, name: "Week 3 Lecture 4" }, { item_id: 5, id: 9, name: "Week 3 Lecture 5" },
                    { item_id: 6, id: 10, name: "Week 3 Lecture 6" }]
                }
            ]
        };
    },
    methods: {
        change_content(item) {
            this.content = item;
        },
        toggleSidebar() {
            this.accordionVisible = !this.accordionVisible;
        },
        closeSidebar() {
            this.accordionVisible = false;
        },
        toggleTheme() {
            const body = document.body;
            body.classList.toggle("dark-mode");
            localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light");
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
                sidebar.style['z-index']=1000;
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
        }
    },
    mounted() {
        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark-mode");
        }
        window.addEventListener("load", this.adjustSidebar);
        window.addEventListener("resize", this.adjustSidebar);
        this.adjustSidebar()


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


        const { id: contentId, name: contentName } = this.$route.query;
        let ans = null;

        if (contentId && contentName) {
            this.weeks.forEach(week => {
                week.content.forEach(item => {
                    if (item.name === contentName && item.id == contentId) {
                        ans = item;
                    }
                });
            });
        }

        // Default to "Course Intro" if no valid content found
        if (!ans) {
            ans = this.weeks[0].content[0];
        }

        this.change_content(ans);

    },
    watch: {
        content(newContent) {
            
            const newParams = { item_id: newContent.item_id, id: newContent.id, name: newContent.name }
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

        }
    }
}
</script>
