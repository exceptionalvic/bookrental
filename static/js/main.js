
document.addEventListener("DOMContentLoaded", function() {
    const filterSelect = document.getElementById("filter-select");
    const filteredResults = document.getElementById("filtered-results");

    filterSelect.addEventListener("change", function() {
        const selectedOption = filterSelect.value;
        if (selectedOption === "due_rentals" || selectedOption === "extended_rentals" || selectedOption === "reset_filter") {
            // Send AJAX request to Django view
            const xhr = new XMLHttpRequest();
            xhr.open("GET", `/admin/dashboard/filter-rentals/?filter=${selectedOption}`);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // Update the filtered results with the response
                        filteredResults.innerHTML = xhr.responseText;
                        // Hide loading spinner and show table
                        loadingSpinner.style.display = "none";
                        filteredResults.querySelector("table").style.display = "table";
                    } else {
                        console.error("Error: " + xhr.status);
                    }
                }
            };
            xhr.send();
        }
    });
});
