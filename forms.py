from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, EqualTo, ValidationError

class PsychologistForm(FlaskForm):
    name = StringField('Ad Soyad', validators=[DataRequired()])
    title = StringField('Ünvan', validators=[DataRequired()])
    specialization = StringField('Uzmanlık Alanı', validators=[DataRequired()])
    about = TextAreaField('Hakkında')
    email = StringField('E-posta', validators=[Optional(), Email()])
    phone = StringField('Telefon', validators=[Optional()])
    photo = FileField('Fotoğraf')
    password = PasswordField('Şifre', validators=[Optional(), Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', 
                         validators=[DataRequired(), 
                                   Length(min=3, message='Kullanıcı adı en az 3 karakter olmalıdır.')])
    
    email = StringField('E-posta',
                       validators=[DataRequired(),
                                 Email(message='Geçerli bir e-posta adresi giriniz.')])
    
    password = PasswordField('Şifre',
                           validators=[DataRequired(),
                                     Length(min=6, message='Şifre en az 6 karakter olmalıdır.')])
    
    confirm_password = PasswordField('Şifre Tekrar',
                                   validators=[DataRequired(),
                                             EqualTo('password', message='Şifreler eşleşmiyor.')])
    
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        from models import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten kullanılıyor.')
            
    def validate_email(self, email):
        from models import User
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor.')

class ProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_picture = FileField('Profil Fotoğrafı')
    submit = SubmitField('Kaydet')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            from models import User
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Bu kullanıcı adı zaten kullanılıyor.')

    def validate_email(self, email):
        if email.data != self.original_email:
            from models import User
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Bu email adresi zaten kullanılıyor.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mevcut Şifre', validators=[DataRequired()])
    new_password = PasswordField('Yeni Şifre', validators=[
        DataRequired(),
        Length(min=6, message='Şifre en az 6 karakter olmalıdır.')
    ])
    confirm_password = PasswordField('Yeni Şifre (Tekrar)', validators=[
        DataRequired(),
        EqualTo('new_password', message='Şifreler eşleşmiyor.')
    ])
    submit = SubmitField('Şifreyi Değiştir')
