**Assignment: Dog Facts API v1 Replica with NodeJS and ExpressJS - AD311 (Week 5)**

*1. Objective:* Build a simplified version of the Dog Facts API using Node.js and Express.js. This API will allow users to retrieve dog facts in JSON format.

*2. Solution:* The solution to the problem is addressed in 'index.js'. To run the program, we first run 'node index.js' in the terminal. If the terminal shows 'Server is running on http://localhost:3000', then users can run the following wordings in normal cases and edge cases to run on the browser.

*3. Test Cases:* The test cases are divided into 3 normal cases and 3 edge cases. 

    Normal Cases:
    (1) Case 1: 'http://localhost:3000/facts' ==> get all the facts
    (2) Case 2: 'http://localhost:3000/facts/?number=1' ==> get 1 fact
    (3) Case 3: 'http://localhost:3000/facts/?number=3' ==> get 3 facts
    Edge Cases:
    (1) Case 1: 'http://localhost:3000/facts/?number=0' ==> []
    (2) Case 2: 'http://localhost:3000/facts/?number=10000' ==> run until the end of the data
    (3) Case 3: 'http://localhost:3000/facts/?number=abcde' ==> []

*4. YouTube Link:* The explanation is provided via the youtube link as follows: https://youtu.be/ZlCEkfwroU0 
