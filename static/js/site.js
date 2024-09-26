const checkbox = document.getElementById("checkbox")
checkbox.addEventListener("change", () => {
    document.body.classList.toggle("dark")
})


const toastLiveExample = document.getElementById('errorToast');
const toast = new bootstrap.Toast(toastLiveExample, { autohide: true });
toast.show();

