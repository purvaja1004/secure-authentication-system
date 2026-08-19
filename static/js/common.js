function togglePassword(inputId, icon){

    const input = document.getElementById(inputId);

    if(input.type === "password"){
        input.type = "text";
        icon.classList.replace("fa-eye","fa-eye-slash");
    }else{
        input.type = "password";
        icon.classList.replace("fa-eye-slash","fa-eye");
    }

}

function showToast(message){

    const toastBody=document.getElementById("toastMessage");
    toastBody.innerText=message;

    const toastLive=document.getElementById("liveToast");

    const toast=new bootstrap.Toast(toastLive,{
        delay:3000
    });

    toast.show();

}