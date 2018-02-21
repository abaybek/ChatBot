import sqlite3
import datetime

class DBHelper:
    def __init__(self, dbname="./data/db.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt = """CREATE TABLE IF NOT EXISTS items (id integer primary key, 
                                               chat_id integer, 
                                           description text, 
                                                  data text)"""
        self.conn.execute(stmt) 
        self.conn.commit()

    def add_item(self, item_text, chat_id):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stmt = "INSERT INTO items (chat_id, description, data) VALUES (?, ?, ?)"
        args = (chat_id, item_text, date, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, chat_id):
        stmt = "DELETE FROM items WHERE description = (?) and chat_id = (?)"
        args = (item_text, chat_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, chat_id):
        stmt = "SELECT description FROM items where chat_id = (?)"
        args = (chat_id, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_last_element(self, chat_id):
        stmt = """
            SELECT description
            FROM    items
            WHERE   id = (SELECT MAX(id)  FROM items) and chat_id = (?);
        """
        args = (chat_id, )
        result = [x[0] for x in self.conn.execute(stmt, args)]
        results = "".join(result)
        return results