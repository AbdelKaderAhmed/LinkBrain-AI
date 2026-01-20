import sqlite3
from datetime import datetime

def log_performance(tool_name, latency, status, length):
    try:
        conn = sqlite3.connect('linkbrain_admin.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS perf_logs 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      tool_name TEXT, 
                      timestamp DATETIME, 
                      latency REAL, 
                      status TEXT,
                      content_length INTEGER)''')
        
        c.execute("INSERT INTO perf_logs (tool_name, timestamp, latency, status, content_length) VALUES (?, ?, ?, ?, ?)",
                  (tool_name, datetime.now(), latency, status, length))
        conn.commit()
        conn.close()
    except:
        pass #