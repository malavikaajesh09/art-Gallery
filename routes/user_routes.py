
from flask import Blueprint, request, redirect, render_template_string, session, render_template_string, session, render_template_string, session
from config import db, cursor

user_bp = Blueprint('user', __name__)
# -----------------------LOGIN----------------------------
@user_bp.route('/login/<role>', methods=['GET','POST'])
def login(role):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if role == 'admin':
            cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s AND role='admin'",
                           (username, password))
            user = cursor.fetchone()

            if user:
                return redirect('/admin_dashboard')

        else:
            cursor.execute("SELECT * FROM users WHERE name=%s AND password=%s",
                           (username, password))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user[0]   
                return redirect('/book_ticket')   # ✅ DIRECT REDIRECT

        return "<h3 style='color:red;text-align:center;'>Invalid Login</h3>"

    return f'''
    <link rel="stylesheet" href="/static/style.css">
    <style>
    body {{
        margin:0;
        font-family: Arial;
        background: linear-gradient(to right, #000000, #434343);
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
    }}

    .login-box {{
        background: rgba(0,0,0,0.8);
        padding:40px;
        border-radius:10px;
        box-shadow: 0 0 20px rgba(255,0,0,0.5);
        width:300px;
        text-align:center;
    }}

    h2 {{
        color:red;
        margin-bottom:20px;
    }}

    input {{
        width:100%;
        padding:10px;
        margin:10px 0;
        border:none;
        border-radius:5px;
    }}

    button {{
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
        color:orange;
        text-decoration:none;
    }}
    </style>

    <div class="login-box">
        <h2>{role.upper()} LOGIN</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password(min 8)" required>
            <button>Login</button>
        </form>
        <br>
        {"<a href='/signup'>New user? Sign up</a>" if role=='user' else ""}
        <br><br>
        <a href="/">Back Home</a>
    </div>
    '''

#---------- SIGN UP------------
@user_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # EMAIL VALIDATION
        if not email.endswith("@gmail.com"):
            return "<h3 style='color:red;text-align:center;'>Email must contain @gmail.com</h3>"

        # PASSWORD VALIDATION
        if len(password) < 8:
            return "<h3 style='color:red;text-align:center;'>Password must be at least 8 characters</h3>"

        cursor.execute("INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
                       (name,email,password))
        db.commit()

        return '''
        <h2 style="text-align:center;">Signup Successful 🎉</h2>
        <center><a href="/login/user">Login Now</a></center>
        '''

    return '''
    <style>
    body {
        margin:0;
        font-family: Arial;
        background: linear-gradient(to right, #000000, #434343);
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
    }

    .box {
        background: rgba(0,0,0,0.8);
        padding:40px;
        border-radius:10px;
        width:300px;
        text-align:center;
        box-shadow: 0 0 20px red;
    }

    h2 { color:red; }

    input {
        width:100%;
        padding:10px;
        margin:10px 0;
        border:none;
        border-radius:5px;
    }

    button {
        width:100%;
        padding:10px;
        background:red;
        color:white;
        border:none;
        border-radius:5px;
    }
    </style>

    <div class="box">
        <h2>User Signup</h2>
        <form method="POST">
            <input name="name" placeholder="Name" required>
            <input name="email" placeholder="name@gmail.com" required>
            <input type="password" name="password" placeholder="Password(8 min)" required>
            <button>Sign Up</button>
        </form>
        <br>
        <a href="/login/user">Already have account?</a>
    </div>
    '''
# ----------------------TICKET BOOKING----------------------
@user_bp.route('/book_ticket', methods=['GET','POST'])
def book_ticket():
    vid = session.get('user_id')
    if request.method == 'POST':

        children = int(request.form['children'])
        adult = int(request.form['adult'])
        senior = int(request.form['senior'])
        date = request.form['date']

        # 💰 price calculation
        total = children*15 + adult*30 + senior*25

        cursor.execute("""
        INSERT INTO tickets(V_ID, Children, Adult, SeniorAdult, total_amount, Date)
        VALUES(%s,%s,%s,%s,%s,%s)
        """, (vid, children, adult, senior, total, date))


        db.commit()

        # ✅ SUCCESS PAGE
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        body {{
            background: black;
            color: white;
            font-family: Arial;
            text-align: center;
            padding-top: 100px;
        }}

        h2 {{
            color: lightgreen;
        }}

        a {{
            background: red;
            padding: 10px 20px;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
        </style>
        </head>

        <body>

        <h2>🎉 Ticket Booked Successfully</h2>
        <p>Total Amount: ₹{total}</p>

        <a href="/">Go Home</a>

        </body>
        </html>
        '''

    # ✅ BOOKING PAGE (ONLY ONE return here)
    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Book Ticket</title>

    <style>
    body {
        margin: 0;
        font-family: Arial;
        background: black;
        color: white;
    }

    .main {
        display: flex;
        height: 100vh;
    }

    /* LEFT SIDE */
    .left {
        flex: 1;
        background: linear-gradient(to bottom right, #000000, #1a1a1a);
        padding: 60px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .left h1 {
        color: red;
        font-size: 40px;
    }

    .left p {
        margin-top: 15px;
        line-height: 1.6;
    }
    .update-box {
    margin-top: 25px;
    padding: 15px;
    background: rgba(255,255,255,0.05);
    border: 1px solid red;
    border-radius: 10px;
    width: 80%;
}

.update-box h3 {
    color: red;
}

.update-box input {
    width: 90%;
    padding: 8px;
    margin: 8px 0;
    border: none;
    border-radius: 5px;
}
.top-buttons {
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 10;
}

.top-btn {
    background: yellow;
    color: black;
    padding: 10px 15px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
}

.top-btn:hover {
    background: orange;
}
.update-box button {
    background: red;
    color: white;
    border: none;
    padding: 8px;
    width: 95%;
    border-radius: 5px;
    cursor: pointer;
}

.update-box button:hover {
    background: darkred;
}
    .icon {
        font-size: 60px;
        margin-bottom: 20px;
    }

    .right {
    flex: 1;
    background: url('https://images.unsplash.com/photo-1549880338-65ddcdfd017b') center/cover;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;   /* ⭐ VERY IMPORTANT */
}
    .form-box {
        background: rgba(255,255,255,0.1);
        padding: 30px;
        border-radius: 10px;
        width: 320px;
        backdrop-filter: blur(10px);
        text-align: center;
    }
    .logout-btn {
    background: red;
    color: white;
    padding: 10px 14px;
    border-radius: 6px;
    text-decoration: none;
    margin-left: 8px;
    font-weight: bold;
}

.logout-btn:hover {
    background: darkred;
}
    h2 {
        color: red;
    }
    .art-img {
    width: 60%;        /* reduced size */
    max-width: 300px;  /* prevents too big */
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(255,0,0,0.3);
}
    input {
        width: 90%;
        padding: 10px;
        margin: 10px 0;
        border: none;
        border-radius: 5px;
    }

    button {
        background: red;
        color: white;
        padding: 10px;
        border: none;
        width: 100%;
        border-radius: 5px;
        cursor: pointer;
    }

    button:hover {
        background: darkred;
    }
    </style>
    </head>

    <body>

    <div class="main">

        <!-- LEFT -->
       <div class="left">

    <img src="https://images.unsplash.com/photo-1541961017774-22349e4a1262" class="art-img">

    <h1>🎨 ART FLOW</h1>

    <p>
        Welcome to Art Flow, where creativity meets expression.
        Explore paintings, sculptures, and modern artworks.
    </p>

    <p>
        Experience immersive galleries and artistic storytelling.
    </p>

     </div>

        <!-- RIGHT -->
        <div class="right">
       <div class="top-buttons">
    <a href="/update_profile" class="top-btn">👤 Update</a>
    <a href="/logout" class="logout-btn">🚪 Logout</a>
</div>
           <div class="top-buttons">
           </div>

            <div class="form-box">
                <h2>🎟️ Book Ticket</h2>

                <form method="POST">
                    
                    Children (₹15) <input name="children" value="0"><br>
                    Adult (₹30) <input name="adult" value="0"><br>
                    Senior (₹25) <input name="senior" value="0"><br>
                    Date <input type="date" name="date"><br>

                    <button>Book Ticket</button>
                </form>
               
               
            </div>
        </div>

    </div>

    </body>
    </html>
    '''

# ------------------- VISITOR -------------------

@user_bp.route('/visitor', methods=['GET','POST'])
def visitor():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['email'],
            request.form['contact'],
            request.form['house']
        )
        cursor.execute("""
        INSERT INTO visitor(Name,Email,Contact,House_Name)
        VALUES(%s,%s,%s,%s)
        """, data)
        db.commit()
        return "Visitor Registered Successfully <br><a href='/'>Home</a>"

    return render_template_string('''
    <h2>Visitor Registration</h2>
    <form method="post">
        Name <input name="name"><br>
        Email <input name="email"><br>
        Contact <input name="contact"><br>
        House Name <input name="house"><br>
        <button>Register</button>
    </form>
    ''')
# --------------------VIEW TICKET----------------------

@user_bp.route('/view_tickets')
def view_tickets():
    cursor.execute("SELECT * FROM tickets")
    data = cursor.fetchall()

    table = ""
    for t in data:
        table += f"<tr><td>{t[0]}</td><td>{t[1]}</td><td>{t[2]}</td><td>{t[3]}</td><td>{t[4]}</td><td>{t[5]}</td></tr>"

    return f'''
    <h2>Tickets</h2>
    <table border=1>
    <tr><th>Children</th><th>Adult</th><th>Senior</th><th>Total</th><th>Date</th></tr>
    {table}
    </table>
    '''
# --------------------TICKET REPORT-------------------------
@user_bp.route('/ticket_report')
def ticket_report():
    cursor.execute("""
    SELECT users.name, tickets.Children, tickets.Adult, tickets.SeniorAdult,
           tickets.total_amount, tickets.Date
    FROM tickets
    JOIN users ON tickets.V_ID = users.id
    """)

    data = cursor.fetchall()

    rows = ""
    for r in data:
        rows += f"""
        <tr>
        <td>{r[0]}</td>
        <td>{r[1]}</td>
        <td>{r[2]}</td>
        <td>{r[3]}</td>
        <td>{r[4]}</td>
        <td>{r[5]}</td>
        </tr>
        """

    return f'''
    <h2>Ticket Report</h2>
    <table border=1>
    <tr>
    <th>Name</th>
    <th>Children</th>
    <th>Adult</th>
    <th>Senior</th>
    <th>Total</th>
    <th>Date</th>
    </tr>
    {rows}
    </table>
    '''
#-------------------------profile updation------------------------
@user_bp.route('/update_profile', methods=['GET','POST'])
def update_profile():
    vid = session.get('user_id')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s",
               (name, email, vid))
        db.commit()

        return "Profile Updated"

    return '''
<!DOCTYPE html>
<html>
<head>
<style>

body {
    margin: 0;
    font-family: Arial;
    background: linear-gradient(to right, #000000, #1a1a1a);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

/* CARD BOX */
.container {
    background: rgba(0,0,0,0.85);
    padding: 35px;
    border-radius: 12px;
    width: 350px;
    text-align: center;
    box-shadow: 0 0 25px rgba(255,0,0,0.6);
}

/* TITLE */
h2 {
    color: red;
    margin-bottom: 20px;
}

/* INPUT FIELDS */
input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: none;
    border-radius: 6px;
    outline: none;
}

/* BUTTON */
button {
    width: 100%;
    padding: 12px;
    background: red;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background: darkred;
}

/* BACK BUTTON */
.back-btn {
    display: inline-block;
    margin-top: 15px;
    padding: 8px 14px;
    border: 1px solid red;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}

.back-btn:hover {
    background: red;
}

</style>
</head>

<body>

<div class="container">

    <h2>👤 Update Profile</h2>

    <form method="POST">
        <input name="name" placeholder="Enter Name" required>
        <input name="email" placeholder="Enter Email" required>
        <button type="submit">Update</button>
    </form>

</body>
</html>
'''

#----------------- DELETE USER---------------
@user_bp.route('/delete_user/<int:id>')
def delete_user(id):

    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    db.commit()
    return redirect('/admin_dashboard?view=users')
# ---------------LOGOUT-------------------
@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user_bp.route('/update_user/<int:id>', methods=['GET','POST'])
def update_user(id):

    error = ""   

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # ✅ EMAIL VALIDATION
        if not email.endswith("@gmail.com"):
            error = "Email must contain @gmail.com"

        else:
            cursor.execute("""
            UPDATE users
            SET name=%s, email=%s
            WHERE id=%s
            """, (name, email, id))

            db.commit()
            return redirect('/admin_dashboard?view=users')

    # GET → fetch existing data
    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    u = cursor.fetchone()

    return f'''
<!DOCTYPE html>
<html>
<head>
<title>Update User</title>

<style>

body {{
    margin:0;
    font-family: Arial;
    background:black;
    color:white;
}}

.form-box {{
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
    font-size:16px;
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

</style>

</head>

<body>

<div class="form-box">

    <h2>✏️ Update User</h2>

    <form method="POST">

        <label>Name</label>
        <input name="name" value="{u[1]}" required>

        <input name="email" value="{request.form.get('email', u[2])}" 
        placeholder="name@gmail.com"
       pattern=".+@gmail\.com" 
       title="Email must end with @gmail.com"
       required>

        <button>Update User</button>

    </form>

    <a href="/admin_dashboard?view=users">⬅ Back to Dashboard</a>

</div>

</body>
</html>
'''