from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from . import auth_bp
from .forms import RegistrationForm, LoginForm
from models import create_user, find_user_by_email, User


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if find_user_by_email(form.email.data):
            flash('An account with that email already exists.', 'danger')
            return render_template('register.html', form=form)
        create_user(form.username.data, form.email.data, form.password.data)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_doc = find_user_by_email(form.email.data)
        if user_doc:
            user = User(user_doc)
            if user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next') or url_for('books.bookshelf')
                return redirect(next_page)
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))