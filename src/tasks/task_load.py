from prefect import task
import mysql.connector

@task(name="Cargar datos")
def task_load(offers):
    try:
        conn = mysql.connector.connect(
            user='root',
            password='mysqljavier',
            host='localhost',
            database='datag3'
        )
        cursor = conn.cursor()

        query_table = """
        create table if not exists db_linkedin_offers(
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(255),
        ubicacion VARCHAR(255),
        empresa VARCHAR(255),
        fecha DATE,
        url TEXT,
        skill VARCHAR(255)
        )
        """
        cursor.execute(query_table)
        conn.commit()

        query_insert = """
        insert into db_linkedin_offers(titulo,ubicacion,empresa,fecha,url,skill)
        values(%s,%s,%s,%s,%s,%s)
        """

        for offer in offers:
            cursor.execute(query_insert,offer)

        conn.commit()
        cursor.close()
        conn.close()
        print("datos guardados en la base de datos")
    except mysql.connector.Error as err:
        print(err)