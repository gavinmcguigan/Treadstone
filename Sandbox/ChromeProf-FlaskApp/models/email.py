from db import db 
from datetime import datetime 

class EmailModel(db.Model):
    __tablename__ = 'emails'

    account_id = db.Column(db.Integer, primary_key=True)
    account_email = db.Column(db.String(120))
    zip_filename = db.Column(db.String(120))
    machine_name = db.Column(db.String(80))
    uploads = db.Column(db.Integer)
    downloads = db.Column(db.Integer)
    created = db.Column(db.String(50))
    updated = db.Column(db.String(50))

    def __init__(self, account_email, zip_filename, machine_name, uploads=0, downloads=0):
        self.account_email = account_email 
        self.zip_filename = zip_filename
        self.machine_name = machine_name 
        self.uploads = uploads
        self.downloads = downloads
        self.created = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.updated = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    @classmethod
    def find_by_account_and_machine(cls, account_email, machine_name):
        return cls.query.filter_by(machine_name=machine_name).filter_by(account_email=account_email).first()

    @classmethod 
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        self.updated = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'account_email': self.account_email,
                'zip_filename': self.zip_filename,
                'machine_name': self.machine_name,
                'created': self.created,
                'updated': self.updated,
                'uploads': self.uploads,
                'downloads': self.downloads }
