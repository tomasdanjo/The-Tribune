function updateToYearOptions() {
    const startYearSelect = document.getElementById('start_year');
    const endYearSelect = document.getElementById('end_year');

    // Get the current year
    const currentYear = new Date().getFullYear();

    // Get the selected "From Year" and "To Year"
    const selectedStartYear = parseInt(startYearSelect.value);
    const selectedEndYear = parseInt(endYearSelect.value);

    // Clear the "To Year" dropdown but save the current selected value
    endYearSelect.innerHTML = '<option value="">Select Year</option>';

    // If no valid "From Year" is selected, reset "To Year" options to all years
    if (isNaN(selectedStartYear)) {
        const years = Array.from({ length: currentYear - 2000 + 1 }, (v, k) => k + 2000).reverse();
        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            if (year === selectedEndYear) {
                option.selected = true;
            }
            endYearSelect.appendChild(option);
        });

        showMonth();
        updateToMonthOptions()  
        return;
    }

    // Populate "To Year" options starting from the selected "From Year"
    const years = Array.from({ length: currentYear - 2000 + 1 }, (v, k) => k + 2000).reverse();
    years.forEach(year => {
        if (year >= selectedStartYear) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            if (year === selectedEndYear) {
                option.selected = true;
            }
            endYearSelect.appendChild(option);
        }
    });
    showMonth();
    updateToMonthOptions() 
}

function updateFromYearOptions() {
    const startYearSelect = document.getElementById('start_year');
    const endYearSelect = document.getElementById('end_year');

    // Get the current year
    const currentYear = new Date().getFullYear();

    // Get the selected "From Year" and "To Year"
    const selectedStartYear = parseInt(startYearSelect.value);
    const selectedEndYear = parseInt(endYearSelect.value);

    // Clear the "From Year" dropdown but save the current selected value
    startYearSelect.innerHTML = '<option value="">Select Year</option>';

    // If no valid "To Year" is selected, reset "From Year" options to all years
    if (isNaN(selectedEndYear)) {
        const years = Array.from({ length: currentYear - 2000 + 1 }, (v, k) => k + 2000).reverse();
        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            if (year === selectedStartYear) {
                option.selected = true;
            }
            startYearSelect.appendChild(option);
        });

        showMonth();
        updateToMonthOptions() 
        return;
    }

    // Populate "From Year" options based on the selected "To Year"
    const years = Array.from({ length: currentYear - 2000 + 1 }, (v, k) => k + 2000).reverse();
    years.forEach(year => {
        if (year <= selectedEndYear) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            if (year === selectedStartYear) {
                option.selected = true;
            }
            startYearSelect.appendChild(option);
        }
    });
    showMonth();
    updateToMonthOptions() 
}

function showMonth() {
    const startYearSelect = document.getElementById('start_year');
    const endYearSelect = document.getElementById('end_year');

    fromMonth_container = document.getElementById('fromMonth');
    toMonth_container = document.getElementById('toMonth');

    // month_container = document.getElementById('toFromMonth');
    const selectedStartYear = parseInt(startYearSelect.value);
    const selectedEndYear = parseInt(endYearSelect.value);

    if (isNaN(selectedStartYear) || isNaN(selectedEndYear)) {
        // month_container.classList.add('hidden'); 
        fromMonth_container.classList.remove('filter-group');
        toMonth_container.classList.remove('filter-group');
    } else {
        // month_container.classList.remove('hidden'); 
        fromMonth_container.classList.add('filter-group');
        toMonth_container.classList.add('filter-group');
    }
    

}

function getMonthVal(month) {
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for (i = 0; i < months.length; i++) {
        if (months[i] == month) {
            return i + 1;
        }
    }
}

function updateToMonthOptions() {
    const startMonthSelect = document.getElementById('start_month');
    const endMonthSelect = document.getElementById('end_month');

    const startYearSelect = document.getElementById('start_year');
    const endYearSelect = document.getElementById('end_year');

    // Get the selected "From Month" and "To Month"
    const selectedStartMonth = startMonthSelect.value;
    const selectedEndMonth = endMonthSelect.value;

    // Get the selected "From Year" and "To Year"
    const selectedStartYear = parseInt(startYearSelect.value);
    const selectedEndYear = parseInt(endYearSelect.value);

    // Clear existing options in endMonthSelect
    endMonthSelect.innerHTML = '<option value="">Any Month</option>';

    // If "From Year" is the same as "To Year"
    if (selectedStartYear === selectedEndYear) {
        const selectedStartMonthIndex = getMonthVal(selectedStartMonth);
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        months.forEach((month, index) => {
            const option = document.createElement('option');
            option.value = month;
            option.textContent = month;

            // Check if "Any Month" is selected
            if (selectedStartMonth === "") {
                // If "Any Month" is selected, append all months
                endMonthSelect.appendChild(option);
            } else {
                // Add months from the selected start month onwards
                if (index + 1 >= selectedStartMonthIndex) {
                    endMonthSelect.appendChild(option);
                }
            }

            // Set the selected option if it matches the selected end month
            if (month === selectedEndMonth) {
                option.selected = true;
            }
        });
    } else {
        // Populate all months if the years are different or not selected
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        months.forEach(month => {
            const option = document.createElement('option');
            option.value = month;
            option.textContent = month;
            endMonthSelect.appendChild(option);

            // Set the selected option if it matches the selected end month
            if (month === selectedEndMonth) {
                option.selected = true;
            }
        });
    }
}


function updateFromMonthOptions() {
    const startMonthSelect = document.getElementById('start_month');
    const endMonthSelect = document.getElementById('end_month');

    const startYearSelect = document.getElementById('start_year');
    const endYearSelect = document.getElementById('end_year');

    // Get the selected "From Month" and "To Month"
    const selectedStartMonth = startMonthSelect.value;
    const selectedEndMonth = endMonthSelect.value;

    // Get the selected "From Year" and "To Year"
    const selectedStartYear = parseInt(startYearSelect.value);
    const selectedEndYear = parseInt(endYearSelect.value);

    // Clear existing options in startMonthSelect
    startMonthSelect.innerHTML = '<option value="">Any Month</option>';

    // If "To Year" is the same as "From Year"
    if (selectedStartYear === selectedEndYear) {
        const selectedEndMonthIndex = getMonthVal(selectedEndMonth);
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        months.forEach((month, index) => {
            const option = document.createElement('option');
            option.value = month;
            option.textContent = month;

            // Only add months up to the selected end month
            if (index + 1 <= selectedEndMonthIndex) {
                startMonthSelect.appendChild(option);
            }

            // Set the selected option if it matches the selected start month
            if (month === selectedStartMonth) {
                option.selected = true;
            }
        });
    } else {
        // Populate all months if the years are different or not selected
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        months.forEach(month => {
            const option = document.createElement('option');
            option.value = month;
            option.textContent = month;
            startMonthSelect.appendChild(option);

            // Set the selected option if it matches the selected start month
            if (month === selectedStartMonth) {
                option.selected = true;
            }
        });
    }
}
