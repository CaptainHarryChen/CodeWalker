import sqlite3


def DB_pwd():
    with sqlite3.connect("users.db") as usersDB:
        usersDB.execute('''create table if not exists users
        (name primary key not null,
        password varchar(16) not null)
        ''')
        
        '''
        usersDB.execute(
            "insert into users (name,password) values('CaptainChen','12345')")
        usersDB.execute(
            "insert into users (name,password) values('Zhongli','12345')")
        usersDB.execute(
            "insert into users (name,password) values('Xingqiu','12345')")
        usersDB.execute(
            "insert into users (name,password) values('Xiangling','12345')")
        usersDB.execute(
            "insert into users (name,password) values('Beidou','12345')")
        usersDB.execute(
            "insert into users (name,password) values('Hu Tao','12345')")
        '''

        usersDB.commit()


if __name__ == "__main__":
    DB_pwd()
