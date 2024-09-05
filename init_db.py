import sqlite3

connection = sqlite3.connect("test.db")

with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO books (title, current_lowest_price, link) VALUES (?, ?, ?)",
            ("Alice in Wonderland", 4.28, "https://www.amazon.co.uk/Alice-Wonderland-Original-Complete-Illustrations/dp/B0948LPG76")
            )
cur.execute("INSERT INTO books (title, current_lowest_price, link) VALUES (?, ?, ?)",
            ("The Three-Body Problem", 8.40, "https://www.amazon.co.uk/The-Three-Body-Problem-1/dp/B01MZ6MTL1")
            )

connection.commit()
connection.close()
