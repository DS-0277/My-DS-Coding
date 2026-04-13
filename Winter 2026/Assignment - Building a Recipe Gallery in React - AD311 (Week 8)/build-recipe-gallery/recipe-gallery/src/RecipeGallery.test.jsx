import RecipeGallery from './RecipeGallery';
import { render, screen } from '@testing-library/react';
import { test, expect } from 'vitest';
import '@testing-library/jest-dom/vitest';

// NORMAL TEST CASES
// Case 1: (Rendering recipe titles)
test("Rendering recipe titles", () => {
    render(<RecipeGallery />);
    expect(screen.getByText("Spaghetti Carbonana")).toBeInTheDocument;
    expect(screen.getByText("Avocado Toast")).toBeInTheDocument;
});
// Case 2: (Rendering ingredients for the first recipe)
test("Rendering ingredients for the first recipe", () => {
    render(<RecipeGallery />);
    expect(screen.getByText("Pasta"));
    expect(screen.getByText("Cheese"));
    expect(screen.getByText("Bacon"));
    expect(screen.getByText("Eggs"));
});
// Case 3: (Rendering ingredients for the second recipe)
test("Rendering ingredients for the second recipe", () => {
    render(<RecipeGallery />);
    expect(screen.getByText("Avocado"));
    expect(screen.getByText("Bread"));
    expect(screen.getByText("Salt"));
    expect(screen.getByText("Lemon"));
});


// EDGE TEST CASES
// Case 1: (Rendering only one recipe title)
test("Rendering only one recipe title", () => {
    render(<RecipeGallery />);
    expect(screen.getByText("Spaghetti Carbonana")).toBeInTheDocument;
});
// Case 2: (Rendering only one ingredient)
test("Rendering only one ingredient", () => {
    render(<RecipeGallery />);
    expect(screen.getByText("Pasta")).toBeInTheDocument;
});
// Case 3: (Rendering one ingredient from each recipe)
test("Rendering one ingredient from each recipe", () => {
    render(<RecipeGallery />);
    expect(screen.getByText("Pasta")).toBeInTheDocument;
    expect(screen.getByText("Avocado")).toBeInTheDocument;
});