from flask_app.config.mysqlconnection import connectToMySQL

class Team:
    @staticmethod
    def add_user_to_team(data):
        query = "INSERT INTO teams VALUES(%(idea_id)s,%(user_id)s);"
        connectToMySQL().query_db(query,data)
