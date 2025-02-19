<template>
    <div>
        <seek-nav type="admin" title="Admin"></seek-nav>
      <div class="admin-form-box">
        <div class="admin">
          <h2>Download Report</h2>
          <form @submit.prevent="submitForm">
            <label for="course">Select a Course:</label>
            <input list="courses" id="course" v-model="selectedCourse" placeholder="Enter course code" />
            <datalist id="courses">
              <option v-for="course in courses" :key="course.code" :value="course.code">
                {{ course.name }}
              </option>
            </datalist>
  
            <label for="start-date">Start Date:</label>
            <input type="date" id="start-date" v-model="startDate" @change="updateMinDate" />
  
            <label for="end-date">End Date:</label>
            <input type="date" id="end-date" v-model="endDate" :min="startDate" />
  
            <button type="submit">Download PDF</button>
          </form>
        </div>
      </div>
  
      <footer class="footer">
        <b>SE Project | JAN 2025 Term</b>
      </footer>
    </div>
  </template>
  
  <script>
  import SeekNavbar from '@/components/SeekNavbar.vue';
  export default {
    components:{'seek-nav':SeekNavbar},
    data() {
      return {
        selectedCourse: "",
        startDate: "",
        endDate: "",
        courses: [
          { code: "Course Code 1", name: "Course Name 1" },
          { code: "Course Code 2", name: "Course Name 2" },
          { code: "Course Code 3", name: "Course Name 3" },
          { code: "Course Code 4", name: "Course Name 4" }
        ]
      };
    },
    methods: {
      updateMinDate() {
        this.endDate = "";
      },
      submitForm() {
        console.log("Selected Course:", this.selectedCourse);
        console.log("Start Date:", this.startDate);
        console.log("End Date:", this.endDate);
        alert("Form submitted! Check the console for details.");
      }
    }
  };
  </script>
  
  