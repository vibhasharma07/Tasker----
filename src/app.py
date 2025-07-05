from flask import Flask, render_template, request, redirect
import database

app = Flask(__name__)

database.init_db()


@app.route('/')
def home():
    db_tasks = database.get_all_tasks()
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

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    deadline = request.form['deadline']
    priority = int(request.form['priority'])

    database.add_task(title, description, deadline, priority)
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    database.mark_task_completed(task_id)
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    database.delete_task(task_id)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
