from flask import Flask, render_template, request, redirect, session, url_for, flash
from PIL import Image, ImageDraw, ImageFont
import random
import string
import sqlite3
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure key

def init_db():
    """Initialize the database and create a users table if not exists."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT UNIQUE,
                 email TEXT UNIQUE,
                 password TEXT,
                 dob TEXT,
                 mobile TEXT)''')
    conn.commit()
    conn.close()

# Function to generate CAPTCHA text
def generate_captcha_text(length=6):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Function to generate a CAPTCHA image
def generate_captcha_image(captcha_text):
    width, height = 160, 60
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()

    x_start = 10
    y_positions = [15, 20, 25, 30]
    for char in captcha_text:
        x_start += random.randint(15, 25)
        y_position = random.choice(y_positions)
        draw.text((x_start, y_position), char, font=font, fill=(0, 0, 0))

    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    return base64.b64encode(image_bytes.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_captcha = request.form['captcha']

        if user_captcha != session.get('captcha_text'):
            flash('Invalid CAPTCHA. Try again.', 'danger')
            return redirect(url_for('login'))

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE name = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            flash('Login Successful!', 'success')
            return render_template('welcome.html', user=username)
        else:
            flash('Invalid username or password.', 'danger')

    captcha_text = generate_captcha_text()
    session['captcha_text'] = captcha_text
    captcha_image_base64 = generate_captcha_image(captcha_text)
    return render_template('login.html', captcha_image=captcha_image_base64)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        mobile = request.form['mobile']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password, dob, mobile) VALUES (?, ?, ?, ?, ?)",
                      (name, email, password, dob, mobile))
            conn.commit()
            flash('Registration Successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('User already exists or email is taken.', 'danger')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]
    values = [random.randint(1000, 5000) for _ in labels]
    deposit_vs_withdrawal = [random.randint(5000, 10000), random.randint(1000, 5000)]
    return render_template("dashboard.html", labels=labels, values=values, deposit_vs_withdrawal=deposit_vs_withdrawal)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
