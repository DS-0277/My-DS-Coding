**Assignment - E-Commerce Order Processing System - AD312 (Week 7)**


**1. Objective:** Imagine you're developing a system for an e-commerce platform where orders are processed in a sequence. However, due to a change in fulfillment strategy, you need to process the most recent orders first to ensure faster delivery for last-minute purchases. The orders are currently stored in a singly linked list, with the head being the first order received. Your task is to reverse the list so the most recent orders are processed first.

**2. Solution:** The solution to the problem is addressed in a directory named 'e-commerce-order-processing-system' comprising two files: (1) 'main.py' and 'test_main.py'. To run the main file, run 'python3 main.py' in the terminal. To run the test case, run 'python3 -m pytest -q' in the terminal.
  
**3. Time and Space Complexity:** The time complexity is O(n) since each is looped through the singly linked list while the space complexity is O(1) since no extra space is needed so this approach is the efficient one compared to another approach using stack.

**4. Clarifying Questions:**

1) What would happen if we use reverse function for only one node itself?
2) Does the program work if there is no node in the singly linked list?
3) Would it return the original value if we perform reversal twice for two nodes? 

**5. YouTube Link:** The explanation is provided via the youtube link as follows: https://youtu.be/F6Gos9629kk
