*** Settings ***
# Test Setup          Local: Clear Accounts 
Library             SLSOLibrary
Resource            ${CURDIR}/../../../slso-suite-test/keywords/kw_slso_purchase.txt

*** Variables ***
@{accounts}=        gavinmcguigan.teacher@smartwizardschool.com     gavinmcguigan.student@smartwizardschool.com 
${account}          gavinmcguigan.teacher@smartwizardschool.com 
${ca_account}       slso.purchase.ca@smartwizardschool.com
${country}          UK 
${stripe_acc1}      SMART_TEST_ULC
${stripe_acc2}      SMART_TEST_CORP 
${cust_id}          cus_JGsaUvdoV0Bgja

*** Test Cases ***
# ----------------------- Purchase Tests -----------------------
Fill In Purchase Pages Concurrently
    Multi Process Purchases

Fill In Purchase Pages 
    Single Process Purchases

# ----------------------- Library Tests ------------------------
Go To Libraries Concurrently
    Multi Process Login 

Go To Libraries
    Single Process Login 

# ----------------------- Stripe Tests ------------------------
Stripe Get Customer
    SLSOLibrary.Stripe Get Customers On All Accounts                ${ca_account}

Stripe Get Customers 
    SLSOLibrary.Stripe Get Customers On All Accounts                ${accounts}

Stripe Delete Customer  
    SLSOLibrary.Stripe Delete Customers On All Accounts             ${account}

Stripe Delete Customers
    SLSOLibrary.Stripe Delete Customers On All Accounts             ${accounts}

Stripe Delete Customer With Email And Country 
    SLSOLibrary.Stripe Delete Customer By Email And Country         ${account}      ${country}

Stripe Delete Customer With Email And Stripe Account 
    Stripe Delete Customer By Email And Stripe Account  ${account}      ${stripe_acc1}

Stripe Get Customer With Their ID 
    SLSOLibrary.Stripe Show Customer By ID                          ${cust_id}

*** Keywords ***
Local: Clear Accounts
    SLSO: Clean Up All Purchase Accounts
