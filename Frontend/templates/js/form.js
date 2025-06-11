const API_BASE_URL = "https://liftologybackend-production.up.railway.app";

// Check authentication and plan status
document.addEventListener("DOMContentLoaded", async () => {
  const currentUser = JSON.parse(localStorage.getItem("currentUser"));

  if (!currentUser) {
    window.location.href = "signin-signup.html";
    return;
  } else if (currentUser.exercise_plan) {
    // User already has a plan
    window.location.href = "plan.html";
    return;
  }

  // Initialize dropdowns
  initializeDropdowns();
});

// Form submission handler
document.getElementById("predictForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  if (
    validateInput(
      document.getElementById("weight"),
      /^(30|[3-9][0-9]|1[0-9]{2}|2[0-4][0-9]|250)$/
    ) &&
    validateInput(
      document.getElementById("height"),
      /^(5[0-9]|[6-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/
    ) &&
    validateInput(
      document.getElementById("age"),
      /^(?:[1-9]?[0-9]|1[01][0-9]|120)$/
    ) &&
    validateInput(document.getElementById("gender"), /(male|female)/) &&
    validateInput(document.getElementById("fitnessPlan"), /(weight_loss|muscle_gain|maintenance|general_fitness)/)
  ) {
    const currentUser = JSON.parse(localStorage.getItem("currentUser"));
    if (!currentUser) {
      window.location.href = "signin-signup.html";
      return;
    }

    const payload = {
      weight: parseFloat(document.getElementById("weight").value),
      height: parseFloat(document.getElementById("height").value / 100),
      bmi: document.getElementById("bmi").value
        ? parseFloat(document.getElementById("bmi").value)
        : weight / Math.pow(height, 2),
      body_fat_percentage: document.getElementById("bodyFat").value,
      age: parseFloat(document.getElementById("age").value),
      gender: document.getElementById("gender").value,
      fitnessGoal: document.getElementById("fitnessPlan").value,
    };

    try {
      // Generate fitness plan
      const response = await fetch(
        `${API_BASE_URL}/generate/${currentUser.user_info.email}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(
          errorData?.message ||
            `Server error: ${response.status} ${response.statusText}`
        );
      }

      const result = await response.json();

      if (!result || result.status !== "success") {
        throw new Error(
          result?.message ||
            "Failed to generate plan: Invalid response from server"
        );
      }

      currentUser.exercise_plan = {};
      currentUser.exercise_plan.input = payload;
      currentUser.exercise_plan.output = result.plan;
      localStorage.setItem("currentUser", JSON.stringify(currentUser));
      window.location.href = "plan.html";
    } catch (error) {
      console.error("Error details:", error);
      showErrorAlert(error.message || "Failed to generate your plan. Please try again.");
    }
  }
});

// Navbar scroll effect
window.addEventListener("scroll", function () {
  const navbar = document.querySelector(".navbar");
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});

// Theme Toggle Functionality
const themeToggle = document.getElementById("themeToggle");
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

// Check for saved theme preference or use system preference
const currentTheme =
  localStorage.getItem("theme") ||
  (prefersDarkScheme.matches ? "dark" : "light");

// Apply the current theme
if (currentTheme === "dark") {
  document.documentElement.setAttribute("data-theme", "dark");
  themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
} else {
  document.documentElement.removeAttribute("data-theme");
  themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
}

// Toggle theme on button click
themeToggle.addEventListener("click", () => {
  let theme;
  if (document.documentElement.getAttribute("data-theme")) {
    document.documentElement.removeAttribute("data-theme");
    theme = "light";
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
  } else {
    document.documentElement.setAttribute("data-theme", "dark");
    theme = "dark";
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
  }
  localStorage.setItem("theme", theme);
});

// Listen for system theme changes
prefersDarkScheme.addEventListener("change", (e) => {
  if (!localStorage.getItem("theme")) {
    if (e.matches) {
      document.documentElement.setAttribute("data-theme", "dark");
      themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
      document.documentElement.removeAttribute("data-theme");
      themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
  }
});

// Input validation function
function validateInput(input, regex) {
  var bool = regex.test(input.value);
  input.classList.toggle("is-valid", bool);
  input.classList.toggle("is-invalid", !bool);
  input.nextElementSibling.classList.toggle("d-none", bool);
  return bool;
}

// Initialize custom dropdowns
function initializeDropdowns() {
  const dropdowns = document.querySelectorAll('.dropdown');
  
  dropdowns.forEach(dropdown => {
    const button = dropdown.querySelector('.form-select');
    const items = dropdown.querySelectorAll('.dropdown-item');
    const hiddenInput = dropdown.querySelector('input[type="hidden"]');
    const errorMessage = dropdown.querySelector('.text-danger');
    
    items.forEach(item => {
      item.addEventListener('click', function(e) {
        e.preventDefault();
        const value = this.getAttribute('data-value');
        const text = this.textContent;
        
        // Update button text
        button.querySelector('.selected-option').textContent = text;
        
        // Update hidden input
        hiddenInput.value = value;
        
        // Update validation state
        button.classList.remove('is-invalid');
        button.classList.add('is-valid');
        if (errorMessage) {
          errorMessage.classList.add('d-none');
        }
        
        // Update active state
        items.forEach(i => i.classList.remove('active'));
        this.classList.add('active');
      });
    });
  });
}

// Show error alert
function showErrorAlert(message) {
  const errorAlert = document.createElement("div");
  errorAlert.className = "alert alert-danger alert-dismissible fade show";
  errorAlert.style.position = "fixed";
  errorAlert.style.top = "20px";
  errorAlert.style.left = "50%";
  errorAlert.style.transform = "translateX(-50%)";
  errorAlert.style.zIndex = "9999";
  errorAlert.style.minWidth = "300px";
  errorAlert.style.textAlign = "center";
  errorAlert.innerHTML = `
    <strong>Error!</strong> ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;

  document.body.appendChild(errorAlert);

  // Auto dismiss after 5 seconds
  setTimeout(() => {
    errorAlert.remove();
  }, 5000);
} 