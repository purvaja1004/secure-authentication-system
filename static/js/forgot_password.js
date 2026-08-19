async function forgotPassword() {

    const email = document.getElementById("email").value;

    if (email === "") {

        showToast("Please enter your email.");

        return;
    }

    const response = await fetch("/forgot-password", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            email: email

        })

    });

    const data = await response.json();

   showToast(data.message);

    if (response.ok) {

        localStorage.setItem("resetEmail", email);

        window.location.href = "/reset-page";

    }

}