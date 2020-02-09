import os
import secrets
import PIL
from PIL import Image
from app import app

def save_profile_pic(form_picture, user):
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = user.username + '_pic_' + random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/uploads/users/{user.username}/imgs', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

def save_band_logo(form_picture, band):
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = band.username + '_logo_' + random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/uploads/bands/{band.username}/logo/', picture_fn)
    basewidth = 300
    i = Image.open(form_picture)
    wpercent = (basewidth / float(i.size[0]))
    hsize = int((float(i.size[1]) * float(wpercent)))
    i.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    i.save(picture_path)
    
    return picture_fn

def save_band_pic(form_picture, band):
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = band.username +'_pic_' + random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/uploads/bands/{band.username}/imgs/', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    
    return picture_fn

def save_venue_pic(form_picture, venue):
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = venue.name + '_pic_' + random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/uploads/venues/{venue.username}/imgs/', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    
    return picture_fn

def save_festival_logo(form_picture, festival):
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = festival.name + '_logo_' + random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/uploads/festivals/{festival.username}/logo/', picture_fn)
    basewidth = 300
    i = Image.open(form_picture)
    wpercent = (basewidth / float(i.size[0]))
    hsize = int((float(i.size[1]) * float(wpercent)))
    i.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    i.save(picture_path)
    
    return picture_fn

def save_festival_pic(form_picture, festival):
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = festival.name +'_pic_' + random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/uploads/festivals/{festival.username}/imgs/', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    
    return picture_fn

def save_grounds_pic(form_picture, festival):
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = festival.name +'_pic_' + random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/uploads/festivals/{festival.username}/imgs/', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    
    return picture_fn