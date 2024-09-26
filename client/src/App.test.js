import React from 'react';
import { render, fireEvent, screen, act } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import App from './App';

test('renders login form and submits successfully', async () => {
  render(<App />);

  // Select the second occurrence of the Username and Password input (Login form)
  const loginUsernameInput = screen.getAllByPlaceholderText(/username/i)[1];
  const loginPasswordInput = screen.getAllByPlaceholderText(/password/i)[1];
  const loginButton = screen.getAllByText(/login/i)[0];

  expect(loginUsernameInput).toBeInTheDocument();
  expect(loginPasswordInput).toBeInTheDocument();
  expect(loginButton).toBeInTheDocument();

  // Simulate typing into the login inputs
  fireEvent.change(loginUsernameInput, { target: { value: 'testuser' } });
  fireEvent.change(loginPasswordInput, { target: { value: 'password123' } });

  // Simulate clicking the login button and wait for state changes
  await act(async () => {
    fireEvent.click(loginButton);
  });

  // Use a function matcher to check for success message flexibly
  const message = await screen.findByText((content, element) => {
    return content.includes('logged in successfully');
  });
  expect(message).toBeInTheDocument();
});

test('renders register form and submits successfully', async () => {
  render(<App />);

  // Select the first occurrence of the Username and Password input (Register form)
  const registerUsernameInput = screen.getAllByPlaceholderText(/username/i)[0];
  const registerPasswordInput = screen.getAllByPlaceholderText(/password/i)[0];
  const registerButton = screen.getAllByText(/register/i)[0];

  expect(registerUsernameInput).toBeInTheDocument();
  expect(registerPasswordInput).toBeInTheDocument();
  expect(registerButton).toBeInTheDocument();

  // Simulate typing into the register inputs
  fireEvent.change(registerUsernameInput, { target: { value: 'newuser' } });
  fireEvent.change(registerPasswordInput, { target: { value: 'newpassword' } });

  // Simulate clicking the register button and wait for state changes
  await act(async () => {
    fireEvent.click(registerButton);
  });

  // Use a function matcher to check for success message flexibly
  const message = await screen.findByText((content, element) => {
    return content.includes('user registered successfully');
  });
  expect(message).toBeInTheDocument();
});

test('renders scraper form and submits with keywords', async () => {
  render(<App />);

  // Simulate successful login to access the scraper form
  fireEvent.change(screen.getAllByPlaceholderText(/username/i)[1], { target: { value: 'testuser' } });
  fireEvent.change(screen.getAllByPlaceholderText(/password/i)[1], { target: { value: 'password123' } });

  // Ensure login is successful before accessing the scraper form
  await act(async () => {
    fireEvent.click(screen.getAllByText(/login/i)[0]);
  });

  // Now wait for the scraper form to appear
  const urlInput = await screen.findByPlaceholderText(/enter website url/i);
  const keywordInput = await screen.findByPlaceholderText(/enter keywords/i);
  const scrapeButton = await screen.findByText(/scrape website/i);

  expect(urlInput).toBeInTheDocument();
  expect(keywordInput).toBeInTheDocument();
  expect(scrapeButton).toBeInTheDocument();

  // Simulate typing into the scraper inputs
  fireEvent.change(urlInput, { target: { value: 'https://example.com' } });
  fireEvent.change(keywordInput, { target: { value: 'test' } });

  // Simulate clicking the scrape button and check for spinner
  await act(async () => {
    fireEvent.click(scrapeButton);
  });

  // Check if the loading spinner appears
  const spinner = await screen.findByText((content, element) => {
    return content.includes('scraping...');
  });
  expect(spinner).toBeInTheDocument();
});
