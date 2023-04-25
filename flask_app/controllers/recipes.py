from flask_app import app, render_template, request, redirect, session
from flask_app.models.recipe import Recipe



#! CREATE
@app.route('/recipes/new')
def new():
    return render_template('recipes/new.html')


@app.route('/recipes/create', methods=['post'])
def create():
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    Recipe.save(request.form)
    return redirect('/recipes/dashboard')

#! READ ALL
@app.route('/recipes/dashboard')          # The "@" decorator associates this route with the function immediately following
def dashboard():
    if "user_id" not in session:
        return redirect('/logout')
    recipes = Recipe.get_all()
    # print(recipes)
    return render_template('recipes/dashboard.html', recipes = recipes)

#! READ ONE
@app.route('/recipes/<int:id>')
def show(id):
    data = {'id': id}
    recipe = Recipe.get_recipe(data)
    return render_template('recipes/show.html', recipe = recipe)



#! UPDATE
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    data = {'id': id}
    return render_template('recipes/edit.html', recipe = Recipe.get_recipe(data))

@app.route('/recipes/update', methods=['post'])
def update_recipe():
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")
    Recipe.update_recipe(request.form)
    return redirect('/recipes/dashboard')


#! DELETE
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    data = {'id': id}
    Recipe.delete_recipe(data)
    return redirect('/')