import base64, json 
from Crypto.Hash import SHA512
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from datetime import datetime, timedelta 
from time import time, mktime 
import string, random  
from .RequestHandler import get, post 
from urllib.parse import parse_qs, urlparse, urlunparse, urlencode


def removeAccessTokenQueryParam(url, headers):
    '''If the access token exists as a query parameter it is moved into an Authorization header 
       (which is appended along with any other existing headers).
    '''
    # print('\n\n\n')
    # print(f"url:        {url}")
    # print(f"headers:    {headers}")

    u = urlparse(url)
    query = parse_qs(u.query)
    if 'access_token' in query:
       token = query.pop('access_token', None)
       myToken = "Bearer "+ token[0]
       u = u._replace(query=urlencode(query, True))
       url = urlunparse (u)
       if headers == "":
           print("WARNING: header is empty")
       elif headers != None: 
           headers = eval(str(headers))         
           headers.update({'Authorization': myToken})
       else:
           headers = {'Authorization': myToken}  
    return (url, headers) 


def get_list_of_accounts(email_to_query="gavinmcguigan.teacher@smartwizardschool.com"):
    header = {
        'alg': 'RS512', 
        'typ': 'JWT', 
        'kid': 'testharness12345:GET_TOKEN_KEY_PAIR_SUPPORT_ADMIN'
        }
    claimSet = {
        'exp': int(time() + 20*60),         # +20 mins from now
        'aud': 'id.smarttech-dev.com', 
        'iss': '66e60347-8652-4f06-b22d-5f9fb8c46efc', 
        'jti': ''.join(random.choice(string.ascii_lowercase) for _ in range(15)), 
        'iat': int(time()), 
        'scope': 'scope:api.smarttech.com/account entitlement.write entitlement'}
    
    pem = """-----BEGIN RSA PRIVATE KEY-----
            MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCPbUF0ZiYsOufV
            hUhoiuxbOstRT/mWOGZibjNbnuYjYIXBhlRv+GCpusjIqnXF92tOEV2ZZ2kn0WKB
            ihZ47aRIAULZNmUaxyx4v/FxSo7MYVRoPmIUtFJwID7eUfEm8ytyVu6n4zFRGYRw
            RoKKMHz/b9AyxL4LdEJBwqfWa/tpFdg8WXDVwnAFjSknY8XqRXkGG8OPLahOdpbK
            hnVhdsrSk+EJ9+HIdJF4IkCulzGUZ6fWI52oHTlzdpk/CCVANk9Q4zLu+K2q/MZM
            rlMHOVwWrdEVq3RzT3XcccCWNbzgVQz1Yr8GpuHQRixtNMqkLZuF8GOpFIDrL2oi
            7eXy8mjHAgMBAAECggEAclbxNXAxwlT7eRcWEHGf12LZr2sIWB+CT7n2q3XTliRe
            vVbvfYwO04CajI6H8Vg7bTMe4Sq1hA7Cbu68147rxpNqzWs10tExvNmYC28axAhb
            l/cTjdnrVoP+WpIMo7Z7zl1LSQAv0q17DV7Ito3NOH3VBoQd1VfLck1SK/hNpwmX
            oRlSs9iib7tkRkqYumZjjtmauHSRmPRqzd3ePdiIFW/aQjXDEj2N/CICnSHZQnUQ
            THgGlRIG4U40Q5GJ3TnZXZ3S2vRqtD+g0pKRR7L3ZeRX+PZR4dy8WHFr1VE0x1Xc
            o+Q9dJ+tOYphjaVq2Tgzoo6jmmPP0P/HQdLahTYdQQKBgQDApTyZEumTiYN8nISd
            KgG8HpjEYPnLVm0eW4WIMvl+8oSOD8qAzhvf9dTb3o2FsY2FNLV9UYAuEH1wolVm
            lTIR6j/U4UGYVsUmVcHp94mrd6yO2hOS8nMGk+qZ2pkjK7IyvQsYJLSnvh9oDPg5
            sFFamBAMZftHbQR5qgwb4i0F0QKBgQC+mFA5XwKT3cMdjiP86WOMWZ/mA6pImjQy
            34+NWc9/VYfBWh38o0gzAUc8YgXlhussZLqKOsJrz1+PDOqnyCIWTWhcS6xLoFmq
            AiMuojOoirh58C60kgb8AKhK+Ag7J5CifWgyd3TCxaV5GoQfNAi4jTM1BsEYElKv
            oQB2AypzFwKBgFrEwEOjrJiOf3yURsvCgiTACdzlkGzlYO6f0s/0rKfK3vgMqq57
            7phcvRmHyAjJOtQbnLPaVdnefSw34KNAAuJ8C+1i4URFBglk+MQjlSNMdOquB/EB
            +X6M7UnmvKbcrM7JUdPjX5d1tliRW9faospbwZwF5RqnXCdzHtd4fxwxAoGBALdc
            vcGUIFy1euNSPlkxB+6cwvJ9EDPs9s8CuY6ZmsC8PnDMDBFj3TAEyM3U2Ctr05DQ
            D46w3R7vUNXE7XQhXHnsWryAqO/RArJGgCZ7Mgux+ayGX8ikvEdxMnd9jB2tAL7y
            u23h8tj3YSzTT8zdOI6keWFIcDiCWD5TPKhMf2hdAoGBAMCf5uZwSfMiqJVbYtlw
            qPb72bZF8FzXXh7S++aPFE5O1aUe0R4CyAPQd9sD83snAsLblFurECu9BO+k30tP
            HMXLsG4VPHaWptbtk8/+3piv3MgZGVSRHmtocveJhhFOgbCDVoKcz70LA8wiIz+f
            oNoeVTyd3H0EsGkm7fQkHjup
            -----END RSA PRIVATE KEY-----"""


    # 1. encode the Header: encodedHeader
    encodedHeader = base64.urlsafe_b64encode(json.dumps(header).encode())
    
    # 2. encode the ClaimSet: encodedClaimSet
    encodedClaimSet = base64.urlsafe_b64encode(json.dumps(claimSet).encode())

    # 3. Join them together with a '.' to create: unsignedJwt 
    unsignedJwt = encodedHeader.decode() + "." + encodedClaimSet.decode()
    
    # 4. Form the jwt to be returned.  

    #       a. Generate hash  using the unsignedJwt
    ahash = SHA512.new(unsignedJwt.encode())
    
    #       b. Create a signature with the hash.
    privateKey = RSA.importKey(pem)
    signer = PKCS1_v1_5.new(privateKey) 
    signature = signer.sign(ahash)

    #       c. encode the signature 
    encodedSignature = base64.urlsafe_b64encode(signature)
    #       d. jwt is a combination of encodedJeader.encodedClaimSet.encdoedSignature
    jwt = f"{encodedHeader.decode()}.{encodedClaimSet.decode()}.{encodedSignature.decode()}"

    print('\n\n -------------------------------------------------- Get Access Token')

    # Exchange JWT for Access Token 
    grant_type = "urn:ietf:params:oauth:grant-type:jwt-bearer"
    
    BASE_URL = "https://id.smarttech-dev.com/"
    url = f"{BASE_URL}api/oauth2/token?grant_type={grant_type}&assertion={jwt}"
    response, response_json = get(url=url)
    print(response)
    print(response_json)
    print()

    access_token = response_json.get('access_token')
    print(f"access_token: {access_token}")
    
    print("\n\n")
    print(f"-------------------------------------------------- Cache Token")
    # credential_cache_server_base = "https://credcache.smarttech-dev.com"
    # admin_email = "supportadmin@mugglesmarttech.com"
    # admin_pass = "Sm@rt123"
    # app_url = "smart-identity-dev.appspot.com"
    # scopes = "scope:api.smarttech.com/account "
    # REFRESHABLE_TOKEN = ""
    
    # cache_url = f"{credential_cache_server_base}/cache?email={admin_email}&password={admin_pass}&application={app_url}&scopes={scopes}entitlement.write entitlement&force_refresh=true&kind=REFRESHABLE_TOKEN&expiry=5399&credential_resource={access_token}"
    cache_header = {'content-type': 'application/json'}

    # print(cache_url)

    log_examp = f"https://credcache.smarttech-dev.com/cache?email=supportadmin@mugglesmarttech.com&password=Sm@rt123&application=smart-identity-dev.appspot.com&scopes=scope:api.smarttech.com/account entitlement.write entitlement&force_refresh=true&kind=REFRESHABLE_TOKEN&expiry=5399&credential_resource=AUSIcoRLhZdG5zDYreF4le093jILDMRJ-fXKRVDtZLz0vG5DY6OkOneFBaOSlCVmXF3pf6X9hBHZhopLPqmuvi8562tXSQEEFrmEi_HbN_kMm8donVVVs7WB4ptQW8Tez8lXAmA3WTq0YkBqiXRRRNhtAFFoIDUn7w"
    cache_url = f"https://credcache.smarttech-dev.com/cache?email=supportadmin@mugglesmarttech.com&password=Sm@rt123&application=smart-identity-dev.appspot.com&scopes=scope:api.smarttech.com/account entitlement.write entitlement&force_refresh=true&kind=REFRESHABLE_TOKEN&expiry=5399&credential_resource={access_token}"
    new_url, new_headers = removeAccessTokenQueryParam(cache_url, access_token)

    response, response_json = post(url=new_url, headers=cache_header)

    print(response)
    print(response_json)
    

    # vermine = "https://credcache.smarttech-dev.com/cache?email=supportadmin@mugglesmarttech.com&password=Sm@rt123&application=smart-identity-dev.appspot.com&scopes=scope:api.smarttech.com/account entitlement.write entitlement&force_refresh=true&kind=REFRESHABLE_TOKEN&expiry=5399&credential_resource=AUSIcoTLZAYqT1Npks7zMqhKqibhS8rRI6LDzsZfNP2C86yRXCgwgchwO-Ar_blV9ulgB5li35YtVrDxiQFfsd8qvOKPARJ9L1M-NXHki_cejSi8HSArpiyU_ymUIZWS9HGvOS_TR1t3DylQsvkb8vtSrVmwcit-WQ"

    # notmine = "https://credcache.smarttech-dev.com/cache?email=supportadmin@mugglesmarttech.com&password=Sm@rt123&application=smart-identity-dev.appspot.com&scopes=scope:api.smarttech.com/account entitlement.write entitlement&force_refresh=true&kind=REFRESHABLE_TOKEN&expiry=5399&credential_resource=AUSIcoQZYhuWACyBeQYKO1MQ-sZVbw9u7y4OsSEvixcJ19ZO7AZ_0SvpbzJZ9s6uamGvrB5YmVsdFElKbDOL6dhHNzXVxYzQ1SmPq77_JZ7ql9uPNbc_IxWXLQXEIEc5qIXeYcv-sVtGCt3pXgsbHJf96Ey5WfQDdA"

    print("\n\n")
    print(f"-------------------------------------------------- Query user email: {email_to_query}")

    # user = "gavinmcguigan.teacher@smartwizardschool.com"
    # gav_url = f"https://id.smarttech-dev.com/api/account/search/email?q={user}"
    gav_url = f"https://id.smarttech-dev.com/api/account/search/email?q={email_to_query}&access_token={access_token}"
    # headers = {'Authorization': f'Bearer {access_token}'}

    new_url, new_headers = removeAccessTokenQueryParam(url, access_token)
    heads = {'Authorization': access_token}

    response, response_json = get(url=gav_url, headers=heads, verify=True, data=None, cookies=None)
    print(response)
    print(response_json)

    for each in response_json:
        userid = each.get('id')
        if userid:
            print(f"\nuserid: {userid}")
            return userid, access_token 

    print("\n\n")
    print(f"-------------------------------------------------- Now get subscriptions for user id: {userid}")

    get_subscriptions_url = f"https://newactivations.smarttech-dev.com/api/v1/accounts/{userid}/subscriptions"
    payload = {"email": f"{email_to_query}", "idps": ['google']}
    
    headers = {'Authorization': f"Bearer {access_token}", "content-type": "application/json"}
    new_url, new_headers = removeAccessTokenQueryParam(get_subscriptions_url, access_token)

    payload = '{"email": "gavinmcguigan.teacher@smartwizardschool.com", "idps": ["google"]}'

    response, response_json = get(url=new_url, headers=headers, data=payload, verify=True, cookies=None, timeout=None)

    print(response)
    print(response.headers)
    print(response_json)


# Get list of subscriptions 
def get_list_of_subscriptions():
    app_url = 'smart-identity-dev.appspot.com'
    header = {'content-type': 'application/json'}
    
    username = 'supportadmin@mugglesmarttech.com'
    passwd = 'Sm@rt123'
    userID = '66e60347-8652-4f06-b22d-5f9fb8c46efc'
    token_key_id = 'testharness12345:GET_TOKEN_KEY_PAIR_SUPPORT_ADMIN'
    
    audience = "id.smarttech-dev.com"

    # url = f"https://id.smarttech-dev.com/api/oauth2/token?grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion={}"


def get_the_access_token():
    header = {
        'alg': 'RS512', 
        'typ': 'JWT', 
        'kid': 'testharness12345:GET_TOKEN_KEY_PAIR_SUPPORT_ADMIN'}
    claimSet = {
        'exp': int(time() + 20*60),         # +20 mins from now
        'aud': 'id.smarttech-dev.com', 
        'iss': '66e60347-8652-4f06-b22d-5f9fb8c46efc', 
        'jti': ''.join(random.choice(string.ascii_lowercase) for _ in range(15)), 
        'iat': int(time()), 
        'scope': 'scope:api.smarttech.com/account entitlement.write entitlement'}
    
    pem = """-----BEGIN RSA PRIVATE KEY-----
            MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCPbUF0ZiYsOufV
            hUhoiuxbOstRT/mWOGZibjNbnuYjYIXBhlRv+GCpusjIqnXF92tOEV2ZZ2kn0WKB
            ihZ47aRIAULZNmUaxyx4v/FxSo7MYVRoPmIUtFJwID7eUfEm8ytyVu6n4zFRGYRw
            RoKKMHz/b9AyxL4LdEJBwqfWa/tpFdg8WXDVwnAFjSknY8XqRXkGG8OPLahOdpbK
            hnVhdsrSk+EJ9+HIdJF4IkCulzGUZ6fWI52oHTlzdpk/CCVANk9Q4zLu+K2q/MZM
            rlMHOVwWrdEVq3RzT3XcccCWNbzgVQz1Yr8GpuHQRixtNMqkLZuF8GOpFIDrL2oi
            7eXy8mjHAgMBAAECggEAclbxNXAxwlT7eRcWEHGf12LZr2sIWB+CT7n2q3XTliRe
            vVbvfYwO04CajI6H8Vg7bTMe4Sq1hA7Cbu68147rxpNqzWs10tExvNmYC28axAhb
            l/cTjdnrVoP+WpIMo7Z7zl1LSQAv0q17DV7Ito3NOH3VBoQd1VfLck1SK/hNpwmX
            oRlSs9iib7tkRkqYumZjjtmauHSRmPRqzd3ePdiIFW/aQjXDEj2N/CICnSHZQnUQ
            THgGlRIG4U40Q5GJ3TnZXZ3S2vRqtD+g0pKRR7L3ZeRX+PZR4dy8WHFr1VE0x1Xc
            o+Q9dJ+tOYphjaVq2Tgzoo6jmmPP0P/HQdLahTYdQQKBgQDApTyZEumTiYN8nISd
            KgG8HpjEYPnLVm0eW4WIMvl+8oSOD8qAzhvf9dTb3o2FsY2FNLV9UYAuEH1wolVm
            lTIR6j/U4UGYVsUmVcHp94mrd6yO2hOS8nMGk+qZ2pkjK7IyvQsYJLSnvh9oDPg5
            sFFamBAMZftHbQR5qgwb4i0F0QKBgQC+mFA5XwKT3cMdjiP86WOMWZ/mA6pImjQy
            34+NWc9/VYfBWh38o0gzAUc8YgXlhussZLqKOsJrz1+PDOqnyCIWTWhcS6xLoFmq
            AiMuojOoirh58C60kgb8AKhK+Ag7J5CifWgyd3TCxaV5GoQfNAi4jTM1BsEYElKv
            oQB2AypzFwKBgFrEwEOjrJiOf3yURsvCgiTACdzlkGzlYO6f0s/0rKfK3vgMqq57
            7phcvRmHyAjJOtQbnLPaVdnefSw34KNAAuJ8C+1i4URFBglk+MQjlSNMdOquB/EB
            +X6M7UnmvKbcrM7JUdPjX5d1tliRW9faospbwZwF5RqnXCdzHtd4fxwxAoGBALdc
            vcGUIFy1euNSPlkxB+6cwvJ9EDPs9s8CuY6ZmsC8PnDMDBFj3TAEyM3U2Ctr05DQ
            D46w3R7vUNXE7XQhXHnsWryAqO/RArJGgCZ7Mgux+ayGX8ikvEdxMnd9jB2tAL7y
            u23h8tj3YSzTT8zdOI6keWFIcDiCWD5TPKhMf2hdAoGBAMCf5uZwSfMiqJVbYtlw
            qPb72bZF8FzXXh7S++aPFE5O1aUe0R4CyAPQd9sD83snAsLblFurECu9BO+k30tP
            HMXLsG4VPHaWptbtk8/+3piv3MgZGVSRHmtocveJhhFOgbCDVoKcz70LA8wiIz+f
            oNoeVTyd3H0EsGkm7fQkHjup
            -----END RSA PRIVATE KEY-----"""


    # 1. encode the Header: encodedHeader
    encodedHeader = base64.urlsafe_b64encode(json.dumps(header).encode())
    
    # 2. encode the ClaimSet: encodedClaimSet
    encodedClaimSet = base64.urlsafe_b64encode(json.dumps(claimSet).encode())

    # 3. Join them together with a '.' to create: unsignedJwt 
    unsignedJwt = encodedHeader.decode() + "." + encodedClaimSet.decode()
    
    # 4. Form the jwt to be returned.  

    #       a. Generate hash  using the unsignedJwt
    ahash = SHA512.new(unsignedJwt.encode())
    
    #       b. Create a signature with the hash.
    privateKey = RSA.importKey(pem)
    signer = PKCS1_v1_5.new(privateKey) 
    signature = signer.sign(ahash)

    #       c. encode the signature 
    encodedSignature = base64.urlsafe_b64encode(signature)
    #       d. jwt is a combination of encodedJeader.encodedClaimSet.encdoedSignature
    jwt = f"{encodedHeader.decode()}.{encodedClaimSet.decode()}.{encodedSignature.decode()}"

    print('\n\n -------------------------------------------------- Get Access Token')

    # Exchange JWT for Access Token 
    grant_type = "urn:ietf:params:oauth:grant-type:jwt-bearer"
    
    BASE_URL = "https://id.smarttech-dev.com/"
    url = f"{BASE_URL}api/oauth2/token?grant_type={grant_type}&assertion={jwt}"
    response, response_json = get(url=url)
    print(response)
    print(response_json)
    print()

    access_token = response_json.get('access_token')
    print(f"access_token: {access_token}")
    return access_token


