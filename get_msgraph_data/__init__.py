import logging,requests,os
import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request {}'.format(req))
    try:
            endpoint= req.get_json()['endpoint']
            logging.info(endpoint)
            url = 'https://login.microsoftonline.com/krassy.onmicrosoft.com/oauth2/v2.0/token'
            data = {
                'grant_type': 'password',
                'client_id': os.getenv('client_id'),
                'scope': 'https://graph.microsoft.com/.default',
                'client_secret': os.getenv('client_secret'),
                'username': os.getenv('user_name'),
                'password': os.getenv('password')
            }
            resp = requests.post(url, data=data)
            token = resp.json().get('access_token')
            headers = {'Authorization': 'Bearer {}'.format(token)}
            graphdata = requests.get(endpoint, headers=headers).text
            logging.info(graphdata)
            return func.HttpResponse(graphdata)

    except Exception as error:
            logging.info(error)

