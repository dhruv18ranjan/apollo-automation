# import requests
# import time

# #api_key = 'cWUh7N4hOx8YS5iumDkV8A' # tushar
# #api_key = '_PPnPZAICbkT-lwJy4jdpw' # contact
# api_key = 'Fp0GnXKcBng02hY8x4Yn7g' # nandini
# #api_key = 'cWUh7N4hOx8YS5iumDkV8A' # nilesh

# list_name = 'test list'


# def enrich_people(lurl):
#     url = "https://api.apollo.io/v1/people/match"

#     data = {
#         "linkedin_url": lurl,
#         "reveal_personal_emails": True,
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("POST", url, headers=headers, json=data)

#     return response.json()


# def enrich_org(primary_domain):

#     url = "https://api.apollo.io/v1/organizations/enrich"

#     querystring = {
#         "domain": primary_domain
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("GET", url, headers=headers, params=querystring)
#     return response.json()



# def search_contact(lurl, response_data):
#     url = "https://api.apollo.io/v1/contacts/search"

#     data = {
#         "q_keywords": response_data["person"]["email"],
#         "sort_by_field": "contact_last_activity_date",
#         "sort_ascending": False,
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("POST", url, headers=headers, json=data)
#     response = response.json()

#     if response["contacts"] == []:
#         create_contact(lurl, response_data) 
#     elif lurl == response["contacts"][0]["linkedin_url"]:
#         update_contact(response_data, response["contacts"][0]["id"])
#     else:
#         create_contact(lurl, response_data)


# def update_contact(response_data, contact_id):
#     url = "https://api.apollo.io/v1/contacts/" + contact_id

#     response_data["label_names"] = [list_name]

#     data = {
#         "first_name": response_data["person"]["first_name"],
#         "last_name": response_data["person"]["last_name"],
#         "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
#         "title": response_data["person"]["title"],
#         "email": response_data["person"]["email"],
#         "website_url": response_data["person"]["organization"]["primary_domain"],
#         "label_names": response_data["label_names"]
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("PUT", url, headers=headers, json=data)




# def create_contact(lurl, response_data):

#     url = "https://api.apollo.io/v1/contacts"

#     response_data["label_names"] = [list_name]

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }


#     try:
#         primary_domain = response_data["person"]["organization"]["primary_domain"]
#         org_data = enrich_org(primary_domain)
#     except:
#         data = {
#             "first_name": response_data["person"]["first_name"],
#             "last_name": response_data["person"]["last_name"],
#             "title": response_data["person"]["title"],
#             "email": response_data["person"]["email"],
#             "label_names": response_data["label_names"]
#         }        
#         response = requests.request("POST", url, headers=headers, json=data)
#         return



#     if "account_id" in org_data["organization"]:
#         data = {
#             "first_name": response_data["person"]["first_name"],
#             "last_name": response_data["person"]["last_name"],
#             "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
#             "title": response_data["person"]["title"],
#             "account_id": org_data["organization"]["account_id"],
#             "email": response_data["person"]["email"],
#             "website_url": response_data["person"]["organization"]["primary_domain"],
#             "label_names": response_data["label_names"]
#         }
#     elif "id" in org_data["organization"]:
#         data = {
#             "first_name": response_data["person"]["first_name"],
#             "last_name": response_data["person"]["last_name"],
#             "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
#             "title": response_data["person"]["title"],
#             "account_id": org_data["organization"]["id"],
#             "email": response_data["person"]["email"],
#             "website_url": response_data["person"]["organization"]["primary_domain"],
#             "label_names": response_data["label_names"]
#         }
#     else:
#         data = {
#             "first_name": response_data["person"]["first_name"],
#             "last_name": response_data["person"]["last_name"],
#             "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
#             "title": response_data["person"]["title"],
#             "email": response_data["person"]["email"],
#             "website_url": response_data["person"]["organization"]["primary_domain"],
#             "label_names": response_data["label_names"]
#         }


#     response = requests.request("POST", url, headers=headers, json=data)


# def check_api():
#     url = "https://api.apollo.io/v1/auth/health"

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("GET", url, headers=headers)

#     print(response.text)


# print ("Started")
# #check_api()



# with open('input.txt', 'r', encoding='utf-8') as file:
#     # Read all lines and store them in a list
#     lines = file.readlines()

# lines = [line.strip() for line in lines]

# i = 0
# for line in lines:
#     print(line)
#     try:
#         response_data = enrich_people(line)
#         search_contact(line, response_data)
#     except Exception as e:
#         print(e)
#         with open('errors.txt', 'a', encoding='utf-8') as error_file:
#             error_file.write(line + '\n')









import requests
import time

# api_key = 'cWUh7N4hOx8YS5iumDkV8A' # tushar
# api_key = '_PPnPZAICbkT-lwJy4jdpw' # contact
api_key = 'Fp0GnXKcBng02hY8x4Yn7g' # nandini
# api_key = 'cWUh7N4hOx8YS5iumDkV8A' # nilesh

list_name = 'test list'


def enrich_people(lurl):
    url = "https://api.apollo.io/v1/people/match"

    data = {
        "linkedin_url": lurl,
        "reveal_personal_emails": True,
    }

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }

    response = requests.request("POST", url, headers=headers, json=data)
    return response.json()


def enrich_org(primary_domain):
    url = "https://api.apollo.io/v1/organizations/enrich"

    querystring = {
        "domain": primary_domain
    }

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()


def search_contact(lurl, response_data):
    url = "https://api.apollo.io/v1/contacts/search"

    data = {
        "q_keywords": response_data["person"]["email"],
        "sort_by_field": "contact_last_activity_date",
        "sort_ascending": False,
    }

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }

    response = requests.request("POST", url, headers=headers, json=data)
    response = response.json()

    if response["contacts"] == []:
        create_contact(lurl, response_data) 
    elif lurl == response["contacts"][0]["linkedin_url"]:
        update_contact(response_data, response["contacts"][0]["id"])
    else:
        create_contact(lurl, response_data)


def update_contact(response_data, contact_id):
    url = "https://api.apollo.io/v1/contacts/" + contact_id

    response_data["label_names"] = [list_name]

    data = {
        "first_name": response_data["person"]["first_name"],
        "last_name": response_data["person"]["last_name"],
        "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
        "title": response_data["person"]["title"],
        "email": response_data["person"]["email"],
        "website_url": response_data["person"]["organization"]["primary_domain"],
        "label_names": response_data["label_names"]
    }

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }

    response = requests.request("PUT", url, headers=headers, json=data)


def create_contact(lurl, response_data):
    url = "https://api.apollo.io/v1/contacts"

    response_data["label_names"] = [list_name]

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }

    try:
        primary_domain = response_data["person"]["organization"]["primary_domain"]
        org_data = enrich_org(primary_domain)
    except Exception as e:
        data = {
            "first_name": response_data["person"]["first_name"],
            "last_name": response_data["person"]["last_name"],
            "title": response_data["person"]["title"],
            "email": response_data["person"]["email"],
            "label_names": response_data["label_names"]
        }        
        response = requests.request("POST", url, headers=headers, json=data)
        return

    data = {
        "first_name": response_data["person"]["first_name"],
        "last_name": response_data["person"]["last_name"],
        "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
        "title": response_data["person"]["title"],
        "email": response_data["person"]["email"],
        "website_url": response_data["person"]["organization"]["primary_domain"],
        "label_names": response_data["label_names"]
    }

    if "account_id" in org_data["organization"]:
        data["account_id"] = org_data["organization"]["account_id"]
    elif "id" in org_data["organization"]:
        data["account_id"] = org_data["organization"]["id"]

    response = requests.request("POST", url, headers=headers, json=data)


def check_api():
    url = "https://api.apollo.io/v1/auth/health"

    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }

    response = requests.request("GET", url, headers=headers)


print("Started")
# check_api()

with open('input.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]

for line in lines:
    print(line)
    try:
        response_data = enrich_people(line)
        search_contact(line, response_data)
    except Exception as e:
        print(e)
        with open('errors.txt', 'a', encoding='utf-8') as error_file:
            error_file.write(line + '\n')
