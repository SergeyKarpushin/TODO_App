from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.String(50), nullable=True)

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('home.html', todos=tasks)

@app.route('/add', methods=['POST'])
def add_todo():
    task_text = request.form.get('task')
    if task_text:
        new_task = Task(task=task_text, done=False)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    task = Task.query.get(todo_id)
    if task:
        task.done = not task.done
        task.completion_date = datetime.now().strftime('%b-%d %I-%M %p') if task.done else None
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    task = Task.query.get(todo_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/update-order', methods=['POST'])
def update_order():
    # This route can be implemented if you want to persist the order of tasks
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
