**Tech Interview Prep: Simple Text Editor with Undo Functionality - AD311 (Week 7)**

*1. Objective:* Implement a simple text editor that allows adding text, deleting the last character, and an undo feature using a stack data structure. You are creating a simple text editor that allows the user to input text, delete the last character, and undo the last operation. Your task is to use a stack to keep track of the changes made to the text so that you can undo the last operation when required.

*2. Solution:* The solution to the problem is addressed in 'simple_text_editor.py'.

*3. Unit Testing:* The testing is addressed in 'unittest_cases.py'.

*4. Diagrams or Flowcharts:* Any diagram or flowchart is addressed via link as follows: https://www.figma.com/board/Yz4eTADGAYztH1Df9ojUzr/Technical-Interview-Prep---Simple-Text-Editor-with-Undo-Functionality---AD311--Week-7-?node-id=0-1&t=LUmWADJs9ynVNos8-1

*5. YouTube Link:* The explanation is provided via the youtube link as follows: https://youtu.be/zI63nQvvn6A

*6. Time and Space Complexity:* With respect to the "add", "delete" and "undo" operations, the time complexity is O(n) while the space complexity is O(1).

*7. Clarifying Questions:*

    - Is it possible to delete on the emptry string?
    - Is there any issue if we try to undo with no history?
    - What happen when we undo multiple times?
