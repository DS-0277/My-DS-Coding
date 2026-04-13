const products = [
    {
        id: 1,
        name: "Laptop",
        description: "High-performance laptop for professionals",
        price: "1200"
    },
    {
        id: 2,
        name: "Smartphone",
        description: "Good smartphone for daily uses",
        price: "1000"
    },
    {
        id: 3,
        name: "Digital Book",
        description: "Portable e-reader",
        price: "300"
    }
];

function ProductList() {
    return (
        <div>
            {products.map(product => (
                <div key={product.id}>
                    <h2>{product.name}</h2>
                    <ul>
                        <li>Description: {product.description}</li>
                        <li>Price: USD{product.price}</li>
                    </ul>
                </div>
            ))}
        </div>
    );
}

export default ProductList;