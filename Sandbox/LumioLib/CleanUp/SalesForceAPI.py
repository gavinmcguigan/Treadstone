# 1. Loads the credentials from the the json file and logs in with them. 
import requests 
import xml.dom.minidom
from robot.api import logger

# **************** LOGIN CREDENTIALS ****************
USERNAME, PASSWORD, TOKEN = "smartpdtest@smarttech.com.training", "pdtest123", "yBkd1UCmXzmV8ZCcSZwSpcMG" 
   
class SalesForceAPI:
    def __init__(self): 
        self.username = USERNAME 
        self.password = PASSWORD 
        self.security_token = TOKEN
        self.sf_version = '40.0'    
        self.headers = None 
        self.session = requests.Session() 
        self.base_url = None 
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

    def login_to_salesforce(self):
        sf_version = '40.0'
        client_id = f"RestForce/test"       
        soap_url = f'https://test.salesforce.com/services/Soap/u/{sf_version}'       
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
            'SOAPAction': 'login'}

        response = self.session.post(soap_url, soap_body, headers=soap_headers)
        logger.info('Salesforce Login... Ok' if response.status_code == 200 else 'Salesforce Login... Fail')
        if response.status_code != 200:
            logger.error(self.getUniqueElementValueFromXmlString(response.content, 'faultstring'))
            return 

        session_id = self.getUniqueElementValueFromXmlString(response.content, 'sessionId')
        server_url = self.getUniqueElementValueFromXmlString(response.content, 'serverUrl')

        self.base_url = f"https://{server_url.split('/')[2]}/services/data/v{sf_version}/"

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + session_id,
            'X-PrettyPrint': '1'}
        
        return True

    def query(self, query, msg):
        url = self.base_url + 'query/'
        response = self.session.request('GET', url, params={'q': query}, headers=self.headers)
        logger.info(f"GET -> {f'{msg}':<69}{response.status_code}")
        return response.json() if response.status_code == 200 else {}

    def queries(self, account_id):
        logger.info(f"\nQueries\n{80*'*'}")

        # ------------- Query Saleforce Api for account id passed in. -------------
        q = f"SELECT Account__c from Related_System_ID__c where Source_System_Name_Field__c = 'SMART ID' and Source_System_ID__c = '{account_id}'"
        result = self.query(q, f"Accounts with ID: {account_id}")

        # Not sure I need to do this. i.e. add to a list. 
        accounts = [d.get('Account__c') for d in result.get('records', {})]
        if accounts:
            self.account_c = accounts[0]
            self.delete_dict[9] = {'url_addon': 'Account', 'items': accounts}
        else:
            logger.info(f"\nNo Accounts Found.\n")
            return 

        # ------------------------------ Get list of Asset Ids ------------------------------
        result = self.query(f"SELECT ID from Asset where AccountId = '{self.account_c}'", f"Assets ")
        assetids = [d.get('Id') for d in result.get('records', {})]
        self.delete_dict[2] = {'url_addon': 'Asset', 'items': assetids}

        # ------------------------------ Get list of Contract Line Items --------------------
        contractlineitems = []
        for aid in assetids:
            result = self.query(f"SELECT ID from ContractLineItem where AssetId = '{aid}'", f"ContractLineItems")
            for r in [d.get('Id') for d in result.get('records', {})]:
                contractlineitems.append(r)
        self.delete_dict[0] = {'url_addon': 'ContractLineItem', 'items': contractlineitems}

        # ------------------------------ Get list of Order Line Assets ---------------------
        orderlineassets = []
        for aid in assetids:
            result = self.query(f"SELECT ID from Sales_Order_Line_Asset__c where Asset__c = '{aid}'", f"OrderLineAssests")
            for r in [d.get('Id') for d in result.get('records', {})]:
                orderlineassets.append(r)
        self.delete_dict[1] = {'url_addon': 'Sales_Order_Line_Asset__c', 'items': orderlineassets}

        # ------------------------------ Get Order -----------------------------------------
        result = self.query(f"SELECT ID from Order where AccountId ='{self.account_c}'", f"Orders")
        orders = [d.get('Id') for d in result.get('records', {})]
        self.delete_dict[4] = {'url_addon': 'Order', 'items': orders}

        # ------------------------------ Get ServiceContract -------------------------------
        result = self.query(f"SELECT ID from ServiceContract where AccountId = '{self.account_c}'", f"ServiceContracts")
        servicecontracts = [d.get('Id') for d in result.get('records', {})]
        self.delete_dict[3] = {'url_addon': 'ServiceContract', 'items': servicecontracts}

        # ------------------------------ Get Portal_Group ----------------------------------
        result = self.query(f"SELECT ID from Portal_Group__c where Account__c = '{self.account_c}'", f"Portal_Groups")
        portalgroups = [d.get('Id') for d in result.get('records', {})]
        self.delete_dict[5] = {'url_addon': 'Portal_Group__c', 'items': portalgroups}

        # ------------------------------ Get Related_System_Id -----------------------------
        result = self.query(f"SELECT ID from Related_System_ID__c where Account__c = '{self.account_c}'", f"Related_System_IDs")
        related_system_ids = [d.get('Id') for d in result.get('records', {})]
        self.delete_dict[6] = {'url_addon': 'Related_System_ID__c', 'items': related_system_ids}

        # ------------------------------ Get Contract ------------------------------- 
        result = self.query(f"SELECT ID from Contact where AccountId = '{self.account_c}'", f"Contracts")
        contracts = [d.get('Id') for d in result.get('records', {})]
        self.delete_dict[7] = {'url_addon': 'Contact', 'items': contracts}

        # ------------------------------ Get Account_Address -------------------------------
        result = self.query(f"SELECT ID from Account_Address__c where Account__c = '{self.account_c}'", f"Account_Addresses")
        account_addresses = [d.get('Id') for d in result.get('records', {})]
        self.delete_dict[8] = {'url_addon': 'Account_Address__c', 'items': account_addresses}

    def _delete_entries(self):
        if self.delete_dict:
            logger.info(f"\nDeleting Entries\n{80*'*'}")

        for n in range(len(self.delete_dict)):
            v = self.delete_dict.get(n)
            for item in v['items']:
                url = f"{self.base_url}sobjects/{v['url_addon']}/{item}"
                response = self.session.request('DELETE', url, headers=self.headers)
                logger.info(f"DELETE -> {item} from {v['url_addon']:<42}{response.status_code}")

        self.delete_dict = {}

    def _show_entries(self):
        if self.delete_dict:
            logger.info(f"\nShow Entries\n{80*'*'}")

        for n in range(len(self.delete_dict)):
            logger.info(f"{n:<7}{self.delete_dict[n]['url_addon']:<71}{len(self.delete_dict[n]['items'])}")
   
    def cleanup(self, user_account_id, really_delete):
        if self.login_to_salesforce():
            self.queries(account_id=user_account_id)
            self._delete_entries() if really_delete else self._show_entries()

