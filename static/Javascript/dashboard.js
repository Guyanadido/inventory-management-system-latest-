const dateSelectors = document.querySelectorAll(".top2");
const display = document.querySelector('.records')

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, options);
}

dateSelectors[0].addEventListener("change", async function() {
    info_based_on_date(dateSelectors[0]);
})


async function info_based_on_date(dateSelector) {
    let value = dateSelector.value;
        if (value) {
            let response = await fetch("/info_based_on_date?q=" + value + "&column=SUM(total_price)");
            let records = await response.json();
            let html = ''
            if (records.length > 1) {
                for(let i=0; i < 3; i++) {
                    totalrevenue = records[i]['SUM(total_price)'].toFixed(2).replace('<', '&lt;').replace('&', '&amp;');
                    productName = records[i]['product_name'].replace('<', '&lt;').replace('&', '&amp;');
                    html += '<span class=text>' + productName + ': ' + '$' + totalrevenue + '</span>' 
                }
    
                if(html) {
                    display.innerHTML = html
                } else {
                    display.innerHTML = "NO RECORDS " + value.toUpperCase()
                }
            } else {
                display.innerHTML = "NO RECORDS " + value.toUpperCase()
            }
        }
}
info_based_on_date(dateSelectors[0])


let y_axis = [];
let x_axis = [];
let myChart;
// Function to create the chart
function createChart() {
    const ctx = document.getElementById('myChart').getContext('2d');

    //destroy the existing chart if exist
    if (myChart) {
        myChart.destroy();
    }

    // Sample data
    const data = {
        labels: x_axis,
        datasets: [
            {
                label: 'Sales',
                data: y_axis,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }
        ]
    };

    // Chart configuration
    const config = {
        type: 'line',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    // Create and render the chart
    myChart = new Chart(ctx, config);
}

// Fetch and populate data
async function chartdata(dateSelector) {
    let value = dateSelector.value;
    if (value) {
        let response = await fetch("/info_based_on_date?q=" + value + "&column=order_date");
        let records = await response.json();

        y_axis.length = 0; // Clear the arrays
        x_axis.length = 0;

        for (let record of records) {
            let price = record['SUM(total_price)'].toFixed(2).replace('<', '&lt;').replace('&', '&amp;');
            let orderdate = formatDate(record['order_date']);
            y_axis.push(price);
            x_axis.push(orderdate);
        }

        createChart(); // Call the function to create the chart when data is ready
    }
}

chartdata(dateSelectors[2]);


// Register event listeners
document.addEventListener('DOMContentLoaded', function () {
    dateSelectors[2].addEventListener('input', function () {
        chartdata(dateSelectors[2]);
    });
});

