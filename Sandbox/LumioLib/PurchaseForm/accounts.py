# Account_CA = "slso.purchase.ca.new@smartwizardschool.com"
# Account_UK = "slso.purchase.uk.new@smartwizardschool.com"
# Account_USA = "slso.purchase.us.new@smartwizardschool.com"
# Account_AUS = "slso.purchase.aus.new@smartwizardschool.com"
Account_CA = "slso.purchase.ca@smartwizardschool.com"
Account_UK = "slso.purchase.uk@smartwizardschool.com"
Account_USA = "slso.purchase.us@smartwizardschool.com"
Account_AUS = "slso.purchase.aus@smartwizardschool.com"

UserPass = "Smart!23"
PurchaseAccounts = [Account_CA, Account_UK, Account_USA, Account_AUS]

# To know when we've reached the purchase page.
ElementExpected =  '//*[contains(text(),"Calculate total") and contains(@class, "calculate sls-blue-btn")]'


# List of data for purchases
# [(Address Form Data), (Prices and Taxes expected), user_email_accont, currency_expected ]
PURCHASE_DATA = { 
    Account_CA: [
        (('CA', 'Wayne Gretzky', 'Unit 8 - 1905 Evergreen Court', '2nd Line', 'Kelowna', 'BC', 'V1Y 9L4'), ('77', '77.00', '9.24', '86.24'), 'CAD'),
        (('CA', 'Celine Dion', 'Casilla 162 Correo La Dehesa, Lo Barnechea', '2nd Line', 'Montreal', 'QC', 'H2V 4L2'), ('77', '77.00', '11.53', '88.53'), 'CAD'),
        (('CA', 'Ryan Reynolds', '3636 Research Road NW', '2nd Line', 'Calgary', 'AB', 'T2L 1Y1'), ('77', '77.00', '3.85', '80.85'), 'CAD'),
        (('CA', 'Chris Hadfield', 'Unit 1 - 35 East Beaver Creek Road', '2nd Line', 'Richmond Hill', 'ON', 'L4B 1B3'), ('77', '77.00', '10.01', '87.01'), 'CAD')],
    Account_UK: [
        (('GB', 'Harry Potter', '111 Newton Road', '2nd Line', 'Eden Terrace, Auckland', '', '1001^$'), ('40.74', '40.74', '8.15', '48.89'), 'GBP'),
        (('GB', 'Harry Potter', 'Unit 10 Shannon Way, Tewkesbury Business Park', '2nd Line', 'Tewkesbury', '', 'GL20 8SL*& '), ('40.74', '40.74', '8.15', '48.89'), 'GBP')],
    Account_USA: [
        (('US', 'Iron Man', '980 Runway Drive', '2nd Line', 'Conway', 'AR', '72032-7115'), ('59', '59.00', '0.00', '$59.00'), 'USD'),
        (('US', 'Spider Man', '17350 North Hartford Drive', '2nd Line', 'Scottsdale', 'AZ', '85255-5694'), ('59', '59.00', '$4.22', '$63.22'), 'USD'),   
        (('US', 'Black Widow', '3351 Michelson Drive Suite 100', '2nd Line', 'Irvine', 'CA', '92612'), ('59', '59.00', '0.00', '$59.00'), 'USD'),   
        (('US', 'Captain America', 'A-6 700 West Mississippi Avenue', '2nd Line', 'Denver', 'CO', '80223'), ('59', '59.00', '2.84', '$61.84'), 'USD')], 
    Account_AUS: [
        (('AU', 'Wolver Ine', 'Lot 4  Parkland Estate  23 South Street ', '2nd Line', 'Rydalmere', 'NSW', '2116'), ('79.38', '79.38', '$7.94', '$87.32'), 'AUD'),
        (('AU', 'Th Or', '111 Newton Road', '2nd Line', 'Eden Terrace, Auckland', 'NT', '10 01'), ('79.38', '79.38', '$7.94', '$87.32'), 'AUD')]
}

# Credit cards
VALID_CREDIT_CARD_NUM = ['4242424242424242', '0225', '123']
FAILED_PAYMENT_CREDIT_CARD_NUM = ['4000000000000010', '0223', '456']
INVALID_CREDIT_CARD_NUM = ['9999 9999 9999 9999', '0212', '65']

# Zip/Postal Codes 
postalCode_or_zip = "12345"
invalid_zip_code =  "123456"
valid_postcode = "A1A 1A1"

