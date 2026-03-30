from flask import Flask, render_template_string
from routes.user_routes import user_bp
from routes.employee_routes import employee_bp
from routes.artifact_routes import artifact_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.secret_key = "secret123"

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(artifact_bp)
app.register_blueprint(admin_bp)


# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template_string('''
    <style>
     body {
        margin: 0;
        font-family: Arial;
        background: black;
        color: white;
    }

    .hero {
        height: 100vh;
        background: url('https://images.unsplash.com/photo-1549880338-65ddcdfd017b') center/cover;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        background-blend-mode: overlay;
        background-color: rgba(0,0,0,0.7);
    }

    h1 {
        font-size: 50px;
        color: red;
    }

    p {
        font-size: 20px;
        margin-bottom: 30px;
    }

    a {
        padding: 12px 25px;
        margin: 10px;
        background: red;
        color: white;
        text-decoration: none;
        border-radius: 5px;
    }

    a:hover {
        background: darkred;
    }
    </style>

    <div class="hero">
        <h1>ART FLOW</h1>
        <p>Explore Creativity & Timeless Art</p>

        <a href="/login/user">User Login/sign up</a>
        <a href="/login/admin">Admin Login</a>
    </div>
    ''')


if __name__ == "__main__":
    app.run(debug=True)