from flask_app.models.stack import Stack
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.config.regex import EMAIL_REGEX,CAP_REGEX,SYM_REGEX,NUM_REGEX
from flask_app import bcrypt

class User:
    def __init__(self,data):
        self.id=data['id']
        self.username=data['username']
        self.email=data['email']
        self.password=data['password']
        self.profile_pic=data['profile_pic']
        self.github_profile=data['github_profile']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.known_stacks= Stack.get_stacks_by_id({'id':data['id']})
    def validate_pw(self,pw):
        return bcrypt.check_password_hash(self.password,pw)
    @classmethod
    def get_by_id(cls,data):
        query = 'SELECT * FROM users WHERE id=%(id)s;'
        results = connectToMySQL().query_db(query,data)
        return cls(results[0]) if len(results) > 0 else None
    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email=%(email)s;'
        results = connectToMySQL().query_db(query,data)
        return cls(results[0]) if len(results) > 0 else None
    @classmethod
    def get_by_username(cls,data):
        query = 'SELECT * FROM users WHERE username=%(username)s;'
        results = connectToMySQL().query_db(query,data)
        return cls(results[0]) if len(results) > 0 else None
    @staticmethod
    def valid_reg(data):
        if len(data['username']) < 3:
            return False
        if len(data['username']) > 45:
            return False
        if(User.get_by_username(data)):
            return False
        if not EMAIL_REGEX.match(data['email']):
            return False
        if len(data['email']) > 100:
            return False
        if(User.get_by_email(data)):
            return False
        if len(data['password']) < 8:
            return False
        pw=data['password']
        if not (CAP_REGEX.search(pw) and NUM_REGEX.search(pw) and SYM_REGEX.search(pw)):
            return False
        if not pw == data['confirm_password']:
            return False
        return True
    @staticmethod
    def encrypt_password(data):
        hash=bcrypt.generate_password_hash(data['password'])
        print (hash)
        newData={
            'email':data['email'],
            'username':data['username'],
            'password':hash
        }
        return newData
    @classmethod
    def save(cls,data):
        query="INSERT INTO users(email, username, password) VALUES(%(email)s, %(username)s, %(password)s);"
        return connectToMySQL().query_db(query,User.encrypt_password(data))