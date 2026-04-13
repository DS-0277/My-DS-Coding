import AlertButton from './AlertButton';

function Toolbar() {

    const buttons = [
        {
            message: 'Downloading!', children: 'Download File'
        },
        {
            message: 'Sharing!', children: 'Share Document'
        },
        {
            message: 'Uploading!', children: 'Upload Document'
        },
        {
            message: 'Testing!@#$%&*😇', children: 'Test Symbols!@#$%&*😇'
        }
    ];

    return (
        <div>
            {buttons.map((button, index) => (
                <AlertButton
                key={index}
                message={button.message}
                children={button.children}
                />
            ))}
        </div>
    );
};

export default Toolbar;