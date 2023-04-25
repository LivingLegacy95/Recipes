from flask_app import app
from flask_app.controllers import users, recipes
print("Hello World")

if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)