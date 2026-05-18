import { useContext } from 'react';
import { ThemeContext } from '../ThemeContext';

export default function ThemeSwitcher() {
    const { theme, toggleTheme } = useContext(ThemeContext);
    
    return (
        <button onClick={toggleTheme}>{theme === 'dark' ? 'dark-mode' : 'light-mode'}</button>
    );
}


