import bcrypt
import pandas
import base64
class usermgmt:
    def authenticate(uname:str, passwd:str):
        logindf = pandas.read_csv('conf/login.csv')
        logindf = logindf.query(f'username == @uname')
        if len(logindf.index)==0:
            return "No such user"
        salt=logindf.iloc[0].salt
        pwhash = str(bcrypt.hashpw(bytes(passwd, 'utf-8'), bytes(salt, 'utf-8')), 'utf-8')
        spwhash = logindf.iloc[0].hash
        if pwhash == spwhash:
            return True
        else:
            return False
    def adduser(uname:str, passwd:str):
        if len(passwd)>72:
            return False, "Passwords must be under 72 characters long"
        if ',' in uname:
            return False, "No commas allowed in username"
        logindf = pandas.read_csv('conf/login.csv')
        if logindf.query(f'username == @uname').empty == False:
            return "user already exists"
        salt = bcrypt.gensalt()
        pwhash = bcrypt.hashpw(bytes(passwd, 'utf-8'), salt)
        pwhash = str(pwhash, 'utf-8')
        salt = str(salt, 'utf-8')
        logindf.loc[len(logindf.index)] = [uname, pwhash, salt]
        logindf.to_csv('conf/login.csv', index=False)
        return "user successfuly added"
    def rmuser(uname:str, passwd:str):
        pass