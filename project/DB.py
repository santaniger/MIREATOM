import sqlite3
def getList():
    '''
        Получение всех данных и инициализация базы
    '''
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS latex_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latex_string TEXT NOT NULL,
        description TEXT NOT NULL,
        source TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute('SELECT latex_string, description, source FROM latex_entries')
    rows = cursor.fetchall()
    conn.close()
    return rows

def getInfo(latex):
    '''
    Получение полных данных о формуле
    '''
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT latex_string, description, source FROM latex_entries
    WHERE latex_string = ?
    ''', (latex,))
    row = cursor.fetchone()
    conn.close()
    return row