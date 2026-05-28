import { useState, useEffect } from 'react';

export default function App() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight
  });

  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    }

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const isMobile = windowSize.width < 768;

  return (
    <div>
      <h1>{isMobile ? 'Mobile View' : 'Desktop View'}</h1>
      <h2>Width: {windowSize.width}</h2>
      <h2>Height: {windowSize.height}</h2>
    </div>
  );
}

// TEST CASES

// Normal Cases
// Case 1: Desktop ==> Resize the screen to be 768px and above ==> Display 'Desktop View'
// Case 2: Mobile ==> Resize the screen to be less than 768px ==> Display 'Mobile View'
// Case 3: Real-Time Resizing ==> Display changes in values for width and height in real time

// Edge Cases
// Case 1: Resizing to the smallest width ==> Display screen without crash
// Case 2: Refresh the page ==> Display as it is without any change or crash
// Case 3: Resizing at a fast pace ==> Display screen without crash