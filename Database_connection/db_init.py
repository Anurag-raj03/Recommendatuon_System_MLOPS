import sqlite3
import os
import logging

DB_NAME = "Database_connection/anime_dat.db"
DB_NAME2 = "Database_connection/anime_preprocessed_dat.db"
DB_PATH = os.path.join(DB_NAME)
DB_PATH2 = os.path.join(DB_NAME2)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def create_database(db_path):
    if not os.path.exists(db_path):
        open(db_path, 'w').close()
        logger.info(f"Database '{db_path}' created successfully.")
    else:
        logger.info(f"Database '{db_path}' already exists.")

def create_table(conn, create_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_sql)
        conn.commit()
        logger.info("Table has been created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error creating table: {e}")
    finally:
        cur.close()

def anime_name_checking(conn, English):
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM anime WHERE English = ?", (English,))
        result = cur.fetchone()
        return result is not None
    except sqlite3.Error as e:
        logger.error(f"Error checking anime existence: {e}")
        return False
    finally:
        cur.close()

def insert_new_anime_data(conn, anime_data):
    if anime_name_checking(conn, anime_data['English']):
        logger.info(f"Anime '{anime_data['English']}' already exists in the database.")
        return

    sql = """
        INSERT INTO anime (
            ID,Title, English, Type, Premiered, Producers, Studios,
            Source, Genres, Themes, Demographics, Rating, Score, Synopsis
        )
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    values = (
        anime_data["ID"],anime_data["Title"], anime_data["English"], anime_data["Type"],
        anime_data["Premiered"], anime_data["Producers"], anime_data["Studios"],
        anime_data["Source"], anime_data["Genres"], anime_data["Themes"],
        anime_data["Demographics"], anime_data["Rating"], anime_data["Score"],
        anime_data["Synopsis"]
    )
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        logger.info("New anime data added successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error inserting anime data: {e}")
    finally:
        cur.close()
    check_insert = anime_name_checking(conn, anime_data['English'])
    if check_insert:
        logger.info(f"Anime '{anime_data['English']}' successfully inserted into the database.")
    else:
        logger.error(f"Failed to insert anime '{anime_data['English']}'.")

def insert_preprocessed_data(conn, preprocessed_anime):
    sql = """INSERT INTO anime_preprocessed_table (English, About) VALUES (?, ?);"""
    try:
        cur = conn.cursor()
        cur.executemany(sql, list(zip(preprocessed_anime["English"], preprocessed_anime["About"])))
        conn.commit()
        logger.info("New preprocessed anime data added successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error inserting preprocessed data: {e}")
    finally:
        cur.close()
    for english_title in preprocessed_anime["English"]:
        cur = conn.cursor()
        cur.execute("SELECT * FROM anime_preprocessed_table WHERE English = ?", (english_title,))
        result = cur.fetchone()
        if result:
            logger.info(f"Preprocessed data for anime '{english_title}' successfully inserted.")
        else:
            logger.error(f"Failed to insert preprocessed data for anime '{english_title}'.")

if __name__ == "__main__":
    create_database(DB_PATH)
    create_database(DB_PATH2)
#The below anime detail is for testing purposes only u can remove this if you want
    conn1 = get_connection(DB_PATH)
    if conn1:
        create_table(conn1, """
            CREATE TABLE IF NOT EXISTS anime(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                English TEXT NOT NULL UNIQUE,
                Type TEXT NOT NULL,
                Premiered TEXT NOT NULL,
                Producers TEXT NOT NULL,
                Studios TEXT NOT NULL,
                Source TEXT NOT NULL,
                Genres TEXT NOT NULL,
                Themes TEXT NOT NULL,
                Demographics TEXT NOT NULL,
                Rating TEXT NOT NULL,
                Score REAL NOT NULL,
                Synopsis TEXT NOT NULL
            );
        """)
        cyberpunk_data = {
            "ID":"42310",
            "Title": "Cyberpunk: Edgerunners",
            "English": "Cyberpunk: Edgerunners",
            "Type": "ONA",
            "Premiered": "September 2022",
            "Producers": "CD Projekt",
            "Studios": "Trigger",
            "Source": "Game",
            "Genres": "Action, Sci-Fi",
            "Themes": "Cyberpunk",
            "Demographics": "Seinen",
            "Rating": "R - 17+ (violence & profanity)",
            "Score": 8.6,
            "Synopsis": "Dreams are doomed to die in Night City, a futuristic Californian metropolis. As a teenager living in the city's slums, David Martinez is trying to fulfill his mother's lifelong wish for him to reach the top of Arasaka, the world's leading security corporation. To this end, he attends the prestigious Arasaka Academy while his mother works tirelessly to keep their family afloat.When an incident with a street gang leaves David's life in tatters, he stumbles upon Sandevistan cyberware—a prosthetic that grants its wearer superhuman speed. Fueled by rage, David implants the device in his back, using it to exact revenge on one of his tormentors. This gets him expelled from the academy, shattering his hopes of ever making his mother proud.After witnessing David's newfound abilities, the beautiful data thief Lucyna Lucy Kushinada offers to team up with him, handing him a ticket to salvation. However, associating with Lucy introduces David to the world of Edgerunners—cyborg criminals who will break any law for money. Edgerunners often lose their lives, if the cyberware does not break their minds first; but in his fight for survival inside a corrupt system, David is ready to risk it all."
        }

        insert_new_anime_data(conn1, cyberpunk_data)
        conn1.close()

    conn2 = get_connection(DB_PATH2)
    if conn2:
        create_table(conn2, """
            CREATE TABLE IF NOT EXISTS anime_preprocessed_table(
                English TEXT NOT NULL,
                About TEXT NOT NULL
            );
        """)

        conn2.close()
