# Placeholder for route definitions like login, dashboard, cert management
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import Client, HCP, Residence, User
from app.forms import LoginForm, HCPForm, ClientForm


@app.route('/')
@login_required
def dashboard():
    hcps = HCP.query.all()
    clients = Client.query.all()
    return render_template('dashboard.html', hcps=hcps, clients=clients)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/hcp/new', methods=['GET', 'POST'])
@login_required
def new_hcp():
    form = HCPForm()
    if form.validate_on_submit():
        hcp = HCP(name=form.name.data)
        db.session.add(hcp)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('cert_form.html', form=form)


@app.route('/client/new', methods=['GET', 'POST'])
@login_required
def new_client():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(initials=form.initials.data, is_primary=form.is_primary.data)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('cert_form.html', form=form)
