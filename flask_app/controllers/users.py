from flask_app import app, render_template, redirect, request, session, bcrypt, flash
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['post'])
def register():
    print(request.form)

    #TODO validate user
    if not User.validate_user(request.form):
        return redirect('/')

    # TODO Find user in database
    user = User.find_by_email(request.form['email'])
    if user:
        flash("*Email already exists*")
        return redirect('/')

    #TODO hash the password

    hashed_pw = bcrypt.generate_password_hash(request.form['password'])

    #TODO save the user to the database
    temp_user = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    user = User.save(temp_user)
    
    #TODO login the user 
    session['user_id'] = user
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    
    return redirect('/recipes/dashboard')

@app.route('/login', methods=['post'])
def login():

    #TODO check if the email is in the DB
    user = User.find_by_email(request.form['email'])
    if not user:
        flash("Invalid Credentials")
        return redirect('/')
    #TODO verify if password matches the hash
    validate_password = bcrypt.check_password_hash(user.password, request.form['password'])
    if not validate_password: 
        flash("Invalid Credentials")
        return redirect('/')
    #TODO login the user
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/recipes/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
