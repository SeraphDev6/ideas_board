from flask_app.models.team import Team
from flask_app.models.stack import Stack
from flask_app.config.mysqlconnection import connectToMySQL

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
        self.team = Team.get_team_by_id({'id':data['id']})
        
    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM ideas WHERE id=%(id)s;'
        results = connectToMySQL().query_db(query,data)
        return cls(results[0]) if len(results) > 0 else None
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM ideas;'
        from_db = connectToMySQL().query_db(query)
        arr=[]
        for idea in from_db:
            arr.append(cls(idea))
        return arr