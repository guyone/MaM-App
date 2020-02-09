from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from app.models import User, Band, Venue, Festival
from app import bcrypt

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SIGN UP')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('There is already an account with that email. Please log in or choose another email address.')

class UpdateUser(FlaskForm):
    username = StringField('Username: ', validators=[Length(min=4, max=20)])
    email = StringField('Email: ', validators=[Email()])
    admin = BooleanField('Is this user an admin?')
    promoter = BooleanField('Is this user a Promoter?')
    submit = SubmitField('UPDATE')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if username.data != user.username:
                raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if email.data != user.email:
            raise ValidationError('There is already an account with that email. Please log in or choose another email address.')

class UpdateAccountEmailForm(FlaskForm):
    password = PasswordField('Current Password:', validators=[DataRequired(), Length(min=4, message="Your password must be at least 4 characters long.")])
    email = StringField('Update Email Address:', validators=[DataRequired(), Email()])
    submit = SubmitField('UPDATE')

    def validate_password(self, password):
        user = current_user
        if not bcrypt.check_password_hash(user.password, self.password.data):
            raise ValidationError('You have entered the wrong password. Try again or request a reset.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('There is already an account attached to that email. Please use a different address.')

class UpdateAccountPasswordForm(FlaskForm):
    current_password = PasswordField('Current Password:', validators=[DataRequired()])
    new_password = PasswordField('New Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password:', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('CHANGE')

    def validate_password(self, current_password):
        if current_password.data != current_user.password:
            raise ValidationError('The password you typed is not your current password. Try again or request a password reset.')


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('LOGIN')

class RegisterPromoterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    text = TextAreaField('Details:', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')

class NewBandForm(FlaskForm):
    name = StringField('Band name:', validators=[DataRequired(), Length(max=120)])
    email = StringField('Contact email:', validators=[DataRequired(), Email()])
    formed = IntegerField('Year formed:', validators=[DataRequired()])
    is_active = SelectField('Is the band active?', choices=[('Active', 'Yes'), ('Not Active', 'No')])
    genre = StringField('Main genre:', validators=[DataRequired()])
    subgenre = StringField('Subgenre:', validators=[DataRequired()])
    lyrical_theme = StringField('Lyrical themes:', validators=[DataRequired()])
    website = StringField('Website address:', validators=[URL()])
    twitter = StringField('twitter link:', validators=[URL()])
    facebook = StringField('facebook link:', validators=[URL()])
    instagram = StringField('Instagram link:', validators=[URL()])
    bandcamp = StringField('Bandcamp page:', validators=[URL()])
    city = StringField('City the band is from:', validators=[DataRequired()])
    province = SelectField('Province:', choices=[('BC', 'British Columbia'), ('AB', 'Alberta'), ('SK', 'Saskatchewan'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ('NB', 'New Brunswick'), ('NS', 'Nova Scotia'), ('PE', 'Prince Edward Island'), ('NL', 'Newfoundland'), ('YT', 'Yukon'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut')])
    country = StringField('Country:', validators=[DataRequired()])
    logo = FileField('Upload logo pic:', validators=[FileAllowed(['jpg', 'png'])])
    band_pic = FileField('Upload band pic:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('SUBMIT')

    def validate_name(self, name):
        band = Band.query.filter_by(name=name.data).first()
        if band:
            raise ValidationError('That band has already been submitted to the database.')

class UpdateUserProfilePic(FlaskForm):
    profile_pic = FileField('Upload new profile pic:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('UPLOAD')

class UpdateBandForm(FlaskForm):
    name = StringField('Band name:', validators=[DataRequired(), Length(max=120)])
    email = StringField('Contact email:', validators=[DataRequired(), Email()])
    formed = IntegerField('Year formed:', validators=[DataRequired()])
    is_active = SelectField('Is the band active?', choices=[('Active', 'Yes'), ('Not Active', 'No')])
    genre = StringField('Main genre:', validators=[DataRequired()])
    subgenre = StringField('Subgenre:', validators=[DataRequired()])
    lyrical_theme = StringField('Lyrical themes:', validators=[DataRequired()])
    website = StringField('Website address:', validators=[URL()])
    twitter = StringField('twitter link:', validators=[URL()])
    facebook = StringField('facebook link:', validators=[URL()])
    instagram = StringField('Instagram link:', validators=[URL()])
    bandcamp = StringField('Bandcamp page:', validators=[URL()])
    city = StringField('City the band is from:', validators=[DataRequired()])
    province = SelectField('Province:', choices=[('BC', 'British Columbia'), ('AB', 'Alberta'), ('SK', 'Saskatchewan'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ('NB', 'New Brunswick'), ('NS', 'Nova Scotia'), ('PE', 'Prince Edward Island'), ('NL', 'Newfoundland'), ('YT', 'Yukon'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut')])
    country = StringField('Country:', validators=[DataRequired()])
    logo = FileField('Upload logo pic:', validators=[FileAllowed(['jpg', 'png'])])
    band_pic = FileField('Upload band pic:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('UPDATE')

    def validate_bandname(self, name):
        if name.data != band.name:
            band = Band.query.filter_by(name=name.data).first()
            if band:
                raise ValidationError('That band is already in the database.')

class NewVenueForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    founded = IntegerField('Year Founded:', validators=[DataRequired()])
    is_active = SelectField('Is the venue active?', choices=[('Active', 'Yes'), ('Not Active', 'No')])
    street_name = StringField('Street Name:')
    street_number = IntegerField('Street Number:')
    unit_number = IntegerField('Unit Number:')
    postal_code = StringField('Postal Code:')
    province = SelectField('Province:', choices=[('BC', 'British Columbia'), ('AB', 'Alberta'), ('SK', 'Saskatchewan'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ('NB', 'New Brunswick'), ('NS', 'Nova Scotia'), ('PE', 'Prince Edward Island'), ('NL', 'Newfoundland'), ('YT', 'Yukon'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut')])
    country = StringField('Country:', validators=[DataRequired()])
    phone_number = StringField('Phone Number:')
    website = StringField('Website:', validators=[URL()])
    twitter = StringField('twitter account name:', validators=[URL()])
    facebook = StringField('facebook link:', validators=[URL()])
    instagram = StringField('Instagram account name:', validators=[URL()])
    city = StringField('City the venue is located in:', validators=[DataRequired()])
    capacity = IntegerField('Venue capacity during a gig:')
    venue_pic = FileField('Upload venue main photo:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('SUBMIT')

    def validate_name(self, name):
        venue = Venue.query.filter_by(name=name.data).first()
        if venue:
            raise ValidationError('That venue has already been submitted to the database.')

class UpdateVenueForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    founded = IntegerField('Year Founded:', validators=[DataRequired()])
    is_active = SelectField('Is the venue active?', choices=[('Active', 'Yes'), ('Not Active', 'No')])
    street_name = StringField('Street Name:')
    street_number = IntegerField('Street Number:')
    unit_number = IntegerField('Unit Number:')
    postal_code = StringField('Postal Code:')
    province = SelectField('Province:', choices=[('BC', 'British Columbia'), ('AB', 'Alberta'), ('SK', 'Saskatchewan'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ('NB', 'New Brunswick'), ('NS', 'Nova Scotia'), ('PE', 'Prince Edward Island'), ('NL', 'Newfoundland'), ('YT', 'Yukon'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut')])
    country = StringField('Country:', validators=[DataRequired()])
    phone_number = StringField('Phone Number:')
    website = StringField('Website:', validators=[URL()])
    twitter = StringField('twitter account name:', validators=[URL()])
    facebook = StringField('facebook link:', validators=[URL()])
    instagram = StringField('Instagram account name:', validators=[URL()])
    city = StringField('City the venue is located in:', validators=[DataRequired()])
    capacity = IntegerField('Venue capacity during a gig:')
    venue_pic = FileField('Upload venue main photo:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('UPDATE')

    def validate_venuename(self, name):
        if name.data != venue.name:
            venue = Venue.query.filter_by(name=name.data).first()
            if venue:
                raise ValidationError('That venue is already in the database.')

class NewFestivalForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    founded = IntegerField('Year Founded:', validators=[DataRequired()])
    is_active = SelectField('Is the festival active?', choices=[('Active', 'Yes'), ('Not Active', 'No')])
    street_name = StringField('Street Name:')
    street_number = IntegerField('Street Number:')
    unit_number = IntegerField('Unit Number:')
    postal_code = StringField('Postal Code:')
    phone_number = StringField('Phone Number:')
    website = StringField('Website:', validators=[URL()])
    twitter = StringField('twitter account name:', validators=[URL()])
    facebook = StringField('facebook link:', validators=[URL()])
    instagram = StringField('Instagram account name:', validators=[URL()])
    city = StringField('City the festival is located in:', validators=[DataRequired()])
    province = SelectField('Province:', choices=[('BC', 'British Columbia'), ('AB', 'Alberta'), ('SK', 'Saskatchewan'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ('NB', 'New Brunswick'), ('NS', 'Nova Scotia'), ('PE', 'Prince Edward Island'), ('NL', 'Newfoundland'), ('YT', 'Yukon'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut')])
    country = StringField('Country:', validators=[DataRequired()])
    capacity = IntegerField('Festival capacity during a gig:')
    logo = FileField('Upload festival logo:', validators=[FileAllowed(['jpg', 'png'])])
    festival_pic = FileField('Upload festival main photo:', validators=[FileAllowed(['jpg', 'png'])])
    grounds_map = FileField('Upload festival grounds map:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('SUBMIT')

    def validate_name(self, name):
        festival = Festival.query.filter_by(name=name.data).first()
        if festival:
            raise ValidationError('That festival has already been submitted to the database.')

class UpdateFestivalForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    founded = IntegerField('Year Founded:', validators=[DataRequired()])
    is_active = SelectField('Is the festival active?', choices=[('Active', 'Yes'), ('Not Active', 'No')])
    street_name = StringField('Street Name:')
    street_number = IntegerField('Street Number:')
    unit_number = IntegerField('Unit Number:')
    postal_code = StringField('Postal Code:')
    province = SelectField('Province:', choices=[('BC', 'British Columbia'), ('AB', 'Alberta'), ('SK', 'Saskatchewan'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec'), ('NB', 'New Brunswick'), ('NS', 'Nova Scotia'), ('PE', 'Prince Edward Island'), ('NL', 'Newfoundland'), ('YT', 'Yukon'), ('NT', 'Northwest Territories'), ('NU', 'Nunavut')])
    country = StringField('Country:', validators=[DataRequired()])
    phone_number = StringField('Phone Number:')
    website = StringField('Website:', validators=[URL()])
    twitter = StringField('twitter account name:', validators=[URL()])
    facebook = StringField('facebook link:', validators=[URL()])
    instagram = StringField('Instagram account name:', validators=[URL()])
    city = StringField('City the festival is located in:', validators=[DataRequired()])
    capacity = IntegerField('Festival capacity during a gig:')
    logo = FileField('Upload festival logo:', validators=[FileAllowed(['jpg', 'png'])])
    festival_pic = FileField('Upload festival main photo:', validators=[FileAllowed(['jpg', 'png'])])
    grounds_map = FileField('Upload festival grounds map:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('UPDATE')

    def validate_festivalName(self, name):
        if name.data != festival.name:
            festival = Festival.query.filter_by(name=name.data).first()
            if festival:
                raise ValidationError('That festival is already in the database.')

class ThreadForm(FlaskForm):
    title = StringField('Title of post:', validators=[DataRequired()])
    text = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('POST')

class RequestResetForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('SEND EMAIL')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('RESET')