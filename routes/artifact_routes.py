
from flask import Blueprint, request, redirect, render_template_string
from config import db, cursor

artifact_bp = Blueprint('artifact', __name__)
# ------------ ARTIFACT -------------------
@artifact_bp.route('/add_artifact', methods=['GET','POST'])
def add_artifact():

    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        type_ = request.form['type'].lower()
        dept = request.form['dept']
        place = request.form['place']

        cursor.execute("""
        INSERT INTO artifact(Name,Year,Type,Department,place)
        VALUES(%s,%s,%s,%s,%s)
        """, (name, year, type_, dept, place))

        db.commit()

        return '''
        <h2 style="text-align:center;color:lightgreen;">Artifact Added Successfully 🎉</h2>
        <center><a href="/admin_dashboard?view=artifacts">Back to Dashboard</a></center>
        '''

    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Add Artifact</title>

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

    input{
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
    select{
    width:105%;
    padding:10px;
    margin-top:5px;
    border:none;
    border-radius:5px;
   }

    </style>

    </head>

    <body>

    <div class="form-box">

        <h2> Add New Artifact</h2>

        <form method="POST">

            <label>Name</label>
            <input name="name" required>

            <label>Year</label>
            <input name="year" required>

            <label>Type</label>
            <select name="type" required>
             <option value="">Select Type</option>
             <option value="painting">Painting</option>
             <option value="sculpture">Sculpture</option>
             <option value="mask">Mask</option>
             <option value="manuscript">Manuscript</option>
             <option value="antique">Antique</option>
             <option value="craft">Craft</option>
             <option value="costume">Costume</option>
            </select>
            
            <label>Department</label>
            <select name="dept" required>
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

            <label>Place</label>
            <input name="place" required>

            <button>Add Artifact</button>

        </form>

        <a href="/admin_dashboard?view=artifacts">⬅ Back to Dashboard</a>

    </div>

    </body>
    </html>
    '''

# DELETE ARTIFACT
@artifact_bp.route('/delete_artifact/<int:id>')
def delete_artifact(id):
    cursor.execute("DELETE FROM artifact WHERE id=%s", (id,))
    db.commit()
    return redirect('/admin_dashboard?view=artifacts')

@artifact_bp.route('/view_artifact')
def view_artifact():
    cursor.execute("SELECT * FROM artifact")
    data = cursor.fetchall()

    table=""
    for a in data:
        table+=f"<tr><td>{a[0]}</td><td>{a[1]}</td><td>{a[2]}</td><td>{a[3]}</td><td>{a[4]}</td><td>{a[5]}</td></tr>"

    return render_template_string(f'''
    <h2>Artifact List</h2>
    <table border=1>
    <tr><th>ID</th><th>Name</th><th>Year</th><th>Type</th><th>Dept</th><th>Place</th></tr>
    {table}
    </table>
    <br><a href="/admin">Back</a>
    ''')
