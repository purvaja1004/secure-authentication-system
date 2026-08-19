window.onload = async function () {

    const token = localStorage.getItem("token");

    if (!token) {

        window.location.href = "/login-page";
        return;

    }

    const response = await fetch("/profile", {

        headers: {

            Authorization: "Bearer " + token

        }

    });

    if (!response.ok) {

        localStorage.removeItem("token");
        window.location.href = "/login-page";
        return;

    }

    const data = await response.json();

    document.getElementById("userName").innerText = data.name;
    document.getElementById("userEmail").innerText = data.email;

}

function logout() {

    localStorage.removeItem("token");

    window.location.href = "/login-page";

}