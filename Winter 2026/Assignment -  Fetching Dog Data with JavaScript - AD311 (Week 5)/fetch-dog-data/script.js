// Part 1: Basic Fetch Request & Part 2: Handling Responses
async function fetchDogBreeds() {
    try {
        const response = await fetch("https://dogapi.dog/api/v2/breeds");
        if (!response.ok) {
            throw new Error("Failed to fetch dog breeds");
        }
        const data = await response.json();
        console.log("All dog breeds:", data);
    } catch (error) {
        console.error("Error fetching dog breeds", error);
    }
}
fetchDogBreeds();

// Part 3: Displaying Detailed Breed Information
async function fetchDogBreedDetails() {
    try {
        const response = await fetch("https://dogapi.dog/api/v2/breeds");
        if (!response.ok) {
            throw new Error("Failed to fetch dog breed details");
        }
        const data = await response.json();
        const firstBreedID = data.data[0].id;
        const detailResponse = await fetch(`https://dogapi.dog/api/v2/breeds/${firstBreedID}`);
        if (!detailResponse.ok) {
            throw new Error("Failed to fetch dog breed details");
        }
        const detailData = await detailResponse.json();
        console.log("Dog breed details", detailData.data);
    } catch (error) {
        console.error("Error fetching dog breed details", error);
    }
}
fetchDogBreedDetails();

// Part 5: Working with Dog Facts and Groups
    // Dog Facts
async function fetchDogFacts() {
    try {
        const response = await fetch("https://dogapi.dog/api/v2/facts");
        if (!response.ok) {
            throw new Error("Failed to fetch dog facts");
        }
        const data = await response.json();
        console.log("Dog facts:", data.data);
    } catch (error) {
        console.error("Error fetching dog facts");
    }
}
fetchDogFacts();

    // Dog Groups
async function fetchDogGroups() {
    try {
        const response = await fetch("https://dogapi.dog/api/v2/groups");
        if (!response.ok) {
            throw new Error("Failed to fetch dog groups");
        }
        const data = await response.json();
        console.log("Dog groups:", data.data);
    } catch (error) {
        console.error("Error fetching dog groups");
    }
}
fetchDogGroups();