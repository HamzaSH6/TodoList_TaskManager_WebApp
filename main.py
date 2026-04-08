# Imports
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Flask and Flask SQLAlchemy Init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Task Table
class ToDo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.NVARCHAR(250), nullable=False)
    order = db.Column(db.Integer, nullable=True)
    checked = db.Column(db.Boolean, default=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='tasks')


# CategoryTable
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.NVARCHAR(250), nullable=False)
    order = db.Column(db.Integer, nullable=True)
    tasks = db.relationship('ToDo', back_populates='category', order_by='ToDo.order', lazy=True)


with app.app_context():
    db.create_all()


# Index Route
@app.route("/")
def index():
    try:
        all_tasks = ToDo.query.all()
        all_categories = Category.query.order_by(Category.order).all()
    except Exception as e:
        flash(f"Error: {e}", "error")
    return render_template("index.html", all_tasks=all_tasks, all_categories=all_categories)


### Task Routes
# Adding Task Route
@app.route("/add_task", methods=["POST"])
def add_task():
    try:
        task_name = request.form.get("task_name")
        task_category = request.form.get("task_category")
        max_order = ToDo.query.order_by(ToDo.order.desc()).first()
        task_order = (max_order.order + 1) if max_order else 0

        new_task = ToDo(
            name=task_name,
            category_id=task_category,
            order=task_order
        )
        db.session.add(new_task)
        db.session.commit()
        flash(f"Task: '{task_name}' Added Successfully!", "success")
    except Exception as e:
        flash(f"Got Error while Adding Task: {e}", "error")
    return redirect(url_for("index"))


# Removing Task Route
@app.route("/remove_task/<task_id>", methods=["POST"])
def remove_task(task_id):
    try:
        task = ToDo.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        flash(f"Task: '{task.name}' Removed Successfully!", "success")
    except Exception as e:
        flash(f"Got Error while Removing Task: {e}", "error")
    return redirect(url_for("index"))


# Checking Task Route
@app.route("/check_task/<task_id>", methods=["POST"])
def check_task(task_id):
    try:
        task = ToDo.query.filter_by(id=task_id).first()

        is_checked = "is_checked" in request.form
        task.checked = is_checked

        db.session.commit()
        if is_checked:
            flash(f"Task: '{task.name}' Checked Successfully!", "success")
        else:
            flash(f"Task: '{task.name}' Unchecked Successfully!", "success")
    except Exception as e:
        flash(f"Got Error while Checking/Unchecking Task: {e}", "error")
    return redirect(url_for("index"))


### Category Routes

# Add Category Route
@app.route("/add_category", methods=["POST"])
def add_category():
    try:
        category_name = request.form.get("category_name")
        max_order = Category.query.order_by(Category.order.desc()).first()
        category_order = (max_order.order + 1) if max_order else 0

        new_category = Category(
            name=category_name,
            order=category_order
        )
        db.session.add(new_category)
        db.session.commit()
        flash(f"Category: '{category_name}' Added Successfully!", "success")
    except Exception as e:
        flash(f"Got Error while Adding Category: {e}", "error")
    return redirect(url_for("index"))


# Remove Category Route
@app.route("/remove_category/<category_id>", methods=["POST"])
def remove_category(category_id):
    try:
        category = Category.query.filter_by(id=category_id).first()
        db.session.delete(category)
        db.session.commit()
        flash(f"Category: '{category.name}' Removed Successfully!", "success")
    except IntegrityError:
        flash(f"Cannot Remove Category because it has Tasks in it", "error")
    except Exception as e:
        flash(f"Got Error while Removing Category: {e}", "error")
    return redirect(url_for("index"))


# Task Ordering Route
@app.route("/update_task_order", methods=["POST"])
def update_task_order():
    try:
        data = request.get_json()
        order = data["order"]
        category_id = data["category_id"]

        for index, task_id in enumerate(order):
            task = ToDo.query.get(task_id)
            task.order = index
            task.category_id = category_id

        db.session.commit()
    except Exception as e:
        flash(f"Got Error while Updating Task Order: {e}", "error")
    return redirect(url_for("index"))


# Category Ordering Route
@app.route("/update_category_order", methods=["POST"])
def update_category_order():
    try:
        data = request.get_json()
        order = data["order"]

        for index, cat_id in enumerate(order):
            cat = Category.query.get(cat_id)
            cat.order = index

        db.session.commit()
    except Exception as e:
        flash(f"Got Error while Updating Category Order: {e}", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
