
import MySQLdb

def main():
    # Connect to the database
    db = MySQLdb.connect(host="terraform-20230616200457941200000001.csh8tbkzf6ga.us-east-1.rds.amazonaws.com",
        user="root",
        password="G3F3yeUwkCE#EfJ",
        database="mydb")

    # Get a cursor object
    cursor = db.cursor()

    # Insert a new row
    cursor.execute('''INSERT INTO message (msg) VALUES (%s);''', ('John Doe',))

    # Commit the changes
    db.commit()

    # Close the connection
    db.close()

if __name__ == '__main__':
    main()

