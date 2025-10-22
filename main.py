# app.py
import sys
import mysql.connector as mysql
from db_connect import get_conn, DB_NAME

def connect():
    return get_conn(DB_NAME)

def listar_series(limit=10):
    with connect() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT serie_id, titulo, `año_lanzamiento`, genero
                FROM Series
                ORDER BY serie_id
                LIMIT %s
            """, (limit,))
            rows = cur.fetchall()
            if not rows:
                print("No hay series.")
            for r in rows:
                print(r)

def crear_serie():
    print("\n== Crear Serie ==")
    titulo = input("Título: ").strip()
    desc = input("Descripción: ").strip()
    try:
        anio = int(input("Año de lanzamiento (ej. 2016): ").strip())
    except ValueError:
        print("Año inválido."); return
    genero = input("Género: ").strip()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO Series (titulo, descripcion, `año_lanzamiento`, genero)
                VALUES (%s, %s, %s, %s)
            """, (titulo, desc, anio, genero))
            conn.commit()
            print("Serie creada con serie_id:", cur.lastrowid)

def actualizar_serie():
    print("\n== Actualizar Serie ==")
    try:
        serie_id = int(input("serie_id a actualizar: ").strip())
    except ValueError:
        print("ID inválido."); return
    nuevo_titulo = input("Nuevo título (deja vacío para no cambiar): ").strip()
    nuevo_genero = input("Nuevo género (deja vacío para no cambiar): ").strip()

    sets = []
    params = []
    if nuevo_titulo:
        sets.append("titulo=%s")
        params.append(nuevo_titulo)
    if nuevo_genero:
        sets.append("genero=%s")
        params.append(nuevo_genero)

    if not sets:
        print("Nada por actualizar.")
        return

    params.append(serie_id)
    sql = f"UPDATE Series SET {', '.join(sets)} WHERE serie_id=%s"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            conn.commit()
            print("Filas afectadas:", cur.rowcount)

def borrar_serie():
    print("\n== Borrar Serie ==")
    try:
        serie_id = int(input("serie_id a borrar: ").strip())
    except ValueError:
        print("ID inválido."); return
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Series WHERE serie_id=%s", (serie_id,))
            conn.commit()
            print("Eliminadas:", cur.rowcount)

def buscar_por_titulo():
    print("\n== Buscar Serie por título ==")
    patron = input("Texto a buscar: ").strip()
    with connect() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT serie_id, titulo, genero
                FROM Series
                WHERE titulo LIKE %s
                ORDER BY 1
            """, (f"%{patron}%",))
            rows = cur.fetchall()
            if not rows:
                print("Sin resultados.")
            for r in rows:
                print(r)

def join_demo():
    print("\n== JOIN Series x Episodios ==")
    titulo = input("Título exacto de la serie (ej. Stranger Things): ").strip()
    with connect() as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT s.titulo AS serie,
                       e.titulo AS episodio,
                       e.temporada,
                       e.rating_imdb
                FROM Series s
                INNER JOIN Episodios e ON s.serie_id = e.serie_id
                WHERE s.titulo = %s
                ORDER BY e.temporada, e.fecha_estreno
            """, (titulo,))
            rows = cur.fetchall()
            if not rows:
                print("No se encontraron episodios o el título no coincide.")
            for r in rows:
                print(r)

def menu():
    while True:
        print("\n=== Menú NetflixDB ===")
        print("1) Listar series (top 10)")
        print("2) Crear serie")
        print("3) Actualizar serie")
        print("4) Borrar serie")
        print("5) Buscar por título")
        print("6) JOIN demo (Series x Episodios)")
        print("0) Salir")
        op = input("Elige opción: ").strip()
        if op == "1":
            listar_series(10)
        elif op == "2":
            crear_serie()
        elif op == "3":
            actualizar_serie()
        elif op == "4":
            borrar_serie()
        elif op == "5":
            buscar_por_titulo()
        elif op == "6":
            join_demo()
        elif op == "0":
            print("Adiós.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    try:
        menu()
    except mysql.Error as e:
        print("Error MySQL:", e)
        sys.exit(1)
