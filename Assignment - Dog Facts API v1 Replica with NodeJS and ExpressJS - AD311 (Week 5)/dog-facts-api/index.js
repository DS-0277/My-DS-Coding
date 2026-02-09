import express from "express";
import dogFacts from "./dog_facts-1.js";

const PORT = 3000;
const app = express();

app.get("/facts", (req,res) => {
    if (req.query.number) {
        const number = parseInt(req.query.number);
        res.json(dogFacts.slice(0, number));
    } else {
        res.json(dogFacts);
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Normal Cases:
// Case 1: get all the facts
// Case 2: get only one fact
// Case 3: get 3 facts

// Edge Cases:
// Case 1: 0 => empty 
// Case 2: 10000 => end of its data
// Case 3: abced => empty 
