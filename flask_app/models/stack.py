from flask_app.config.mysqlconnection import connectToMySQL

class Stack:
    @staticmethod
    def get_by_id(data):
        query = 'SELECT * FROM stacks WHERE id=%(id)s;'
        results = connectToMySQL().query_db(query,data)
        return results[0] if len(results)>0 else 0
    @staticmethod
    def get_stacks_by_id(data):
        query="SELECT stack_id,name FROM known_stacks JOIN stacks ON known_stacks.stack_id = stacks.id WHERE known_stacks.user_id = %(id)s;"
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
    def update_stacks(user_id,data):
        connectToMySQL().query_db(f"DELETE FROM known_stacks WHERE user_id={user_id}")
        for i in range(1,len(Stack.get_all())+1):
            if str(i) in data:
                connectToMySQL().query_db(f"INSERT INTO known_stacks VALUES({user_id},{i});")
