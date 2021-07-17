from flask_restful import Resource, reqparse, request
from models.email import EmailModel


class Email(Resource):
    def get(self, email):
        machine_name = request.args.get('machine_name')
        email_obj = EmailModel.find_by_account_and_machine(email, machine_name)
        if email_obj:
            return email_obj.json()
        return {"message": f"Email: {email} doesn't exist."}, 404

    def post(self, email):
        zip_filename = request.args.get('zip_file')
        machine_name = request.args.get('machine_name')
        if not machine_name:
            return {'message': "'machine_name' parameter is required. "}

        email_obj = EmailModel.find_by_account_and_machine(email, machine_name)
        if email_obj:
            return {'message': f'Entry for email + machine name already exists.'}

        email_obj = EmailModel(email, zip_filename, machine_name)
        try:
            email_obj.save_to_db()
        except:
            return {'message': 'An error occurred while creating the account!'}

        return {'Created': email_obj.json()}

    def put(self, email):
        zip_filename = request.args.get('zip_filename')
        machine_name = request.args.get('machine_name')
        downloads = request.args.get('downloads', 0)
        uploads = request.args.get('uploads', 0)
        created = request.args.get('created')

        email_obj = EmailModel.find_by_account_and_machine(email, machine_name)
        if not email_obj:
            email_obj = EmailModel(email, zip_filename, machine_name, uploads, downloads)
        else:
            email_obj.zip_filename = zip_filename
            email_obj.machine_name = machine_name
            email_obj.downloads = downloads if downloads else email_obj.downloads  
            email_obj.uploads = uploads if uploads else email_obj.uploads
            email_obj.created = created if created else email_obj.created
        
        try:
            email_obj.save_to_db()
        except:
            return {'message': f'An error occurred while updating {email}!'}

        return {'Updated': email_obj.json()}

    def delete(self, email):
        email_obj = EmailModel.find_by_account_and_machine(email, request.args.get('machine_name'))
        if email_obj:
            email_obj.delete_from_db()
            return email_obj.json()

        return {'message': f"{email} doesn't exist"}, 404


class Emails(Resource):
    def get(self):
        return {"Emails": [email.json() for email in EmailModel.find_all()]}
