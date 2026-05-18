import { useContext } from 'react';
import { ThemeContext } from './ThemeContext';
import ThemeSwitcher from './components/ThemeSwitcher';

export default function App() {
  const { theme, lightTheme, darkTheme } = useContext(ThemeContext);

  const currentTheme = theme === 'dark' ? darkTheme : lightTheme;

  return (
    <div style={{ backgroundColor: currentTheme.backgroundColor, color: currentTheme.color }}>
      <h1>Global Theme Switcher</h1>
      <ThemeSwitcher />
    </div>
  );
}

// TEST CASES

// Normal Cases
// Case 1: Initial load ==> Display heading and button as expected in light mode
// Case 2: Click button once ==> Switch the theme to dark mode (dark grey) 
// Case 3: Click button twice ==> Switch the theme back to light mode

// Edge Cases
// Case 1: Clicking button multiple times ==> Switch the theme mode back and forth
// Case 2: Change the background color to 'black' ==> Switch to dark mode (black)
// Case 3: Rename background color to 'dark gray' ==> No rendering of background color