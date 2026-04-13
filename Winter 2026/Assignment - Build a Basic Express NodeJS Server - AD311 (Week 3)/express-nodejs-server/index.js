// Setup and Intialization (Import Express)
import express from "express";

// Server Configuration
const PORT = process.env.PORT || 3000;
const app = express();

// Routing
app.get("/", (req, res) => {
    res.send("Hello World");
});

app.get("/about", (req, res) => {
    res.send("About");
});

// Conditional Routing 
app.get("/foo", (req, res, next) => {
    if (Math.random() > 0.5) {
        res.send("sometimes this");
    } else {
        next();
    }
});

app.get("/foo", (req, res) => {
    res.send("and sometimes that");
});

// Regular Expression Routes
app.get(/^\/user(name)?$/, (req, res) => {
    res.send("Regular Expression works");
});

// Dynamic Route Handling
app.get("/user/:username", (req, res) => {
    res.send(`Hello ${req.params.username}`);
});

// Query String Handling
app.get("/get", (req, res) => {
    console.log(req.query);
    res.send("Query String Handling works");
});

// Error Handling
app.use((req, res) => {
    res.status(404).send("404 - Not Found");
});

// Server Activation
app.listen(PORT, () => {
    console.log(`The server is running on port ${PORT}`);
});

