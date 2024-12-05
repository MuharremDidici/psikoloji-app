from models import User, Psychologist, Appointment
from datetime import datetime
from werkzeug.security import generate_password_hash

def create_test_data(db):
    # Danışan kullanıcısı oluştur
    test_user = User(
        username="test_user2",
        email="test2@example.com",
        password_hash=generate_password_hash("test123"),
        is_admin=False,
        is_psychologist=False  # Danışan
    )
    db.session.add(test_user)

    # Terapist kullanıcısı oluştur
    therapist_user = User(
        username="ayse_dr",
        email="ayse2@example.com",
        password_hash=generate_password_hash("therapist123"),
        is_admin=True,
        is_psychologist=True  # Terapist
    )
    db.session.add(therapist_user)

    # Test terapisti oluştur
    test_therapist = Psychologist(
        name="Dr. Ayşe Yılmaz",
        title="Klinik Psikolog",
        specialization="Bilişsel Davranışçı Terapi",
        email="ayse2@example.com",
        phone="5551234567"
    )
    db.session.add(test_therapist)
    db.session.commit()

    # Bugün için online randevu oluştur
    now = datetime.now()
    appointment_time = now.replace(hour=14, minute=0, second=0, microsecond=0)

    test_appointment = Appointment(
        user_id=test_user.id,
        psychologist_id=test_therapist.id,
        client_name=test_user.username,
        client_email=test_user.email,
        appointment_date=appointment_time,
        appointment_type='online',
        is_online=True,
        status='confirmed'
    )
    db.session.add(test_appointment)
    db.session.commit()

    print("Test kullanıcıları ve randevu oluşturuldu!")
    print("\nDanışan hesabı:")
    print(f"Kullanıcı adı: {test_user.username}")
    print(f"Şifre: test123")
    print("\nTerapist hesabı:")
    print(f"Kullanıcı adı: {therapist_user.username}")
    print(f"Şifre: therapist123")
    print(f"\nRandevu saati: {appointment_time.strftime('%H:%M')}")

if __name__ == '__main__':
    from app import app, db
    with app.app_context():
        create_test_data(db)