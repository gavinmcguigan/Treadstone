import requests
import os
from lib import download_chrome_profile, upload_chrome_profiles

folders_emails = [('Australia', 'slso.purchase.aus@smartwizardschool.com'), 
                  ('UK', 'slso.purchase.uk@smartwizardschool.com'), 
                  ('USA', 'slso.purchase.us@smartwizardschool.com'), 
                  ('Canada', 'slso.purchase.ca@smartwizardschool.com')]

# ------------------------- Test functions -------------------------
def post_all_profiles():
    for folder, email in folders_emails:
        upload_chrome_profiles(folder, email)

def get_all_profiles():
    for _, email in folders_emails:
        download_chrome_profile(email)


if __name__ == "__main__":
    get_all_profiles()
