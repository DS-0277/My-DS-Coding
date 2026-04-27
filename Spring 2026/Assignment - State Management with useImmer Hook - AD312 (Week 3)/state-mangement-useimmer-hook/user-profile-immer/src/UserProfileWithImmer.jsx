import { useImmer } from 'use-immer';

function UserProfileWithImmer() {
    const [userProfile, updateUserProfile] = useImmer({
        name: "John",
        email: "johnexample@gmail.com",
        contactDetails: {
            phone: "123-456-7890",
            address: "Seattle"
        },
        preferences: {
            newsletter: false,
            notifications: true
        }
    });

    const updateContactDetails = (newPhoneNumber, newAddress) => {
        updateUserProfile(draft => {
            draft.contactDetails.phone = newPhoneNumber;
            draft.contactDetails.address = newAddress;
        });
    };

    const toggleNewsletterSubscription = () => {
        updateUserProfile(draft => {
            draft.preferences.newsletter = !draft.preferences.newsletter;
        });
    };
    
    return (
        <div>
            <h1>User Profile</h1>
            <p>Phone Number</p>
            <input type="text" value={userProfile.contactDetails.phone} onChange={(e) => updateContactDetails(e.target.value, userProfile.contactDetails.address)} />
            <p>Address</p>
            <input type="text" value={userProfile.contactDetails.address} onChange={(e) => updateContactDetails(userProfile.contactDetails.phone, e.target.value)} />
            <p>Newsletter</p>
            <button onClick={toggleNewsletterSubscription}>Toggle</button>
            <h2>New Values</h2>
            <p>Phone Number: {userProfile.contactDetails.phone}</p>
            <p>Address: {userProfile.contactDetails.address}</p>
            <p>Newsletter: {userProfile.preferences.newsletter ? "Yes" : "No"}</p>
        </div>
    );
}

export default UserProfileWithImmer;



// TEST CASES:

// Normal Cases:
// Case 1: Change phone number input ==> Produce new output as expected
// Case 2: Change address input ==> Produce new output as expected
// Case 3: Click "Toggle" for newsletter ==> Change boolean status

// Edge Cases:
// Case 1: Refresh page ==> Go to original state
// Case 2: Leave inputs blank ==> Produce no output except for default boolean value
// Case 3: Click "Toggle" multiple times ==> Change boolean status accordingly