import pizza from './pizza.svg';
import burger from './burger.svg';
import pasta from './pasta.svg';
import { Link } from "react-router";

function Gallery() {

    const recipes = [
        {
            id: 1,
            title: "Pizza",
            image: pizza
        },
        {
            id: 2,
            title: "Burger",
            image: burger
        },
        {
            id: 3,
            title: "Pasta",
            image: pasta
        }
    ];

    return (
        <div>
            {recipes.map((recipe) => (
                <div key={recipe.id}>
                    <Link to={`/recipe/${recipe.id}`}>
                        <img src={recipe.image} alt={recipe.title} />
                        <p>{recipe.title}</p>
                    </Link>
                </div>
            ))}
        </div>
    );
}

export default Gallery;