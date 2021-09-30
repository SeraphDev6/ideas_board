from os import stat
from flask_app.config.mysqlconnection import connectToMySQL

class Stack:
    @staticmethod
    def get_stacks_by_id(data):
        query="SELECT name FROM known_stacks JOIN stacks ON known_stacks.stack_id = stacks.id WHERE known_stacks.user_id = %(id)s;"
        from_db=connectToMySQL().query_db(query,data)
        arr=[]
        for stack in from_db:
            arr.append(stack)
        return arr

    @staticmethod
    def get_all():
        query = 'SELECT * FROM stacks;'
        from_db = connectToMySQL().query_db(query)
        arr=[]
        for stack in from_db:
            arr.append(stack)
        return arr

    @staticmethod
    def get_by_id(data):
        query = 'SELECT * FROM table WHERE id=%(id)s;'
        results = connectToMySQL().query_db(query,data)
        return results[0] if len(results) > 0 else None