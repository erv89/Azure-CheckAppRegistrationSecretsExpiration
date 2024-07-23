from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient
from datetime import datetime, timedelta, timezone
import dotenv
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

# Load environment variables
dotenv.load_dotenv()

# Get the variables from environment variables
tenant_id = os.getenv('tenant_id')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
sendgridkey = os.getenv('SENDGRID_API_KEY')
email_subject = os.getenv('subject')

# Create a credential object
credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
client = GraphClient(credential=credential)

# Time Variables
current_date = datetime.now(timezone.utc).isoformat().replace(
    "+00:00", "Z")  # current date in iso format
days_from_now = datetime.now(
    timezone.utc) + timedelta(days=60)  # 60 days from now, but can be change for any number of days

# Fetch the list of app registrations from Graph API
app_registrations = client.get(f'https://graph.microsoft.com/v1.0/{tenant_id}/applications?$select=id,displayName,passwordCredentials')
# Convert the response to JSON format
data = json.loads(app_registrations.content)

## Function to retrieve secret expiring in 60 days
def printOutExpirationSecrets():
    expiring_secrets = []
    try:
        for app in data['value']:
            for secret in app['passwordCredentials']:
                if secret['endDateTime'] is not None:
                    if secret['endDateTime'] >= current_date and secret['endDateTime'] <= days_from_now.isoformat():
                        endDate = datetime.fromisoformat(secret['endDateTime'])
                        expiring_secrets.append({
                            "app_name": app['displayName'],
                            "end_date": secret['endDateTime'][:10],
                            "days_until_expiration": str((endDate - datetime.now(timezone.utc)).days)
                        })
                        with open("ExpiringSecretsReport.txt", "a") as f:
                            f.write("Application Name: " + app['displayName'] + "\n" "Secret is expiring on " +
                                    secret['endDateTime'][:10] + "\n" + "Days until expiration: " +
                                    str((endDate - datetime.now(timezone.utc)).days) + "\n\n")
                            f.close()
        print("Expiring secrets found:", expiring_secrets)  # Debug print
    except Exception as e:
        print("Error:", e)
    return expiring_secrets

## Function to read the content of the text file and convert it to an HTML table
def txt_to_html_table(file_path):
    try: 
        with open(file_path, 'r') as file:
            content = file.read().strip()

            lines = content.split('\n\n')

            table = '<table style="border: 1px solid black; border-collapse: collapse;">'
            # Add table headers
            table += '''
            <tr>
                <th style="border: 1px solid black; padding: 5px;">Application Name</th>
                <th style="border: 1px solid black; padding: 5px;">Secret Expiration</th>
                <th style="border: 1px solid black; padding: 5px;">Days Until Expiration</th>
            </tr>
            '''
            for entry in lines:
                fields = entry.split('\n')

                app_name = fields[0].split(': ')[1]
                expiration = fields[1].split(' ')[4]
                days_until = fields[2].split(': ')[1]

                table += f'''
                <tr>
                    <td style="border: 1px solid black; padding: 5px;align="left"">{app_name}</td>
                    <td style="border: 1px solid black; padding: 5px;"align="center">{expiration}</td>
                    <td style="border: 1px solid black; padding: 5px; color: red"; align="center">{days_until}</td>
                </tr>
                '''
            table += '</table>'
            return table
    except Exception as e:
        print("Error:", e)
        return None
    
## Function to send an email with the HTML table
def send_email(html_content, no_expiring_secrets=False):
    if no_expiring_secrets:
        html_content = "<p>There are no secrets expiring in the next 60 days.</p>"
    message = Mail(
        from_email='appregistrationnotifications@sample.com',
        to_emails=[
            To('recipient1@sample.com'),
            To('recipient1@sample.com'),
            # add more emails or emails group as needed

        ],
        subject=email_subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(sendgridkey)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

# Call the function
expiring_secrets = printOutExpirationSecrets()
if expiring_secrets:
    html_table = txt_to_html_table("ExpiringSecretsReport.txt")
    send_email(html_table)
else:
    send_email("", no_expiring_secrets=True)
# Clear the content of the text file
open("ExpiringSecretsReport.txt", "w").close()
