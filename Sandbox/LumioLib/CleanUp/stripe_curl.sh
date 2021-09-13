#!/bin/sh

# Reads in arguments form the user.  Pass in -c for customer_id or -e for the customer email. 
while getopts e:c:d: flag 
do 
    case "${flag}" in 
        e) EMAIL=${OPTARG};;
        c) CUST_ID=${OPTARG};;
        d) DEL_FLAG=0
    esac
done 

# Secret keys for Stripe accounts. 
SMART_TEST_ULC=sk_test_51HN4ePBIfmR0J8RSv9yFJBMrQiTHUqt7MjcmZgRzfSTJH117qdauTnmdah5W6nHgnMCmM4W1CVTcKRrtWUPUGK7D007YrOoqtD
SMART_TEST_CORP=sk_test_51H78kFFCLKlKjWryZkwbBFU4tbiGNGdCd30uc4l8FfgMc0IaPcuM5X5wTLghwYHuSHF1ApF88P9SwIS8n2vmQTsy00FKmtyqPF

# Secret key assigned to variable in function calls. 
SECRET_KEY=$SMART_TEST_ULC

function delete_customer_with_cust_id() {
    # Deletes the customer directly if it exists. 
    echo 
    echo "Delete stripe customer with id: ${CUST_ID}"
    echo
    output=$(curl https://api.stripe.com/v1/customers/$CUST_ID \
    -u $SECRET_KEY: \
    -X DELETE)
    echo 
    echo "$output";
}

function get_customer_by_customer_id() {
    # Get the customer by id
    echo 
    echo "Get stripe customer with id: ${CUST_ID}"
    echo
    output=$(curl https://api.stripe.com/v1/customers/$CUST_ID \
    -u $SECRET_KEY: \
    -X GET)
    echo
    echo "$output";
}

function get_customer_objs_by_email() {
    # Returns a json: The "data" field will contain a list of all customer objects that match the email given. 
    # Each customer object will have an "id".  This is what is required to delete that customer. 
    echo 
    echo "Getting stripe customers with email: ${EMAIL}"
    echo 
    output=$(curl https://api.stripe.com/v1/customers \
    -u $SECRET_KEY: \
    -d email=$EMAIL \
    -X GET)
    echo 
    echo "$output";
}

if [ ! -z "$EMAIL" ]
then 
    get_customer_objs_by_email                          # If -e is used, call this func to get all customer objects for that user email. 
else 
    if [ ! -z "$CUST_ID" ]
    then 
        # get_customer_by_customer_id                    # If -c is used, call this func to get a single object with this customer id.
        delete_customer_with_cust_id
    else  
        echo "Usage examples: "
        echo "./stripe_curl.sh -c cus_Io0RBOP2TJMF2w"
        echo "OR" 
        echo "./stripe_curl.sh -e mrtickle.teacher@smartwizardschool.com"
    fi 
fi


