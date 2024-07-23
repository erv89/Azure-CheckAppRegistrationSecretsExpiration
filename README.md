# Introduction:
Python Solution that check for Azure App Registration Secrets close to Expire and send it as a report by email.

## Overview:
- Python solution containerized
- Container published on Azure Registry
- Container executed by Azure Container Job 
- Solution retrieve Azure App Registration secrets and check expiration date
- Report send by email with the Ap Registration Name with secrets expiring soon.
- Solution can only read the expiration date, not the Secret value
- Used Azure DevOps for CI/CD

## Architecture:
![Image](/diagram/App-CheckExpoiringSecretsSmall.png)

## Requirement
- Register an Azure App Registration, grant Microsoft Graph API Apps.Read.All over the tenant that need be monitored.
- Secure store Azure App Registration values (client_id, client-secret and tenant_id)
- SendGrid API Key, with send all permission
- Azure DevOps repository
- Azure Registry
- In this sample, I choose run the container from an Azure Container App Job. But can be run from Kube, AKS, etc.

## Tools and resources used:
- Python
- Azure EntraID App Registration
- Azure Container Job App
- Docker
- SendGrid
- Azure DevOps

### Created by:
&copy; Erik Rodriguez Vitier
