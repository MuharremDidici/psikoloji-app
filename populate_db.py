import sqlite3

# Veritabanı bağlantısı oluştur
conn = sqlite3.connect('c:/Users/Lenovo/CascadeProjects/windsurf-project/database.db')
cursor = conn.cursor()

# Örnek psikolog verileri ekle
psychologists = [
    ('Dr. Ayşe Yılmaz',),
    ('Dr. Mehmet Demir',),
    ('Dr. Zeynep Kaya',)
]

cursor.executemany('INSERT INTO psychologist (name) VALUES (?)', psychologists)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
