import ErrorBoundary from './ErrorBoundary';
import BuggyComponent from './BuggyComponent';

export default function App() {
  return (
    <div>
      <h1>Social Media Dashboard</h1>
      <ErrorBoundary>
        <BuggyComponent />
      </ErrorBoundary>
      <p>This content still works.</p>
    </div>
  );
}

// TEST CASES

// Normal Cases
// Case 1: There is no error ==> Display the component normally (e.g. 'Hello')
// Case 2: Replace 'Hello' with 'Weather Widget' ==> Display the 'Weather Widget' text
// Case 3: Repalce '<h2>' tag with '<button>' tag ==> Display the button within the component

// Edge Cases
// Case 1: Error is detected ('Server Error') ==> Display the fallback UI (e.g. 'Something went wrong')
// Case 2: Error is detected ('Crash') ==> Display the fallback UI (e.g. 'Something went wrong')
// Case 3: Error is detected ('Invalid Data') ==> Display the fallback UI (e.g. 'Something went wrong')