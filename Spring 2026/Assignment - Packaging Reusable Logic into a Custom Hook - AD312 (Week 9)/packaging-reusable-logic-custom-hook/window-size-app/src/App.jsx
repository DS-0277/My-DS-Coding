import useWindowSize from './useWindowSize';

export default function App() {
  const { width, height } = useWindowSize();

  return (
    <div>
      <h1>Window Size Tracker</h1>
      <h2>Width: {width}px</h2>
      <h2>Height: {height}px</h2>
      {width < 768 ? (<h3>Mobile Layout</h3>) : (<h3>Desktop Layout</h3>)}
    </div>
  );
}

// TEST CASES

// Normal Cases:
// Case 1: Resize to 768px ==> Display 'Desktop Layout' message
// Case 2: Resize to more than 768px ==> Display 'Desktop Layout' message
// Case 3: Resize to less than 768px ==> Display 'Mobile Layout' message

// Edge Cases:
// Case 1: Refresh the page ==> Display the current values without changing
// Case 2: Resize to the smallest size ==> Display 'Mobile Layout' message without crashing
// Case 3: Resize quickly across the browser ==> Switch back and forth between layouts without crashing