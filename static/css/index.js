document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting immediately
            alert("Login successfully!");
            loginForm.submit(); // Submit the form after showing the alert
        });
    }
});
