from datetime import time
from app import app, db, Availability

# Örnek müsaitlik: Pazartesi-Cuma 09:00-17:00
availabilities = [
    Availability(
        psychologist_id=1,  # İlk psikolog için
        day_of_week=day,    # 0=Pazartesi, 4=Cuma
        start_time=time(9, 0),  # 09:00
        end_time=time(17, 0)    # 17:00
    )
    for day in range(5)  # Pazartesi-Cuma
]

with app.app_context():
    for availability in availabilities:
        db.session.add(availability)
    db.session.commit()
    print("Müsaitlikler başarıyla eklendi!")
