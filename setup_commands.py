import sqlite3

# Connect to the database
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

# Insert common web applications
web_commands = [
    ("youtube", "https://www.youtube.com"),
    ("facebook", "https://www.facebook.com"),
    ("instagram", "https://www.instagram.com"),
    ("twitter", "https://www.twitter.com"),
    ("gmail", "https://mail.google.com"),
    ("google", "https://www.google.com"),
    ("github", "https://www.github.com"),
    ("netflix", "https://www.netflix.com"),
    ("amazon", "https://www.amazon.com"),
    ("whatsapp", "https://web.whatsapp.com"),
    ("reddit", "https://www.reddit.com"),
    ("linkedin", "https://www.linkedin.com"),
    ("wikipedia", "https://www.wikipedia.org"),
    ("stackoverflow", "https://stackoverflow.com"),
    ("spotify", "https://open.spotify.com")
]

# Insert common system applications (update paths as needed for your system)
sys_commands = [
    ("notepad", "C:\\Windows\\System32\\notepad.exe"),
    ("calculator", "C:\\Windows\\System32\\calc.exe"),
    ("paint", "C:\\Windows\\System32\\mspaint.exe"),
    ("cmd", "C:\\Windows\\System32\\cmd.exe"),
    ("powershell", "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"),
    ("explorer", "C:\\Windows\\explorer.exe"),
    ("control panel", "C:\\Windows\\System32\\control.exe"),
    ("task manager", "C:\\Windows\\System32\\taskmgr.exe"),
    ("registry editor", "C:\\Windows\\regedit.exe"),
    ("system configuration", "C:\\Windows\\System32\\msconfig.exe")
]

try:
    # Clear existing data
    cursor.execute("DELETE FROM web_command")
    cursor.execute("DELETE FROM sys_command")
    
    # Insert web commands
    for name, url in web_commands:
        cursor.execute("INSERT INTO web_command VALUES (null, ?, ?)", (name, url))
    
    # Insert system commands
    for name, path in sys_commands:
        cursor.execute("INSERT INTO sys_command VALUES (null, ?, ?)", (name, path))
    
    conn.commit()
    print("Database populated successfully!")
    
    # Verify the data
    cursor.execute("SELECT COUNT(*) FROM web_command")
    web_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM sys_command")
    sys_count = cursor.fetchone()[0]
    
    print(f"Added {web_count} web commands and {sys_count} system commands")
    
    # Show some examples
    print("\nSample web commands:")
    cursor.execute("SELECT name, url FROM web_command LIMIT 5")
    for row in cursor.fetchall():
        print(f"  {row[0]} -> {row[1]}")
    
    print("\nSample system commands:")
    cursor.execute("SELECT name, path FROM sys_command LIMIT 5")
    for row in cursor.fetchall():
        print(f"  {row[0]} -> {row[1]}")

except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()