## ✅ Todo List Task Manager Web App

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-Styling-38BDF8)
![SortableJS](https://img.shields.io/badge/SortableJS-Drag%20%26%20Drop-orange)
![Font Awesome](https://img.shields.io/badge/Font%20Awesome-Icons-38BDF8)

A modern task manager web app built with **Flask**, **SQLAlchemy**, **SQLite**, **Tailwind CSS**, and **SortableJS**.  
It allows users to create categories, add tasks, mark tasks as complete, delete tasks/categories, and drag tasks between
categories while keeping their order updated in the database.

---

### 🧠 Features:

- Add new categories
- Add new tasks through a modal
- Assign tasks to a selected category
- Mark tasks as completed/uncompleted
- Delete tasks/categories
- Drag and drop tasks inside a category
- Move tasks from one category to another
- Drag and reorder categories/tasks
- Automatically save updated task/category order in the database
- Flash messages for user actions and error handling
- Clean, responsive, minimal and modern UI using Tailwind CSS

---

### ⚙️ Tech Stack / Libraries:

- **Flask** - Backend web framework
- **Flask-SQLAlchemy** - ORM for database handling
- **SQLite** - Lightweight database *(Used for development, PostgreSQL is recommended for production)*
- **HTML + Jinja2 + Tailwind CSS + JS** - Frontend
- **SortableJS** - Drag and drop sorting
- **Font Awesome** - Icons

---

### 🗂️ Database Structure:

**Category Table:**

- `id`
- `name`
- `order`
- `tasks` (relationship)

**ToDo Table:**

- `id`
- `name`
- `order`
- `checked`
- `category_id`
- `category` (relationship)

**Relationship:**  
A category can have multiple tasks (One to Many Relationship)

---

### 📌 Example Screenshots:

#### Adding Task Modal:

<img src="screenshots/add_task_img.png" width="550">

#### Main Example:

<img src="screenshots/example_img.png" width="550">

---

### 🚀 How to Run:

```text
pip install -r requirements.txt
python main.py
```