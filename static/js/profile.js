window.onload = loadProfile;

async function loadProfile() {

    const token = localStorage.getItem("token");

    if (!token) {

        window.location.href = "/login-page";
        return;

    }

    const response = await fetch("/profile", {

        method: "GET",

        headers: {
            "Authorization": "Bearer " + token
        }

    });

    if (response.status === 401) {

        localStorage.removeItem("token");
        window.location.href = "/login-page";
        return;

    }

    const data = await response.json();

    document.getElementById("name").value = data.name;
    document.getElementById("email").value = data.email;

}

async function updateProfile() {

    const token = localStorage.getItem("token");

    const name = document.getElementById("name").value;

    const response = await fetch("/update-profile", {

        method: "PUT",

        headers: {

            "Content-Type": "application/json",
            "Authorization": "Bearer " + token

        },

        body: JSON.stringify({

            name: name

        })

    });

    const data = await response.json();

    showToast(data.message);

}