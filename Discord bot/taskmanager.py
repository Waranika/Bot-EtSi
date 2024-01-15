import sqlite3

class TaskManager:
    def __init__(self, db_name=r"Discord bot\translator_afro.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def add_task(self, name, description, members, status):
        self.cursor.execute('''
            INSERT INTO tasks (name, description, members, status)
            VALUES (?, ?, ?, ?)
        ''', (name, description, members, status))
        self.connection.commit()

    def get_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        tasks = self.cursor.fetchall()
        return tasks

    def close_connection(self):
        self.connection.close()