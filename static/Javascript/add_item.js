// makie sure all the required prompts are fireld
const form = document.querySelector('form'), 
      requiredInputs = form.querySelectorAll(".required"),
      warning = form.querySelectorAll('p'),
      submitForm = form.querySelector('button');

submitForm.addEventListener('click', () => {
    for (let i = 0; i < requiredInputs.length; i++)
    {
        if (requiredInputs[i].value === '') {
            warning[i].innerText = "*input required";
            break;
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const cancelButton = document.querySelector(".cancelButton");
    cancelButton.addEventListener("click", function () {
        // Redirect to another page
        window.location.href = "/product";
    });
});