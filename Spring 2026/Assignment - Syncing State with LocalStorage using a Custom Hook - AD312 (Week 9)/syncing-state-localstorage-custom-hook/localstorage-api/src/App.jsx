import useLocalStorage from './useLocalStorage';

export default function App() {
  const [darkMode, setDarkMode] = useLocalStorage('darkMode', false);

  return (
    <div style={{
      backgroundColor: darkMode ? 'black' : 'white',
      color: darkMode ? 'white' : 'black',
      minHeight: '100vh'
    }}>
      <h1>{darkMode ? 'Dark Mode' : 'Light Mode'}</h1>
      <button onClick={() => setDarkMode(!darkMode)}>Toggle Theme</button>
    </div>
  );
}

// TEST CASES

// Normal Cases:
// Case 1: Initial page load ==> Display in Light Mode
// Case 2: Click 'Toggle Theme' once ==> Display in Dark Mode
// Case 3: Refresh the page durng Dark Mode ==> Keep in Dark Mode


// Edge Cases:
// Case 1: Refresh the page multiple times ==> Keep the current mode
// Case 2: Click 'Toggle Theme' button multiple times ==> Switch between modes accordingly
// Case 3: Leave the page and then re-enter ==> Keep the current mode