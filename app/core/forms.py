"""Various forms used within the application."""
from wtforms import (
    Form, StringField, PasswordField, validators, SelectMultipleField,
    BooleanField
)


class LoginForm(Form):

    """Login form validator."""

    username = StringField('username', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [validators.DataRequired()])


class RegisterForm(Form):

    """Register form."""

    username = StringField('username', [validators.Length(min=6, max=35)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    first_name = StringField('first_name', [validators.Length(min=1, max=35)])
    last_name = StringField('last_name', [validators.Length(min=1, max=35)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('password_confirm')


class ChangePasswordForm(Form):

    """Change password form."""

    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('password_confirm')
    user_id = StringField('user_id', [validators.Length(min=1, max=35)])


class AccountSettingsForm(Form):

    """Account settings form."""

    email = StringField('email', [validators.Length(min=6, max=35)])
    first_name = StringField('first_name', [validators.Length(min=1, max=35)])
    last_name = StringField('last_name', [validators.Length(min=1, max=35)])
    user_id = StringField('user_id', [validators.Length(min=1, max=35)])


class MonitorForm(Form):

    """Monitor form validator."""

    term = StringField('term', [validators.Length(min=1, max=35)])
    type = StringField('type', [validators.Length(min=1, max=35)])
    category = StringField('category', [validators.Length(min=1, max=35)])
    tags = StringField('tags')


class AdminForm(Form):

    """Admin form validator."""

    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('password', [validators.DataRequired()])