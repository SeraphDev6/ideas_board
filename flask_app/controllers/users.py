from os import error
from flask import render_template, redirect, request, session
import flask
from flask.app import Flask
from flask_app import app
from flask_app.models.stack import Stack
from flask_app.models.user import User
from flask_app.models.idea import Idea
from flask_app.models.team import Team
from flask_app.models.invitation import Invitation
from flask_app.config.regex import EMAIL_REGEX,CAP_REGEX,SYM_REGEX,NUM_REGEX

@app.route('/register/')
def register():
    if 'user' in session:
        return redirect('/')
    return render_template('register.html',stacks=Stack.get_all())

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
        print(request.form)
        Stack.update_stacks(session['user'],request.form)
        return redirect('/')

@app.route('/users/<int:id>/')
def view_user(id):
    user=User.get_by_id({'id':id});
    return render_template('view_user.html',user=user)

@app.route('/users/edit/<int:id>/')
def edit_user(id):
    user=User.get_by_id({'id':id});
    if not ('user' in session and session['user']==id):
        return render_template('view_user.html',user=user)
    return render_template('edit_user.html',user=user,stacks=Stack.get_all())

@app.route('/users/update/<int:id>', methods=['POST'])
def update_user(id):
    if 'user' in session and session['user'] == id:
        if User.valid_update(id,request.form):
            User.update(id,request.form)
            Stack.update_stacks(id,request.form)
    return redirect(f"/users/{id}")

# AJAX
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
        return render_template('partials/login.html')
    if not user.validate_pw(request.form['password']):
        return render_template('partials/login.html')
    session['user']=user.id
    return render_template('partials/login.html',valid=True)

@app.route('/ajax/users/manage_request', methods=['POST'])
def manage_request():
    user = User.get_by_id({'id':request.form['user_id']})
    idea = Idea.get_by_id({'id':request.form['idea_id']})
    if int(request.form['approved']) > 0:
        for stack in user.known_stacks:
            if stack['name'] == idea.stack['name']:
                Team.add_user_to_team(request.form)
                Invitation.delete(request.form)
                return render_template("partials/request_response.html",approved=True,user=user,idea=idea)
        Invitation.delete(request.form)
        return render_template("partials/request_response.html",approved=False,error='invalid',user=user,idea=idea)
    Invitation.delete(request.form)
    return render_template("partials/request_response.html",approved=False,error='denied',user=user,idea=idea)

@app.route('/ajax/users/update_team', methods=['POST'])
def update_team():
    idea=Idea.get_by_id({'id':request.form['idea_id']})
    return render_template('partials/team.html',idea=idea)

@app.route('/ajax/users/add_request', methods=['POST'])
def add_request():
    if not Invitation.get_by_ids(request.form):
        Invitation.save(request.form)
        return render_template('partials/request_button.html')
    return render_template('partials/request_button.html')