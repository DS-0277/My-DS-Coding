import { useImmer } from 'use-immer';
import { useState } from 'react';

function ShoppingListWithImmer() {
    // State Initialization
    const [shoppingList, updateShoppingList] = useImmer([]);
    const [name, setName] = useState('');
    const [quantity, setQuantity] = useState('');
    const [category, setCategory] = useState('');
    const [notes, setNotes] = useState('');

    // Add Item
    const addItem = (name, quantity, category, notes) => {
        updateShoppingList(draft => {
            draft.push({ id: Date.now(), name: name, quantity: Number(quantity), details: { category: category, notes: notes} });
        });
    };

    // Update Item
    const updateItem = (id, name, quantity, category, notes) => {
        updateShoppingList(draft => {
            const matchedItem = draft.find(item => item.id === id)
            matchedItem.name = name;
            matchedItem.quantity = Number(quantity);
            matchedItem.details.category = category;
            matchedItem.details.notes = notes;
        });
    };

    // Remove Item
    const removeItem = (id) => {
        updateShoppingList(draft => {
            const filterShoppingList = draft.filter(item => item.id !== id);
            return filterShoppingList;
        });
    };

    
    // Build UI
    return (
        <div>
            <h1>Shopping List</h1>
            <input type="text" value={name} placeholder="Item Name" onChange={(e) => setName(e.target.value)} />
            <input type="text" value={quantity} placeholder="Quantity" onChange={(e) => setQuantity(e.target.value)} />
            <input type="text" value={category} placeholder="Category" onChange={(e) => setCategory(e.target.value)} />
            <input type="text" value={notes} placeholder="Notes" onChange={(e) => setNotes(e.target.value)} />
            <button onClick={() => addItem(name, quantity, category, notes)}>ADD</button>
            {shoppingList.map(item => (
                <div key={item.id}>
                    <h2>Item Name: {item.name}</h2>
                    <p>Quantity: {item.quantity}</p>
                    <p>Category: {item.details.category}</p>
                    <p>Notes: {item.details.notes}</p>
                    <button onClick={() => updateItem(item.id, name, quantity, category, notes)}>UPDATE</button>
                    <button onClick={() => removeItem(item.id)}>REMOVE</button>
                </div>
            ))}
        </div>
    );
}

export default ShoppingListWithImmer;

// TEST CASES

// Normal Cases
// Case 1: Provide all inputs and click "ADD" ==> Provide result as expected
// Case 2: Update one input field and click "UPDATE" ==> Provide update as expected
// Case 3: Remove one item and click "REMOVE" ==> Remove from array as expected

// Edge Cases
// Case 1: Refresh the page ==> Remove all info and return to original version
// Case 2: Click "ADD" without any inputs ==> Display property without value
// Case 3: Leave one input field blank and click "ADD" ==> Display as expected