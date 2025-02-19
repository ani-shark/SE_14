<template>
    <h3>{{ details ? details.name : 'No content available' }}</h3>

    <div class="assignment-section">
        <p style="align-self:flex-start;"><strong>This assignment is only for practice.</strong></p>
        <p style="align-self: flex-start;"><strong>Deadline:</strong> <span style="color: red;">04/02/2025</span></p>
        <p class="success-message" id="success-message">Assignment Submitted Successfully!</p>
        <div class="assignment-question">
            <div class="assignment-question-content">
                <p>1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vitae lacus velit.</p>
                <ul>
                    <li><input type="radio" name="question1"> Option 1</li>
                    <li><input type="radio" name="question2"> Option 2</li>
                    <li><input type="radio" name="question3"> Option 3</li>
                    <li><input type="radio" name="question4"> Option 4</li>
                </ul>
            </div>

            <button class="get-help-btn-assign" @click="getHelp()">Get Help</button>
        </div>
        <div class="assignment-question">
            <div class="assignment-question-content">
                <p>2. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vitae lacus velit.</p>
                <ul>
                    <li><input type="radio" name="question1"> Option 1</li>
                    <li><input type="radio" name="question2"> Option 2</li>
                    <li><input type="radio" name="question3"> Option 3</li>
                    <li><input type="radio" name="question4"> Option 4</li>
                </ul>
            </div>

            <button class="get-help-btn-assign" @click="getHelp()">Get Help</button>
        </div>

        <button class="submit-btn" id="submit-btn">Submit</button>
        <p class="success-message" id="success-message">Assignment Submitted Successfully!</p>
    </div>

</template>

<script>
export default {
    props: {
        details: {
            type: Object,
            required: true
        }
    },
    data() {
        return {

        };
    },
    methods: {
        // Get AI Agent guidance for this Mcq
        getHelp(){
            const query = {...this.details};
            this.$router.push({path:'/Agent',query:query})
        }
    },
};
</script>
