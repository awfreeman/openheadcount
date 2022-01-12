import bcrypt
class usermgmt:
    def authenticate(uname:str, passwd:str):
        users = open('conf/users', mode='r')
        users.close()
    def adduser(uname:str, passwd:str, permissions:str):
        users = open('conf/users', mode='r+')
        users.close()
    def rmuser(uname:str, passwd:str):
        users = open('conf/users', mode='r+')
        users.close()