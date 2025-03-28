$(document).ready(function () {
    const personnelButton = document.getElementById('personnel');
    const clientButton = document.getElementById('client');
    const container = document.getElementById('container');

    const personnelloginForm = document.getElementById('loginFormPersonnel');
    const personnelloginButton = document.getElementById('loginButtonP');
    const personnelemailInput = document.getElementById('emailP');
    const personnelpasswordInput = document.getElementById('passwordP');
    const personnelauthStateInput = document.getElementById('authStateP');

    personnelButton.addEventListener('click', function () {
        container.classList.add("right-panel-active");
        centerOverlayText('.overlay-panel.overlay-left');
    });

    clientButton.addEventListener('click', function () {
        container.classList.remove("right-panel-active");
        centerOverlayText('.overlay-panel.overlay-right');
    });

    function centerOverlayText(selector) {
        const overlayPanel = document.querySelector(selector);
        overlayPanel.style.display = 'flex';
        overlayPanel.style.alignItems = 'center';
        overlayPanel.style.justifyContent = 'center';
    }

    $("#loginButtonP").click(function () {
        var email = document.getElementById('emailP').value;
        var password = document.getElementById('passwordP').value;

        $.ajax({
            type: "post",
            url: "http://127.0.0.1:5000/login",
            data: {
                'email': email,
                'password': password,
            },
            success: function (response) {
                validarAcceso(response);
                $('#emailP').val('');
                $('#passwordP').val('');
            }
        });
        return false;
    });

    function validarAcceso(response) {
        if (response === 'Acceso válido') {
            personnelauthStateInput.value = "true";
            window.location.href = "adopcion_admin.html";
        } else {
            alert("Usuario o contraseña incorrectos");
        }
    }
});
