import sqlite3

def connection_wrapper(func):
    def inner(*args):
        conn = sqlite3.connect(database='chess.db')
        cursor = conn.cursor()
        result = func(*args, cursor=cursor, conn=conn)
        cursor.close()
        conn.close()
        return result
    return inner

class db:
    @staticmethod
    @connection_wrapper
    def write_id(username: str, user_id: int, cursor, conn) -> None:
        cursor.execute(f"""INSERT INTO username_to_id
         SELECT ?, ? WHERE NOT EXISTS(SELECT 1 FROM username_to_id WHERE user_id = ?)""", (user_id, username, user_id))
        conn.commit()

    @staticmethod
    @connection_wrapper
    def get_id(username: str, cursor, conn) -> int:
        cursor.execute("""SELECT user_id FROM username_to_id WHERE username = ?""", (username,))
        user_id = cursor.fetchone()[0]
        return user_id

    @staticmethod
    @connection_wrapper
    def write_game_results(white_id: int, black_id: int, result: int, cursor, conn) -> None:
        """result in (-1, 0, 1) notation"""
        cursor.execute("""INSERT INTO games
        VALUES (?, ?, ?)""", (white_id, black_id, result))
        conn.commit()