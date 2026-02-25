# TextOperation class
class TextOperation:
    def __init__(self, operation_type, character):
        self.operation_type = operation_type
        self.character = character

# TextEditor class
class TextEditor:
    def __init__(self):
        # Store current text
        self.text = ""
        # Store record
        self.history = []
    
    # Add character
    def add(self, char):
        self.text += char
        self.history.append(TextOperation("add", char))
    # Delete character
    def delete(self):
        if self.text != "":
            removed_char = self.text[-1]
            self.text = self.text[:-1]
            self.history.append(TextOperation("delete", removed_char))
    # Undo last operation
    def undo(self):
        if not self.history:
            return
        last_operation = self.history.pop()
        if last_operation.operation_type == "add":
            self.text = self.text[:-1]
        elif last_operation.operation_type == "delete":
            self.text += last_operation.character

    # Get the text
    def get_text(self):
        return self.text

# Run the program
if __name__ == "__main__":
    editor = TextEditor()
    editor.add("A")
    editor.add("B")
    print("Text:", editor.get_text())
    editor.delete()
    print("After delete:", editor.get_text())
    editor.undo()
    print("After undo:", editor.get_text())

