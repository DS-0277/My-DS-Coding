import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    const handleIncrement = () => setCount(count + 1);
    const handleIncrementDelay = () => {
        setTimeout(() => {
            setCount(count + 1);
        }, 2000);
    };
    const handleIncrementTwice = () => {
        setCount(count + 1);
        setCount(count + 1);
    };
    const handleCorrectIncrementTwice = () => {
        setCount(prevCount => prevCount + 1)
        setCount(prevCount => prevCount + 1)
    };
    const handleDecrement = () => setCount(count - 1);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={handleIncrement}>Increment</button>
            <button onClick={handleIncrementDelay}>Increment After Delay</button>
            <button onClick={handleIncrementTwice}>Increment Twice</button>
            <button onClick={handleCorrectIncrementTwice}>Correct Increment Twice</button>
            <button onClick={handleDecrement}>Decrement</button>
        </div>
    );
}

export default Counter;



// TEST CASES

// Normal Test Cases
// Case 1: Increment by 1 ==> Before: '0' => After: '1'
// Case 2: Increment by 1 after 2 seconds ==> Before: '0' => After: '1' after 2s
// Case 3: Increment by 2 ==> Before: '0' => After: '2'

// Edge Test Cases
// Case 1: Decrement by 1 ==> Before: '2' => After: '1'
// Case 2: Decrement when current value is 0 ==> Before: '0' => After: '-1' 
// Case 3: Increment when in negative value ==> Before: '-1' => After: '0'
