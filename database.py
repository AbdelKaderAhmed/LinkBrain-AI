import sqlite3
from datetime import datetime

def log_performance(tool_name, latency, status, length):
    """
    Performance Logging Engine: Tracks API latency, status codes, and response length
    for the LinkBrain Developer Dashboard.
    """
    try:
        # Connect to the local SQLite database
        conn = sqlite3.connect('linkbrain_admin.db')
        c = conn.cursor()
        
        # Create the logs table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS perf_logs 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      tool_name TEXT, 
                      timestamp DATETIME, 
                      latency REAL, 
                      status TEXT,
                      content_length INTEGER)''')
        
        # Insert the performance metrics into the database
        c.execute("INSERT INTO perf_logs (tool_name, timestamp, latency, status, content_length) VALUES (?, ?, ?, ?, ?)",
                  (tool_name, datetime.now(), latency, status, length))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
    except Exception as e:
        # Fail silently in production, but helpful for debugging during development
        print(f"Database Logging Error: {e}")

def get_recent_logs(limit=10):
    """
    Utility function to fetch the most recent performance logs.
    """
    try:
        conn = sqlite3.connect('linkbrain_admin.db')
        c = conn.cursor()
        c.execute("SELECT * FROM perf_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        logs = c.fetchall()
        conn.close()
        return logs
    except:
        return []