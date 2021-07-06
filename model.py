import os
all_user = []

class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        all_user.append(self.username)

    def getCurrentUser(self):
        return self.username

def removeImages(current_image=None):
    for imagename in os.listdir("./static/images/"):
        if imagename == 'mushroom_wallpaper.jpg' or imagename == current_image:
            pass
        else:
            os.remove("./static/images/"+imagename)

def listOfAllLoginUsers():
        return all_user

def checkUsernameAndPassword(username,password):
    import sqlite3
    connection = sqlite3.connect('./static/database/mushroom.db', check_same_thread=False)

    my_cursor = connection.cursor()

    my_cursor.execute(""" SELECT username, password FROM user_info WHERE username='{user}' 
    AND password='{passw}';""".format(user=username, passw=password))

    bool_user = False
    if my_cursor.fetchone():
        bool_user = True
    
    connection.commit()
    my_cursor.close()
    connection.close()

    return bool_user

def checkUserExist(username):
    import sqlite3
    connection = sqlite3.connect('./static/database/mushroom.db', check_same_thread=False)

    my_cursor = connection.cursor()

    my_cursor.execute(""" SELECT username FROM user_info WHERE username='{user}';""".format(user=username))

    bool_user = False
    if my_cursor.fetchone():
        bool_user = True

    connection.commit()
    my_cursor.close()
    connection.close()

    return bool_user

def insertData(username,password):
    if checkUserExist(username) == True:
        return "Username already exist. Choose different username."
    else:
        import sqlite3
        connection = sqlite3.connect('./static/database/mushroom.db', check_same_thread=False)

        my_cursor = connection.cursor()

        my_cursor.execute(""" INSERT INTO user_info(username,
	    password) VALUES ('{user}','{passw}');""".format(user=username, passw=password))

        connection.commit()
        my_cursor.close()
        connection.close()
        return username+", you have registered successfully!! Please Login."