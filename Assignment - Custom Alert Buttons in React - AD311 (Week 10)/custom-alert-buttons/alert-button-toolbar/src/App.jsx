import Toolbar from './Toolbar';

function App() {
  return (
    <div>
      <h1>Custom Alert Buttons</h1>
      <Toolbar />
    </div>
  )
}

export default App


/*

Test Cases:

# Normal Case 1: click 'Play' button => trigger 'Playing Now' alert
# Normal Case 2: click 'Upload' button => trigger 'Uploading Now' alert
# Normal Case 3: click 'Delete' button => trigger 'Deleted Already' alert

# Edge Case 1: handle long text => trigger long text alert
# Edge Case 2: handle '@#$%&*' symbols => trigger content with symbols alert
# Edge Case 3: handle emoji '😊' => trigger emoji alert

*/