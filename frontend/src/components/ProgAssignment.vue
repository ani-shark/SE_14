<template>
    <div class="programming-assignment">
        <h4>Programming Assignment</h4>
        <p>This is for practice only</p>
        <p>Deadline: <span style="color: red;">DD-MM-YYYY</span></p>
        <div class="programming-question">
            <p>
                Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Architecto esse alias ipsa reiciendis veniam ut, magnam officiis
                numquam sed optio consequuntur at unde corporis sint quasi,
                sapiente sequi eaque recusandae. Lorem, ipsum dolor sit amet
                consectetur adipisicing elit. Ad autem perspiciatis saepe fugit
                asperiores vero, aliquam delectus! Ab, harum, necessitatibus
                quidem consectetur ex officia placeat rem amet doloremque delectus
                sint. Lorem ipsum dolor sit amet consectetur adipisicing elit.
                Soluta odio nobis assumenda in ad ratione velit laudantium dolorum
                vitae rem facere laborum exercitationem, ea praesentium magnam
                natus earum sapiente labore? Lorem, ipsum dolor sit amet
                consectetur adipisicing elit. Minima amet quam explicabo hic?
                Quaerat dignissimos aspernatur ad quidem libero explicabo
                voluptatem perferendis sequi praesentium deleniti ut, iste harum
                illum cumque.
            </p>
        </div>
        <div class="format-details">
            <div class="code-format">
                Input Format
                <div>Code</div>
            </div>
            <div class="code-format">
                Output Format
                <div>Code</div>
            </div>
        </div>

        <div class="programming-assignment-btns">
            <div class="submit-code">
                <label class="custom-file-upload">
                    <input type="file" />
                    <i class="fas fa-upload"></i> Upload File
                </label>
            </div>
            <button class="get-help-btn">Get Help</button>
        </div>

        <div class="test-results">
            Public Test Cases:&nbsp; <span>5/5 passed</span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProgAssignment',
    data() {
        return {
            // Add your component data here
        };
    },
    methods: {
        // Add your component methods here
    },
    computed: {
        // Add your computed properties here
    },
    mounted() {
        // Lifecycle hook when the component is mounted
    }
};
</script>
