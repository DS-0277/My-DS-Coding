import React from "react";
import { useState } from "react";

function Gallery() {
    const [number, setNumber] = useState(0);

    const images = [
        {id: 1, url: './src/assets/bacon.png', description: 'Bacon'},
        {id: 2, url: './src/assets/eggs.png', description: 'Eggs'},
        {id: 3, url: './src/assets/garlic.png', description: 'Garlic'},
        {id: 4, url: './src/assets/pepper.png', description: 'Pepper'},
        {id: 5, url: './src/assets/spaghetti.png', description: 'Spaghetti'}
    ];

    const decrement = () => {
        if (number > 0) {
            setNumber(number - 1);
        }
    };

    const increment = () => {
        if (number < images.length - 1) {
            setNumber(number + 1);
        }
    };
    
    return (
        <div>
            <img src={images[number].url} alt={images[number].description} />
            <p>{images[number].description}</p>
            <button onClick={decrement}>Previous</button>
            <button onClick={increment}>Next</button>
        </div>
    );
}

export default Gallery;


// TEST CASES

// NORMAL CASES
// Case 1: Click 'Next' ==> Change image from 'Bacon' to 'Eggs'
// Case 2: Click 'Previous' ==> Change image from 'Eggs' to 'Bacon'
// Case 3: Click 'Next' two times ==> Change image from 'Bacon' to 'Garlic'

// EDGE CASES
// Case 1: Refresh the page ==> Go to 'Bacon'
// Case 2: Click 'Previous' at index 0 ==> Stay at 'Bacon'
// Case 3: Click 'Next' at the last index ==> Stay at 'Spaghetti'