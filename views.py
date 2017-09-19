from app import app, db
from flask import render_template, flash, request, jsonify, redirect, url_for, session, g
from models import Member, User

from forms import RegistrationForm, LoginForm
from passlib.hash import sha256_crypt

from get_data import update_hist_data

from keras.models import load_model
import numpy as np
from math import sqrt
from sklearn.metrics import mean_squared_error

@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

@app.route('/', methods=['GET','POST'])
def homepage():
	if not g.user:
		return redirect(url_for('login'))
	if request.method == 'POST':
		symbol = request.form['symbol']
		# get current time and craw up to 1 year of data
		update_hist_data(symbol,'./static/data/'+symbol+'.csv')
		# get prediction using trained lstm model
		model = load_model('./model/data/modelMetaData.h5')
		model.summary()
		# model_conf = model.get_config()
		# print model_conf
		rmse, prediction = predict(model,'./static/data/'+symbol+'.csv')
		print str(rmse)+','+str(prediction)
		# render template with real-time properties, charts and predictions
		data = {
			'symbol': symbol,
			'tomorrow_date': '2017-9-20',
			'tomorrow_prediction': str(prediction),
			'RMSE':str(rmse),
		}
		return render_template('index.html', data = data)
	return render_template('welcome.html')

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	try:
		form = LoginForm(request.form)
		
		if request.method == 'POST' and form.validate():
			user = form.username.data
			result = User.query.filter_by(username= user).first()
			if result is not None:
				if sha256_crypt.verify(form.password.data, result.password):
					session['user'] = user
					return redirect(url_for('homepage'))
				else:
					error = "password not valid."
			else:
				error = "User doesn't exist."
				
		return render_template('login.html', form=form, error = error)
	except Exception as e:
		return render_template('login.html', form=form, error = e)
	

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('homepage'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = None
	try:	
		form = RegistrationForm(request.form)
		
		if request.method == 'POST' and form.validate():
			username = form.username.data
			email = form.email.data
			password = sha256_crypt.encrypt((str(form.password.data)))
			### validate email address
			newuser = User(username=username, email=email, password=password)
			db.session.add(newuser)
			db.session.commit()
			session['user'] = username
			flash("Successfully registered in!", 'success')
			return redirect(url_for('homepage'))

		return render_template('signup.html', form=form)

	except Exception as e:
		# if e is database error 
		return render_template('signup.html', form=form, error = e)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ------------------------------------------------------- Admin
@app.route('/create_token/<token_name>/<password>')
def add_token(token_name,password):
	if password != "hackru":
		return render_template('login.html')
	firstmember = Member.query.first()
	return '<h1>The first member is: '+ firstmember.name + '\n'
    # download data from finance api and save as draw.csv
    # fill data to the database of new token
    # return render_template('priceChart.html')

# ------------------------------------------------------ error handle
@app.errorhandler(404)
def page_not_found(e):
	return "Woops! page not found!"

@app.errorhandler(405)
def method_not_found(e):
	return "Woops! method doesn't exist!"

# --------------------------------------------------------- LSTM predictor

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data

def RMSE(orig, predictions):
	return sqrt(mean_squared_error(orig, predictions))

def predict(model,filename, seq_len=50, normalise_window=True):
	f = open(filename, 'r').read()
	prices = f.split('\n')

	data = []
	for i in range(len(prices)-1)[1:]:
		data.append(prices[i].split(',')[4])
	data.reverse()

	print "testing data length: " + str(len(data))
	data.append(0)
	sequence_length = seq_len + 1
	result = []
	for index in range(len(data) - sequence_length):
		result.append(data[index: index + sequence_length])
	print "windowed testing data length: "+ str(len(result))

	if normalise_window:
		result = normalise_windows(result)

	result = np.array(result)
	x_test = result[:, :-1]
	y_test = result[:, -1]
	y_test_restorer = data[:len(y_test)]
	x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
	predictions = model.predict(x_test)

	if normalise_window: # restore the normalised data and predictions to the original value=
		for i in range(len(y_test)):
			y_test[i] = (y_test[i]+1) * float(y_test_restorer[i])
			predictions[i] = (predictions[i]+1) * float(y_test_restorer[i])

	return RMSE(y_test[:-1], predictions[:-1]), predictions[-1][0]
