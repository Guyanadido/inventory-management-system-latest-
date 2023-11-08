const table = document.querySelector('.table');
const columnSelector = document.getElementById('inputGroupSelect02');
const edit_icons = document.querySelectorAll(".edit_icon"); 
const new_customer = document.querySelector(".new-item")
const form = document.querySelector(".add_customers")

new_customer.addEventListener("click", function() {
    form.classList.toggle("visible");
  });

columnSelector.addEventListener('change', () => {
    sortTable(columnSelector.value);
});

function sortTable(column) {
    const rows = Array.from(table.rows).slice(1); // Exclude the header row
    rows.sort((a, b) => {
        const cellA = a.cells[column].textContent.toLowerCase();
        const cellB = b.cells[column].textContent.toLowerCase();
        return cellA.localeCompare(cellB);
    });

    // Clear the table body
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    // Append the sorted rows to the table body
    rows.forEach(row => {
        table.tBodies[0].appendChild(row);
    });
}


const search_input = document.querySelector(".search-input .input > input");
const search_results = document.querySelector(".search-results");
const searchBy = document.getElementById("inputGroupSelect01")
search_input.addEventListener("input", async function() {

    if (search_input.value) {
        search_results.style.display = "flex"
        searchByValue = searchBy.value;
        let response = await fetch("/search_item?q=" + search_input.value + "&table=persons&column=" + searchByValue);
        let records = await response.json();
        let html = "";
        for(let record of records) {
            column = record[searchByValue].replace('<', '&lt;').replace('&', '&amp;');
            html += '<li>' + column + '</li>';
        }
        search_results.innerHTML = html;
    } else {
        search_results.style.display = "none"
    }

    
})

// the code for editing any record in the table
edit_icons.forEach( (input, index) => {
    input.addEventListener("click", () => {
        const next_sibling_form = document.querySelectorAll(".edit_form")[index];
        const previous_sibling_text = document.querySelectorAll(".table-text")[index];
        next_sibling_form.style.display = "flex";
        next_sibling_form.children[3].focus();
        previous_sibling_text.style.display = "none";
    });
} )

document.addEventListener("DOMContentLoaded", () => {
    const cancelButton = document.querySelector(".cancelButton");
    cancelButton.addEventListener("click", function () {
        form.classList.toggle("visible");
    });
});