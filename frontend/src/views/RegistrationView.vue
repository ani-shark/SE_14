<template>
    <div class="register-body">
      <div class="register-header">
        <img src="@/assets/iitm-logo.png" alt="IITM Logo" />
        <div class="iit-title">
          <div>Indian Institute of Technology Madras</div>
          <div style="font-size: 1.1rem">Online Course Portal</div>
        </div>
      </div>
  
      <div class="register-form-box">
        <div class="register">
          <h2>Registration Form</h2>
          <form @submit.prevent="register">
            <label for="email">Email:</label>
            <input
              type="email"
              id="email"
              v-model="email"
              required
              placeholder="Enter your email"
            />
  
            <label for="courses">Course List:</label>
            <select id="courses" multiple @select="addCourses()">
              <option value="Math">Math</option>
              <option value="Science">Science</option>
              <option value="History">History</option>
              <option value="Computer Science">Computer Science</option>
              <option value="Art">Art</option>
            </select>
  
            <button type="button" @click="addCourses">Add</button>
            <div id="selectedCoursesPanel">
              <div v-for="course in selectedCourses" :key="course" class="selected-course">
                {{ course }}
                <a href="#" @click.prevent="removeCourse(course)">
                  <i class="fa fa-times" aria-hidden="true"></i>
                </a>
              </div>
            </div>
  
            <button type="submit">Register</button>
          </form>
          <span style="margin-top: 1rem;">
            Already enrolled? <router-link to="/SignIn" style="color: aqua">Sign in now</router-link>
          </span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState, mapMutations } from "vuex";
  import { useRouter } from "vue-router";
  
  export default {
    data() {
      return {
        email: "",
        selectedCourses: []
      };
    },
    methods: {
      ...mapMutations(["setUser"]),
      addCourses() {
        console.log('Course Added')
        const coursesSelect = document.getElementById("courses");
      const selectedOptions = Array.from(coursesSelect.selectedOptions);
      const selectedValues = selectedOptions.map(option => option.value);
      selectedValues.forEach(course => {
    if (!this.selectedCourses.includes(course)) {
      this.selectedCourses.push(course);
    }
  });
      
      },
      removeCourse(course) {
        const index = this.selectedCourses.indexOf(course);
        if (index > -1) {
          this.selectedCourses.splice(index, 1);
        }
      },
      register() {
        const userData = {
          email: this.email,
          selectedCourses: this.selectedCourses,
        };
        
        // Commit to Vuex store to save the user
        this.setUser(userData);
  
        // Redirect to student dashboard
        this.$router.push("/SignIn");
      }
    }
  };
  </script>
  

  