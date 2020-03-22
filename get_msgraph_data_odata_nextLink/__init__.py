import logging,os,requests,json
import azure.functions as func

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        endpoint = 'https://graph.microsoft.com/v1.0/users/krassy@krassy.onmicrosoft.com/messages?$select=sender,subject,receivedDateTime'
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
        msg_response_data = json.loads(requests.get(endpoint, headers=headers).text)
        print(msg_response_data)
        messages = []
        for msg in msg_response_data['value']:
            messages.append(msg['sender']['emailAddress']['address'])
            messages.append(msg['subject'])
            messages.append(msg['receivedDateTime'])

        while '@odata.nextLink' in msg_response_data:
            msg_response_data = json.loads(requests.get(endpoint, headers=headers).text)
            if '@odata.nextLink' in msg_response_data:
                endpoint = msg_response_data['@odata.nextLink']
                for msg in msg_response_data['value']:
                    messages.append(msg['sender']['emailAddress'])
                    messages.append(msg['subject'])
                    messages.append(msg['receivedDateTime'])

        return func.HttpResponse(json.dumps(messages,indent=4))

    except Exception as error:
            logging.info(error)