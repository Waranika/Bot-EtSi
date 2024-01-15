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
    
    def be_member(self, tasks:list, member:str):
        # Assuming 'tasks' table has columns 'name' and 'members'
        for task in tasks:
            self.cursor.execute(f'''
                UPDATE tasks
                SET members = COALESCE(members || ',', '') || ?
                WHERE name = ?
            ''', (member, task))

        self.connection.commit()
        print(f"Member '{member}' added to the tasks {tasks} successfully!")


    def close_connection(self):
        self.connection.close()
        

# Example usage
if __name__ == "__main__":
    manager = TaskManager()

    # Assuming you have a task called 'example_task' and a list of members
    task_name = 'Evaluation'
    # Assuming you have a list of tasks and a single member
    tasks_list = ['task1', 'task2', 'task3']
    member = 'toto'

    manager.be_member(tasks_list, member)