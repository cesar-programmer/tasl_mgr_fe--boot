from flask import Flask, render_template, request, redirect, url_for
import requests

# Si estás trabajando con un backend separado, asegúrate de tener la URL correcta.
BACKEND_URL = 'http://127.0.0.1:5000/tasks'

app = Flask(__name__)

@app.get('/')
def index():
  return render_template('tasks.html')

@app.get('/about')
def about():
  return render_template('about.html')

@app.get('/tasks')
def tasks_list():
  response = requests.get(BACKEND_URL)
  if response.status_code == 200:
      tasks_list = response.json().get('tasks')
      return render_template('list.html', tasks=tasks_list)
  else:
      return render_template('error.html', err=response.status_code), response.status_code

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
  if request.method == 'POST':
      task_data = {
          'name': request.form['name'],
          'summary': request.form['summary'],
      }
      response = requests.post(f'{BACKEND_URL}/create', json=task_data)
      if response.status_code == 204:
          return redirect(url_for('tasks_list'))
      else:
          return render_template('error.html', err=response.status_code), response.status_code
  return render_template('create_task.html')


@app.get('/tasks/delete/<int:pk>')
def delete_task(pk):
  response = requests.delete(f"{BACKEND_URL}/delete/{pk}")
  if response.status_code == 204:
      return redirect(url_for('tasks_list'))
  else:
      return render_template('error.html', err=response.status_code), response.status_code
