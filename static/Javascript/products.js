const edit_icons = document.querySelectorAll(".edit_icon"); 
const search_input = document.querySelector(".search-input .input > input");
const search_results = document.querySelector(".search-results");


function editEffect(input) {
    input.nextElementSibling.style.display = "flex";
}

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

// asyncronies function who fetchs items that matchs with user input
search_input.addEventListener("input", async function() {

    if (search_input.value) {
        search_results.style.display = "flex"
            let response = await fetch("/search_item?q=" + search_input.value + "&table=inventory_data&column=product_name");
            let records = await response.json();
            let html = "";
            for(let record in records) {
                product_name = records[record].product_name.replace('<', '&lt;').replace('&', '&amp;');
                html += '<li>' + product_name + '</li>';
            }
            search_results.innerHTML = html;
    } else {
        search_results.style.display = "none"
    }

    
})
