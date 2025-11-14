from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app=Flask(__name__)

def init_db():
    con=sqlite3.connect('students.db')
    con.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, course TEXT)')
    con.close()
    
init_db()


@app.route('/')
def index():
    con=sqlite3.connect('students.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM students")
    rows=cur.fetchall()
    con.close()
    return render_template('index.html',rows=rows)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        course=request.form['course']
        
        con=sqlite3.connect('students.db')
        cur=con.cursor()
        cur.execute("INSERT  INTO students (name, email, course) VALUES (?, ?, ?)", (name, email, course))
        con.commit()
        con.close()
        
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    con=sqlite3.connect('students.db')
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM students WHERE id=?",(id,))
    student=cur.fetchone()
    
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        course=request.form['course']
        
        cur.execute("UPDATE students SET name=?,email=?,course=? WHERE id=?",(name,email,course,id))
        con.commit()
        con.close()
        return redirect(url_for('index'))
    
    con.close()
    return render_template('update.html',student=student)

@app.route('/delete/<int:id>')
def dele(id):
    con=sqlite3.connect('students.db')
    cur=con.cursor()
    cur.execute("DELETE FROM students where id=?",(id,))
    con.commit()
    con.close()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)
