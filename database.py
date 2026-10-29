import psycopg2
def connect_to_database():
    try:
        pass
        connection=psycopg2.connect(
            host="localhost",
            port="5432",
            database="banksystemmanagement",
            user="postgres",
            password=1592005
        )
        print("Connected to PostgresSQL database!")
        return connection
    
    except Exception as error:
        print("Enter connecting to PostgreSQL database:", error)
        return None
    
if __name__ == '__main__':
    conn=connect_to_database()
    if conn:
        conn.close()
        print("connection Closed")
        