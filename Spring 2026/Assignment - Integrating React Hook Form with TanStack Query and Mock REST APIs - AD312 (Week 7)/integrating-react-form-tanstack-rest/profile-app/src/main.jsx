import ReactDOM from 'react-dom/client';
import App from './App';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>
)


// TEST CASES:

// Normal Cases:

// Case 1: Provide full information ==> Show all information as expected
// Case 2: Change the username ==> Change the username in the server
// Case 3: Change the email ==> Change the email in the server


// Edge Cases:

// Case 1: In case no input ==> Show all no input in the server (without error)
// Case 2: In case one input is missing ==> Show remaining input fields (without error)
// Case 3: In case input field is changed but without save ==> No update is executed (without error)