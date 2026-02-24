import { render, screen } from '@testing-library/react';
import App from './App';
import UserProfile from './components/UserProfile';
import photo from './components/user-profile.png';


// NORMAL TEST CASES

// Case 1: (Rendering user profile)
test('Rendering user profile', () => {
  render(<App />);
  const heading = screen.getByText('User Profile');
  expect(heading).toBeInTheDocument();
});
// Case 2: (Rendering name)
test('Rendering name', () => {
  render(<App />);
  const nameText = screen.getByText('Name: Jane Doe');
  expect(nameText).toBeInTheDocument();
});
// Case 3: (Rendering email)
test('Rendering email', () => {
  render(<App />);
  const emailText = screen.getByText('Email: jane.doe@example.com');
  expect(emailText).toBeInTheDocument();
});


// EDGE TEST CASES

// Case 1: (Missing name)
test('Handling missing name', () => {
  render(
    <UserProfile
      name=""
      email="jane.doe@example.com"
      photo={photo}
    />
  );
  const nameMissing = screen.getByText('Name:');
  expect(nameMissing).toBeInTheDocument();
});
// Case 2: (Missing email)
test('Handling missing email', () => {
  render(
    <UserProfile
      name="Jane Doe"
      email=""
      photo={photo}
    />
  );
  const emailMissing = screen.getByText('Email:');
  expect(emailMissing).toBeInTheDocument();
})
// Case 3: (Invalid photo URL)
test('Handling invalid photo URL', () => {
  render(
    <UserProfile
      name="Jane Doe"
      email="jane.doe@example.com"
      photo="https://example.com/user-photo.jpg"
    />
  );
  const invalidPhotoUrl = screen.getByRole('img');
  expect(invalidPhotoUrl).toHaveAttribute('src', 'https://example.com/user-photo.jpg');
});