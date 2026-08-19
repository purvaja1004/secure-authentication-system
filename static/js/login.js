async function loginUser() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
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

    showToast(data.message);

    if (response.status == 200) {

        localStorage.setItem("token", data.token);

        // Wait 2 seconds before redirecting
        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 2000);

    }

}