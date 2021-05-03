from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app import db
from app.mod_auth.forms import LoginForm
from app.mod_auth.models import User

#define blueprint
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

#Set route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])

#Sign in procedure
def signin():

	form = LoginForm(request.form)

	if form.validate_on_submit():

		user = User.query.filter_by(name=form.name.data).first()

		if user: #Password validation goes here, if it's implemented

			session['user_id'] = user.id
			flash('Welcome %s' % user.name)
			return redirect(url_for('auth.home'))

		else:

			flash('Wrong sign in', 'error-message')
			return render_template("auth/signin.html", form=form)
