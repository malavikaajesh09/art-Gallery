
# Handle employee records and their management forms.
from flask import Blueprint, request, redirect, render_template_string, render_template_string, render_template_string
from config import db, cursor
import re
employee_bp = Blueprint('employee', __name__)
# DELETE EMPLOYEE
@employee_bp.route('/delete_employee/<int:id>')
def delete_employee(id):
    cursor.execute("DELETE FROM employee WHERE id=%s", (id,))
    db.commit()
    return redirect('/admin_dashboard?view=employees')

# ------------------- EMPLOYEE -------------------
@employee_bp.route('/add_employee', methods=['GET','POST'])
def add_employee():
    error = "" 
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        designation = request.form['designation']
        phone = request.form['phone']

# PHONE VALIDATION
        if not re.fullmatch(r'\d{10}', phone):
         return "<h3 style='color:red;text-align:center;'>Phone number must be exactly 10 digits</h3>"
        else:
         salary = request.form['salary']
         dept = request.form['department']

         cursor.execute("""
          INSERT INTO employee(Name,Age,Gender,Designation,Phone_no,Salary,Department)
          VALUES(%s,%s,%s,%s,%s,%s,%s)
          """, (name, age, gender, designation, phone, salary, dept))

         db.commit()

        return f'''
        <h2 style="text-align:center;color:lightgreen;">Employee Added Successfully 🎉</h2>
        <center><a href="/admin_dashboard?view=employees">Back to Dashboard</a></center>
        '''

    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Add Employee</title>

    <style>

    body{
        margin:0;
        font-family:Arial;
        background:black;
        color:white;
    }

    .form-box{
        width:420px;
        margin:80px auto;
        background:#111;
        padding:30px;
        border-radius:10px;
        box-shadow:0 0 15px rgba(255,0,0,0.6);
    }

    h2{
        text-align:center;
        color:red;
        margin-bottom:20px;
    }

    label{
        display:block;
        margin-top:10px;
    }

    input, select{
        width:100%;
        padding:10px;
        margin-top:5px;
        border:none;
        border-radius:5px;
    }

    button{
        margin-top:20px;
        width:100%;
        padding:10px;
        background:red;
        color:white;
        border:none;
        border-radius:5px;
        cursor:pointer;
        font-size:16px;
    }
    select{
    width:100%;
    padding:10px;
    margin-top:5px;
    border:none;
    border-radius:5px;
    } 

    button:hover{
        background:darkred;
    }

    a{
        display:block;
        text-align:center;
        margin-top:15px;
        color:white;
        text-decoration:none;
    }

    </style>

    </head>

    <body>

    <div class="form-box">

        <h2>➕ Add Employee</h2>

        <form method="POST">

            <label>Name</label>
            <input name="name" required>

            <label>Age</label>
            <input name="age" required>

            <label>Gender</label>
            <select name="gender">
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
            </select>

            <label>Designation</label>
            <input name="designation" required>

            <label>Phone</label>
            <input name="phone" required>

            <label>Salary</label>
            <input name="salary" required>

            <label>Department</label>
           <select name="department" required>
           <option value="">Select Department</option>
           <option value="Fine Arts">Fine Arts</option>
           <option value="Archaeology">Archaeology</option>
           <option value="Culture">Culture</option>
           <option value="History">History</option>
           <option value="Anthropology">Anthropology</option>
           <option value="Literature">Literature</option>
           <option value="Woodwork">Woodwork</option>
           <option value="Handicraft">Handicraft</option>
            <option value="Textile">Textile</option>
          </select>

            <button>Add Employee</button>

        </form>

        <a href="/admin_dashboard?view=employees">⬅ Back to Dashboard</a>

    </div>

    </body>
    </html>
    '''

  

@employee_bp.route('/view_employee')
def view_employee():
    cursor.execute("SELECT * FROM employee")
    data = cursor.fetchall()

    table = ""
    for e in data:
        table += f"<tr><td>{e[0]}</td><td>{e[1]}</td><td>{e[2]}</td><td>{e[3]}</td><td>{e[4]}</td><td>{e[5]}</td><td>{e[6]}</td><td>{e[7]}</td></tr>"

    return render_template_string(f'''
    <h2>Employee List</h2>
    <table border=1>
    <tr><th>ID</th><th>Name</th><th>Age</th><th>Gender</th><th>Designation</th><th>Phone</th><th>Salary</th><th>Dept</th></tr>
    {table}
    </table>
    <br><a href="/admin">Back</a>
    ''')


# employee update
@employee_bp.route('/update_employee/<int:id>', methods=['GET','POST'])
def update_employee(id):
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        salary = request.form['salary']
        gender = request.form['gender']
        age = request.form['age']
        phone = request.form['phone']
        department = request.form['department']
        if not re.fullmatch(r'\d{10}', phone):
            error = "Phone number must be exactly 10 digits"

        cursor.execute("""
        UPDATE employee 
        SET Name=%s, Designation=%s, Salary=%s, Gender=%s, Age=%s, Phone_no=%s, Department=%s 
        WHERE id=%s
        """, (name, designation, salary, gender, age, phone, department, id))

        db.commit()
        return redirect('/admin_dashboard?view=employees')

    cursor.execute("SELECT * FROM employee WHERE id=%s", (id,))
    e = cursor.fetchone()

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Update Employee</title>

    <style>

    body {{
        margin:0;
        font-family: Arial;
        background:black;
        color:white;
    }}

    .form-container {{
        width:400px;
        margin:80px auto;
        background:#111;
        padding:30px;
        border-radius:10px;
        box-shadow:0 0 15px rgba(255,0,0,0.6);
    }}

    h2 {{
        text-align:center;
        color:red;
        margin-bottom:20px;
    }}

    label {{
        display:block;
        margin-top:10px;
    }}

    input {{
        width:100%;
        padding:10px;
        margin-top:5px;
        border:none;
        border-radius:5px;
    }}

    button {{
        margin-top:20px;
        width:100%;
        padding:10px;
        background:red;
        color:white;
        border:none;
        border-radius:5px;
        cursor:pointer;
    }}

    button:hover {{
        background:darkred;
    }}

    a {{
        display:block;
        text-align:center;
        margin-top:15px;
        color:white;
        text-decoration:none;
    }}

    select{{
    width:100%;
    padding:10px;
    margin-top:5px;
    border:none;
    border-radius:5px;
    }}

    </style>

    </head>

    <body>

    <div class="form-container">

        <h2>✏️ Update Employee</h2>

        <form method="POST">

            <label>Name</label>
            <input name="name" value="{e[1]}" required>

            <label>Age</label>
            <input name="age" value="{e[2]}" required>

            <label>Gender</label>
            <input name="gender" value="{e[3]}" required>

            <label>Designation</label>
            <input name="designation" value="{e[4]}" required>

            <label>Phone</label>
            <input name="phone" value="{e[5]}" required>

            <label>Salary</label>
            <input name="salary" value="{e[6]}" required>
            <label>Department</label>
            <select name="department" required>
            <option value="{e[7]}">{e[7]} (Current)</option>
            <option value="Fine Arts">Fine Arts</option>
            <option value="Archaeology">Archaeology</option>
            <option value="Culture">Culture</option>
            <option value="History">History</option>
            </select>
            <button>Update Employee</button>

        </form>

        <a href="/admin_dashboard?view=employees">⬅ Back to Dashboard</a>

    </div>

    </body>
    </html>
    '''
