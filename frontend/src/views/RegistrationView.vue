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
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="name" required placeholder="Enter your full name" />
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required placeholder="Enter your email" />
          <label for="courses">Available Courses:</label>
          <select id="courses" ref="coursesSelect" multiple>
            <option value="1">PDSA</option>
            <option value="2">BDM</option>
            <option value="3">English II</option>
            <option value="4">MLF</option>
          </select>

          <button type="button" @click="addCourses">Add Selected Courses</button>
          
          <div id="selectedCoursesPanel">
            <div v-for="course in selectedCourses" :key="course.id" class="selected-course">
              {{ course.name }}
              <a href="#" @click.prevent="removeCourse(course)">
                <i class="fa fa-times" aria-hidden="true"></i>
              </a>
            </div>
          </div>

          <button type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Registering...' : 'Complete Registration' }}
          </button>
        </form>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <span style="margin-top: 1rem;">
          Already enrolled? <router-link to="/SignIn" style="color: aqua">Sign in now</router-link>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: "",
      email: "",
      selectedCourses: [],
      isSubmitting: false,
      errorMessage: ""
    };
  },
  methods: {
    addCourses() {
      const coursesSelect = this.$refs.coursesSelect;
      const selectedOptions = Array.from(coursesSelect.selectedOptions);
      
      selectedOptions.forEach(option => {
        const existing = this.selectedCourses.find(c => c.id === option.value);
        if (!existing) {
          this.selectedCourses.push({
            id: option.value,
            name: option.text
          });
        }
      });

      coursesSelect.selectedIndex = -1;
    },
    removeCourse(course) {
      this.selectedCourses = this.selectedCourses.filter(c => c.id !== course.id);
    },
    async register() {
      this.isSubmitting = true;
      this.errorMessage = "";

      try {
        const payload = {
          email: this.email,
          name: this.name,
          role: "student",
          register_courses: this.selectedCourses.map(c => [c.id, c.name])
        };

        const response = await axios.post('http://127.0.0.1:5000/user/register', payload);
        
        if (response.status === 201) {
          this.$router.push("/SignIn");
        }
      } catch (error) {
        console.error('Registration error:', error);
        this.errorMessage = error.response?.data?.error || 
          "Registration failed. Please check your details and try again.";
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>