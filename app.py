from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'prithi'

# MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'client_db'

mysql = MySQL(app)

# Route for Login Page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['username'] = username
            return redirect(url_for('client'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('home.html')

# Route for Client Management Page
@app.route('/client', methods=['GET', 'POST'])
def client():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clients")
        clients = cur.fetchall()
        cur.close()
        return render_template('client.html', clients=clients)
    return redirect(url_for('login'))

# Add a new client
@app.route('/add_client', methods=['POST'])
def add_client():
    if 'username' in session and request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        company = request.form['company']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clients (name, email, company) VALUES (%s, %s, %s)", (name, email, company))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('client'))
    return redirect(url_for('login'))

# Edit a client
@app.route('/edit_client/<int:id>', methods=['POST'])
def edit_client(id):
    if 'username' in session and request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        company = request.form['company']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE clients SET name=%s, email=%s, company=%s WHERE id=%s", (name, email, company, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('client'))
    return redirect(url_for('login'))

# Delete a client
@app.route('/delete_client/<int:id>', methods=['GET'])
def delete_client(id):
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM clients WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('client'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
