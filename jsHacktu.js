
function login(role) {
  if (role === "psychiatrist") {
    window.location.href = "doctor.html";
  } else {
    window.location.href = "patient.html";
  }
}


function doctorLogin() {
  const email = document.getElementById("doctoremail").value;
  const password = document.getElementById("doctorpassword").value;

  if (email === "" || password === "") {
    alert("Please fill all fields");
    return;
  }

 
  window.location.href = "doctor-dashboard.html";
}


function toggleProfile() {
  const dropdown = document.getElementById("profileDropdown");
  dropdown.style.display =
    dropdown.style.display === "block" ? "none" : "block";
}


function logout() {
  window.location.href = "index.html";
}


function forgotPassword() {
  alert("Please contact system administrator to reset your password.");
}
function searchPatient() {
  const input = document.querySelector(".search-patient").value.toLowerCase();
  const cards = document.querySelectorAll(".patient-card");

  cards.forEach(card => {
    const name = card.querySelector(".patient-name").innerText.toLowerCase();

    if (name.includes(input)) {
      card.style.display = "block";
      card.classList.add("highlight");
    } else {
      card.style.display = "none";
      card.classList.remove("highlight");
    }
  });

  if (input === "") {
    cards.forEach(card => {
      card.style.display = "block";
      card.classList.remove("highlight");
    });
  }
}
function openRegistration() {
  window.location.href = "registrationpage.html";
}
function togglePatient(btn) {
  const card = btn.closest(".patient-card");
  const dropdown = card.querySelector(".patient-dropdown");

  dropdown.style.display =
    dropdown.style.display === "block" ? "none" : "block";
}

async function doctorLogin() {
  const email = document.getElementById("doctoremail").value;
  const password = document.getElementById("doctorpassword").value;

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {
    const response = await fetch("http://localhost:3000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    const data = await response.json();

    if (data.user) {

      // Optional: Ensure only doctors can login here
      if (data.user.role !== "doctor") {
        alert("Access denied. Not a doctor account.");
        return;
      }

      // Store user info
      localStorage.setItem("user", JSON.stringify(data.user));

      alert("Login successful");

      // Redirect to dashboard page
      window.location.href = "doctor-dashboard.html";  // change if needed

    } else {
      alert(data.error || "Login failed");
    }

  } catch (error) {
    console.error(error);
    alert("Server error. Make sure backend is running.");
  }
}