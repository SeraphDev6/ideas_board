from flask import render_template, redirect, request, session
from flask_app.models.idea import Idea
from flask_app.models.user import User
from flask_app import app

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html',user=User.get_by_id({'id':session['user']}),ideas=Idea.get_all())
    return render_template('index.html',ideas=Idea.get_all())