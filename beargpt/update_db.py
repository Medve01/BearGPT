import os
import sqlite3
from assistant import config

# Set up the database filename and SQL directory
db_file = config.config('chat_history_db')
sql_dir = './SQL'

print("   ___                  ___   ___  _____ ")
print("  / __\ ___  __ _ _ __ / _ \ / _ \/__   \\")
print(" /__\/// _ \/ _` | '__/ /_\// /_)/  / /\/")
print("/ \/  \  __/ (_| | | / /_\\\\/ ___/  / /   ")
print("\_____/\___|\__,_|_| \____/\/      \/    ")
print("")                                      
print("")                                      
print("Welcome to the database update tool")
print("==========================================")
print("This tool will update your BearGPT database to the latest version.")
print("If you are running this tool for the first time, it will create the database.")
print("If you are running this tool for the second time or later, it will update the database.")
print("The database file is located at: " + db_file)
print("The SQL files are located at: " + sql_dir)
print("==========================================")

# Check if the database exists
if not os.path.exists(db_file):
    # If the database does not exist, create it and run all SQL files in the SQL directory
    print("Creating database file: " + db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    for sql_file in sorted(os.listdir(sql_dir)):
        if sql_file.endswith('.sql'):
            sql_number = int(sql_file.split('.')[0])
            with open(os.path.join(sql_dir, sql_file), 'r') as f:
                print("Running SQL file: " + sql_file)
                cursor.executescript(f.read())
    cursor.close()
    conn.close()
    print("Database created with version " + str(sql_number))
else:
    # If the database already exists, check if the 'meta' table exists
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='meta'")
    result = cursor.fetchone()
    if result:
        # If the 'meta' table exists, check if it has a 'last_sql' value
        cursor.execute("SELECT value FROM meta WHERE key='last_sql'")
        result = cursor.fetchone()
        if result:
            # If the 'last_sql' value exists, run all SQL files after that number
            last_sql = int(result[0])
            for sql_file in sorted(os.listdir(sql_dir)):
                if sql_file.endswith('.sql'):
                    sql_number = int(sql_file.split('.')[0])
                    if sql_number > last_sql:
                        with open(os.path.join(sql_dir, sql_file), 'r') as f:
                            print("Running SQL file: " + sql_file)
                            cursor.executescript(f.read())
            # Update the 'last_sql' value to the number of the last SQL file that was executed
            cursor.execute("UPDATE meta SET value=? WHERE key='last_sql'", (str(sql_number),))
            conn.commit()
            print("Database updated to version " + str(sql_number))
        else:
            # If the 'last_sql' value does not exist, stop with a consistency error
            print("Consistency error: 'last_sql' value is missing from the 'meta' table. Unable to determine how to continue.")
    else:
        # If the 'meta' table does not exist, run all SQL files starting with '2'
        for sql_file in sorted(os.listdir(sql_dir)):
            if sql_file.endswith('.sql'):
                sql_number = int(sql_file.split('.')[0])
                if sql_number >= 2:
                    with open(os.path.join(sql_dir, sql_file), 'r') as f:
                        print("Running SQL file: " + sql_file)
                        cursor.executescript(f.read())
        # Add a row to the 'meta' table with a 'last_sql' value of the number of the last SQL file that was executed
        cursor.execute("INSERT INTO meta (key, value) VALUES (?, ?)", ('last_sql', str(sql_number)))
        conn.commit()
        print("Database updated to version " + str(sql_number))
    cursor.close()
    conn.close()
print("\033[92mAll done.\033[0m")
