from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
import database

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# ---------------- Home ----------------
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    db_tasks = database.get_all_tasks(session['user_id'])
    tasks = []
    for t in db_tasks:
        task = {
            'id': t[0],
            'title': t[1],
            'description': t[2],
            'deadline': t[3],
            'priority': t[4],
            'completed': t[5]
        }
        tasks.append(task)

    return render_template('home.html', tasks=tasks)

# ---------------- Add Task ----------------
@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect('/login')

    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']
    priority = request.form['priority']

    database.add_task(title, description, deadline, priority, session['user_id'])
    return redirect('/')

# ---------------- Complete Task ----------------
@app.route('/complete/<int:task_id>')
def complete(task_id):
    if 'user_id' not in session:
        return redirect('/login')

    database.mark_task_completed(task_id, session['user_id'])
    return redirect('/')

# ---------------- Delete Task ----------------
@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' not in session:
        return redirect('/login')

    database.delete_task(task_id, session['user_id'])
    return redirect('/')

# ---------------- Login ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.get_user(username)

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Try again.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# ---------------- Register ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        success = database.register_user(username, hashed_password)
        if success:
            return redirect('/login')
        else:
            return render_template('register.html', error='Username already taken')

    return render_template('register.html')

# ---------------- Logout ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------- Run App ----------------
if __name__ == '__main__':
    database.init_db()  # Ensure tables exist
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
