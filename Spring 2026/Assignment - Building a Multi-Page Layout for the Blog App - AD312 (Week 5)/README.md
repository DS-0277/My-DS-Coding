**Assignment - Building a Multi-Page Layout for the Blog App - AD312 (Week 5)**


**1. Objective:** For this assignment, you will take the role of a frontend developer tasked with converting a static, single-view Blog application into a functional Multi-Page Application (MPA) experience. Using React Router (Remix), you will organize blog content into logical views: a Home feed, an About page, and a dynamic Post view. While this assignment can be completed using Remix or Vite, the instructions below are specifically tailored for the Remix framework. There are 4 objectives: (1) Utilize file-based routing to manage application views; (2) Implement a persistent Navigation Layout using the <Outlet/> pattern; (3) Use Dynamic Routing to load specific blog posts based on their ID; (4) Practice the useNavigate hook for programmatic navigation (e.g., clicking a button to go back).

**2. Solution:** The solution to the problem is addressed in a directory named 'blog-remix-app' which is located inside another directory named 'building-multipage-layout-blog-app'. To run the program, we need to make sure we are located at 'blog-remix-app' by running the command prompt 'cd blog-remix-app'. We can check our status by running 'pwd' in the terminal. After that, we can run the server by running 'npm run dev'. The main component file is named '_index.jsx' along with the description of test cases followed by relevant components namely, 'about.jsx' and 'post.$postId.jsx'.
  
**3. Time and Space Complexity:** As for the homepage, the time complexity is O(n) since .map() method loops through all posts once while the space complexity is O(1) since there is no extra data structure being created. Turning to the dynamic post page (e.g. .find() method), the time complexity is also O(n) because it needs to check every post until it finds the correct one while the space complexity is O(1) since only one variable (post) is stored and no extra array or object being created.

**4. Clarifying Questions:**

1) What would happen if we refer to the path beyond the range for the post (e.g. post/4)?
2) Does the program work if we provide alphabetic value instead of numeric for the post (e.g. post/a)?
3) Would it return to the homepage when the current page is located more than one layer of path? 

**5. YouTube Link:** The explanation is provided via the youtube link as follows: https://youtu.be/BqPXm8761RE
