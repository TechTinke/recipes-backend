from . import db

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    recipes = db.relationship('Recipe', backref='cuisine', lazy=True)
    recipe_cuisines = db.relationship('RecipeCuisine', backref='cuisine', lazy=True)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'), nullable=False)
    reviews = db.relationship('Review', backref='recipe', lazy=True)
    recipe_cuisines = db.relationship('RecipeCuisine', backref='recipe', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commenter_name = db.Column(db.String(100), nullable=False)
    commenter_email = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

class RecipeCuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'), nullable=False)
    serving_size = db.Column(db.Integer, nullable=False)