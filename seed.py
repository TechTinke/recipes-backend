from app import create_app, db
from app.models import Cuisine, Recipe, Review, RecipeCuisine

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    cuisines = [
        Cuisine(name="Indian"),
        Cuisine(name="Italian")
    ]
    recipes = [
        Recipe(
            title="Butter Chicken",
            ingredients="Chicken, butter, cream, tomatoes, spices",
            instructions="Marinate chicken, cook with spices, simmer in tomato-cream sauce.",
            prep_time=45,
            cuisine_id=1
        ),
        Recipe(
            title="Tiramisu",
            ingredients="Mascarpone, coffee, ladyfingers, cocoa",
            instructions="Layer soaked ladyfingers with mascarpone cream, chill, dust with cocoa.",
            prep_time=30,
            cuisine_id=2
        )
    ]
    reviews = [
        Review(
            commenter_name="Priya",
            commenter_email="priya@gmail.com",
            comment="Amazingly creamy!",
            rating=5,
            recipe_id=1
        )
    ]
    recipe_cuisines = [
        RecipeCuisine(recipe_id=1, cuisine_id=1, serving_size=4),
        RecipeCuisine(recipe_id=2, cuisine_id=2, serving_size=6)
    ]
    
    db.session.add_all(cuisines + recipes + reviews + recipe_cuisines)
    db.session.commit()
    print("Seeded 2 cuisines, 2 recipes, 1 review, 2 recipe_cuisines")