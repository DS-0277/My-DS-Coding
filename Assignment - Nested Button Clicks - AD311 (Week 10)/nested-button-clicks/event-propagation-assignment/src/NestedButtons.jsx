import react from 'react';

function NestedButtons() {
    const handleOuterClick = () => {
        alert("Outer Clicked");
    };
    const handleInnerClick = (e) => {
        e.stopPropagation();
        alert("Inner Clicked");
    };

    return (
        <div onClick={handleOuterClick}
            style={{
                background : 'lightblue',
                width: '200px',
                margin: '0 auto',
                padding: '10px'
            }}>Outer
            <button onClick={handleInnerClick}>Inner</button>
        </div>
    );
};

export default NestedButtons;