import json 
import pprint
import requests

json_file = "api.json"
pp = pprint.PrettyPrinter(indent=4)
UPLOAD_URL_ENDPOINT = 'http://127.0.0.1:5002'

def read_in_json():
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    
    except IOError as ioe:
        print(f"Failed to read from config file: {ioe}")
        return {}
    except json.decoder.JSONDecodeError as jde:
        print(f"Json decode error: {jde}")
        return {}
    else:
        return data.get('Emails', [])


def send_request(email_obj):
    pp.pprint(email_obj)

    email = email_obj.get('account_email')
    downloads = email_obj.get('downloads')
    uploads = email_obj.get('uploads')
    machine_name = email_obj.get('machine_name')
    zip_filename = email_obj.get('zip_filename')
    created = email_obj.get('created')

    params = {'created': created, 
              'email': email, 
              'downloads': downloads,
              'uploads': uploads, 
              'machine_name': machine_name, 
              'zip_filename': zip_filename}


    r = requests.put(url=f"{UPLOAD_URL_ENDPOINT}/email/{email}", params=params)
    print(r.status_code)

def main():
    for email_obj in read_in_json():
        send_request(email_obj)
         




if __name__ == "__main__":
    main()