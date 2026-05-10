function Home() {
    return (
        <div>
            <h1>Welcome to Recipe Gallery homepage</h1>
            <h2>Here is your favorite meal !!!</h2>
        </div>
    );
}

export default Home;



// TEST CASES


// Normal Cases
// Case 1: Click "Gallery" ==> Show gallery page as expected
// Case 2: Click "Pizza" ==> Show pizza detail page as expected
// Case 3: Click "Back to Gallery" ==> Show gallery page as expected


// Edge Cases
// Case 1: Click "Home" ==> Show homepage
// Case 2: Go to path "recipe/4" ==> Show 'Recipe is not found' message as expected
// Case 3: Go to path "recipe/a" ==> Show 'Recipe is not found' message as expected