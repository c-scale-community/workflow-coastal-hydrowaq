import os
from datetime import datetime
from coastserv import db
from flask import current_app

class Model(db.Model):
    id       = db.Column(db.Integer, primary_key = True)
    name     = db.Column(db.String(100), nullable = False)
    tstart   = db.Column(db.String(100), nullable = False)
    tend     = db.Column(db.String(100), nullable = False)
    tref     = db.Column(db.String(100), nullable = False)
    xmin     = db.Column(db.String(100), nullable = False, default = -1)
    xmax     = db.Column(db.String(100), nullable = False, default = 1)
    ymin     = db.Column(db.String(100), nullable = False, default = -1)
    ymax     = db.Column(db.String(100), nullable = False, default = 1)
    pli_file = db.Column(db.String(255), default = 'default.jpg')
    dataset  = db.Column(db.String(100), nullable = False)
    user     = db.Column(db.String(100), nullable = False)

