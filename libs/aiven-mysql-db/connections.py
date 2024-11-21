
import pymysql


user=""
password=""




def test(user,password):
        
    timeout = 10
    connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="defaultdb",
    host="mysql-3a760b11-marktine-b6f6.c.aivencloud.com",
    password=password,
    read_timeout=timeout,
    port=15559,
    user=user,
    write_timeout=timeout,)

    try:    

        cursor = connection.cursor()

    except:
        print("Some Error occured. Could not connect to database ")
        return False

        
    else:
        print("Connected to Database")
        # cursor.execute("CREATE TABLE mytest (id INTEGER PRIMARY KEY)")
        # cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
        cursor.execute("SELECT * FROM mytest")
        print(cursor.fetchall())
        return True 

test(user,password)



