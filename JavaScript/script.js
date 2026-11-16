// A small amount of JavaScript to help the pages.
// The real application logic is done in Python (Flask).

// ----- Login page: check that both boxes are filled in -----
var loginForm = document.getElementById("login-form");

if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
        var username = document.getElementById("username").value.trim();
        var password = document.getElementById("password").value.trim();

        if (username === "" || password === "") {
            event.preventDefault();  // stop the form from being sent
            document.getElementById("error-message").textContent =
                "Please enter your User ID and password.";
        }
    });
}

// ----- Course page: ask before removing a student -----
var removeButtons = document.querySelectorAll(".remove-button");

for (var i = 0; i < removeButtons.length; i++) {
    removeButtons[i].addEventListener("click", function (event) {
        if (!confirm("Are you sure you want to remove this student from the course?")) {
            event.preventDefault();
        }
    });
}

// ----- Course page: the date box -----
var dateInput = document.getElementById("date");

if (dateInput) {
    // Build today's date in the format YYYY-MM-DD, for example 2026-11-16.
    var today = new Date();
    var month = String(today.getMonth() + 1).padStart(2, "0");
    var day = String(today.getDate()).padStart(2, "0");
    var todayText = today.getFullYear() + "-" + month + "-" + day;

    dateInput.max = todayText;  // the calendar will not allow future dates

    // When the teacher picks another date, reload the page for that date
    // so the saved Present / Late / Absent options are shown.
    dateInput.addEventListener("change", function () {
        if (dateInput.value !== "") {
            window.location = "?date=" + dateInput.value;
        }
    });
}
