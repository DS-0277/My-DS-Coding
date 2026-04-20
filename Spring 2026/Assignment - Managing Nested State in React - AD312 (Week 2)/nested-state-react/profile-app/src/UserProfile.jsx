import { useState } from "react";

function UserProfile() {
    const [user, setUser] = useState({
        name: "John",
        email: "john@gmail.com",
        address: {street: 123, city: "Seattle", country: "USA"}
    });

    const [street, setStreet] = useState("");
    const [city, setCity] = useState("");
    const [country, setCountry] = useState("");

    const updateAddress = () => {
        setUser({...user, address: {...user.address, street: street, city: city, country: country}});
    }
    
    return (
        <div>
            <div>
                <input type="text" value={street} onChange={(e) => setStreet(e.target.value)} placeholder="e.g. 123"></input>
            </div>
            <div>
                <input type="text" value={city} onChange={(e) => setCity(e.target.value)} placeholder="e.g. Seattle"></input>
            </div>
            <div>
                <input type="text" value={country} onChange={(e) => setCountry(e.target.value)} placeholder="e.g. USA"></input>
            </div>
            <p>{user.name}'s address is: {user.address.street}, {user.address.city}, {user.address.country}</p>
            <button onClick={updateAddress}>CLICK TO CHANGE ADDRESS</button>
        </div>
    );
}

export default UserProfile;



// TEST CASES

// NORMAL TEST CASES:
// Case 1: Provide inputs and click the button ==> New address is rendered
// Case 2: Provide only one input and click the button ==> Only that input field is changed
// Case 3: Provide two inputs and click the button ==> Only those two input fields are changed


// EDGE TEST CASES:
// Case 1: Refresh the page ==> Revert to the pre-defined info 
// Case 2: Click the button without providing any info ==> No information is rendered
// Case 3: Add spaces before the input ==> Information is rendered without spaces