import AlertButton from './AlertButton';

function Toolbar() {
    return (
        <div>
            <AlertButton message="Playing Now">
                Play
            </AlertButton>
            <AlertButton message="Uploading Now">
                Upload
            </AlertButton>
            <AlertButton message="Deleted Already">
                Delete
            </AlertButton>
            <AlertButton message="This is the test case to check whether the alert is triggered or not. Some symbols are @#$%&* 😊">
                Test
            </AlertButton>
        </div>
    );
};

export default Toolbar;