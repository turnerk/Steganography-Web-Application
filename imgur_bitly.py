from imgurpython import ImgurClient
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# give image to post path returns bitly hash
def imgur_bitly(image_path):
    # imgur client tokens for our application
    client_id = 'cfdb2f95b4dacfb'
    client_secret = '5c851763a35fcbe72e515e3a8c53faa7e8d4c629'
    # bitly access token for our application
    access_token = '0fa519129d179eb71349baa4610eda3a78940c77'

    # establish client connection with imgur anonymously
    client = ImgurClient(client_id, client_secret)

    # posts the image to imgur
    resp = client.upload_from_path(image_path, config=None, anon=True)
    imgur_url = resp['link']

    # runs the resulting url through bitly
    query_params = {'access_token': access_token,
                    'longUrl': imgur_url}
    response = requests.get('https://api-ssl.bitly.com/v3/shorten', params=query_params, verify=False)

    # returns and prints bitly hash
    data = json.loads(response.content)
    return(data['data']['hash'])

path = "pup.png"
hash1 = imgur_bitly(path)
print(hash1)
