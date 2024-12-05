document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form.needs-validation');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');

    // Şifre eşleşme kontrolü
    function validatePassword() {
        if (password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity('Şifreler eşleşmiyor');
        } else {
            confirmPassword.setCustomValidity('');
        }
    }

    password.addEventListener('change', validatePassword);
    confirmPassword.addEventListener('keyup', validatePassword);

    // Form gönderilmeden önce validasyon
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });
});
