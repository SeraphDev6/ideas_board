from flask import render_template, redirect, request, session
from flask.app import Flask
from flask_app import app
from flask_app.models.user import User
from flask_app.config.regex import EMAIL_REGEX,CAP_REGEX,SYM_REGEX,NUM_REGEX

@app.route('/register/')
def register():
    if 'user' in session:
        return redirect('/')
    return render_template('register.html')

@app.route('/login/')
def login():
    if 'user' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/new', methods=['POST'])
def finish_reg():
    if User.valid_reg(request.form):
        session['user']=User.save(request.form)
        return redirect('/')



@app.route('/ajax/user/username', methods=['POST'])
def valid_username():
    if len(request.form['username']) < 3:
        return render_template('partials/username.html',reason='short')
    if len(request.form['username']) > 45:
        return render_template('partials/username.html',reason='long')
    if(User.get_by_username(request.form)):
        return render_template('partials/username.html',reason='taken')
    return ""

@app.route('/ajax/user/email', methods=['POST'])
def valid_email():
    if not EMAIL_REGEX.match(request.form['email']):
        return render_template('partials/email.html',reason='not_email')
    if len(request.form['email']) > 100:
        return render_template('partials/email.html',reason='long')
    if(User.get_by_email(request.form)):
        return render_template('partials/email.html',reason='taken')
    return ""

@app.route('/ajax/user/password', methods=['POST'])
def valid_password():
    if len(request.form['password']) < 8:
        return render_template('partials/password.html',reason='short')
    pw=request.form['password']
    if not (CAP_REGEX.search(pw) and NUM_REGEX.search(pw) and SYM_REGEX.search(pw)):
        return render_template('partials/password.html',reason='not_valid')
    return ""

@app.route('/ajax/user/confirm_password', methods=['POST'])
def valid_confirm_password():
    if not request.form['confirm_password'] == request.form['password']:
        return render_template('partials/confirm_password.html',reason='not_valid')
    return ""

@app.route('/ajax/user/login', methods=['POST'])
def valid_login():
    user = User.get_by_email(request.form)
    if not user:
        print('email')
        return render_template('partials/login.html')
    if not user.validate_pw(request.form['password']):
        print('pw')
        return render_template('partials/login.html')
    session['user']=user.id
    return render_template('partials/login.html',valid=True)
