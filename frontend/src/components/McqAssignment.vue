<template>
  <div>
    <h1>MCQ Assignments</h1>

    <div v-if="isAdmin">
      <button @click="openCreateModal">Create Assignment</button>
    </div>

    <div v-for="assignment in assignments" :key="assignment.id" class="assignment">
      <h2>{{ assignment.title }}</h2>
      <p>{{ assignment.description }}</p>

      <div v-if="isAdmin">
        <button @click="editAssignment(assignment)">Edit</button>
        <button @click="deleteAssignment(assignment.id)">Delete</button>
      </div>

      <div v-for="question in assignment.questions" :key="question.id" class="question">
        <p>{{ question.text }}</p>
        <div v-for="option in question.options" :key="option">
          <label>
            <input type="radio" :name="'q' + question.id" :value="option" v-model="userAnswers[question.id]" />
            {{ option }}
          </label>
        </div>
      </div>

      <button @click="submitAnswers(assignment.id)">Submit Answers</button>
      <p v-if="scores[assignment.id]">Your Score: {{ scores[assignment.id] }}</p>
    </div>

    <div v-if="showModal" class="modal">
      <input v-model="newAssignment.title" placeholder="Title" />
      <textarea v-model="newAssignment.description" placeholder="Description"></textarea>
      <button @click="saveAssignment">Save</button>
      <button @click="showModal = false">Cancel</button>
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
      showModal: false,
      newAssignment: { title: "", description: "" },
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
        const response = await fetch("http://127.0.0.1:5000/assignment/mcq/1", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf_access_token,
          },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch assignments");
        }
        this.assignments = await response.json();
      } catch (error) {
        console.error("Error fetching assignments:", error);
      }
    },

    async submitAnswers(assignmentId) {
      try {
        const csrf_access_token = await this.getToken();
        const payload = { assignment_id: assignmentId, answers: this.userAnswers };
        const response = await fetch("http://127.0.0.1:5000/assignment/submit/mcq", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf_access_token,
          },
          credentials: "include",
          body: JSON.stringify(payload),
        });
        if (!response.ok) {
          throw new Error("Failed to submit answers");
        }
        const data = await response.json();
        this.scores[assignmentId] = data.score;
      } catch (error) {
        console.error("Error submitting answers:", error);
      }
    },

    async checkAdmin() {
      try {
        const csrf_access_token = await this.getToken();
        const response = await fetch("http://127.0.0.1:5000/user/get", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf_access_token,
          },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to check admin status");
        }
        const data = await response.json();
        this.isAdmin = data.role === "admin";
      } catch (error) {
        console.error("Error checking admin status:", error);
      }
    },

    openCreateModal() {
      this.showModal = true;
    },

    async saveAssignment() {
      try {
        const csrf_access_token = await this.getToken();
        await fetch("http://127.0.0.1:5000/assignment/mcq", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf_access_token,
          },
          credentials: "include",
          body: JSON.stringify(this.newAssignment),
        });
        this.showModal = false;
        this.fetchAssignments();
      } catch (error) {
        console.error("Error creating assignment:", error);
      }
    },

    async editAssignment(assignment) {
      const updatedTitle = prompt("Edit Title", assignment.title);
      if (updatedTitle) {
        try {
          const csrf_access_token = await this.getToken();
          await fetch(`http://127.0.0.1:5000/assignment/mcq/${assignment.id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRF-TOKEN": csrf_access_token,
            },
            credentials: "include",
            body: JSON.stringify({ title: updatedTitle }),
          });
          this.fetchAssignments();
        } catch (error) {
          console.error("Error updating assignment:", error);
        }
      }
    },

    async deleteAssignment(id) {
      try {
        const csrf_access_token = await this.getToken();
        await fetch(`http://127.0.0.1:5000/assignment/mcq/${id}`, {
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
    },
  },
};
</script>


<style>
.assignment {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
}
.question {
  margin: 10px 0;
}
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border: 1px solid #ccc;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}
</style>
