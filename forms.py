from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=20)])
	email = StringField('Email Address', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [validators.Required(), 
		validators.EqualTo('confirm', message="Password must match")])
	confirm = PasswordField('Repeat password')
	accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class LoginForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=20)])
	password = PasswordField('Password')