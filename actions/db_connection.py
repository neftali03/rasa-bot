import psycopg2
import toml


def load_db_config():
    """Load database configuration from env."""
    config = toml.load("env.toml")
    db_config = config["database"]
    return db_config


def fetch_questions():
    """Fetch the first user's first name from the database."""
    db_config = load_db_config()
    with psycopg2.connect(
        dbname=db_config["name"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"],
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT question_text FROM questions")
            rows = cursor.fetchall()
            questions = [row[0] for row in rows]
    return questions
