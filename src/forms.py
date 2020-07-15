"""All the forms."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
    """A registeration form validator."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Make sure that the user alreay doesn't exist."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username was alreay taken! Please choose another one...')

    def validate_email(self, email):
        """Make sure that the user alreay doesn't exist."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email was alreay taken! Please choose another one...')


class LoginForm(FlaskForm):
    """A login form."""

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """A registeration form validator."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        """Make sure that the user alreay doesn't exist."""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username was alreay taken! Please choose another one...')

    def validate_email(self, email):
        """Make sure that the user alreay doesn't exist."""
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken! Please choose a different one.')


class PostForm(FlaskForm):
    """Make sure posts are valid."""

    title = StringField('Tile', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    """A Request email form."""

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """Make sure that the user exist."""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There was no account with the email, Please register first.')


class ResetPasswordForm(FlaskForm):
    """Reset the password."""

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Reset Password')
