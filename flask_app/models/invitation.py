from flask_app.config.mysqlconnection import connectToMySQL

class Invitation:
    @staticmethod
    def delete(data):
        query = "DELETE FROM invitations WHERE team_id=%(idea_id)s AND user_id=%(user_id)s;"
        return connectToMySQL().query_db(query,data)

    @staticmethod
    def get_by_ids(data):
        query = "SELECT * FROM invitations WHERE team_id=%(idea_id)s AND user_id=%(user_id)s;"
        return connectToMySQL().query_db(query,data)

    @staticmethod
    def save(data,init=1):
        query = f"INSERT INTO invitations VALUES(%(idea_id)s,%(user_id)s,{init},%(message)s);"
        connectToMySQL().query_db(query,data)