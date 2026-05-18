import UserProvider from './UserContext';
import Dashboard from './components/Dashboard';

export default function App() {
  return (
    <UserProvider>
      <Dashboard />
    </UserProvider>
  );
}


// TEST CASES

// Normal Cases
// Case 1: Insert data normally ==> Show the data as expected
// Case 2: Change the data ==> Change the data as expected
// Case 3: Add another user ==> Add another user as expected

// Edge Cases
// Case 1: Mispell the data ==> Does not crash but no data shown
// Case 2: Remove one property from the object ==> Does not crash but no data shown
// Case 3: Remove data from a user ==> Does not crash but empty data for that user