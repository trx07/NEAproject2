from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo



class usernameform(FlaskForm):
    username = StringField('Summoner name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=16)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Check player stats')


class loginInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Log In')

class signUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    chosenLeagueUsername = StringField('League Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword', message=("Passwords must be matching"))])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Sign Up')