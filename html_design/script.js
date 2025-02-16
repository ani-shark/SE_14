
//  Dark Mode Script
document.addEventListener("DOMContentLoaded", function () {
const toggleButton = document.getElementById("theme-toggle");
const body = document.body;

if (localStorage.getItem("theme") === "dark") {
  body.classList.add("dark-mode");
  toggleButton.textContent = "☀️";
} else {
  toggleButton.textContent = "🌙";
}

toggleButton.addEventListener("click", function () {
  body.classList.toggle("dark-mode");
  localStorage.setItem(
    "theme",
    body.classList.contains("dark-mode") ? "dark" : "light"
  );
  toggleButton.textContent = body.classList.contains("dark-mode")
    ? "☀️"
    : "🌙";
  const sidebar = document.getElementById("accordion");
  if (localStorage.getItem("theme") === "dark") {
    sidebar.style.background = "#333";
  } else {
    sidebar.style.background = "#f8f9fa";
  }
});
});

// End


// Sidebar Responsiveness Script
function adjustSidebar() {
const sidebar = document.getElementById("accordion");
const toggleButton = document.getElementById("accordion-toggle");

if (window.innerWidth <= 968) {
  sidebar.style.left = "0";
  sidebar.style.width = "250px";
  sidebar.style.height = "100%";
  sidebar.style.position = "fixed";
  sidebar.style.top = "0";
  sidebar.style.transition = "left 0.3s ease-in-out";
  toggleButton.style.display = "block";
} else {
  sidebar.style.height = "100%";
  sidebar.style.position = "";
  sidebar.style.width = "25%";
  toggleButton.style.display = "none"; 
}
}

window.addEventListener("load", adjustSidebar);
window.addEventListener("resize", adjustSidebar);

document.addEventListener("DOMContentLoaded", function () {
const accordion = document.getElementById("accordion");
const toggleButton = document.getElementById("accordion-toggle");
const closeButton = document.getElementById("close-accordion");

function handleSidebarDisplay() {
  if (window.innerWidth <= 968) {
    accordion.style.display = "none";
    toggleButton.style.display = "block";
    closeButton.style.display = "block";
  } else {
    accordion.style.display = "block";
    toggleButton.style.display = "none";
    closeButton.style.display = "none";
  }
}

handleSidebarDisplay();

window.addEventListener("resize", handleSidebarDisplay);

toggleButton.addEventListener("click", function () {
  accordion.style.display = "block";
  this.style.display = "none"; 
});


closeButton.addEventListener("click", function () {
  accordion.style.display = "none";
  toggleButton.style.display = "block"; 
});
});

// End

// Accordion content expansion
document.querySelectorAll(".accordion-header").forEach((item) => {
    item.addEventListener("click", function () {
      this.classList.toggle("active");
      let content = this.nextElementSibling;
      content.style.display =
        content.style.display === "block" ? "none" : "block";
    });
  });

