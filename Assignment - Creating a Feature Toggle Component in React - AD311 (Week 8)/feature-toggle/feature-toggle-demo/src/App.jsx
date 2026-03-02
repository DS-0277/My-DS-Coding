import './App.css'
import FeatureToggle from './FeatureToggle'

function App() {
  return (
    <>
      <h1>Feature Toggle</h1>
      <div>
        <FeatureToggle isEnabled={true} featureName={"Chat"} />
        <FeatureToggle isEnabled={false} featureName={"Payment"} />
        <FeatureToggle isEnabled={true} featureName={"Notification"} />
      </div>
    </>
  )
}

export default App
