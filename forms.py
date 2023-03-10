from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo, email_validator)
from models import User
from flask import request

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with the email address already exists.')


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with the name already exists.')


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message="Username should be one word, letters, numbers, and underscores only."
            ),
            name_exists,
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message="Passwords must match.")
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
