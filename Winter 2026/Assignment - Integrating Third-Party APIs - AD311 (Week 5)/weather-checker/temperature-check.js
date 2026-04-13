async function getTemperature() {
    const city = document.getElementById("city").value;
    const result = document.getElementById("result");
    if (!city) {
        result.textContent = "Please provide a city name";
        return;
    }
    // Geocoding API
    const geoResponse = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${city}`);
    const geoData = await geoResponse.json();
    if (!geoData.results) {
        result.textContent = "City not found";
        return;
    }
    const { latitude, longitude } = geoData.results[0];

    // Weather API
    const weatherResponse = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`);
    const weatherData = await weatherResponse.json();
    const temperature = weatherData.current_weather.temperature;
    result.textContent = `The current temperture of ${city}: ${temperature} degrees Celsius`;
}