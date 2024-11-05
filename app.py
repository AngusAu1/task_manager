# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy                                 # ORM of python for communication with db
from datetime import datetime                                           # record time use


# Connect to the db, for 'add', 'update' and 'delete' tasks
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'             # connect app to the db: sqlite 'test.db'

# Initialize the database ORM (Object-Relational Mapping)
with app.app_context():
    db = SQLAlchemy(app)


# Create db schema, based on Flask-SQLAlchemy ORM model to handle Todo in the database 
# create schema: primary key - id, content and date_created
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)                        # define primary key = id, and it is integer type
    content = db.Column(db.String(200), nullable=False)                 # define content column, to store the todo content. Each content allow 200 string. nullable=False, it cannot be null.
    date_created = db.Column(db.DateTime, default=datetime.utcnow)      # define date_created column. It is the creation date and time. default=datetime.utcnow is default as UTC time when created a new todo task.
    completed = db.Column(db.Boolean, default=False)                    # define a completed for the checkbox function

    # class method: to return the task id
    def __repr__(self):
        return '<Task %r>' % self.id


# There are total 3 routes (add, delete and update)

# add method for task
@app.route('/', methods=['POST', 'GET'])                                # define the route at root /, it can accept POST and GET two HTTP requests. GET for read and display data; POST for submit and handle data
def add():
    if request.method == 'POST':                                        # When there is a POST request
        task_content = request.form['content']                          # the 'content' will be retrieved from the 'form' that input by user
        new_task = Todo(content=task_content)                           # And then create a new Todo object "new_task", and the content attribute is the content that user submitted.


        # push the 'new create task' push to database / store to the databse
        try:
            db.session.add(new_task)                                    # add the new_task
            db.session.commit()                                         # commit 
            return redirect('/')                                        # After commit success, redirect to root /, which mean reflash the main page, and display the new/updated todo list
        
        # Return error when it is failed create task
        except:
            return 'There was as issue adding your task'                # If failed commit, return an error message


    else:                                                               # When there is GET request; which 1. user 1st access main page or, 2. redirect to main page after create new or update a todo task.
        tasks = Todo.query.order_by(Todo.date_created).all()            # Display the new created task to the main page; it enquiry all the todo tasks, and order by the date_created, then return to index.html for rendering
        return render_template('index.html', tasks=tasks)               # Render the main page

# delete method for task
@app.route('/delete/<int:id>')                                          # define the route /delete/<int:id>; <int:id> is path parameter, it's allow user to delete the task id, this id will pass with the requst on the route
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)                          # To query the task-to-delete from the db by the id; if cannot found it, then return 404 error. It is flask to handle error in the easy way.

    # delete the task-to-delete in the db, and then commit
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')                                            # After commit success, redirect to root /, reflash the main page, and display the record(s) 
    
    # Return error when it is failed delete a task
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])                 # define the route /update/<int:id>; this route is supporting both GET and POST methods
def update(id):
    task_to_update = Todo.query.get_or_404(id)                          # Todo.query.get_or_404(id): To query the specify task by id, it will return the task if found the id; or return 404 if can't found
    if request.method == 'POST':                                        # When the user submitted the form (Post method), this code will be update the content, which the conten is according to the submitted form request.form['content']
        task_to_update.content = request.form['content']                
        
        try:                                                            # commit and then redirect to root /, and let the user to check the updated task
            db.session.commit()
            return redirect('/')
        except:                                                         # return error message, if exception occurred
            return 'There was an issue updating your task'              
        
    else:                                                               # When GET method /update/<id>, this code will be render the update.html, and pass the tasks object task_to_update to the template.
        return render_template('update.html', task=task_to_update)

@app.route('/toggle_complete/<int:id>', methods=['POST'])
def toggle_complete(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed  # 切換完成狀態
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem updating the task status'

if __name__ == '__main__':
    app.run(debug=True)                                                     # debug mode on