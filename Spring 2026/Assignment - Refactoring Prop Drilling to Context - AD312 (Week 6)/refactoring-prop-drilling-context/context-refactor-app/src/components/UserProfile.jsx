import { useContext } from 'react'; 
import { UserContext } from '../UserContext';

export default function UserProfile() {
    const { users } = useContext(UserContext);

    return (
        <div>
            <h3>User Profile</h3>
            {users.map((user) => (
                <div key={user.id}>
                    <hr />
                    <p>Name: {user.name}</p>
                    <p>Email: {user.email}</p>
                    <p>Theme Preference: {user.themePreference}</p>
                    <hr />
                </div>
            ))}
        </div>
    );
}