function FeatureToggle({ isEnabled, featureName }) {
    if (isEnabled) {
        return <p>{featureName}</p>
    } else {
        return <p>Feature {featureName} is disabled</p>
    }
};

export default FeatureToggle;