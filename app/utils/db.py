import pyodbc
import sqlite3
import os
from app.utils.logger import logger

class Database:
    def __init__(self, server=r"localhost", database="school_db"):
        self.db_type = os.getenv("DB_TYPE", "mssql")
        
        if self.db_type == "sqlite":
            # Determine path for sqlite db
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            self.sqlite_db_path = os.path.join(base_dir, "school_db.sqlite")
            self.connection = None
        else:
            self.server = os.getenv("DB_SERVER", server)
            self.database = os.getenv("DB_DATABASE", database)
            self.user = os.getenv("DB_USER")
            self.password = os.getenv("DB_PASSWORD")
            
            if self.user and self.password:
                self.connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={self.server};Database={self.database};UID={self.user};PWD={self.password};"
            else:
                self.connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={self.server};Database={self.database};Trusted_Connection=yes;"
            self.connection = None

    def get_connection(self):
        if self.db_type == "sqlite":
            try:
                if self.connection:
                    try:
                        self.connection.execute("SELECT 1")
                        return self.connection
                    except sqlite3.Error:
                        self.connection = None
                
                self.connection = sqlite3.connect(self.sqlite_db_path, check_same_thread=False)
                # To make sqlite behave somewhat like pyodbc returning tuples
                self.connection.row_factory = sqlite3.Row
                return self.connection
            except sqlite3.Error as e:
                logger.error(f"Error connecting to SQLite Database: {e}")
                return None
        else:
            try:
                # Check if connection exists and is not closed
                if self.connection:
                    try:
                        # Execute a dummy query to test the connection
                        self.connection.cursor().execute("SELECT 1")
                        return self.connection
                    except pyodbc.Error:
                        self.connection = None
                
                self.connection = pyodbc.connect(self.connection_string)
                logger.info("Successfully connected to the MSSQL database")
                return self.connection
            except pyodbc.Error as e:
                logger.error(f"Error connecting to MSSQL Database: {e}")
                return None

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                logger.info("Database connection is closed")
            except Exception:
                pass

# Singleton instance
db = Database()

def get_db_connection():
    return db.get_connection()
