from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,RadioField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,Optional,ValidationError
from models import User
from wtforms.fields import SelectMultipleField



class RegistrationForm(FlaskForm):
    FullName = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    phoneNumber = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    # gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    # gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user =User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('that username is taken. please choose diffrent one')
        
    def validate_username(self, email):
        user =User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('that email is taken. please choose diffrent one')        
   
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class Send_message(FlaskForm):
    messages = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('send-message')

