console.log("JS Loaded");

document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for filter inputs/buttons
    document.getElementById('filter-button').addEventListener('click', applyFilters);
    document.getElementById('reset-button').addEventListener('click', resetFilters);
});

function applyFilters() {
    // set for brake type
    let brakeTypeFilter = document.getElementById('brake-type-filter').value.trim().toLowerCase();
    // set for tyre type
    let tyreTypeFilter = document.getElementById('tyres-type-filter').value.trim().toLowerCase();
    // set for set weight
    let weightSetFilterOperator = document.getElementById('weight-set-filter-operator').value.trim().toLowerCase();
    let weightSetFilterValue = document.getElementById('weight-set-filter-value').value.trim();
    // set for rim material
    let rimMaterialFilter = document.getElementById('rim-material-filter').value.trim().toLowerCase();
    // set for set price
    let priceFilterOperator = document.getElementById('price-set-filter-operator').value.trim().toLowerCase();
    let priceFilterValue = document.getElementById('suggested-price-value').value.trim();

    let table = document.getElementById('results-table');
    let rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        let brakeType = rows[i].getElementsByTagName('td')[3].innerText.trim().toLowerCase();
        let tyreType = rows[i].getElementsByTagName('td')[4].innerText.trim().toLowerCase();
        let weightSet = rows[i].getElementsByTagName('td')[5].innerText.trim();
        let rimMaterial = rows[i].getElementsByTagName('td')[11].innerText.trim().toLowerCase();
        let priceSet = rows[i].getElementsByTagName('td')[17].innerText.trim();

        // Check if the brake type, rim material, tyre type, and weight set match the filters.
        if (
            (brakeTypeFilter === "" || brakeType === brakeTypeFilter) &&
            (tyreTypeFilter === "" || tyreType === tyreTypeFilter) &&
            (weightSetFilterOperator === "" ||
                (weightSetFilterOperator === "more" && weightSet > weightSetFilterValue) ||
                (weightSetFilterOperator === "less" && weightSet < weightSetFilterValue)) &&
            (rimMaterialFilter === "" || rimMaterial === rimMaterialFilter) &&
            (priceFilterOperator === "" ||
                (priceFilterOperator === "more" && priceSet > priceFilterValue) ||
                (priceFilterOperator === "less" && priceSet < priceFilterValue))
        ) {
            // If they do, show the row.
            rows[i].style.display = "";
        } else {
            // If they don't, hide the row.
            rows[i].style.display = "none";
        }
    }
}

// reset the filter for break type, rim material, tyre type, weight and price
function resetFilters() {
    document.getElementById('brake-type-filter').value = "";
    document.getElementById('tyres-type-filter').value = "";
    document.getElementById('weight-set-filter-operator').value = "";
    document.getElementById('weight-set-filter-value').value = "";
    document.getElementById('rim-material-filter').value = "";
    document.getElementById('price-set-filter-operator').value = "";
    document.getElementById('suggested-price-value').value = "";

    let table = document.getElementById('results-table');
    let rows = table.getElementsByTagName('tr');
    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = '';
    }
}
