window.onload = function () {

    const email = localStorage.getItem("resetEmail");

    document.getElementById("email").value = email;

}

async function resetPassword() {

    const email = document.getElementById("email").value;

    const otp = document.getElementById("otp").value;

    const password = document.getElementById("password").value;

    const confirmPassword = document.getElementById("confirmPassword").value;

    if(password !== confirmPassword){

        showToast("Passwords do not match");

        return;

    }

    const response = await fetch("/reset-password",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            email:email,

            otp:otp,

            new_password:password

        })

    });

    const data = await response.json();

showToast(data.message);

if (response.ok) {

    localStorage.removeItem("resetEmail");

    setTimeout(() => {

        window.location.href = "/login-page";

    }, 1500);

}

}