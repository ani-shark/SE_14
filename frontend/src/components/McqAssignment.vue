<template>
  <div>
    <div v-if="loading" class="loading">Loading MCQ assignments...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else>
      <h1>MCQ Assignments</h1>

      <div v-if="isAdmin" class="admin-controls">
        <button @click="openCreateModal">Create Assignment</button>
      </div>

      <div
        v-for="assignment in assignments"
        :key="assignment.id"
        class="assignment-card"
      >
        <div class="assignment-header">
          <h2>{{ assignment.title }}</h2>
          <p>{{ assignment.description }}</p>

          <div v-if="isAdmin" class="admin-actions">
            <button @click="editAssignment(assignment)">Edit</button>
            <button @click="deleteAssignment(assignment.id)">Delete</button>
          </div>
        </div>

        <div class="questions-section">
          <div
            v-for="question in assignment.questions"
            :key="question.id"
            class="question-card"
          >
            <p class="question-text">{{ question.text }}</p>

            <div class="options-grid">
              <label
                v-for="(option, index) in question.options"
                :key="index"
                class="option-label"
              >
                <input
                  type="radio"
                  :name="`assignment-${assignment.id}-q${question.id}`"
                  :value="option"
                  v-model="userAnswers[assignment.id][question.id]"
                />
                <span class="option-text">{{ option }}</span>
              </label>
            </div>
          </div>
        </div>

        <div class="submission-controls">
          <button
            @click="submitAnswers(assignment.id)"
            :disabled="!hasAnswers(assignment.id)"
          >
            Submit Answers
          </button>
          <p v-if="scores[assignment.id] !== undefined" class="score-display">
            Score: {{ scores[assignment.id] }}/{{ assignment.questions.length }}
          </p>
        </div>
      </div>

      <div v-if="showModal" class="modal-overlay">
        <div class="modal-content">
          <h3>Create New Assignment</h3>
          <input v-model="newAssignment.title" placeholder="Title" />
          <textarea
            v-model="newAssignment.description"
            placeholder="Description"
          ></textarea>
          <div class="modal-actions">
            <button @click="saveAssignment">Save</button>
            <button @click="showModal = false">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      assignments: [],
      userAnswers: {},
      scores: {},
      isAdmin: false,
      loading: true,
      error: null,
      showModal: false,
      newAssignment: {
        title: "",
        description: "",
        questions: [],
      },
    };
  },
  created() {
    this.fetchAssignments();
    this.checkAdmin();
  },
  methods: {
    ...mapActions(["getToken"]),

    async fetchAssignments() {
      try {
        const csrf_access_token = await this.getToken();
        const response = await fetch("http://localhost:5000/assignment/mcq/1", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf_access_token,
          },
          credentials: "include",
        });

        if (!response.ok) throw new Error("Failed to fetch assignments");

        const data = await response.json();
        this.assignments = Array.isArray(data) ? data : [data];

        this.assignments.forEach((assignment) => {
          this.userAnswers[assignment.id] = {};
          if (!this.userAnswers[assignment.id]) {
            this.userAnswers = {
              ...this.userAnswers,
              [assignment.id]: {},
            };
          }
        });
      } catch (error) {
        console.error("Error fetching assignments:", error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },

    async submitAnswers(assignmentId) {
  try {
    const csrf_access_token = await this.getToken();
    const payload = {
      assignment_id: assignmentId,
      answers: this.userAnswers[assignmentId] || {}
    };

    const response = await fetch(
      "http://localhost:5000/assignment/submit/mcq",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": csrf_access_token,
          "Authorization": `Bearer ${localStorage.getItem('access_token')}`
        },
        credentials: "include",
        body: JSON.stringify(payload),
      }
    );

    if (!response.ok) {
      const errorData = await response.json(); // Get detailed error
      throw new Error(errorData.message || "Submission failed");
    }

    const data = await response.json();
    this.scores = { ...this.scores, [assignmentId]: data.score };
    
  } catch (error) {
    console.error("Submission error:", error.message);
    alert(`Submission failed: ${error.message}`);
  }
},

    hasAnswers(assignmentId) {
      return Object.keys(this.userAnswers[assignmentId] || {}).length > 0;
    },

    // Admin methods
    async checkAdmin() {
      try {
        const csrf_access_token = await this.getToken();
        const response = await fetch("http://localhost:5000/user/get", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf_access_token,
          },
          credentials: "include",
        });

        if (!response.ok) throw new Error("Admin check failed");

        const data = await response.json();
        this.isAdmin = data.role === "admin";
      } catch (error) {
        console.error("Error checking admin status:", error);
      }
    },

    async saveAssignment() {
      try {
        const csrf_access_token = await this.getToken();
        await fetch("http://localhost:5000/assignment/mcq", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf_access_token,
          },
          credentials: "include",
          body: JSON.stringify(this.newAssignment),
        });

        this.showModal = false;
        this.newAssignment = { title: "", description: "", questions: [] };
        this.fetchAssignments();
      } catch (error) {
        console.error("Error creating assignment:", error);
      }
    },

    async editAssignment(assignment) {
      const newTitle = prompt("Edit title:", assignment.title);
      if (newTitle) {
        try {
          const csrf_access_token = await this.getToken();
          await fetch(`http://localhost:5000/assignment/mcq/${assignment.id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRF-TOKEN": csrf_access_token,
            },
            credentials: "include",
            body: JSON.stringify({ title: newTitle }),
          });

          this.fetchAssignments();
        } catch (error) {
          console.error("Error updating assignment:", error);
        }
      }
    },

    async deleteAssignment(id) {
      if (confirm("Are you sure you want to delete this assignment?")) {
        try {
          const csrf_access_token = await this.getToken();
          await fetch(`http://localhost:5000/assignment/mcq/${id}`, {
            method: "DELETE",
            headers: {
              "X-CSRF-TOKEN": csrf_access_token,
            },
            credentials: "include",
          });

          this.fetchAssignments();
        } catch (error) {
          console.error("Error deleting assignment:", error);
        }
      }
    },

    openCreateModal() {
      this.showModal = true;
    },
  },
};
</script>

<style scoped>
.loading,
.error {
  padding: 20px;
  text-align: center;
  font-size: 1.2rem;
}

.error {
  color: #dc3545;
}

.assignment-card {
  max-height: 80vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.assignment-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.admin-controls {
  margin: 20px 0;
}

.admin-actions button {
  margin-left: 10px;
  padding: 5px 15px;
}

.questions-section {
  margin-top: 20px;
}

.question-card {
  padding: 15px;
  margin: 15px 0;
  background: #f8f9fa;
  border-radius: 6px;
}

.question-text {
  font-weight: 500;
  margin-bottom: 10px;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.option-label {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.option-label:hover {
  background: #f8f9fa;
}

input[type="radio"] {
  margin-right: 10px;
}

.submission-controls {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.score-display {
  font-weight: bold;
  color: #28a745;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 500px;
}

.modal-content input,
.modal-content textarea {
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}

.modal-actions {
  margin-top: 20px;
  text-align: right;
}

.modal-actions button {
  margin-left: 10px;
  padding: 8px 20px;
}
</style>
