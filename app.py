from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        with sqlite3.connect('database.db') as conn:
            conn.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
        return redirect(url_for('index'))
    return render_template('form.html', action="Add")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        conn.execute("UPDATE students SET name = ?, age = ? WHERE id = ?", (name, age, id))
        conn.commit()
        return redirect(url_for('index'))
    student = conn.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('form.html', action="Edit", student=student)

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect('database.db') as conn:
        conn.execute("DELETE FROM students WHERE id = ?", (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
