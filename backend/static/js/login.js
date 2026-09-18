const passwordField = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");

const loginForm = document.getElementById("loginForm");
const errorMessage = document.getElementById("errorMessage");
const loginButton = document.getElementById("loginButton");

// =========================================================
// SHOW / HIDE PASSWORD
// =========================================================

togglePassword.addEventListener("click", function () {

    
const isPassword =
    passwordField.type === "password";

passwordField.type =
    isPassword ? "text" : "password";

const icon =
    this.querySelector(".material-symbols-outlined");

icon.textContent =
    isPassword ? "visibility_off" : "visibility";

this.setAttribute(
    "aria-label",
    isPassword
        ? "Hide password"
        : "Show password"
);


});

// =========================================================
// LOGIN
// =========================================================

loginForm.addEventListener("submit", async function (event) {

event.preventDefault();


const username =
    document.getElementById("username")
        .value
        .trim();

const password =
    passwordField.value;


// Clear previous error
errorMessage.classList.add("d-none");
errorMessage.innerText = "";


// Disable button
loginButton.disabled = true;

loginButton.querySelector(".button-text")
    .innerText = "Logging in...";


try {

    const response = await fetch(
        "/api/users/login/",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })
        }
    );


    const data = await response.json();


    if (response.ok) {

        // Store JWT tokens
        localStorage.setItem(
            "access_token",
            data.tokens.access
        );

        localStorage.setItem(
            "refresh_token",
            data.tokens.refresh
        );


        // Store user information
        localStorage.setItem(
            "user",
            JSON.stringify(data.user)
        );


        // Redirect to home
        window.location.href = "/home/";

    } else {

        errorMessage.innerText =
            data.error ||
            "Invalid username or password.";

        errorMessage.classList.remove("d-none");
    }


} catch (error) {

    console.error(
        "Login Error:",
        error
    );

    errorMessage.innerText =
        "Unable to connect to the server.";

    errorMessage.classList.remove("d-none");

} finally {

    loginButton.disabled = false;

    loginButton.querySelector(".button-text")
        .innerText = "Login";
}


});
