import ProductList from './ProductList';
import { render, screen } from '@testing-library/react';
import { test, expect } from 'vitest';
import '@testing-library/jest-dom/vitest';

// NORMAL TEST CASES
// Case 1: (Rendering all product names)
test("Rendering all product names", () => {
    render(<ProductList />);
    expect(screen.getByText("Laptop")).toBeInTheDocument();
    expect(screen.getByText("Smartphone")).toBeInTheDocument();
    expect(screen.getByText("Digital Book")).toBeInTheDocument();
});
// Case 2: (Rendering the description labels for all products)
test("Rendering the description labels for all products", () => {
    render(<ProductList />);
    expect(screen.getByText("Description: High-performance laptop for professionals")).toBeInTheDocument();
    expect(screen.getByText("Description: Good smartphone for daily uses")).toBeInTheDocument();
    expect(screen.getByText("Description: Portable e-reader")).toBeInTheDocument();
});
// Case 3: (Rendering the price labels for all products)
test("Rendering the price labels for all products", () => {
    render(<ProductList />);
    expect(screen.getByText("Price: USD1200")).toBeInTheDocument();
    expect(screen.getByText("Price: USD1000")).toBeInTheDocument();
    expect(screen.getByText("Price: USD300")).toBeInTheDocument();
});

// EDGE TEST CASES
// Case 1: (Ensuring that each product name has only one)
test("Ensuring that each product name has only one", () => {
    render(<ProductList />);
    expect(screen.getAllByText("Laptop")).toHaveLength(1);
    expect(screen.getAllByText("Smartphone")).toHaveLength(1);
    expect(screen.getAllByText("Digital Book")).toHaveLength(1);
});
// Case 2: (Ensuring that description appears three times)
test("Ensuring that description appears three times", () => {
    render(<ProductList />);
    expect(screen.getAllByText(/Description/)).toHaveLength(3);
});
// Case 3: (Ensuring that USD300 appears once)
test("Ensuring that USD300 appears once", () => {
    render(<ProductList />);
    expect(screen.getAllByText(/USD300/)).toHaveLength(1);
});