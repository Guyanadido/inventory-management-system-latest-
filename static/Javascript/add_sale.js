// price pricing info
const product = document.querySelector('.product_name');
const quantity = document.querySelector('.quantity');
const product_price = document.querySelector('.product_price');
const product_price_input = product_price.previousElementSibling;
const discount = document.querySelector('.discount');
const product_tax = document.querySelector('.product_tax');
const product_tax_input = product_tax.previousElementSibling;
const product_total_price = document.querySelector('.product_total_price');
const product_total_price_input = product_total_price.previousElementSibling;
let prompts = [product, quantity, discount]

// enforcing client side validation
const form = document.querySelector('form'), 
      requiredInputs = form.querySelectorAll(".required"),
      warning = form.querySelectorAll('p'),
      submitForm = form.querySelector('button');


submitForm.addEventListener('click', (event) => {
    let hasEmptyField = false;
    for (let i = 0; i < requiredInputs.length; i++)
        {
            if (requiredInputs[i].value === '') {
                warning[i].innerText = "*input required";
                hasEmptyField = true;
            } else {
                warning[i].innerText = "";
            }
        }
        if (hasEmptyField) {
            event.preventDefault(); // Prevent form submission if there are empty fields
          }
});

async function product_info(name) {
    let response = await fetch("/salesDetail?q=" + name);
    let records = await response.json();
    return records
}

prompts.forEach(function(prompt) {
    prompt.addEventListener('input', async () => {
        if(product.value !== "") {
            let records = await product_info(product.value, discount);
            let price = records[0].selling_price;
            let tax = records[0].tax_rate;
            finalPrice = price + (tax/100) * price 
            if(discount.value) {
                finalPrice -= (discount.value / 100) * price;
            }
            product_price.innerHTML = 'Single Product Price: $' + price;
            product_price_input.setAttribute('value', price)
            product_tax.innerHTML = 'Tax: ' + tax + '%'; 
            product_tax_input.setAttribute('value', tax)
            product_total_price.innerHTML = 'Total Price: $' + finalPrice * quantity.value
            product_total_price_input.setAttribute('value', finalPrice * quantity.value)
       }
    })
})




document.addEventListener("DOMContentLoaded", () => {
    const cancelButton = document.querySelector(".cancelButton");
    cancelButton.addEventListener("click", function () {
        // Redirect to another page
        window.location.href = "/sales";
    });
});