from flask_restful import Resource, request
from flask import Response
from werkzeug.utils import secure_filename 
from flask import send_file
from os import path, remove
from pathlib import Path 
from models.email import EmailModel
# import logging
from flask import current_app

# logger = logging.getLogger('werkzeug')

ALLOWED_EXTENSIONS = ['zip']
PROFILE_FOLDER = path.join(Path(path.dirname(path.realpath(__file__))).parent.absolute(), 'static')

class ProfileZip(Resource):
    def get(self):
        email, machine_name, zip_file, zip_file_path = self.get_parameters()

        email_obj = EmailModel.find_by_account_and_machine(email, machine_name)
        if not email_obj:
            return {"message": f"Bad request"}
            
        email_obj.downloads += 1
        email_obj.save_to_db()
        
        if path.exists(zip_file_path):
            return send_file(zip_file_path)
            # return send_from_directory(zip_file, '.')
        else:
            return {"message": f"Zip file {zip_file} doesn't exist."}, 404

    def post(self):
        email, machine_name, zip_file, _ = self.get_parameters()

        if email and machine_name:
            filename = secure_filename(zip_file)
            where_to_save = path.join(PROFILE_FOLDER, filename)

            current_app.logger.debug(request.headers)
            filelength = 0  
            with open(where_to_save, 'wb+') as zipfile:
                while True:
                    chunk = request.stream.read(2048)
                    if not len(chunk):
                        break 
                    
                    filelength += len(chunk)
                    zipfile.write(chunk)

            email_obj = EmailModel.find_by_account_and_machine(email, machine_name)
            if email_obj:
                email_obj.folder = filename
            else:
                email_obj = EmailModel(email, filename, machine_name)

            email_obj.uploads += 1                
            email_obj.save_to_db()
            return {'Success': f"Received '{filename}' ({filelength/1000/1000:0.2f} Mbs) okay."}

        return {'Error': "Invalid Post Request."}, 400

    def working_post(self):
        email, machine_name, _, _ = self.get_parameters()
        f = request.files.get('file')
        current_app.logger.debug(f)
        current_app.logger.debug(request.headers)
        if f and email and machine_name:
            filename = secure_filename(f.filename)
            where_to_save = path.join(PROFILE_FOLDER, filename)
            f.save(where_to_save)

            email_obj = EmailModel.find_by_account_and_machine(email, machine_name)
            if email_obj:
                email_obj.folder = filename
            else:
                email_obj = EmailModel(email, filename, machine_name)

            email_obj.uploads += 1                
            email_obj.save_to_db()
            return {'Success': f"Zip File Received"}

        return {'Error': "Invalid Post Request."}, 400

    def delete(self):
        _, _, zip_file, zip_file_path = self.get_parameters()
        if zip_file:
            try:
                if path.exists(zip_file_path):
                    remove(zip_file_path)

            except PermissionError as pe:
                return {'Error': f"{pe}"}

            else:
                return {f"Success": f"{zip_file} removed."}

        return {f"Error": f"parameter 'zip_file' must be included. "}
    
    def get_parameters(self):
        email = request.args.get('email')
        machine_name = request.args.get('machine_name')
        zip_file = request.args.get('zip_file', '')
        zip_file_path = path.join(PROFILE_FOLDER, zip_file)
        # current_app.logger.debug(f'{50*"-"}')
        # current_app.logger.debug(f"email:          {email}")
        # current_app.logger.debug(f"machine_name:   {machine_name}")
        # current_app.logger.debug(f"zip_file:       {zip_file}")
        # current_app.logger.debug(f"zip_file_path:  {zip_file_path}")

        return email, machine_name, zip_file, zip_file_path