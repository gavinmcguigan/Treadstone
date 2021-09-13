# from .RequestHandler import get, delete
from LumioLib.CleanUp.RequestHandler import get, delete
import os 
import functools
from robot.api import logger
 

""" 
StripeAPI Library:

"""

class _StripeClient:
    """ Stripe Client object responsible for all calls to the Stripe API. """
    def __init__(self, stripe_account: str, stripe_key: str):   
        self.endpoint = "https://api.stripe.com/v1/customers"
        self.account = stripe_account 
        self.secret_key = stripe_key       
        self.customers = {}
        
    def _set_customers_by_email(self, email: str):
        """ Repeatedly call endpoint (until has_more == false) passing email as a parameter, then append to the self.customers 
        variable {email: [list, of, customers]}.  """
        params = {'limit': 100, 'starting_after': {}, 'email': email}
        logger.info("Checking Stripe Account: {} for email: {}".format(self.account, email))
        while True:
            r, js  = get(url=self.endpoint, auth=(self.secret_key, ""), params=params)
            if r.status_code == 200:
                data = js.get('data', [])
                logger.info("Customers found: {}".format(len(data)))
                for customer in data:
                    customer_id = customer.get('id', None)
                    if customer_id:
                        self.customers[customer_id] = customer
                        params['starting_after'] = customer_id
            else:
                logger.info(js)
            
            if not js.get('has_more', False):
                break 

    def get_customer_by_id(self, customer_id: str):
        """ Check if we already have this customer id, if so log it, 
        else call get method with the id and update customers if we get anything back. """
        logger.info(f"Checking for {customer_id} on Stripe account: {self.account}")
        customer = self.customers.get(customer_id, None)
        if customer:
            logger.info(f"{customer}")
            return True 
        else:
            r, js = get(url=f"{self.endpoint}/{customer_id}", auth=(self.secret_key, ""))
            if r.status_code == 200:
                self.customers[customer_id] = js
                logger.info(f"{js}")
                return True 
            else:
                logger.info(r.status_code)
                logger.info(js)

    def get_customers_by_email(self, email: str):
        self._set_customers_by_email(email)
        for n, cust_id in enumerate(self.customers):
            if self.customers[cust_id].get("email") == email:
                logger.info(f"{n+1:<3} {cust_id}")
        logger.info("")
        
    def delete_customers_by_email(self, email: str):
        """ Delete all customers on this stripe account with this email. """
        self._set_customers_by_email(email) 
        delete_after = []
        for customer_id, customer_data in self.customers.items():
            if customer_data.get('email', None) == email:
                r, _ = delete(url=f"{self.endpoint}/{customer_id}", auth=(self.secret_key, ""))
                if r.status_code == 200:
                    delete_after.append(customer_id)
        
        for customer_id in delete_after:
            self.customers.pop(customer_id)
        
        logger.info("")

    def __str__(self) -> str:
        return self.account

class _StripeClientManager:
    """ Stripe Client Manager object responsible for create StripeClient objects.  """
    def __init__(self):
        self.clients = {}
        self.set_all_available_clients()      # Not recommended
        # self.set_stripe_clients()               # Recommended

    def set_all_available_clients(self):
        """ Not recommended:  """
        stripe_account_secret_keys = {
                "SMART_TEST_ULC": "sk_test_51HN4ePBIfmR0J8RSv9yFJBMrQiTHUqt7MjcmZgRzfSTJH117qdauTnmdah5W6nHgnMCmM4W1CVTcKRrtWUPUGK7D007YrOoqtD",
                "SMART_TEST_CORP": "sk_test_51H78kFFCLKlKjWryZkwbBFU4tbiGNGdCd30uc4l8FfgMc0IaPcuM5X5wTLghwYHuSHF1ApF88P9SwIS8n2vmQTsy00FKmtyqPF",
             }
        for account, secret_key in stripe_account_secret_keys.items():
            self.clients.setdefault(account, _StripeClient(account, secret_key))

    def set_stripe_clients(self):
        """ Recommended: (Not used)  """
        accounts = ["SMART_TEST_ULC", "SMART_TEST_CORP"]
        
        # Get the secret keys from this systems global enviroment variables. 
        for account in accounts:
            key = os.getenv("{}_SECRET_KEY".format(account))
            if key:
                self.clients.setdefault(account, _StripeClient(account, key))

    def reset_clients(self):
        self.clients = {}
    
    def show_clients(self):
        """ Log the clients created, based on the keys found. 
        Client class will just log the account name for the client. """
        for _account, client in self.clients.items():
            logger.info(client)

    def get_stripe_client_for_account(self, account: str):
        """ Return the client with the passed in account name, None if not found. """
        return self.clients.get(account, None)

    def get_all_clients(self):
        """ Returns all stripe api clients created. """
        return [v for _k, v in self.clients.items()]

    def get_client_for_country(self, country: str):
        """ Returns the stripe client for passed in country, or None if not found. 
        Countries for slso accounts use different back end stripe accounts. """
        country = country.upper()
        countries = {
            'CANADA': "SMART_TEST_ULC",
            'USA': "SMART_TEST_CORP",
            'AUSTRALIA': "SMART_TEST_ULC",
            'UK':  "SMART_TEST_ULC"}
        return self.get_stripe_client_for_account(countries.get(country, ''))

    def _pretty_decorator(func):
        def wrapper(self, *args, **kwargs):
            logger.info(f"{100*'-'}")
            result = func(self, *args, **kwargs)
            logger.info(f"{100*'-'}")
            return result
        return wrapper 

    @_pretty_decorator
    def get_customers_on_all_accounts(self, email_list):
        for email in email_list if isinstance(email_list, list) else [email_list]:
            for client in self.get_all_clients():
                client.get_customers_by_email(email)

    @_pretty_decorator
    def get_customer_by_id(self, cust_id):
        for client in self.get_all_clients():
            if client.get_customer_by_id(cust_id):
                break

    def delete_customer_by_email_and_country(self, email, country):
        logger.info(f"{100*'-'}")
        logger.info(f"Country: '{country}'")
        logger.info(f"Email: '{email}'")
        client = self.get_client_for_country(country)
        if client:
            client.delete_customers_by_email(email)
        else:
            # stripe_delete_customer_from_all_stripe_accounts(email)    
            raise NotImplementedError("Country: '{}' not yet implemented. Please update the _StripeClientManager class.".format(country))
        logger.info(f"{100*'-'}")

    def delete_customer_by_email_and_stripe_account(self, email, stripe_account):
        logger.info(f"{100*'-'}")
        logger.info(f"Stripe Account: '{stripe_account}'")
        logger.info(f"Email: {email}")
        client = self.get_stripe_client_for_account(stripe_account)
        if client:
            client.delete_customers_by_email(email)
        else:
            raise LookupError("Stripe account: '{}' not found! ")
        logger.info(f"{100*'-'}")

    def delete_customers_from_all_stripe_accounts(self, list_of_emails):
        logger.info(f"{100*'-'}")
        logger.info(f"Email(s): {str(list_of_emails)}")
        available_clients = self.get_all_clients()
        for email in list_of_emails if isinstance(list_of_emails, list) else [list_of_emails]:
            for client in available_clients:
                client.delete_customers_by_email(email)
        logger.info(f"{100*'-'}")
 

StripeClientManager = _StripeClientManager() 


# Not used, yet!
def stripe_client_mgr_inst(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(_StripeClientManager(*args, **kwargs))
    return wrapper 

