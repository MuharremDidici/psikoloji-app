import sqlite3

# Veritabanı bağlantısı oluştur
conn = sqlite3.connect('c:/Users/Lenovo/CascadeProjects/windsurf-project/database.db')
cursor = conn.cursor()

# Psikologlar tablosunu oluştur
cursor.execute('''CREATE TABLE IF NOT EXISTS psychologist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)''')

# Randevular tablosunu oluştur
cursor.execute('''CREATE TABLE IF NOT EXISTS appointment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    psychologist_id INTEGER,
    client_name TEXT,
    client_email TEXT,
    client_phone TEXT,
    appointment_date TEXT,
    FOREIGN KEY (psychologist_id) REFERENCES psychologist (id)
)''')

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
