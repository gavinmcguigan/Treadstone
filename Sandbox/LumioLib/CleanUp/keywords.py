from LumioLib.CleanUp.SalesForceAPI import SalesForceAPI
from LumioLib.CleanUp.StripeAPI import _StripeClientManager
from typing import List, Union 
from robot.api import logger



def salesforce_cleanup_for_user_id(user_account_id, really_delete=False):
    """ 
        Args: user_account_id, really_delete
        Returns: None 
        
        Calls the salesforce api and deletes OR displays the data for the user account passed in. 

        Default value for really_delete is False which means it will only show data by default.  To 
        delete pass in True. 

        To get the user_account_id for a user, try the following keywords. 

        ${accessToken}=                     Application Access Token For Scopes With Google Login    ${supportadmin_email}    ${supportadmin_password}    ${env}    ${account crud} entitlement.write entitlement&force_refresh=true    ${TRUE}  
        Set Suite Variable                  ${accessToken}
        ${test_account_id}=                 Get User Id From Email API    ${email_account}    ${accessToken}
    """
    sfapi = SalesForceAPI()
    sfapi.cleanup(user_account_id, really_delete)

def stripe_get_customers_on_all_accounts(list_of_emails: Union[List[str], str]) -> None:
    """ Logs all customers in both 'SMART_TEST_ULC' and 'SMART_TEST_CORP' 
        args: list_of_emails -> can be list of strings or single string (email address)
    """
    _StripeClientManager.get_customers_on_all_accounts(list_of_emails)

def stripe_show_customer_by_id(cust_id: str) -> None:
    """ Takes in a customer id and checks if it exists on all registerd stripe accounts. """
    _StripeClientManager.get_customer_by_id(cust_id)

def stripe_delete_customer_by_email_and_country(email: str, country: str) -> None:
    """ Deletes customers with passed in email from the Stripe account mapped to the country passed in. """
    _StripeClientManager.delete_customer_by_email_and_country(email, country)

def stripe_delete_customer_by_email_and_stripe_account(email: str, stripe_account: str) -> None:
    """ Deletes customers with passed in email from passed in Stripe account.  """
    _StripeClientManager.delete_customer_by_email_and_stripe_account(email, stripe_account)
    
def stripe_delete_customers_on_all_accounts(list_of_emails: Union[List[str], str]) -> None:
    """ Deletes all records of the account(s) in both 'SMART_TEST_ULC' and 'SMART_TEST_CORP' 
        args: list_of_emails -> can be list of strings or single string (email address)
    """
    _StripeClientManager.delete_customers_from_all_stripe_accounts(list_of_emails)
    

def test_keyword():
    from time import sleep
    for i in range(10):
        print(i)
        sleep(0.5)

def run_tests():
    from LumioLib.PurchaseForm.accounts import PurchaseAccounts
    import logging 
    logging.getLogger('RobotFramework').setLevel(logging.DEBUG)
    logging.debug('Start')
    cust_id = 'cus_KCDoyjPwCU4HHJ'
    # stripe_get_customers_on_all_accounts(PurchaseAccounts)
    stripe_show_customer_by_id(cust_id=cust_id)    
    
    # stripe_delete_customer_by_email_and_country("slso.purchase.ca@smartwizardschool.com", "CANADA")
    # stripe_delete_customer_by_email_and_stripe_account("slso.purchase.ca@smartwizardschool.com", "SMART_TEST_ULC")
    # stripe_delete_customers_on_all_accounts(PurchaseAccounts)

if __name__ == "__main__":
    run_tests()