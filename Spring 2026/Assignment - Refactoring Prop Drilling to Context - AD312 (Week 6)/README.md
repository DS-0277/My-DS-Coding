**Assignment - Refactoring Prop Drilling to Context - AD312 (Week 6)**


**1. Objective:** As applications grow, passing data through multiple layers of components—known as Prop Drilling—can make code difficult to maintain and debug. In this assignment, you will take a “messy” application where user settings are being passed manually through the component tree and refactor it to use the React Context API and the useContext hook. While this assignment can be completed using Vite or Expo, the instructions below are specifically tailored for Vite. There are 4 objectives: (1) Identify the pain points of “Prop Drilling”; (2) Create a Context Provider to centralize application state; (3) Use the useContext hook to consume data in deeply nested components; (4) Refactor existing code to remove unnecessary props.

**2. Solution:** The solution to the problem is addressed in a directory named 'context-refactor-app' which is located inside another directory named 'refactoring-prop-drilling-context'. To run the program, we need to make sure we are located at 'context-refactor-app' by running the command prompt 'cd context-refactor-app'. We can check our status by running 'pwd' in the terminal. After that, we can run the server by running 'npm run dev'. The main component file is named 'App.jsx' along with the description of test cases followed by relevant components namely, 'Dashboard.jsx', 'Sidebar.jsx', 'UserProfile.jsx' and 'UserContext.jsx'.

**3. YouTube Link:** The explanation is provided via the youtube link as follows: https://youtu.be/AeBE6tVuD2U
