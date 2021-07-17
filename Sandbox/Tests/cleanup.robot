*** Settings ***
Library         ${CURDIR}/../../../shared-web-test/libs/CleanUp
Resource        ${CURDIR}/../../../identity-test/keywords/__include_all_api.txt
Resource        ${CURDIR}/../../../slso-suite-test/keywords/kw_slso_purchase.txt


*** Test Cases ***
DELETE All Purchase Test Accounts
    SLSO: Clean Up All Purchase Accounts

DELETE Smart Wizard Teacher 
    SLSO: Clean Up ID, Stripe, Salesforce With Email        gavinmcguigan.teacher@smartwizardschool.com 

GET Smart Wizard Teacher 
    SLSO: Get ID, Stripe, Salesforce                        gavinmcguigan.teacher@smartwizardschool.com 

DELETE Smart Wizard Student 1
    SLSO: Clean Up ID, Stripe, Salesforce With Email        gavinmcguigan.student1@smartwizardschool.com

GET Smart Wizard Student 1
    SLSO: Get ID, Stripe, Salesforce                        gavinmcguigan.student1@smartwizardschool.com

DELETE Smart Wizard Student 2
    SLSO: Clean Up ID, Stripe, Salesforce With Email        gavinmcguigan.student2@smartwizardschool.com

GET Smart Wizard Student 2
    SLSO: Get ID, Stripe, Salesforce                        gavinmcguigan.student2@smartwizardschool.com
