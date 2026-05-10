import pizza from './pizza.svg';
import burger from './burger.svg';
import pasta from './pasta.svg';
import { Link } from "react-router";
import { useParams } from "react-router";

function RecipeDetail() {
    
    const { id } = useParams();

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

    const recipe = recipes.find((r) => r.id === Number(id));

    if (!recipe) {
        return <p>Recipe is not found</p>
    }
    
    return (
        <div>
            <img src={recipe.image} alt={recipe.title} />
            <p>{recipe.title}</p>
            <Link to="/gallery">Back to Gallery</Link>
        </div>
    );
}

export default RecipeDetail;