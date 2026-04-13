import FeatureToggle from './FeatureToggle';
import { render, screen } from '@testing-library/react';
import { test, expect } from 'vitest';
import '@testing-library/jest-dom/vitest';


// NORMAL TEST CASES
// Case 1: (Rendering feature name 'Chat' when enabled)
test("Rendering feature name'Chat' when enabled", () => {
    render(<FeatureToggle isEnabled={true} featureName={"Chat"} />);
    expect(screen.getByText("Chat")).toBeInTheDocument();
});

// Case 2: (Rendering feature name 'Payment' when disabled)
test("Rendering feature name 'Payment' when disabled", () => {
    render(<FeatureToggle isEnabled={false} featureName={"Payment"} />);
    expect(screen.getByText("Feature Payment is disabled")).toBeInTheDocument();
});

// Case 3: (Rendering feature name 'Notification' when enabled)
test("Rendering feature name 'Notification' when enabled", () => {
    render(<FeatureToggle isEnabled={true} featureName={"Notification"} />);
    expect(screen.getByText("Notification")).toBeInTheDocument();
});

// EDGE TEST CASES

// Case 1: (Handling empty feature name when disabled)
test("Handling empty feature name when disabled", () => {
    render(<FeatureToggle isEnabled={false} featureName="" />);
    expect(screen.getByText("Feature is disabled")).toBeInTheDocument();
});
// Case 2: (Handling empty feature name when enabled)
test("Handling empty feature name when enabled", () => {
    const { container } = render(<FeatureToggle isEnabled={true} featureName="" />);
    expect(container.querySelector("p")).toBeInTheDocument();
});
// Case 3: (Handling null feature name when disabled)
test("Handling null feature name when disabled", () => {
    const { container } = render(<FeatureToggle isEnabled={false} featureName={null} />);
    expect(container.textContent).toBe("Feature  is disabled");
});