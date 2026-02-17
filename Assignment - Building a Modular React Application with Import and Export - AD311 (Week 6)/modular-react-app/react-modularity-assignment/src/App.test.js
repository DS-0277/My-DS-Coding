import { render, screen } from '@testing-library/react';
import App from './App';


// NORMAL TEST CASES
// Case 1: Rendering Header
test('Rendering Header', () => {
  render(<App />);
  expect(screen.getByText('This is the Header')).toBeInTheDocument();
});
// Case 2: Rendering ContentA
test('Rendering ContentA', () => {
  render(<App />);
  expect(screen.getByText('This is ContentA')).toBeInTheDocument();
});
// Case 3: Rendering ContentB
test('Rendering ContentB', () => {
  render(<App />);
  expect(screen.getByText('This is ContentB')).toBeInTheDocument();
});


// EDGE TEST CASES
// Case 1: Rendering Footer
test('Rendering Footer', () => {
  render(<App />);
  expect(screen.getByText('This is the Footer')).toBeInTheDocument();
});
// Case 2: Rendering Shared Button
test('Rendering Shared Button', () => {
  render(<App />);
  expect(screen.getAllByText('Shared Button').length).toBeGreaterThan(0);
});
// Case 3: Redering App without input
test('Rendering App without input', () => {
  render(<App />);
});
