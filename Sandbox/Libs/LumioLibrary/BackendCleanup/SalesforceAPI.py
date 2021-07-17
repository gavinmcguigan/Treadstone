# 1. Loads the credentials from the the json file and logs in with them. 
import requests 
import logging 
import xml.dom.minidom


class SalesForceAPI:
    def __init__(self):
        self.sf_version = '40.0'
        # self.session = requests.Session() 
        # self.proxies = self.session.proxies 
        
        self.username = "smartpdtest@smarttech.com.training" 
        self.password = "pdtest123" 
        # self.security_token = "juGEIFpmSAAkqvPa8yZDQE1Z" 
        self.security_token = "yBkd1UCmXzmV8ZCcSZwSpcMG" 
        self.session_id = None 
        self.instance = None 
        self.instance_url = None 
        self.refresh_token = None 
        self.consumer_id = None
        self.consumer_secret = None 
        self.organizationId = None 
        self.client_id = 'test'
         
        self.session = requests.Session() 
        self.proxies = self.session.proxies

        self.sandbox = True
        self.auth_site = 'https://test.salesforce.com' if self.sandbox else 'https://login.salesforce.com'

        # needs the session id from the login
        self.headers = None 

        # set after login
        self.base_url = None 
        self.apex_url = None 
        self.bulk_url = None 

        # For queries 
        self.requester = requests.Session()

        self.sf_instance = None
        self.session_id = None 
        self.account_c = None

        self.delete_dict = {}

    def getUniqueElementValueFromXmlString(self, xmlString, elementName):
        """
        Extracts an element value from an XML string.

        For example, invoking
        getUniqueElementValueFromXmlString(
            '<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>', 'foo')
        should return the value 'bar'.
        """
        xmlStringAsDom = xml.dom.minidom.parseString(xmlString)
        elementsByName = xmlStringAsDom.getElementsByTagName(elementName)
        elementValue = None
        if len(elementsByName) > 0:
            elementValue = elementsByName[0].toxml().replace(
                '<' + elementName + '>', '').replace('</' + elementName + '>', '')
        return elementValue

    def cleanseInstanceUrl(self, instance_url):
        """Remove some common/likely noise from an instance url"""
        return (instance_url
                .replace('http://', '')
                .replace('https://', '')
                .split('/')[0]
                .replace('-api', ''))

    def login_to_salesforce(self):
        client_id = f"RestForce/{self.client_id}" if self.client_id else "RestForce"       
        domain = 'test' if self.sandbox else 'login'
        soap_url = f'https://{domain}.salesforce.com/services/Soap/u/{self.sf_version}'
        rest_url = f'https://{domain}.salesforce.com/services/oauth2/token'
        

        soap_body =  f"""<?xml version="1.0" encoding="utf-8" ?>
                        <env:Envelope
                                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
                                xmlns:urn="urn:partner.soap.sforce.com">
                            <env:Header>
                                <urn:CallOptions>
                                    <urn:client>{client_id}</urn:client>
                                    <urn:defaultNamespace>sf</urn:defaultNamespace>
                                </urn:CallOptions>
                            </env:Header>
                            <env:Body>
                                <n1:login xmlns:n1="urn:partner.soap.sforce.com">
                                    <n1:username>{self.username}</n1:username>
                                    <n1:password>{self.password}{self.security_token}</n1:password>
                                </n1:login>
                            </env:Body>
                        </env:Envelope>"""
        
        soap_headers = {
            'content-type': 'text/xml',
            'charset': 'UTF-8',
            'SOAPAction': 'login'
        }

        print(f'Salesforce Login....', end=' ')
        response = self.session.post(soap_url, soap_body, headers=soap_headers, proxies=self.proxies)
        print('Ok' if response.status_code == 200 else 'Fail')
        if response.status_code != 200:
            # print(response.content)
            # print(response.status_code)
            faultcode = self.getUniqueElementValueFromXmlString(response.content, 'faultstring')
            print(faultcode)
            return 

        self.session_id = self.getUniqueElementValueFromXmlString(response.content, 'sessionId')
        server_url = self.getUniqueElementValueFromXmlString(response.content, 'serverUrl')

        self.sf_instance = self.cleanseInstanceUrl(server_url)

        self.base_url = f'https://{self.sf_instance}/services/data/v{self.sf_version}/'
        self.apex_url = f'https://{self.sf_instance}/services/apexrest/'
        self.bulk_url = f'https://{self.sf_instance}/services/async/{self.sf_version}/'

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.session_id,
            'X-PrettyPrint': '1'}
        
        return True

    def query(self, query, start=False, **kwargs):
        url = self.base_url + 'query/'
        params = {'q': query}

        # `requests` will correctly encode the query string passed as `params`
        # result = self._call_salesforce('GET', url, params=params, **kwargs)
        # querylen = len(query)
        # if querylen > 77:
        #     displayquery = f"{query[:74]}..."
        # else:
        #     displayquery = f"{query}{(74-querylen)*'.'}..."

        print(f"{query[:73]}..." if len(query) > 73 else f"{query}{(73-len(query))*'.'}...", end=' ')
        

        # print(f"{query[:73]}..." if len(query) > 70 else f"{query}...", end=' ')

        # print(f"GET -> {url}", end=' ')

        response = self.requester.request('GET', url, params=params, headers=self.headers, **kwargs)
        print('Ok' if response.status_code < 300 else response.status_code)

        return response.json() if response.status_code == 200 else {}

    def _call_salesforce(self, method, url, **kwargs):
        retries_remaining = 1
        while retries_remaining >= 0:
            retries_remaining -= 1

            # Make the call
            result = self.requester.request(method, url, headers=self.headers, **kwargs)

            # If we had trouble
            # if result.status_code >= 300:

            #     # Was it an expired session error AND do we have what we need
            #     # to attempt a refresh?
            #     if result.status_code == RESPONSE_CODE_EXPIRED_SESSION \
            #         and self.auth_type == AUTH_TYPE_DIRECT_WITH_REFRESH:

            #         # Let's try to refresh the access_token
            #         session_id, sf_instance = SalesforceLogin(
            #             refresh_token=self.refresh_token,
            #             consumer_id=self.consumer_id,
            #             consumer_secret=self.consumer_secret)

            #         # If it looks like things went well:
            #         if session_id and sf_instance:
            #             # Store the new session ID and rebuild the headers
            #             # to use it
            #             self.session_id = session_id
            #             self._build_headers()
            #             # Replace the old instance URL with the new one for this
            #             # call and then store it internally for future calls
            #             url = url.replace(self.sf_instance, sf_instance)
            #             self.sf_instance = sf_instance

            #             # Continue through the loop again, hopefully
            #             # with success
            #             continue

            #     # If we got here, it's a plain fat old exception
            #     _exception_handler(result)

            # All good, so return the result
            return result

    def queries(self, account_id):
        print('\nQueries')
        print(f"{80*'*'}")

        delete_dict = {}
        q = f"SELECT Account__c from Related_System_ID__c where Source_System_Name_Field__c = 'SMART ID' and Source_System_ID__c = '{account_id}'"
        result = self.query(q)

        accounts = [d.get('Account__c') for d in result.get('records', {})]
        if accounts:
            self.account_c = accounts[0]
            delete_dict[9] = {'url_addon': 'Account', 'items': accounts}
        else:
            print(f"No accounts found with id: {account_id}")
            return 

        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/Account/0010100000BE2YXAA1

        # Assets for Account_c
        # print(f'\n------------------------------ Get list of Asset Ids ------------------------------ ')
        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/Asset/02i01000000ep14AAA
        result = self.query(f"SELECT ID from Asset where AccountId = '{self.account_c}'")
        assetids = [d.get('Id') for d in result.get('records', {})]
        delete_dict[2] = {'url_addon': 'Asset', 'items': assetids}

        # print(f'\n------------------------------ Get list of Contract Line Items -------------------- ')
        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/ContractLineItem/81101000000UsHPAA0
        contractlineitems = []
        for aid in assetids:
            result = self.query(f"SELECT ID from ContractLineItem where AssetId = '{aid}'")
            for r in [d.get('Id') for d in result.get('records', {})]:
                contractlineitems.append(r)
        delete_dict[0] = {'url_addon': 'ContractLineItem', 'items': contractlineitems}

        # print(f'\n------------------------------ Get list of Order Line Assets --------------------- ')
        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/Sales_Order_Line_Asset__c/a1801000000HdpyAAC
        orderlineassets = []
        for aid in assetids:
            result = self.query(f"SELECT ID from Sales_Order_Line_Asset__c where Asset__c = '{aid}'")
            for r in [d.get('Id') for d in result.get('records', {})]:
                orderlineassets.append(r)
        delete_dict[1] = {'url_addon': 'Sales_Order_Line_Asset__c', 'items': orderlineassets}


        # print(f'\n------------------------------ Get Order ----------------------------------------- ')
        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/Order/80101000000JwWKAA0
        result = self.query(f"SELECT ID from Order where AccountId ='{self.account_c}'")
        orders = [d.get('Id') for d in result.get('records', {})]
        delete_dict[4] = {'url_addon': 'Order', 'items': orders}

        # print(f'\n------------------------------ Get ServiceContract ------------------------------- ')
        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/ServiceContract/81001000000DunIAAS
        result = self.query(f"SELECT ID from ServiceContract where AccountId = '{self.account_c}'")
        servicecontracts = [d.get('Id') for d in result.get('records', {})]
        delete_dict[3] = {'url_addon': 'ServiceContract', 'items': servicecontracts}

        # print(f'\n------------------------------ Get Portal_Group ---------------------------------- ')
        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/Portal_Group__c/a1C01000000K2bjEAC
        result = self.query(f"SELECT ID from Portal_Group__c where Account__c = '{self.account_c}'")
        portalgroups = [d.get('Id') for d in result.get('records', {})]
        delete_dict[5] = {'url_addon': 'Portal_Group__c', 'items': portalgroups}

        # print(f'\n------------------------------ Get Related_System_Id ----------------------------- ')
        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/Related_System_ID__c/a3401000000L5QyAAK
        result = self.query(f"SELECT ID from Related_System_ID__c where Account__c = '{self.account_c}'")
        related_system_ids = [d.get('Id') for d in result.get('records', {})]
        delete_dict[6] = {'url_addon': 'Related_System_ID__c', 'items': related_system_ids}

        # print(f'\n------------------------------ Get Contract ------------------------------- ')
        #  https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/Contact/0030100000A502lAAB
        result = self.query(f"SELECT ID from Contact where AccountId = '{self.account_c}'")
        contracts = [d.get('Id') for d in result.get('records', {})]
        delete_dict[7] = {'url_addon': 'Contact', 'items': contracts}


        # print(f'\n------------------------------ Get Account_Address ------------------------------- ')
        # https://smarttechnologies--training.my.salesforce.com/services/data/v40.0/sobjects/Account_Address__c/a1501000000H5w6AAC
        result = self.query(f"SELECT ID from Account_Address__c where Account__c = '{self.account_c}'")
        account_addresses = [d.get('Id') for d in result.get('records', {})]
        delete_dict[8] = {'url_addon': 'Account_Address__c', 'items': account_addresses}

        # self._delete_all(del_dict=delete_dict)

        self.delete_dict = delete_dict

    def _delete_all(self, **kwargs):
        for n in range(len(self.delete_dict)):
            v = self.delete_dict[n]
                        
            # print(f'\n{100*"-"}')
            # print(f"{n}. {v['url_addon']:<30}   {len(v['items'])}")
            # print(f"{n}. {query[:73]}..." if len(query) > 73 else f"{query}{(73-len(query))*'.'}...", end=' ')


            for item in v['items']:
                self.delete_dict['delete_results'] = []

                url = f"{self.base_url}sobjects/{v['url_addon']}/{item}"
    
                # print(f"{url}", end=' ')
                print(f"{url[-73:]}..." if len(url) > 73 else f"{url}{(73-len(url))*'.'}...", end=' ')
                

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.session_id,
                    'X-PrettyPrint': '1'
                }
                additional_headers = kwargs.pop('headers', dict())
                headers.update(additional_headers or dict())
                response = self.session.request('DELETE', url, headers=headers, **kwargs)
                print('Ok' if response.status_code < 300 else 'Fail')

        self.delete_dict = {}

    def show_results(self):
        print('\nResults')
        print(f"{80*'*'}")
        for n in range(len(self.delete_dict)):
            print(f"{n:<8} {self.delete_dict[n]['url_addon']:<40}  Entries:  {len(self.delete_dict[n]['items'])}")


# Keywords start here. 
def Cleanup_Salesforce_For_User_Id(user_account_id, really_delete=False):
    sfapi = SalesForceAPI()
    if sfapi.login_to_salesforce():
        sfapi.queries(account_id=user_account_id)
        if really_delete:
            print(f"Deleting everything")
            sfapi._delete_all()
        else:
            print(f" --- Showing results only --- ")
            sfapi.show_results()
    

def TestFunctionSalesForceAPI(user_account_id, really_delete=False):
    print('Test Function')
    print(user_account_id, type(user_account_id))
    print(really_delete, type(really_delete))
    if really_delete:
        print('Deleting everything!!!')
    else:
        print('Showing results.')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, 
                        format='%(levelname)-7s %(asctime)s : %(lineno)-5d > %(message)s',
                        datefmt="%d-%b-%y %H:%M:%S")   
    logger = logging.getLogger("RobotFramework")
    # Cleanup_Salesforce_For_User_Id('9b6802a5-18ac-486c-aec0-d66a940a89ab')  # Teacher
    # Cleanup_Salesforce_For_User_Id('454ee5f0-2f01-4207-956b-58faa7c090ca')  # Student 1
    salesforce_cleanup_for_user_id(user_account_id='e5be8e9e-341b-4955-a6fa-76a3761e8db9')  # Student 2