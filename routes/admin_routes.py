
# Provide the admin dashboard and gallery revenue reports.
from flask import Blueprint, request, redirect
from config import db, cursor

admin_bp = Blueprint('admin', __name__)
#------------------------Admin dashboard-----------------------------
@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    view = request.args.get('view')
    total=0
    content = "<h2>Select a section</h2>"

    # ---------------- USERS ----------------
    if view == "users":
      search = request.args.get('search')

      if search:
        cursor.execute("""
            SELECT * FROM users 
            WHERE name LIKE %s OR id LIKE %s
        """, (f"%{search}%", f"%{search}%"))
        back_link = "/admin_dashboard?view=users"
      else:
        cursor.execute("SELECT * FROM users")
        back_link = "/admin_dashboard"   

      data = cursor.fetchall()

      rows = ""
      for u in data:
        rows += f"""
        <tr>
            <td>{u[0]}</td>
            <td>{u[1]}</td>
            <td>{u[2]}</td>
            <td>
                <a href='/update_user/{u[0]}'>✏️</a>
                <a href='/delete_user/{u[0]}' 
                 onclick="return confirm('Are you sure you want to delete this user?')"> ❌</a>
            </td>
        </tr>
        """

      content = f"""
    <h2>Users</h2>

    <!-- 🔍 Search Bar -->
    <form method="GET" action="/admin_dashboard">
        <input type="hidden" name="view" value="users">
        <input type="text" name="search" placeholder="Search by ID or Name" 
               style="padding:8px; width:200px;">
        <button type="submit" style="padding:8px; background:red; color:white;">
            🔍 Search
        </button>
    </form>

    <br>

    <table>
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Action</th></tr>
        {rows}
    </table>

    <div class="bottom-btn">
      <a href="{back_link}" class="back-btn">⬅ Back</a>
    </div>
    """
    # ---------------- PROFIT ----------------
    elif view == "profit":

     cursor.execute("SELECT SUM(total_amount) FROM tickets")
     total = cursor.fetchone()[0]

     cursor.execute("SELECT COUNT(*) FROM tickets")
     visitors = cursor.fetchone()[0]


     content = f"""
    <h2>Profit Report</h2>

    <table>
    <tr><th>Total Tickets</th><th>Total Revenue</th></tr>
    <tr>
    <td>{visitors}</td>
    <td>₹{total}</td>
    </tr>
    </table>
    <br><br>

    <a href="/daily_profit" style="padding:10px;background:red;color:white;text-decoration:none;border-radius:5px;">📅 Daily Profit</a>

    <a href="/monthly_profit" style="padding:10px;background:red;color:white;text-decoration:none;border-radius:5px;margin-left:10px;">📆 Monthly Profit</a>
    <div class="bottom-btn">
    <a href="/admin_dashboard" class="back-btn">⬅ Back</a>
 </div>
    """
    
    # ---------------- EMPLOYEE ----------------
    elif view == "employees":
     search = request.args.get('search')
     if search:
      cursor.execute("""
        SELECT * FROM employee
        WHERE name LIKE %s 
           OR id LIKE %s 
           OR designation LIKE %s
       """, (f"%{search}%", f"%{search}%", f"%{search}%"))
      back_link = "/admin_dashboard?view=employees"
     else:
        cursor.execute("SELECT * FROM employee")
        back_link = "/admin_dashboard"

     data = cursor.fetchall()

     rows = ""
     for e in data:
        rows += f"""
        <tr>
            <td>{e[0]}</td>
            <td>{e[1]}</td>
            <td>{e[4]}</td>
            <td>{e[5]}</td>
            <td>{e[6]}</td>
            <td>
                <a href='/update_employee/{e[0]}'>✏️</a>
                <a href='/delete_employee/{e[0]}' 
                onclick="return confirm('Are you sure you want to delete this employee?')">
                ❌
                </a>
            </td>
        </tr>
        """

     content = f"""
    <h2>Employees</h2>

    <!-- 🔍 Search -->
    <form method="GET" action="/admin_dashboard">
        <input type="hidden" name="view" value="employees">
        <input type="text" name="search" placeholder="Search by ID or Name"
               style="padding:8px; width:200px;">
        <button type="submit" style="padding:8px; background:red; color:white;">
            🔍 Search
        </button>
    </form>

    <br>

    <table>
    <tr><th>ID</th><th>Name</th><th>Designation</th><th>Phone</th><th>Salary</th><th>Action</th></tr>
    {rows}
    </table>

    <div style="text-align:right; margin-top:20px;">
        <a href="/add_employee" class="add-btn">➕ Add Employee</a>
    </div>

    <div class="bottom-btn">
        <a href="{back_link}" class="back-btn">⬅ Back</a>
    </div>
    """
    # ---------------- ARTIFACT ----------------
    elif view == "artifacts":
     search = request.args.get('search')

     if search:
      cursor.execute("""
        SELECT * FROM artifact
        WHERE id LIKE %s 
           OR name LIKE %s 
           OR year LIKE %s 
           OR department LIKE %s 
           OR type LIKE %s
       """, (
        f"%{search}%",
        f"%{search}%",
        f"%{search}%",
        f"%{search}%",
        f"%{search}%"
      ))
      back_link = "/admin_dashboard?view=artifacts"
     else:
        cursor.execute("SELECT * FROM artifact")
        back_link = "/admin_dashboard"

     data = cursor.fetchall()

     rows = ""
     for a in data:
        rows += f"""
        <tr>
            <td>{a[0]}</td>
            <td>{a[1]}</td>
            <td>{a[2]}</td>
            <td>{a[3]}</td>
            <td>{a[4]}</td>
            <td>
                <a href='/update_artifact/{a[0]}'>✏️</a>
                <a href='/delete_artifact/{a[0]}' 
                onclick="return confirm('Are you sure you want to delete this artifact?')">❌</a>
            </td>
        </tr>
        """

     content = f"""
    <h2>Artifacts</h2>

    <!-- 🔍 Search -->
    <form method="GET" action="/admin_dashboard">
        <input type="hidden" name="view" value="artifacts">
        <input type="text" name="search" placeholder="Search by ID or Name"
               style="padding:8px; width:200px;">
        <button type="submit" style="padding:8px; background:red; color:white;">
            🔍 Search
        </button>
    </form>

    <br>

    <table>
    <tr><th>ID</th><th>Name</th><th>Year</th><th>Type</th><th>Dept</th><th>Action</th></tr>
    {rows}
    </table>

    <div style="text-align:right; margin-top:20px;">
        <a href="/add_artifact" class="add-btn">➕ Add Artifact</a>
    </div>

    <div class="bottom-btn">
        <a href="{back_link}" class="back-btn">⬅ Back</a>
    </div>
    """
   
    return f'''
     
    <style>
    body {{
        margin:0;
        font-family: Arial;
        background:black;
        color:white;
    }}
     
    .container {{
        display:flex;
        height:100vh;
    }}

    .sidebar {{
        width:220px;
        background:#111;
        padding:20px;
    }}

    .sidebar h2 {{
        color:red;
    }}
    input {{
    border-radius: 5px;
    border: none;
    }}

    button {{
    border: none;
    border-radius: 5px;
    cursor: pointer;}}

    button:hover {{
    background: darkred;
     }}
    .sidebar a {{
        display:block;
        padding:10px;
        margin:10px 0;
        background:#222;
        color:white;
        text-decoration:none;
        border-radius:5px;
    }}

    .sidebar a:hover {{
        background:red;
    }}

    .content {{
        flex:1;
        padding:30px;
    }}
    

    table {{
        width:100%;
        border-collapse: collapse;
    }}

    th, td {{
        padding:10px;
        border:1px solid white;
        text-align:center;
    }}

    th {{
        background:red;
    }}
    .bottom-btn {{
    margin-top: 20px;
    text-align: right;
}}

.back-btn {{
    padding: 10px 18px;
    background-color: red;
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-weight: bold;
}}

.back-btn:hover {{
    background-color: darkred;
}}

    </style>
       
    <div class="container">

        <div class="sidebar">
            <h2>Admin</h2>
            <a href="/admin_dashboard?view=users">👤 Users</a>
            <a href="/admin_dashboard?view=employees">👨‍💼 Employees</a>
            <a href="/admin_dashboard?view=artifacts">🎨 Artifacts</a>
          <a href="/admin_dashboard?view=profit">💰 Profit</a>
         <a href="/view_summary">📋 Ticket Summary</a>
         <a href="/view_category">📂 Category</a>
          <a href="/">Logout</a>
        </div>

        <div class="content">
            {content}
        </div>

    </div>
    '''

#  profit
@admin_bp.route('/profit')
def profit():

    cursor.execute("SELECT SUM(total_amount) FROM tickets")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets")
    visitors = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(total_amount) FROM tickets")
    avg = cursor.fetchone()[0]

    return f'''
    <h2>Gallery Profit Report</h2>

    <p>Total Tickets Sold: {visitors}</p>
    <p>Total Revenue: ₹{total}</p>
    <p>Average Ticket Value: ₹{avg}</p>

    <br>
    <a href="/admin_dashboard">Back</a>
    '''
# VIEW SUMMARY

@admin_bp.route('/view_summary')
def view_summary():

    cursor.execute("SELECT * FROM ticket_summary")
    data = cursor.fetchall()

    rows = ""
    for r in data:
        rows += f"<tr><td>{r[0]}</td><td>₹{r[1]}</td><td>{r[2]}</td></tr>"
       
    return f'''
<html>
<head>
<style>

body {{
    font-family: Arial, sans-serif;
    background-color: #0f0f0f;  /* black theme */
    text-align: center;
    color: white;
}}

h2 {{
    color: red;
    margin-top: 30px;
}}

table {{
    margin: auto;
    border-collapse: collapse;
    width: 60%;
    background-color: #1a1a1a;
    box-shadow: 0 0 10px rgba(0,0,0,0.5);
}}

th {{
    background-color: red;
    color: white;
    padding: 12px;
}}

td {{
    padding: 10px;
    border-bottom: 1px solid #333;
}}

tr:hover {{
    background-color: #222;
}}

.bottom-btn {{
    width: 60%;
    margin: 20px auto;
    text-align: right;
}}

.back-btn {{
    padding: 10px 18px;
    background-color: red;
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-weight: bold;
}}

.back-btn:hover {{
    background-color: darkred;
}}

</style>
</head>

<body>

<h2>Ticket Summary</h2>

<table>
<tr>
    <th>Name</th>
    <th>Total Amount</th>
    <th>Date</th>
</tr>

{rows}

</table>

<!-- ✅ Button OUTSIDE table -->
<div class="bottom-btn">
    <a class="back-btn" href="/admin_dashboard?view=back-btn">⬅ Back</a>
</div>

</body>
</html>
'''
# DAILYPROFITT

@admin_bp.route('/daily_profit')
def daily_profit():

    cursor.execute("""
    SELECT Date, SUM(total_amount)
    FROM tickets
    GROUP BY Date
    """)

    data = cursor.fetchall()

    rows = ""
    for d in data:
        rows += f"<tr><td>{d[0]}</td><td>₹{d[1]}</td></tr>"

    return f"""
    <style>

    body {{
        margin:0;
        font-family: Arial;
        background:black;
        color:white;
        text-align:center;
        padding:40px;
    }}

    h2 {{
        color:red;
        margin-bottom:30px;
    }}

    table {{
        width:60%;
        margin:auto;
        border-collapse: collapse;
    }}

    th, td {{
        padding:12px;
        border:1px solid white;
        text-align:center;
    }}

    th {{
        background:red;
        color:white;
    }}

    tr:hover {{
        background:#222;
    }}

    .back-btn {{
        display:inline-block;
        margin-top:30px;
        padding:10px 20px;
        background:red;
        color:white;
        text-decoration:none;
        border-radius:5px;
    }}

    .back-btn:hover {{
        background:darkred;
    }}

    </style>

    <h2>📅 Daily Profit Report</h2>

    <table>
    <tr>
    <th>Date</th>
    <th>Total Profit</th>
    </tr>

    {rows}

    </table>

    <br>

    <a class="back-btn" href="/admin_dashboard?view=profit">⬅ Back to Profit</a>
    """
@admin_bp.route('/monthly_profit')
def monthly_profit():

    cursor.execute("""
    SELECT MONTHNAME(Date), SUM(total_amount)
FROM tickets
GROUP BY MONTHNAME(Date)
    """)

    data = cursor.fetchall()

    rows = ""
    for m in data:
        rows += f"<tr><td>{m[0]}</td><td>₹{m[1]}</td></tr>"

    return f"""
    <style>

    body {{
        margin:0;
        font-family: Arial;
        background:black;
        color:white;
        text-align:center;
        padding:40px;
    }}

    h2 {{
        color:red;
        margin-bottom:30px;
    }}

    table {{
        width:60%;
        margin:auto;
        border-collapse: collapse;
    }}

    th, td {{
        padding:12px;
        border:1px solid white;
        text-align:center;
    }}

    th {{
        background:red;
        color:white;
    }}

    tr:hover {{
        background:#222;
    }}

    .back-btn {{
        display:inline-block;
        margin-top:30px;
        padding:10px 20px;
        background:red;
        color:white;
        text-decoration:none;
        border-radius:5px;
    }}

    .back-btn:hover {{
        background:darkred;
    }}

    </style>

    <h2>📆 Monthly Profit Report</h2>

    <table>
    <tr>
    <th>Month</th>
    <th>Total Profit</th>
    </tr>

    {rows}

    </table>

    <br>

    <a class="back-btn" href="/admin_dashboard?view=profit">⬅ Back to Profit</a>
    """
@admin_bp.route('/view_category')
def view_category():
    cursor.execute("SELECT * FROM category")
    data = cursor.fetchall()

    cards = ""
    for c in data:
        cards += f"""
        <div class="card">
            <h3>{c[0].capitalize()}</h3>
            <p>{c[1]} Artifacts</p>
        </div>
        """

    return f"""
    <html>
    <head>
    <style>

    body {{
        margin:0;
        font-family: Arial;
        background: black;
        color: white;
        text-align: center;
    }}

    h2 {{
        color: red;
        margin-top: 30px;
    }}

    .container {{
        display: grid;
         grid-template-columns: repeat(3, 1fr);
        justify-content: center;
        gap: 20px;
        padding: 40px;
    }}

    .card {{
        width: 500px;
        padding: 30px;
        background: #111;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(255,0,0,0.6);
        transition: 0.3s;
    }}

    .card:hover {{
         transform: scale(1.05);
         box-shadow: 0 0 20px red;
     }}

    .card h3 {{
        color: red;
        margin-bottom: 10px;
    }}

    .card p {{
        font-size: 18px;
    }}

    .back-btn {{
        display: inline-block;
        margin: 20px;
        padding: 10px 20px;
        background: red;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
    }}

    .back-btn:hover {{
        background: darkred;
    }}

    </style>
    </head>

    <body>

    <h2>📂 Category Overview</h2>

    <div class="container">
        {cards}
    </div>

    <a class="back-btn" href="/admin_dashboard">⬅ Back</a>

    </body>
    </html>
    """
