from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # ← change to something random before deploying

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['company_id'] = user['company_id']
            return redirect(url_for('view_hcps'))
        else:
            return render_template('login.html', error='Invalid credentials.')
    return render_template('login.html')

@app.route('/hcps')
def view_hcps():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    all_hcps = conn.execute('SELECT * FROM HCP').fetchall()
    conn.close()
    company_id = session['company_id']
    role = session['role']
    if role == 'admin':
        editable = all_hcps
        readonly = []
    elif role == 'nurse':
        editable = [hcp for hcp in all_hcps if hcp['company_id'] == company_id]
        readonly = [hcp for hcp in all_hcps if hcp['company_id'] != company_id]
        # NOTE: I'm not sure if I want to remove this feature in the future.
    else:
        editable = []
        readonly = all_hcps
    return render_template('hcp_list.html', editable=editable, readonly=readonly)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
