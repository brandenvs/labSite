const checkbox = document.getElementById("checkbox")

checkbox.addEventListener("change", () => {
    toggleTheme();
});

const toastLiveExample = document.getElementById('errorToast');
const toast = new bootstrap.Toast(toastLiveExample, { autohide: true });
toast.show();

function getTheme() {
    selectedTheme = '';

    $.ajax({
        url: '/fetch-theme/',
        type: 'GET',
        success: function (response) {
            selectedTheme = response;
            document.body.classList.add(response);

            if (response == 'dark') {
                checkbox.checked = true;
            }
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
    return selectedTheme;
}

function toggleTheme() {
    $.ajax({
        url: '/toggle-theme/',
        type: 'GET',

        success: function (response) {
            document.body.classList.remove('light', 'dark');

            selectedTheme = response;
            document.body.classList.add(response);
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
    return selectedTheme;
}
