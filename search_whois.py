'''
Searching about domain using whois

input: domain (example: https://google.com)
interesting info in output:
- domain_name
- registrar
- whois_server
- referral_url
- updated_date
- creation_date
- expiration_date
- name_servers
- status
- emails
- org
- address, city, state, country

Then this info parsing to string
for user message telegram
Also added manipulations with datetime data format
'''
import datetime
import whois
import logging

def search_info(domain: str):
    try:
        info = whois.whois(domain)
    except TypeError:
        print("Error in search_whois: TypeError")
        logger = logging.getLogger('__search_whois_module_logging__')
        logger.exception("Exception occurred in whois.whois() - TypeError")
        return False
    print(info)
    headline = ["domain_name","registrar", "whois_server", "creation_date", "expiration_date", "emails", "org","country"]
    important= ''
    data = ''
    for key in headline:
        if key in info and info[key]!=None:
            if type(info[key]) == list:
                for date in info[key]:
                    if type(date) == datetime.datetime:
                        date = datetime.datetime.strftime(date,"%m.%d.%Y,%H:%M:%S")
                    important += key + ': ' + date + '\n'
            elif type(info[key]) == datetime.datetime:
                data = datetime.datetime.strftime(info[key], "%m.%d.%Y,%H:%M:%S")
            else:
                data = info[key]
            important += (key + ': ' + data + '\n') if type(info[key]) != list else ''

    return important
