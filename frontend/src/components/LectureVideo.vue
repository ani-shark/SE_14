<template>
    <h3>{{ details ? details.name : 'No content available' }}</h3>
    <div class="video-pane">
        <video :key="details?.id" controls>
            <source :src="details?.videoUrl || require('@/assets/default.mp4')" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        <button class="get-help-btn-video">Get Help</button>
    </div>
</template>

<script>
export default {
    props:{details:{
        type:String,
        required:true
    }},
    data() {
        return {
           
        };
    },
    methods: {
       
    },
};
</script>
