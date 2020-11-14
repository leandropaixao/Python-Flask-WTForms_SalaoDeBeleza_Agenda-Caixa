from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Utilisateur', validators=[DataRequired(message="Campo obrigatório")], render_kw={"placeholder": "Utilisateur"})
    password = PasswordField('Mot de passe', validators=[DataRequired(message="Campo obrigatório")], render_kw={"placeholder": "Mot de passe"})
    remember_me = BooleanField('Rappelle moi')
    submit = SubmitField('Se connecter')