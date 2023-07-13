import sqlite3

def notify(*x):
    print ("Hello",*x)

con = sqlite3.connect('instance/project.db')
cur = con.cursor()
print(sqlite3.version)

con.create_function("notify", 1, notify)
# cur.execute("DROP TRIGGER notifier")
# cur.execute("""CREATE TRIGGER notifier AFTER UPDATE ON tests BEGIN SELECT notify(
#             OLD.model_list
#             OLD.
#             ); END;""")

sql = """UPDATE tests set dueDate = datetime('2025-01-07 00:00:00') WHERE id = 123"""
cur.execute(sql)
con.commit()