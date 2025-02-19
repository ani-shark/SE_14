<template>

    <seek-nav title='AI Agent' type="ai agent"></seek-nav>
    <button class="accordion-toggle" id="accordion-toggle">☰</button>
    <div class="chat-content">
        <div class="accordion" id="accordion">
            <button id="close-accordion" class="accordion-close">✖</button>
            <div class="chat-header">
                <div class="text-truncate" >Chat History</div>
                <button @click="buttonNew()" class="new-chat-btn">+ New Chat</button>
            </div>
            
            <div class="chat-list">
                <div class="chat-item" v-for="(chat, index) in chatHistory" :key="index">
                    <div class="text-truncate" style="padding-left: 0.8em">{{ chat.title }}</div>
                    <input type="radio" name="main-content" :value="index" v-model="selectedChat"
                        @change="loadChat(index)" />
                </div>

            </div>
        </div>
        <div class="chat-area">
            <div class="chat-box" id="chat-box">
                <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.sender]">
                    {{ msg.text }}
                </div>
            </div>
            <div class="chat-input">
                <textarea v-model="userInput" placeholder="Type a message..."></textarea>
                <button @click="sendMessage"><i class="fa fa-paper-plane"></i></button>
            </div>
        </div>
    </div>

</template>


<script>
import SeekNavbar from '@/components/SeekNavbar.vue';
export default {
    components: { 'seek-nav': SeekNavbar },
    data() {
        return {
            accordionVisible: false,
            chatHistory: JSON.parse(localStorage.getItem("chatHistory")) || [],
            userInput: "",
            messages: [],
            selectedChat: 0
        };
    },
    methods: {
        toggleSidebar() {
            this.accordionVisible = !this.accordionVisible;
        },
        closeSidebar() {
            this.accordionVisible = false;
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
                sidebar.style.display = 'none';
                closeButton.style.display = 'block';
                sidebar.style['z-index'] = 1000;
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
        },
        // Random Response for a Query
        async fetchAIResponse() {
            try {
                const response = await fetch("https://baconipsum.com/api/?type=meat-and-filler&sentences=10");
                const data = await response.json();
                return data[0] || "Could not generate a response.";
            } catch (error) {
                return "I'm having trouble generating a response right now. Please try again.";
            }
        },

        // Send Query
        async sendMessage() {
            if (this.userInput.trim() === "") return;
            this.messages.push({ text: this.userInput, sender: "user" });
            if (this.chatHistory[this.selectedChat].title === "New Chat") {
                this.chatHistory[this.selectedChat].title = this.userInput.substring(0, 20) || "Untitled Chat";
            }
            this.userInput = "";
            const botResponse = await this.fetchAIResponse();
            this.messages.push({ text: botResponse, sender: "bot" });
            this.saveChat();

        },
        saveChat() {
            if (this.messages.length === 0) return;
            this.chatHistory[this.selectedChat].messages = [...this.messages];
            localStorage.setItem("chatHistory", JSON.stringify(this.chatHistory));
        },

        // Start New Chat
        startNewChat() {
            const urlParams = new URLSearchParams(window.location.search);
            const metaDetails = ['id', 'item_id', 'name']
                .filter(key => urlParams.has(key))
                .reduce((acc, key) => ({ ...acc, [key]: urlParams.get(key) }), {});

            if (Object.keys(metaDetails).length) {
                const existingChatIndex = this.chatHistory.findIndex(chat =>
                    chat.metaDetails &&
                    Object.keys(metaDetails).every(key => chat.metaDetails[key] === metaDetails[key])
                );
                if (existingChatIndex !== -1) {
                    this.selectedChat = existingChatIndex;
                    this.messages = [...this.chatHistory[this.selectedChat].messages];
                }
                else {
                    this.chatHistory = this.chatHistory.filter(chat => chat.title !== "New Chat" || chat.messages.length > 0);
                    const newChat = { title: "New Chat", messages: [] };
                    let msg = null;
                    msg = `What help do you need regarding ${metaDetails.name}?`
                    newChat.title = `${metaDetails.name}`
                    newChat.messages.push({
                        text: msg,
                        sender: "bot"
                    })
                    newChat.metaDetails = metaDetails;
                    this.chatHistory.push(newChat);
                    this.selectedChat = this.chatHistory.length - 1;
                    this.messages = [...newChat.messages];
                    localStorage.setItem("chatHistory", JSON.stringify(this.chatHistory));

                }
            } else {
                this.chatHistory = this.chatHistory.filter(chat => chat.title !== "New Chat" || chat.messages.length > 0);
                const newChat = { title: "New Chat", messages: [] };
                this.chatHistory.push(newChat);
                this.selectedChat = this.chatHistory.length - 1;
                this.messages = [...newChat.messages];
            }

            const url = new URL(window.location);
            url.searchParams.set('chat', this.selectedChat);
            window.history.pushState({}, '', url);
        },
        
        // Start new Chat from Sidebar
        buttonNew() {
            const url = new URL(window.location);
            ['id', 'item_id', 'name'].forEach(param => url.searchParams.delete(param));
            window.history.pushState({}, '', url);
            this.startNewChat()


        },

        // Load Existing Chat
        loadChat(index) {
            const url = new URL(window.location);
            this.selectedChat = index;
            this.messages = [...this.chatHistory[index].messages];

            url.searchParams.set('chat', index);

            if (this.chatHistory[index].metaDetails) {
                Object.entries(this.chatHistory[index].metaDetails).forEach(([key, value]) => {
                    url.searchParams.set(key, value);
                });
            } else {
                ['id', 'item_id', 'name'].forEach(param => url.searchParams.delete(param));
            }

            window.history.pushState({}, '', url);
        }

    },
    mounted() {
        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark-mode");
        }
        window.addEventListener("load", this.adjustSidebar);
        window.addEventListener("resize", this.adjustSidebar);
        this.adjustSidebar();

        // Load Existing Chat on load
        const urlParams = new URLSearchParams(window.location.search);
        const chatIndex = urlParams.get('chat');
        if (chatIndex !== null && !isNaN(chatIndex) && this.chatHistory[Number(chatIndex)]) {
            this.selectedChat = Number(chatIndex);
            this.messages = [...this.chatHistory[this.selectedChat].messages];
        } else {
            this.startNewChat();
        }
    }
};
</script>
