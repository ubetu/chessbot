import psycopg2
from config import PGUSER, PGPASSWORD, ip, DATABASE
class db:
    conn = psycopg2.connect(database=DATABASE, user=PGUSER, password=PGPASSWORD, host=ip)
    cursor = conn.cursor()

    @classmethod
    def write_match_asking(cls, id_asker:int, id_asked:int) -> None:
        cls.cursor.execute(f"""INSERT INTO match_asking(id_asker, id_asked) 
                                VALUES ({id_asker}, {id_asked})""")
    @classmethod
    def match_asking_answer(cls, id_asker:int, id_asked:int, answer:bool) -> None:
        cls.cursor.execute(f"""INSERT INTO match_asking(answer) VALUES({answer})""")

    @classmethod
    def match_asking_check_answer(cls, ) -> None:
        pass
