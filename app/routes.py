from flask import Blueprint, jsonify, request
from . import db
from .models import Recipe, Cuisine, Review, RecipeCuisine

bp = Blueprint('routes', __name__)

@bp.route('/recipes', methods=['GET', 'POST'])
def handle_recipes():
    if request.method == 'GET':
        recipes = Recipe.query.all()
        return jsonify([{
            'id': r.id,
            'title': r.title,
            'ingredients': r.ingredients,
            'instructions': r.instructions,
            'prep_time': r.prep_time,
            'cuisine': r.cuisine.name,
            'cuisine_ids': [rc.cuisine_id for rc in r.recipe_cuisines]
        } for r in recipes])
    else:  # POST
        data = request.get_json()
        recipe = Recipe(
            title=data['title'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            prep_time=data['prep_time'],
            cuisine_id=data['cuisine_id']
        )
        db.session.add(recipe)
        db.session.commit()
        for cuisine_id in data.get('additional_cuisine_ids', []):
            rc = RecipeCuisine(recipe_id=recipe.id, cuisine_id=cuisine_id, serving_size=data['serving_size'])
            db.session.add(rc)
        db.session.commit()
        return jsonify({'message': 'Recipe created', 'id': recipe.id}), 201

@bp.route('/recipes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': recipe.id,
            'title': recipe.title,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'prep_time': recipe.prep_time,
            'cuisine': recipe.cuisine.name,
            'cuisine_ids': [rc.cuisine_id for rc in recipe.recipe_cuisines]
        })
    elif request.method == 'PUT':
        data = request.get_json()
        recipe.title = data['title']
        recipe.ingredients = data['ingredients']
        recipe.instructions = data['instructions']
        recipe.prep_time = data['prep_time']
        recipe.cuisine_id = data['cuisine_id']
        RecipeCuisine.query.filter_by(recipe_id=recipe.id).delete()
        for cuisine_id in data.get('additional_cuisine_ids', []):
            rc = RecipeCuisine(recipe_id=recipe.id, cuisine_id=cuisine_id, serving_size=data['serving_size'])
            db.session.add(rc)
        db.session.commit()
        return jsonify({'message': 'Recipe updated'})
    else:  # DELETE
        RecipeCuisine.query.filter_by(recipe_id=recipe.id).delete()
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted'})

@bp.route('/cuisines', methods=['GET', 'POST'])
def handle_cuisines():
    if request.method == 'GET':
        cuisines = Cuisine.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'recipes': [{'id': r.id, 'title': r.title} for r in c.recipes]
        } for c in cuisines])
    else:  # POST
        data = request.get_json()
        cuisine = Cuisine(name=data['name'])
        db.session.add(cuisine)
        db.session.commit()
        return jsonify({'message': 'Cuisine created', 'id': cuisine.id}), 201

@bp.route('/reviews', methods=['GET', 'POST'])
def handle_reviews():
    if request.method == 'GET':
        recipe_id = request.args.get('recipe_id', type=int)
        if recipe_id:
            reviews = Review.query.filter_by(recipe_id=recipe_id).all()
        else:
            reviews = Review.query.all()
        return jsonify([{
            'id': r.id,
            'commenter_name': r.commenter_name,
            'commenter_email': r.commenter_email,
            'comment': r.comment,
            'rating': r.rating,
            'recipe_id': r.recipe_id
        } for r in reviews])
    else:  # POST
        data = request.get_json()
        review = Review(
            commenter_name=data['commenter_name'],
            commenter_email=data['commenter_email'],
            comment=data['comment'],
            rating=data['rating'],
            recipe_id=data['recipe_id']
        )
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review submitted'}), 201