import spaghettiCarbonara from './assets/spaghetti-carbonara.png';
import avocadoToast from './assets/avocado-toast.png';

const recipes = [
    {
        id: 1,
        title: "Spaghetti Carbonana",
        ingredients: ["Pasta", "Cheese", "Bacon", "Eggs"],
        image: spaghettiCarbonara
    },
    {
        id: 2,
        title: "Avocado Toast",
        ingredients: ["Avocado", "Bread", "Salt", "Lemon"],
        image: avocadoToast
    }
];

function RecipeGallery() {
    return (
        <div>
            {recipes.map((recipe) => (
                <div key={recipe.id}>
                    <h2>{recipe.title}</h2>
                    <img src={recipe.image} alt={recipe.title} />
                    <ul>
                        {recipe.ingredients.map((ingredients, index) => (
                            <li key={index}>{ingredients}</li>
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    );
};

export default RecipeGallery;