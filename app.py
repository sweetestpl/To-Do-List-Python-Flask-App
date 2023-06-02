from flask import Flask, request, render_template, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=True)  # renamed from due_date
    end_date = db.Column(db.DateTime, nullable=True)  # new field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if request.method == 'POST':
            task_content = request.form.get('content')
            start_date_str = request.form.get('start_date')
            start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M") if start_date_str else None
            end_date_str = request.form.get('end_date')
            end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M") if end_date_str else None
            new_task = Todo(task=task_content, start_date=start_date, end_date=end_date, user_id=current_user.id)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(e)
                abort(500)
        else:
            tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.timestamp.desc()).all()
            return render_template('index.html', tasks=tasks)
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect('/')
            else:
                return 'Invalid username or password'
        else:
            return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    password_hash = generate_password_hash(password)
    new_user = User(username=username, password_hash=password_hash)
    try:
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect('/')
    except Exception as e:
        print(e)
        abort(500)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    if task_to_delete.user_id != current_user.id:
        abort(403)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task = Todo.query.get_or_404(id)
    if task.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        task.task = request.form['content']
        start_date_str = request.form.get('start_date')
        task.start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M") if start_date_str else None
        end_date_str = request.form.get('end_date')
        task.end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M") if end_date_str else None
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('index.html', task=task)

@app.route('/tasks-due-dates')
@login_required
def tasks_due_dates():
    tasks = Todo.query.filter_by(user_id=current_user.id).all()
    due_dates = [
        {"title": task.task, "start": task.start_date.strftime("%Y-%m-%dT%H:%M"), "end": task.end_date.strftime("%Y-%m-%dT%H:%M")} 
        for task in tasks if task.start_date and task.end_date
    ]
    return jsonify(due_dates)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
