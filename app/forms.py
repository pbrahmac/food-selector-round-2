from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Regexp
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Invalid username.')

    # def validate_password(self, username, password):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user.check_password(password) == False:
    #         raise ValidationError('Incorrect password.')

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long.'), Regexp(
        "^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d))", message="Password must have at least one upper case, lower case, and numeric/special character.")])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message="Make sure this matches the password field above.")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken. Please use another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is already taken. Please use another one.')

class EditProfileForm(FlaskForm):
    firstname = StringField('Change first name:')
    lastname = StringField('Change last name:')
    username = StringField('Change username:')
    password = PasswordField('Change password:', validators=[Length(min=6, message='Password must be at least 6 characters long.'), Regexp(
        "^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d))", message="Password must have at least one upper case, lower case, and numeric/special character.")])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken. Please use another one.')

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete my account')

class UserSearchForm(FlaskForm):
    searchBox = StringField('')
    submit = SubmitField('Search')

class FoodItemSearchForm(FlaskForm):
    foodSearchBox = StringField('')
    submit = SubmitField('Search')