from flask import Flask, render_template
from datetime import datetime
from flask import request, redirect
app = Flask(__name__)

tasks = []

from datetime import datetime

class Task:
    def __init__(self, title, description, due_date, due_time, repeat=False, repeat_date=None, repeat_time=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.due_time = due_time
        self.repeat = repeat
        self.repeat_date = repeat_date
        self.repeat_time = repeat_time
        self.completed = False
        self.completed_at = None
        self.overdue_counter = 0

    def mark_completed(self):
        self.completed = True
        self.completed_at = datetime.now()

    def is_overdue(self):
        current_datetime = datetime.now()
        task_datetime = datetime.combine(self.due_date, self.due_time)
        if current_datetime > task_datetime and not self.completed:
            return True
        return False

    def update_overdue_counter(self):
        if self.is_overdue():
            current_datetime = datetime.now()
            task_datetime = datetime.combine(self.due_date, self.due_time)
            self.overdue_counter = (current_datetime - task_datetime).days
@app.route('/')
def index():
    for task in tasks:
        if task.is_overdue():
            task.update_overdue_counter()

    return render_template('index.html', tasks=tasks)


@app.route('/add-task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
    due_time = datetime.strptime(request.form['due_time'], '%H:%M').time()
    repeat = 'repeat' in request.form
    repeat_date = request.form['repeat_date'] if repeat else None
    repeat_time = request.form['repeat_time'] if repeat else None

    new_task = Task(title, description, due_date, due_time, repeat, repeat_date, repeat_time)
    tasks.append(new_task)

    return redirect('/')

@app.route('/complete-task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = tasks[task_id]
    task.mark_completed()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
