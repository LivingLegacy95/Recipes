`# checklist

- [x] create a new directory
- [x] inside the directory run:

```bash
pipenv install flask pymysql flask-bycrypt
```

- [ ] activate the virtual environment

```bash
pipenv shell
```
## Moduralized Flask App
- [ ] create [server.py](server.py)

## make `flask_app`

- [ ] [`models`](flask_app/models/user.py)
- [ ] [`config`](flask_app/config/mysqlconnection.py)
- [ ] [`controllers`](flask_app/controllers/users.py)
- [ ] [`templates`](flask_app/templates/index.html)
- [ ] [`static`](flask_app/static/css/style.css)

- [ ] [`__init__.py`](flask_app/__init__.py)

```bash
from flask import Flask, render_template, redirect, request  # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"

@app.route('/')          # The "@" decorator associates this route with the function immediately following
def index():
    return render_template('index.html')  # Return the string 'Hello World!' as a response

## MORE ROUTES HERE 


if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)
``` 

- [ ] go to [localhost:5000](http://localhost:5000/)
- [ ] create a [templates](templates/index.html)

## Connect to a database

- [ ] create ERD: ![](comics_ERD.png)
- [ ] install the module to connect flask to mysql:

```bash
pipenv install pymysql
```

- [ ] create [mysqlconnection.py](mysqlconnection.py)
- [ ] create [model.py](model.py)  "model" is a place holder to be named after whatever you are logging or class name


- [ ] use this code to connect flask_app to database in your config file

```bash
# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = False)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query:str, data:dict=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
```