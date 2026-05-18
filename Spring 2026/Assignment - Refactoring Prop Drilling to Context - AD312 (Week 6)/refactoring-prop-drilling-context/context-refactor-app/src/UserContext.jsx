import { createContext, useState } from 'react';

export const UserContext = createContext();

export default function UserProvider({ children }) {
    const [users, setUser] = useState([
        {
            id: 1,
            name: 'John',
            email: 'john@gmail.com',
            themePreference: 'Light'
        },
        {
            id: 2,
            name: 'Bob',
            email: 'bob@gmail.com',
            themePreference: 'Dark'
        }
    ]);

    return (
        <UserContext.Provider value={{ users }}>
            {children}
        </UserContext.Provider>
    );
}