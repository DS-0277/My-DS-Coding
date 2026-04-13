import Toolbar from './Toolbar';

function App() {
  return (
    <>
      <h1>Dynamic Alert Buttons</h1>
      <Toolbar/>
    </>
  )
}

export default App


/*

Test Cases:

# Normal Case 1: cliick 'Download File' button => trigger 'Downloading!' alert
# Normal Case 2: click 'Share Document' button => trigger 'Sharing!' alert
# Normal Case 3: click 'Upload Document' button => trigger 'Uploading!' alert

# Edge Case 1: handle '@#$%&*' symbols in the message key => trigger all symbols alert
# Edge Case 2: handle '@#$%&*' symbols in the children key => trigger all symbols alert
# Edge Case 3: handle '😇' emoji in both message and children keys => trigger emoji

*/