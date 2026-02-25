import unittest
from simple_text_editor import TextEditor

class TestTextEditor(unittest.TestCase):

    # NORMAL TEST CASES
    # Case 1: (Add character)
    def test_add_character(self):
        editor = TextEditor()
        editor.add("A")
        editor.add("B")
        self.assertEqual(editor.get_text(), "AB")
    # Case 2: (Delete character)
    def test_delete_character(self):
        editor = TextEditor()
        editor.add("A")
        editor.add("B")
        editor.delete()
        self.assertEqual(editor.get_text(), "A")
    # Case 3: (undo the last operation)
    def test_undo_last_operation(self):
        editor = TextEditor()
        editor.add("A")
        editor.add("B")
        editor.delete()
        editor.undo()
        self.assertEqual(editor.get_text(), "AB")

    # EDGE TEST CASES
    # Case 1: (Delete the empty string)
    def test_delete_empty_string(self):
        editor = TextEditor()
        editor.delete()
        self.assertEqual(editor.get_text(), "")
    # Case 2: (Undo no history)
    def test_undo_no_history(self):
        editor = TextEditor()
        editor.undo()
        self.assertEqual(editor.get_text(), "")
    # Case 3: (Multiple undo)
    def test_multiple_undo(self):
        editor = TextEditor()
        editor.add("A")
        editor.add("B")
        editor.add("C")
        editor.undo()
        editor.undo()
        self.assertEqual(editor.get_text(), "A")

if __name__ == "__main__":
    unittest.main()