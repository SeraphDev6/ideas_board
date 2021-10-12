from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.stack import Stack
from flask_app.models.idea import Idea
from flask_app.models.team import Team
from flask_app.config.regex import GITHUB_REGEX
from flask_app import app

@app.route('/ideas/new/')
def new_idea():
    if not 'user' in session:
        return redirect('/')
    return render_template('idea_form.html')

@app.route('/ideas/create', methods=['POST'])
def create_idea():
    if Idea.valid_idea(request.form):
        idea = Idea.save(request.form)
        if int(request.form['include_user']) > 0 :
            Team.add_user_to_team(({'idea_id':idea,'user_id':session['user']}))
            Idea.assign_stack({'idea_id':idea,'stack_id':request.form['stack_id']})
        return redirect(f"/ideas/{idea}")
    return redirect('/ideas/new')

@app.route('/ideas/<int:id>/')
def view_idea(id):
    if 'user' in session:
        return render_template('view_idea.html',idea=Idea.get_by_id({'id':id}),user=User.get_by_id({'id':session['user']}))
    return render_template('view_idea.html',idea=Idea.get_by_id({'id':id}))
@app.route('/ideas/claim/<int:id>/')
def claim_idea(id):
    if not 'user' in session:
        return redirect('/')
    user = User.get_by_id({'id':session['user']})
    if len(user.known_stacks)<1:
        return redirect('/')
    idea = Idea.get_by_id({'id':id})
    return render_template('claim_idea.html',idea=idea,stacks=user.known_stacks)

@app.route('/ideas/claim_idea', methods=['POST'])
def claimed_idea():
    idea=Idea.get_by_title(request.form)
    Team.add_user_to_team(({'idea_id':idea.id,'user_id':session['user']}))
    Idea.assign_stack({'idea_id':idea.id,'stack_id':request.form['stack_id']})
    return redirect(f"/ideas/{idea.id}")

#AJAX
@app.route('/ajax/idea/title', methods=['POST'])
def valid_title():
    if len(request.form['title']) < 3:
        return render_template('partials/title.html',reason="short")
    if Idea.get_by_title(request.form):
        return render_template('partials/title.html',reason="unique")
    return ""

@app.route('/ajax/idea/description', methods=['POST'])
def valid_desc():
    if len(request.form['description']) < 5:
        return render_template('partials/description.html')
    return ""

@app.route('/ajax/idea/explanation', methods=['POST'])
def valid_expla():
    if len(request.form['explanation']) < 5:
        return render_template('partials/explanation.html')
    return ""

@app.route('/ajax/idea/include_user', methods=['POST'])
def include_user():
    if int(request.form['include_user']) > 0:
        return render_template('partials/secondary_idea_form.html',stacks=Stack.get_stacks_by_id({'id':session['user']}))
    return render_template('partials/secondary_idea_form.html')

@app.route('/ajax/idea/github_check', methods=['POST'])
def check_github():
    if GITHUB_REGEX.search(request.form['github_url']):
        return ""
    return render_template('partials/github.html')

@app.route('/ajax/idea/github_submit', methods=['POST'])
def submit_github():
    if GITHUB_REGEX.search(request.form['github_url']):
        Idea.add_github({'url':request.form['github_url'],'idea_id':request.form['idea']})
        return render_template('partials/final_github.html', url=request.form['github_url'])
    return render_template('partials/final_github.html')

@app.route('/ajax/idea/check_update', methods=['POST'])
def check_update():
    if len(request.form['update'])<3:
        return render_template('partials/short_update.html')
    return ""

@app.route('/ajax/idea/add_update', methods=['POST'])
def add_update():
    if 'user' in session and len(request.form['update'])>3:
        data={
            'idea_id':request.form['idea_id'],
            'user_id':session['user'],
            'text':request.form['update']
        }
        print(data)
        Idea.save_update(data)
    idea=Idea.get_by_id({'id':data['idea_id']})
    print(idea)
    return render_template('partials/update_div.html',idea=idea)
