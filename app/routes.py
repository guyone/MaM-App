import os
import re
import secrets
import time
import datetime
import PIL
from app.decorators import check_confirmed
from app.email import send_reset_email, send_confirm_email
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, mail
from app.forms import (RegistrationForm, LogInForm, NewBandForm, NewVenueForm, NewFestivalForm,
                       UpdateAccountEmailForm, ThreadForm, UpdateBandForm, UpdateVenueForm, UpdateFestivalForm,
                       RequestResetForm, ResetPasswordForm, UpdateAccountPasswordForm, UpdateUser, UpdateUserProfilePic,
                       RegisterPromoterForm)
from app.models import User, Band, Thread, Event, Venue, Festival
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc
from flask_mail import Message
from app.token import confirm_token, generate_confirmation_token
from app.images import *

@app.route('/')
def home():
    posts = reversed(Thread.query.all())
    return render_template('home.html', title='Home', posts=posts)

@app.route('/about/')
def about():
    return render_template('about.html', title='Contact Us')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, confirmed=False)
        user.profile_pic=url_for('static', filename='imgs/default.jpg')
        os.mkdir(f'app/static/uploads/users/{user.username}')
        os.mkdir(f'app/static/uploads/users/{user.username}/imgs')
        db.session.add(user)
        db.session.commit()
        send_confirm_email(user)
        flash(f'Your account has been created and you can now log in! Please check your email ({user.email}) to confirm your account.', 'success')
        return redirect(url_for('login'))
    return render_template('login/register.html', title='Register', form=form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account has already been confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thank you!', 'success')
    return redirect(url_for('home'))

@app.route('/resend/')
@login_required
def resend_confirmation():
    if not current_user.confirmed:
        send_confirm_email(current_user)
        flash('A new confirmation email has been sent.', 'success')
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login was unsuccessful. Please check your email and password.', 'danger')
    return render_template('login/login.html', title='Login', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return render_template('login/logout.html', title='Logged out')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been sent to {user.email} with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('login/reset_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token. Please attempt another reset.', 'warn')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        msg = Message('[Metal as Medicine] Your Password Was Reset', sender='noreply@metalasmedicine.com', recipients=[user.email])
        msg.html = render_template('email/reset_confirm.html', user=user)
        mail.send(msg)
        flash('Your password has been reset and you can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateUserProfilePic()
    user = current_user
    if form.validate_on_submit():
        if form.profile_pic.data:
            pro_pic = save_profile_pic(form.profile_pic.data, user)
            user.profile_pic = pro_pic
            db.session.commit()
    return render_template('settings/settings.html', user=user, form=form)

@app.route('/settings/email/', methods=['GET', 'POST'])
@login_required
def change_email():
    form = UpdateAccountEmailForm()
    user = current_user
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.password.data):
            user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return render_template('settings/settings.html', user=user)
        else:
            flash('Your password is incorrect. Please try again or reset your password if you have forgotten it.')
    return render_template('settings/change_email.html', user=user, form=form)

@app.route('/settings/password/', methods=['GET', 'POST'])
@login_required
def change_password():
    form = UpdateAccountPasswordForm()
    user = current_user
    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.current_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            msg = Message('[Metal as Medicine] Your Password Was Changed', sender='noreply@metalasmedicine.com', recipients=[user.email])
            msg.html = render_template('email/change_password_email.html', user=user)
            mail.send(msg)
            flash('Your password has been changed!', 'success')
            return redirect(url_for('settings'))
        flash('Your current password was not correct. Try again.', 'warning')
        return redirect(url_for('change_password'))
    return render_template('settings/change_password.html', user=user, form=form)

@app.route('/u/')
def u():
    return redirect(url_for('users'))

@app.route('/users/')
def users():
    users = User.query.order_by(User.username).all()
    return render_template('users/users.html', title="Users", users=users)

@app.route('/u/<username>/')
def username(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Thread.query.filter_by(user=user)
    return render_template('users/user.html', username=username, user=user, posts=posts)

@app.route('/u/<username>/edit', methods=['GET', 'POST'])
def edit_user(username):
    form = UpdateUser()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.admin = form.admin.data
        db.session.commit()
        flash('%s has been updated!' % user.username, 'success')
        return redirect(url_for('users'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.admin.data = user.admin
    return render_template('users/user_edit.html', user=user, form=form)
# return redirect(url_for('home'))

@app.route('/u/<username>/posts/')
def user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Thread.query.filter_by(user=user).order_by(desc(Thread.date_posted)).limit(3).all()
    profile_pic = url_for('static', filename='imgs/users/profile_pics/' + user.profile_pic)
    return render_template('user.html', user=user, profile_pic=profile_pic, posts=posts)

@app.route('/b/')
def b():
    bands = Band.query.order_by(Band.name).all()
    return render_template('bands/bands.html', bands=bands, title='Bands')

@app.route('/b/new/', methods=['GET', 'POST'])
@login_required
def new_band():
    if current_user.admin != True:
        return redirect(url_for('b'))
    form = NewBandForm()
    if form.validate_on_submit():
        band = Band(name=form.name.data,
        email=form.email.data,
        formed=form.formed.data,
        is_active=form.is_active.data,
        genre=form.genre.data,
        subgenre=form.subgenre.data,
        lyrical_theme=form.lyrical_theme.data,
        website=form.website.data,
        twitter=form.twitter.data,
        facebook=form.facebook.data,
        instagram=form.instagram.data,
        bandcamp=form.bandcamp.data,
        city=form.city.data,
        province=form.province.data,
        country=form.country.data)
        band.username=re.sub(r"\s+", "", band.name).lower()
        os.mkdir(f'app/static/uploads/bands/{band.username}')
        os.mkdir(f'app/static/uploads/bands/{band.username}/logo/')
        os.mkdir(f'app/static/uploads/bands/{band.username}/imgs/')
        if form.logo.data:
            band_logo = save_band_logo(form.logo.data, band)
            band.logo = band_logo
        if form.band_pic.data:
            band_picture = save_band_pic(form.band_pic.data, band)
            band.band_pic = band_picture
        db.session.add(band)
        db.session.commit()
        flash('A new band has been submitted', 'success')
        return redirect(url_for('b'))
    return render_template('bands/band_new.html', form=form)

@app.route('/b/<band>/')
def band(band):
    band = re.sub(r"\s+", "", band).lower()
    band = Band.query.filter_by(username=band).first_or_404()
    return render_template('bands/band.html', band=band)

@app.route('/b/<band>/edit', methods=['GET', 'POST'])
@login_required
def edit_band(band):
    if current_user.admin != True:
        return redirect(url_for('b'))
    form = UpdateBandForm()
    band = Band.query.filter_by(username=band).first_or_404()
    if form.validate_on_submit():
        if form.logo.data:
            path = os.path.join(app.root_path, f'static/uploads/bands/{band.username}/logo/', band.logo)
            os.remove(path)
            band_logo = save_band_logo(form.logo.data, band)
            band.logo = band_logo
        if form.band_pic.data:
            path = os.path.join(app.root_path, f'static/uploads/bands/{band.username}/imgs/', band.band_pic)
            os.remove(path)
            band_picture = save_band_pic(form.band_pic.data, band)
            band.band_pic = band_picture
        band.name = form.name.data
        band.email = form.email.data
        band.formed = form.formed.data
        band.is_active = form.is_active.data
        band.genre = form.genre.data
        band.subgenre = form.subgenre.data
        band.lyrical_theme = form.lyrical_theme.data
        band.website = form.website.data
        band.twitter = form.twitter.data
        band.facebook = form.facebook.data
        band.instagram = form.instagram.data
        band.bandcamp = form.bandcamp.data
        band.city = form.city.data
        band.province = form.province.data
        band.country = form.country.data
        band.username=re.sub(r"\s+", "", band.name).lower()
        db.session.commit()
        flash('%s has been updated!' % band.name, 'success')
        return redirect(url_for('b'))
    elif request.method == 'GET':
        form.name.data = band.name
        form.email.data = band.email
        form.formed.data = band.formed
        form.is_active.data = band.is_active
        form.genre.data = band.genre
        form.subgenre.data = band.subgenre
        form.lyrical_theme.data = band.lyrical_theme
        form.website.data = band.website
        form.twitter.data = band.twitter
        form.facebook.data = band.facebook
        form.instagram.data = band.instagram
        form.bandcamp.data = band.bandcamp
        form.city.data = band.city
        form.province.data = band.province
        form.country.data = band.country
    return render_template('bands/band_edit.html', band=band, form=form)

@app.route('/v/')
def v():
    venues = Venue.query.all()
    return render_template('venues/venues.html', venues=venues, title='Venues')

@app.route('/v/new/', methods=['GET', 'POST'])
def new_venue():
    if current_user.admin != True:
        return redirect(url_for('v'))
    form = NewVenueForm()
    if form.validate_on_submit():
        venue = Venue(name=form.name.data,
        email=form.email.data,
        founded=form.founded.data,
        is_active=form.is_active.data,
        street_name=form.street_name.data,
        street_number=form.street_number.data,
        unit_number=form.unit_number.data,
        postal_code=form.postal_code.data,
        province=form.province.data,
        country=form.country.data,
        phone_number=form.phone_number.data,
        website=form.website.data,
        twitter=form.twitter.data,
        facebook=form.facebook.data,
        instagram=form.instagram.data,
        city=form.city.data,
        capacity=form.capacity.data)
        venue.username=re.sub(r"\s+", "", venue.name).lower()
        os.mkdir(f'app/static/uploads/venues/{venue.username}')
        os.mkdir(f'app/static/uploads/venues/{venue.username}/imgs/')
        if form.venue_pic.data:
            venue_pic = save_venue_pic(form.venue_pic.data, venue)
            venue.venue_pic = venue_pic
        db.session.add(venue)
        db.session.commit()
        flash('A new venue has been submitted', 'success')
        return redirect(url_for('v'))
    return render_template('venues/venue_new.html', title='New Venue', form=form)

@app.route('/v/<venue>/')
def venue(venue):
    venue = Venue.query.filter_by(username=venue).first_or_404()
    return render_template('venues/venue.html', venue=venue)

@app.route('/v/<venue>/edit', methods=['GET', 'POST'])
@login_required
def edit_venue(venue):
    if current_user.admin != True:
        return redirect(url_for('v'))
    form = UpdateVenueForm()
    venue = Venue.query.filter_by(username=venue).first_or_404()
    if form.validate_on_submit():
        if form.venue_pic.data:
            path = os.path.join(app.root_path, 'static/imgs/venues', venue.venue_pic)
            os.remove(path)
            venue_pic = save_venue_pic(form.venue_pic.data, venue)
            venue.venue_pic = venue_pic
        venue.name = form.name.data
        venue.email = form.email.data
        venue.founded = form.founded.data
        venue.is_active = form.is_active.data
        venue.street_name = form.street_name.data
        venue.street_number = form.street_number.data
        venue.unit_number = form.unit_number.data
        venue.postal_code = form.postal_code.data
        venue.province = form.province.data
        venue.country = form.country.data
        venue.phone_number = form.phone_number.data
        venue.website = form.website.data
        venue.twitter = form.twitter.data
        venue.facebook = form.facebook.data
        venue.instagram = form.instagram.data
        venue.city = form.city.data
        venue.province = form.province.data
        venue.country = form.country.data
        venue.capacity = form.capacity.data
        db.session.commit()
        flash('The venue has been updated!', 'success')
        return redirect(url_for('v'))
    elif request.method == 'GET':
        form.name.data = venue.name
        form.email.data = venue.email
        form.founded.data = venue.founded
        form.is_active.data = venue.is_active
        form.street_name.data = venue.street_name
        form.street_number.data = venue.street_number
        form.unit_number.data = venue.unit_number
        form.postal_code.data = venue.postal_code
        form.province.data = venue.province
        form.country.data = venue.country
        form.phone_number.data = venue.phone_number
        form.website.data = venue.website
        form.twitter.data = venue.twitter
        form.facebook.data = venue.facebook
        form.instagram.data = venue.instagram
        form.city.data = venue.city
        form.province.data = venue.province
        form.country.data = venue.country
        form.capacity.data = venue.capacity
    return render_template('venues/venue_edit.html', venue=venue, form=form)

@app.route('/f/')
def f():
    festivals = Festival.query.all()
    return render_template('festivals/festivals.html', festivals=festivals, title='Festivals')

@app.route('/f/new/', methods=['GET', 'POST'])
@login_required
def new_festival():
    if current_user.admin != True:
        return redirect(url_for('f'))
    form = NewFestivalForm()
    if form.validate_on_submit():
        festival = Festival(name=form.name.data,
        email=form.email.data,
        founded=form.founded.data,
        is_active=form.is_active.data,
        street_name=form.street_name.data,
        street_number=form.street_number.data,
        unit_number=form.unit_number.data,
        postal_code=form.postal_code.data,
        province=form.province.data,
        country=form.country.data,
        phone_number=form.phone_number.data,
        website=form.website.data,
        twitter=form.twitter.data,
        facebook=form.facebook.data,
        instagram=form.instagram.data,
        city=form.city.data,
        capacity=form.capacity.data)
        festival.username=re.sub(r"\s+", "", festival.name).lower()
        os.mkdir(f'app/static/uploads/festivals/{festival.username}')
        os.mkdir(f'app/static/uploads/festivals/{festival.username}/logo/')
        os.mkdir(f'app/static/uploads/festivals/{festival.username}/imgs/')
        if form.logo.data:
            logo = save_festival_logo(form.logo.data, festival)
            festival.logo = logo
        if form.festival_pic.data:
            festival_pic = save_festival_pic(form.festival_pic.data, festival)
            festival.festival_pic = festival_pic
        if form.grounds_map.data:
            grounds_map = save_grounds_pic(form.grounds_map.data, festival)
            festival.grounds_map = grounds_map
        db.session.add(festival)
        db.session.commit()
        flash('A new festival has been submitted', 'success')
        return redirect(url_for('f'))
    return render_template('festivals/festival_new.html', title='New Festival', form=form)

@app.route('/f/<festival>/')
def festival(festival):
    festival = Festival.query.filter_by(username=festival).first_or_404()
    return render_template('festivals/festival.html', festival=festival)

@app.route('/f/<festival>/edit', methods=['GET', 'POST'])
@login_required
def edit_festival(festival):
    if current_user.admin != True:
        return redirect(url_for('f'))
    form = UpdateFestivalForm()
    festival = Festival.query.filter_by(username=festival).first_or_404()
    if form.validate_on_submit():
        if form.festival_pic.data:
            path = os.path.join(app.root_path, f'app/static/uploads/festivals/{festival.username}/imgs/', festival.festival_pic)
            os.remove(path)
            festival_pic = save_festival_pic(form.festival_pic.data, festival)
            festival.festival_pic = festival_pic
        if form.logo.data:
            path = os.path.join(app.root_path, f'app/static/uploads/festivals/{festival.username}/logo/', festival.logo)
            os.remove(path)
            logo = save_festival_logo(form.logo.data, festival)
            festival.logo = logo
        if form.grounds_map.data:
            path = os.path.join(app.root_path, f'app/static/uploads/festivals/{festival.username}/imgs/', festival.grounds_map)
            os.remove(path)
            grounds_map = save_grounds_pic(form.grounds_map.data, festival)
            festival.grounds_map = grounds_map
        festival.name = form.name.data
        festival.email = form.email.data
        festival.founded = form.founded.data
        festival.is_active = form.is_active.data
        festival.street_name = form.street_name.data
        festival.street_number = form.street_number.data
        festival.unit_number = form.unit_number.data
        festival.postal_code = form.postal_code.data
        festival.province = form.province.data
        festival.country = form.country.data
        festival.phone_number = form.phone_number.data
        festival.website = form.website.data
        festival.twitter = form.twitter.data
        festival.facebook = form.facebook.data
        festival.instagram = form.instagram.data
        festival.city = form.city.data
        festival.province = form.province.data
        festival.country = form.country.data
        festival.capacity = form.capacity.data
        db.session.commit()
        flash('The festival has been updated!', 'success')
        return redirect(url_for('f'))
    elif request.method == 'GET':
        form.name.data = festival.name
        form.email.data = festival.email
        form.founded.data = festival.founded
        form.is_active.data = festival.is_active
        form.street_name.data = festival.street_name
        form.street_number.data = festival.street_number
        form.unit_number.data = festival.unit_number
        form.postal_code.data = festival.postal_code
        form.province.data = festival.province
        form.country.data = festival.country
        form.phone_number.data = festival.phone_number
        form.website.data = festival.website
        form.twitter.data = festival.twitter
        form.facebook.data = festival.facebook
        form.instagram.data = festival.instagram
        form.city.data = festival.city
        form.province.data = festival.province
        form.country.data = festival.country
        form.capacity.data = festival.capacity
    return render_template('festivals/festival_edit.html', festival=festival, form=form)

@app.route('/events/')
def events():
    events = Event.query.all()
    return render_template('events/events.html', events=events, title='Events')

@app.route('/promoters/')
def promoters():
    return render_template('promoters/promoters.html', title='Promoters')

@app.route('/registerpromoter/', methods=['GET', 'POST'])
def promoter_register():
    form = RegisterPromoterForm()
    return render_template('promoters/register.html', form=form)

@app.route('/post/new/', methods=['GET', 'POST'])
@login_required
def new_post():
    form = ThreadForm()
    if form.validate_on_submit():
        post = Thread(text=form.text.data, title=form.title.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post as been created!', 'success')
        return redirect('/')
    return render_template('new_post.html', title='New Post', form=form)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Thread.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/update')
@login_required
def update_post(post_id):
    post = Thread.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    return render_template('post.html', post=post)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')