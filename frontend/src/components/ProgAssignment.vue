<template>
    <div v-if="loading" class="loading">
        Loading assignment details...
    </div>
    <div v-else-if="error" class="error">
        {{ error }}
    </div>
    <div v-else-if="details" class="programming-assignment">
        <h4>{{ details.title }}</h4>
        <p>{{ details.description }}</p>
        
        <div class="programming-question">
            <p>{{ details.description }}</p>
        </div>
        
        <div class="format-details">
            <div class="code-format">
                Input Format
                <div>
                    <pre v-if="details.test_cases && details.test_cases.length">
                        {{ details.test_cases.map(tc => tc.input).join('\n') }}
                    </pre>
                    <p v-else>No test cases available</p>
                </div>
            </div>
            <div class="code-format">
                Output Format
                <div>
                    <pre v-if="details.test_cases && details.test_cases.length">
                        {{ details.test_cases.map(tc => tc.expected_output).join('\n') }}
                    </pre>
                    <p v-else>No test cases available</p>
                </div>
            </div>
        </div>
        
        <div class="programming-assignment-btns">
            <div class="submit-code">
                <label class="custom-file-upload">
                    <input 
                        type="file" 
                        @change="handleFileUpload" 
                        accept=".py"
                    />
                    <i class="fas fa-upload"></i> Upload Python File
                </label>
            </div>
            <button class="get-help-btn" @click="getHelp()">Get Help</button>
            <button 
                class="submit-btn" 
                @click="submitAssignment" 
                :disabled="!selectedFile"
            >
                Submit Assignment
            </button>
        </div>
        
        <div class="test-results" v-if="submissionResult">
            Public Test Cases: 
            <span :class="submissionResult.score === testCasesCount ? 'success' : 'failed'">
                {{ submissionResult.score }}/{{ testCasesCount }} passed
            </span>
        </div>
        
        <div v-if="submitError" class="error-message">
            {{ submitError }}
        </div>
    </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
    props: {
        id: {
            type: [String, Number],
            required: true
        }
    },
    data() {
        return {
            details: null,
            loading: true,
            error: null,
            selectedFile: null,
            submissionResult: null,
            submitError: null,
            baseUrl: 'http://localhost:5000'  // Direct reference to localhost
        };
    },
    computed: {
        testCasesCount() {
            return this.details?.test_cases ? this.details.test_cases.length : 0;
        }
    },
    created() {
        this.fetchAssignmentDetails();
    },
    watch: {
        // Watch for changes in the route parameter
        id: {
            handler: 'fetchAssignmentDetails',
            immediate: true
        }
    },
    methods: {
        ...mapActions(["getToken"]),
        async fetchAssignmentDetails() {
            this.loading = true;
            this.error = null;

            try {
                const csrf_access_token = await this.getToken();
                // Using fetch API instead of axios
                const response = await fetch(`http://localhost:5000/assignment/programming/1`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRF-TOKEN": csrf_access_token,
                    },
                    credentials: "include",
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                
                const data = await response.json();
                console.log('Assignment details:', data);
                this.details = data;
            } catch (error) {
                console.error('Failed to fetch assignment details:', error);
                this.error = error.message || 'Failed to load assignment details';
            } finally {
                this.loading = false;
            }
        },

        // File upload handler
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file && file.name.endsWith('.py')) {
                this.selectedFile = file;
                this.submitError = null;
            } else {
                this.submitError = 'Please upload a Python (.py) file';
                this.selectedFile = null;
            }
        },

        // Read file content
        async readFileContent(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = (e) => resolve(e.target.result);
                reader.onerror = (e) => reject(e);
                reader.readAsText(file);
            });
        },

        // Submit assignment
        async submitAssignment() {
            if (!this.selectedFile) {
                this.submitError = 'Please upload a Python file first';
                return;
            }

            try {
                const csrf_access_token = await this.getToken();
                // Read file content
                const code = await this.readFileContent(this.selectedFile);
                console.log('Submitted code:', code);

                // Using fetch API for POST request
                const response = await fetch(`${this.baseUrl}/assignment/submit/programming`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        "X-CSRF-TOKEN": csrf_access_token,
                    },
                    body: JSON.stringify({
                        assignment_id: this.id,
                        code: code
                    }),
                    credentials: 'include',
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => null);
                    throw new Error(errorData?.error || `HTTP error! Status: ${response.status}`);
                }

                // Parse the response
                const resultData = await response.json();
                
                // Store submission result
                this.submissionResult = resultData;
                this.submitError = null;
            } catch (error) {
                console.error('Submission error:', error);
                this.submitError = error.message || 'Failed to submit assignment';
                this.submissionResult = null;
            }
        },

        // Get AI Agent guidance for this assignment
        getHelp() {
            const query = { ...this.details };
            this.$router.push({ path: '/Agent', query: query });
        }
    }
};
</script>

<style scoped>
.loading, .error {
    text-align: center;
    margin-top: 20px;
    font-size: 18px;
}
.error {
    color: red;
}
.programming-assignment {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 8px;
}
.format-details {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}
.code-format {
    width: 48%;
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    padding: 15px;
    border-radius: 5px;
}
.programming-assignment-btns {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}
.submit-btn, .get-help-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
.submit-btn {
    background-color: #4CAF50;
    color: white;
}
.submit-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}
.get-help-btn {
    background-color: #2196F3;
    color: white;
}
.test-results {
    margin-top: 20px;
    text-align: center;
    font-weight: bold;
}
.success {
    color: green;
}
.failed {
    color: red;
}
.custom-file-upload {
    display: inline-block;
    padding: 10px 20px;
    background-color: #f0f0f0;
    border-radius: 5px;
    cursor: pointer;
}
.custom-file-upload input[type="file"] {
    display: none;
}
</style>