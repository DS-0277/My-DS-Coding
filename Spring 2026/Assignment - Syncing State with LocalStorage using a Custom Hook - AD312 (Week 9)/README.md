**Assignment - Syncing State with LocalStorage using a Custom Hook - AD312 (Week 9)**


**1. Objective:** Have you ever visited a website, switched it to Dark Mode, and then felt frustrated because it reset back to Light Mode the moment you refreshed the page? To fix this, web developers use the browser's built-in localStorage API. It allows us to save small pieces of data (like user preferences) directly inside the user's browser so the data survives page refreshes. While you could write the localStorage loading and saving code directly inside your components, doing it over and over creates messy, duplicate code. Your goal in this lab is to build a custom hook called useLocalStorage. This hook will act exactly like React's standard useState, except it will automatically backup its value to the browser's memory every time it changes.

**2. Solution:** The solution to the problem is addressed in a directory named 'localstorage-api' which is located inside another directory named 'syncing-state-localstorage-custom-hook'. To run the program, we need to make sure we are located at 'localstorage-api' by running the command prompt 'cd localstorage-api'. We can check our status by running 'pwd' in the terminal. After that, we can run the server by running 'npm run dev'. The main component is named 'App.jsx' along with the description of test cases. The relevant file acting as the custom hook is named 'useLocalStorage.js'.

**3. YouTube Link:** The explanation is provided via the youtube link as follows: 
