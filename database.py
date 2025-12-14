import sqlite3

class DatabaseManager:
    def __init__(self, db_name="lockfolder.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT,
                display_name TEXT,
                password_hash TEXT,
                lock_date TEXT,
                status TEXT
            )
        """)
        self.conn.commit()

    def is_setup_done(self):
        self.cursor.execute("SELECT value FROM config WHERE key='master_password'")
        return self.cursor.fetchone() is not None

    def set_master_password(self, password_hash):
        self.cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES ('master_password', ?)", (password_hash,))
        self.conn.commit()

    def get_master_password(self):
        self.cursor.execute("SELECT value FROM config WHERE key='master_password'")
        result = self.cursor.fetchone()
        return result[0] if result else None 
    
    def insert_folder(self, path, display_name, password_hash):
        import datetime 
        date = datetime.datetime.now().strftime("%b %d, %Y") 
        self.cursor.execute(""" 
            INSERT INTO folders (path, display_name, password_hash, lock_date, status)
            VALUES (?, ?, ?, ?, 'locked')
        """, (path, display_name, password_hash, date))
        self.conn.commit() 

    def get_all_folders(self):
        self.cursor.execute("SELECT id, path, display_name, lock_date FROM folders WHERE status='locked'")
        return self.cursor.fetchall() 
    
    def delete_folder(self, folder_id):
        self.cursor.execute("DELETE FROM folders WHERE id=?", (folder_id,))
        self.conn.commit() 
    
    def get_folder_password(self, folder_id):
        self.cursor.execute("SELECT password_hash FROM folders WHERE id=?", (folder_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None