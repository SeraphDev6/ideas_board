from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Team:
    @staticmethod
    def get_team_by_id(data):
        query = "SELECT * FROM teams JOIN users ON teams.user_id = users.id WHERE teams.idea_id = %(id)s;"
        from_db=connectToMySQL().query_db(query,data)
        arr=[]
        for user in from_db:
            arr.append(User(user))
        return arr