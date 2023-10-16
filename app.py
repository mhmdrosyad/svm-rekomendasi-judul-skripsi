import numpy as np
from flask import Flask, render_template, request, url_for, redirect, session, flash
import pymysql.cursors
import bcrypt
from model_svm import predict_with_svm, X_train, Y_train, a, b

app = Flask(__name__)

app.secret_key = 'svmprogram'

conn = cursor = None

def openDatabase():
    global conn, cursor
    conn = pymysql.connect(host="localhost",user="root",password="",database="db_svm_program")
    cursor = conn.cursor()

def closeDatabase():
    global conn, cursor
    cursor.close()
    conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        openDatabase()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        closeDatabase()

        if user is not None and len(user) > 0:
            if bcrypt.checkpw(password, user[3].encode('utf-8')):
                session['username'] = user[1]
                session['email'] = user[2]
                return redirect(url_for('predict'))
            else:
                flash("Username and Password do not match")
                return redirect(url_for('login'))
        else:
            flash("User not found")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        openDatabase()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hash_password))
        conn.commit()
        closeDatabase()
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route("/", methods=['GET', 'POST'])
def predict():
    if 'username' in session:
        if request.method == 'POST':
            SPK = int(request.form.get('SPK', 0))
            DATA_MINING = int(request.form.get('DATA_MINING', 0))
            PEMROG = int(request.form.get('PEMROG', 0))
            MACHINE = int(request.form.get('MACHINE', 0))

            data_nilai = np.array([[SPK, DATA_MINING, PEMROG, MACHINE]])
            prediksi_user = predict_with_svm(X_train, Y_train, data_nilai, a, b)
            kategori = {1: 'DATA MINING', -1: 'RPL'}
            hasil_prediksi = kategori.get(prediksi_user[0])
            print(hasil_prediksi)
            return render_template("index.html", data=hasil_prediksi)
        return render_template("index.html")
    return render_template("login.html")

@app.route('/check-session')
def check_session():
    if 'username' in session:
        return f'Sesi dengan kunci "username" sudah ada: {session["username"]}'
    else:
        return 'Sesi belum ada.'

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return 'Anda telah logout.'

if __name__ == '__main__':
    app.run(debug=True)
