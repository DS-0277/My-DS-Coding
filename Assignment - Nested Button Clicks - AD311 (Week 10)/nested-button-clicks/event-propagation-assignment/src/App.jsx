import './App.css'
import NestedButtons from './NestedButtons';

function App() {
  return (
    <NestedButtons />
  )
}

export default App


/*

Test Cases:

# Normal Case 1: click the outer element => trigger 'Outer Clicked' alert
# Normal Case 2: click the inner element => trigger 'Inner Clicked' alert
# Normal Case 3: click outer element again => trigger 'Outer Clicked' alert

# Edge Case 1: click the inner element multiple times => trigger 'Inner Clicked' alert every time
# Edge Case 2: click at the edge of outer element => trigger 'Outer Clicked' alert
# Edge Case 3: click TAB and then click ENTER => trigger 'Inner Clicked' alert

*/