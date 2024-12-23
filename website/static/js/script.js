//Add city script
document.getElementById('city-form').onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission
    addCity();
};

function addCity() {
    const cityName = document.getElementById("cityInput").value.trim();
    if (!cityName) {
        alert("Please enter a city name.");
        return false; // Prevent form submission
    }

    const requestData = {
        city_name: cityName
    };

    fetch('/add_city_ajax', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            // Optionally refresh the weather data or update the UI
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error adding the city. Please try again.');
    });

    return false; // Prevent form submission
}

// display cities from database
$(document).ready(function() {
    // Fetch unique cities from the server
    $.ajax({
        url: '/get_unique_cities', // Endpoint to fetch unique cities
        type: 'GET',
        success: function(response) {
            // Populate the dropdown with unique cities
            if (response.unique_cities && response.unique_cities.length > 0) {
                response.unique_cities.forEach(function(city) {
                    $('#cityDropdown').append($('<option></option>').attr('value', city).text(city));
                });
            } else {
                $('#cityDropdown').append($('<option></option>').attr('value', '').text('No cities available'));
            }
        },
        error: function() {
            alert('Failed to fetch cities from the server.');
        }
    });

});
$(document).ready(function() {
    // Fetch unique cities from the server and populate the dropdown
    $.ajax({
        url: '/get_unique_cities', // Endpoint to fetch unique cities
        type: 'GET',
        success: function(response) {
            // Clear the dropdown to avoid duplicates
            $('#cityDropdown').empty();
            
            // Check if cities are returned and populate the dropdown
            if (response.unique_cities && response.unique_cities.length > 0) {
                $('#cityDropdown').append('<option value="">Select a city</option>');
                
                // Loop through the unique cities and add each as an option
                response.unique_cities.forEach(function(city) {
                    $('#cityDropdown').append($('<option></option>').attr('value', city).text(city));
                });
            } else {
                $('#cityDropdown').append($('<option value="">No cities available</option>'));
            }
        },
        error: function() {
            alert('Failed to fetch cities from the server.');
        }
    });

    // Handle the change event of the city dropdown
    $('#cityDropdown').change(function() {
        const selectedCity = $(this).val();

        if (!selectedCity) {
            $('#weatherResult').empty(); // Clear previous results if no city is selected
            return;
        }

        // Fetch and display weather data for the selected city
        $.ajax({
            url: '/get_weather',
            type: 'POST',
            data: { city_name: selectedCity },
            success: function(data) {
                // Display weather data
                const weatherInfo = `
                    <h3>Weather in ${data.city}</h3>
                    <p>Condition: ${data.weather}</p>
                    <p>Temperature: ${data.temperature} °C</p>
                    <p>Humidity: ${data.humidity} %</p>
                `;
                $('#weatherResult').html(weatherInfo);
            },
            error: function() {
                $('#weatherResult').html('<p>Error fetching weather data.</p>');
            }
        });
    });
});

// Get_dropdown_weather scipt

document.getElementById('getWeatherBtn').addEventListener('click', function() {
    const cityName = document.getElementById('cityDropdown').value;

    if (!cityName) {
        alert('Please select a city.');
        return;
    }

    // Fetch current weather data for the selected city
    fetch('/dropdown_get_weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: cityName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Update the HTML with the received current weather data
            document.getElementById('cityDisplay').innerText = data.location.name; // City name
            document.getElementById('temperatureDisplay').innerText = data.current.temp_c + ' °C'; // Temperature
            document.getElementById('descriptionDisplay').innerText = data.current.condition.text; // Weather description
            document.getElementById('windDisplay').innerText = data.current.wind_kph + ' kph'; // Wind speed
            document.getElementById('humidityDisplay').innerText = data.current.humidity + ' %'; // Humidity
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while retrieving weather data.');
    });

    // Fetch forecast data for the next 7 days for the selected city
    fetch('/prediction_weather', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city: cityName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Error:", data.error);
        } else {
            // Update the table with forecast data
            data.forecast.forEach((forecast, index) => {
                // Set the day
                document.getElementById(`day${index + 1}`).textContent = forecast.date;
                
                // Set the icon
                document.getElementById(`icon${index + 1}`).src = `/static/img/${forecast.icon}.svg`;
                
                // Set the temperature
                document.getElementById(`temp${index + 1}Display`).textContent = `${forecast.temperature}°C`;
            });
        }
    })
    .catch(error => {
        console.error("Error fetching forecast:", error);
    });
});

//forcast weather
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('getWeatherBtn1').addEventListener('click', function() {
        const cityName = document.getElementById('cityDropdown').value;

        if (!cityName) {
            alert('Please select a city.');
            return;
        }

        fetch('/prediction_weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ city: cityName })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Forecast data:", data);

            if (data.error) {
                console.error("Error:", data.error);
                alert("Error fetching forecast: " + data.error);
            } else {
                data.forecast.forEach((forecast, index) => {
                    const dayElement = document.getElementById(`day${index + 1}`);
                    const tempElement = document.getElementById(`temp${index + 1}Display`);

                    if (!dayElement) {
                        console.warn(`Element with ID day${index + 1} not found`);
                    } else {
                        dayElement.textContent = forecast.day;  // Use the three-letter abbreviation
                    }

                    if (!tempElement) {
                        console.warn(`Element with ID temp${index + 1}Display not found`);
                    } else {
                        // Format temperature to 2 decimal places
                        const formattedTemperature = forecast.temperature.toFixed(2);
                        tempElement.textContent = `${formattedTemperature}°C`;  // Display the temperature with 2 decimal places
                    }
                });
            }
        })
        .catch(error => {
            console.error("Error fetching forecast:", error);
            alert("An unexpected error occurred: " + error);
        });
    });
});








