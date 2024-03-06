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
    
    def check_member(self, task, member):
        try:
            self.cursor.execute('''
                SELECT members FROM tasks
                WHERE name = ?
            ''', (task,))
            result = self.cursor.fetchone()
            print(f"result: {result}")

            if result:
                existing_members = result[0].split(',')
                
                if member in existing_members:
                    return False  # Member is already associated with the task

            return True  # Member is not associated with the task
        
        except Exception as e:
            print(e)

    def get_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        tasks = self.cursor.fetchall()
        return tasks
    
    def be_member(self, task:str, member:str):
        # Assuming 'tasks' table has columns 'name' and 'members'

        self.cursor.execute('''
                UPDATE tasks
                SET members = ? || COALESCE(members, '')
                WHERE name = ?
            ''', (member + ',', task))

        self.connection.commit()
        print(f"Member '{member}' added to the tasks {task} successfully!")


    def close_connection(self):
        self.connection.close()
        

# Example usage
if __name__ == "__main__":
    manager = TaskManager()
    test = manager.check_member("Website (BackEnd)","theotime")
    print(test)
    if test:
        manager.be_member(task="Website (BackEnd)",member="theotime")