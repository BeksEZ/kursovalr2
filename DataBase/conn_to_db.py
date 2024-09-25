import psycopg2

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="1234",
                        port="5432")


def connect_to_db():
    try:
        connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as error:
        print("Error while connecting to the database:", error)
        return None