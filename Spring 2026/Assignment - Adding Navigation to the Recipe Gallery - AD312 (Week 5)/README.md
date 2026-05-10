**Assignment - Add Navigation to the Recipe Gallery - AD312 (Week 5)**


**1. Objective:** In this assignment, you will transition the Recipe Gallery from a single-page state-based component into a modern multi-page application using React Router (now part of the Remix framework). You will implement server-aware client-side routing to allow users to navigate between a home dashboard, a full gallery, and individual recipe detail pages using the file-based routing system. Note: While this assignment can be completed using Remix or Vite, the instructions below are specifically tailored for the React Router (Remix) framework. There are 4 objectives: (1) implement file-based routing for client-side navigation; (2) create Dynamic Routes to display specific recipe details; (3) use the useParams hook to extract URL parameters; (4) implement a global layout with a navigation bar for a seamless user experience.

**2. Solution:** The solution to the problem is addressed in a directory named 'recipe-router-app' which is located inside another directory named 'adding-navigation-recipe-gallery'. To run the program, we need to make sure we are located at 'recipe-router-app' by running the command prompt 'cd recipe-router-app'. We can check our status by running 'pwd' in the terminal. After that, we can run the server by running 'npm run dev'. The revlevant component files are named '_index.jsx', 'gallery.jsx' and 'recipe.$id.jsx' along with the description of test cases.
  
**3. Time and Space Complexity:** The time complexity and the space complexity are O(n).

**4. Clarifying Questions:**

1) What would happen if click 'Home' when we are locating at the recipe detail page?
2) Does the program show the expected output when the path is out of the given range?
3) Would it return the expect output when the path is given in alphabetical value instead of numeric one? 

**5. YouTube Link:** The explanation is provided via the youtube link as follows: https://youtu.be/qBETdBC-SdM
