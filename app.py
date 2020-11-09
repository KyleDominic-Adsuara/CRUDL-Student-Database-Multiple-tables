from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('CRUD.db')
    return db

@app.route('/', methods = ['GET',"POST"])
def home():
	cur = get_db().cursor()
	if request.method == 'POST':
		userDetails = request.form
		idnum = userDetails['idnum']
		fname = userDetails['fname']
		lname = userDetails['lname']
		yearlv = userDetails['yrlvl']
		gender = userDetails['genderopt']
		course = userDetails['course_sel']
		dept = userDetails['dept_sel']
		cur.execute("INSERT INTO Students VALUES (:idnum, :fname, :lname, :yearlv, :gender, :course, :dept)",
			{'idnum':idnum,'fname':fname,'lname':lname,'yearlv':yearlv,'gender':gender,'course':course,'dept':dept})
		get_db().commit()
		get_db().close()
		return redirect('/List_page')
	cur.execute('SELECT courseCode FROM Course')
	courses = cur.fetchall()
	cur.execute('SELECT dName FROM Department')
	departments = cur.fetchall()
	return render_template('home.html',courses=courses, departments=departments)

@app.route('/List_page')
def student_list():
	cur = get_db().cursor()
	details = cur.execute("""SELECT s.idNum, s.fName, s.lName, s.course, s.yearLvl, s.department, c.college 
		FROM Students s
		LEFT JOIN Course c ON s.course=c.courseCode""")
	students = cur.fetchall()
	return render_template('list.html', students=students)

@app.route('/delete', methods=['GET','POST'])
def delete():
	if request.method == 'POST':
		userDetails = request.form['to_delete']
		cur = get_db().cursor()
		cur.execute("DELETE FROM Students WHERE idNum = :idnum",
			{'idnum': userDetails})
		get_db().commit()
		return redirect(url_for('student_list'))
	return render_template('delete.html')

@app.route('/update/<string:id>', methods=['GET','POST'])
def update(id):
	cur = get_db().cursor()
	if request.method=='POST':
		userDetails= request.form
		idnum = userDetails['idnum']
		fname = userDetails['fname']
		lname = userDetails['lname']
		yearlv = userDetails['yrlvl']
		gender = userDetails['genderopt']
		course = userDetails['course_sel']
		dept = userDetails['dept_sel']
		cur.execute("""UPDATE Students
			SET idNum = :idnum, fName = :fname, lName = :lname, yearLvl = :yearlv, gender = :gender, course = :course, department = :dept
			WHERE idNum = :id""",
			{'idnum': idnum,'fname': fname,'lname': lname,'yearlv': yearlv,'gender': gender,'course': course,'dept': dept,'id': id,})
		get_db().commit()
		get_db().close
		return redirect('/List_page')
	cur.execute("SELECT idNum, fName, lName, yearLvl FROM students WHERE idNum=:idnum",
		{'idnum': id})
	updt = cur.fetchall()
	cur.execute('SELECT courseCode FROM Course')
	courses = cur.fetchall()
	cur.execute('SELECT dName FROM Department')
	departments = cur.fetchall()
	return render_template('update.html', courses=courses, departments=departments, updates=updt)

if __name__ == '__main__':
    app.run(debug=True)