def load_config():
    """Returns the database connection configuration."""
    return {
        "dbname": "phonebook_db", # Make sure to create this database in pgAdmin or psql first
        "user": "kemenger",       # Your PostgreSQL username
        "password": "",   # Your PostgreSQL password
        "host": "localhost",
        "port": "5432"
    }