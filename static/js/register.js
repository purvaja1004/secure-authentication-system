async function registerUser(){

const name=document.getElementById("name").value;

const email=document.getElementById("email").value;

const password=document.getElementById("password").value;

const response=await fetch("/register",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

name:name,

email:email,

password:password

})

});

const data=await response.json();

showToast(data.message);

setTimeout(() => {
    window.location.href = "/login-page";
}, 2000);

}

function checkStrength() {

    const password = document.getElementById("password").value;

    const bar = document.getElementById("strengthBar");

    const text = document.getElementById("strengthText");

    let strength = 0;

    if(password.length >= 8)
        strength++;

    if(/[A-Z]/.test(password))
        strength++;

    if(/[0-9]/.test(password))
        strength++;

    if(/[!@#$%^&*]/.test(password))
        strength++;

    if(strength == 0){

        bar.style.width = "0%";
        bar.className = "progress-bar";
        text.innerHTML = "";

    }

    else if(strength == 1){

        bar.style.width = "25%";
        bar.className = "progress-bar bg-danger";
        text.innerHTML = "Weak Password";

    }

    else if(strength == 2){

        bar.style.width = "50%";
        bar.className = "progress-bar bg-warning";
        text.innerHTML = "Medium Password";

    }

    else if(strength == 3){

        bar.style.width = "75%";
        bar.className = "progress-bar bg-info";
        text.innerHTML = "Good Password";

    }

    else{

        bar.style.width = "100%";
        bar.className = "progress-bar bg-success";
        text.innerHTML = "Strong Password";

    }

}