import config
import psycopg2
import ipaddress

conn = psycopg2.connect(
    host=ipaddress.ip_address('35.185.116.190'),
    database='postgres',
    user=config.DB_USER,
    password=config.DB_PASSWORD)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS person;')
cur.execute('CREATE TABLE person (id serial PRIMARY KEY,'
            'first_name varchar (150) NOT NULL,'
            'last_name varchar (100) NOT NULL,'
            'age integer NOT NULL,'
            'email varchar (100) NOT NULL,'
            'address json NOT NULL,'
            'profile_picture varchar (100),'
            'date_created date DEFAULT CURRENT_TIMESTAMP);'
            )

# Insert data into the table

cur.execute('INSERT INTO person (first_name, last_name, age, email, address, profile_picture)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            ('Test',
             'User 1',
             25,
             'anujmpatel21@gmail.com',
             '{"street_name":"Test Street Name 1", "city":"Test city 1", "state":"Test 1", "zip_code":11111}',
             'sampleprofilepicture1.jpg')
            )

cur.execute('INSERT INTO person (first_name, last_name, age, email, address, profile_picture)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            ('Test',
             'User 2',
             25,
             'vama.trivedi1994@gmail.com',
             '{"street_name":"Test Street Name 2", "city":"Test city 2", "state":"Test 2", "zip_code":22222}',
             'sampleprofilepicture2.jpg')
            )

cur.execute('INSERT INTO person (first_name, last_name, age, email, address, profile_picture)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            ('Test',
             'User 3',
             25,
             'anujmpatel@icloud.com',
             '{"street_name":"Test Street Name 3", "city":"Test city 3", "state":"Test 3", "zip_code":33333}',
             'sampleprofilepicture1.jpg')
            )

conn.commit()

cur.close()
conn.close()
