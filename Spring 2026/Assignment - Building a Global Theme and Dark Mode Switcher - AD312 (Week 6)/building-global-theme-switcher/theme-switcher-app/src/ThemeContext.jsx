import { createContext, useState } from 'react';

export const ThemeContext = createContext();

export default function ThemeProvider({ children }) {

    const lightTheme = {
        backgroundColor: 'white',
        color: 'black'
    };

    const darkTheme = {
        backgroundColor: 'darkgray',
        color: 'white'
    }

    const [theme, setTheme] = useState('light');

    function toggleTheme() {
        if (theme === 'light') {
            setTheme('dark')
        } else {
            setTheme('light')
        }
    }

    return (
        <ThemeContext.Provider value={{ theme, lightTheme, darkTheme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}


