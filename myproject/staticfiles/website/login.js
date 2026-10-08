document.addEventListener("DOMContentLoaded", function() {
    console.log("Hume Properties login script loaded successfully!");

    // --- 0. Password Changed Success Message Check ---
    const successWrapper = document.getElementById('login-success-data');
    if (successWrapper) {
        const successMessage = successWrapper.getAttribute('data-message');
        if (successMessage && successMessage.trim() !== "") {
            Swal.fire({
                title: 'Success!',
                text: successMessage,
                icon: 'success',
                confirmButtonColor: '#2563eb',
                confirmButtonText: 'OK'
            });
        }
    }

    // 1. Role Box Selection
    const roleBoxes = document.querySelectorAll('.role-box');
    roleBoxes.forEach(function(box) {
        box.addEventListener('click', function() {
            roleBoxes.forEach(b => b.style.borderColor = '');
            this.style.borderColor = '#2563eb';
        });
    });

    // 2. Login Form AJAX Submission (Login page par hi popup dikhane ke liye)
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Page ko direct refresh/redirect hone se rokna
            e.stopImmediatePropagation();

            let formData = new FormData(this);

            // Backend par background mein request bhejna
            fetch(this.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                // Agar login successful hokar backend ne redirect response diya hai
                if (response.redirected) {
                    Swal.fire({
                        title: 'Login Successful!',
                        text: 'Welcome back to Hume Properties!',
                        icon: 'success',
                        confirmButtonColor: '#2563eb',
                        timer: 1500, // 1.5 second popup dikhega
                        showConfirmButton: false
                    }).then(() => {
                        window.location.href = response.url; // Popup hatne ke baad redirect hoga
                    });
                } else {
                    // Agar password galat hai ya form invalid hai
                    return response.text().then(html => {
                        Swal.fire({
                            title: 'Login Failed!',
                            text: 'Invalid email/mobile or password. Please try again.',
                            icon: 'error',
                            confirmButtonColor: '#2563eb',
                            confirmButtonText: 'Try Again'
                        });
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }, true);
    }
});

