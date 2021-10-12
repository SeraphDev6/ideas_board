from os import stat
from flask.scaffold import F
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.stack import Stack
# from flask_app.models.user import User
class Idea:
    def __init__(self,data):
        self.id=data['id']
        self.title=data['title']
        self.description=data['description']
        self.explanation=data['explanation']
        self.github_url=data['github_url']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.stack= Stack.get_by_id({'id':data['stack_id']})
        self.team = Idea.get_team_by_idea({'id':data['id']})
        self.eligable_members =Idea.get_eligable_members({'stack_id':data['stack_id'],'id':data['id']})
        self.requests = Idea.get_requests({'id':data['id']})
        self.status_updates = Idea.get_updates({'id':data['id']})

    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM ideas WHERE id=%(id)s;'
        results = connectToMySQL().query_db(query,data)
        return cls(results[0]) if results else None

    @classmethod
    def get_by_title(cls,data):
        query = 'SELECT * FROM ideas WHERE title=%(title)s;'
        results = connectToMySQL().query_db(query,data)
        return cls(results[0]) if len(results) > 0 else None

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM ideas ORDER BY created_at DESC;'
        from_db = connectToMySQL().query_db(query)
        arr=[]
        for idea in from_db:
            arr.append(cls(idea))
        return arr

    @staticmethod
    def get_team_by_idea(data):
        query = "SELECT * FROM teams JOIN users ON teams.user_id = users.id WHERE teams.idea_id = %(id)s;"
        from_db=connectToMySQL().query_db(query,data)
        # arr=[]
        # for user in from_db:
        #     arr.append(User(user))
        # return arr
        return from_db

    @staticmethod
    def get_eligable_members(data,):
        query = "SELECT id,username from users JOIN known_stacks ON users.id = known_stacks.user_id WHERE users.id NOT IN (SELECT users.id FROM teams JOIN users ON teams.user_id = users.id WHERE teams.idea_id = %(id)s) AND users.id NOT IN (SELECT users.id FROM invitations JOIN users ON users.id = invitations.user_id WHERE invitations.team_id = %(id)s) AND known_stacks.stack_id = %(stack_id)s;"
        results = connectToMySQL().query_db(query,data)
        return results
        # if not ids_only:
        #     return results
        # arr = []
        # for result in results:
        #     arr.append(result['id'])
        # return arr
        
    @staticmethod
    def valid_idea(data):
        if len(data['title'])<3:
            return False
        if Idea.get_by_title(data):
            return False
        if len(data['description'])<5:
            return False
        if len(data['explanation'])<5:
            return False
        return True

    @staticmethod
    def save(data):
        query = "INSERT INTO ideas(title, description, explanation) VALUES(%(title)s, %(description)s, %(explanation)s);"
        return connectToMySQL().query_db(query,data)

    @staticmethod
    def assign_stack(data):
        query = "UPDATE ideas SET stack_id = %(stack_id)s WHERE id = %(idea_id)s;"
        return connectToMySQL().query_db(query,data)

    @staticmethod
    def add_github(data):
        query = "UPDATE ideas SET github_url = %(url)s WHERE id = %(idea_id)s;"
        return connectToMySQL().query_db(query,data)

    @staticmethod
    def get_requests(data):
        query = "SELECT * FROM invitations JOIN users ON users.id = invitations.user_id WHERE invitations.team_id = %(id)s AND user_initiated = 1;"
        return connectToMySQL().query_db(query,data)

    @staticmethod
    def get_updates(data):
        query = "SELECT * FROM status_updates JOIN users ON status_updates.user_id = users.id WHERE idea_id = %(id)s ORDER BY status_updates.created_at DESC;"
        return connectToMySQL().query_db(query,data)

    @staticmethod
    def save_update(data):
        query= "INSERT INTO status_updates(user_id , idea_id , text) VALUES( %(user_id)s , %(idea_id)s , %(text)s );"
        connectToMySQL().query_db(query,data)