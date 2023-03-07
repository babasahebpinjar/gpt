import requests
import json
import base64

##############################################
# Login and Authenication Details
##############################################

# Set up the API endpoint URL and payload data
#url = "https://your-jira-instance/rest/api/2/issue/"
url = "https://babatestsite.atlassian.net/rest/api/2/issue"

# Encode your Jira username and API token in base64
auth_string = "babasahebpinjar@gmail.com:ATATT3xFfGF0-f9lu6Lf4cxznqREq_bsC2sPbrMw5nIhi63Jt9A3S41oOJ3JRNWsAIa-4nnZ8su1xYTho5jLMCxhSrQBemxO62YLlRIUU0rKId93qMztwOWZvGRrBzo3kM_FbCLZa6u42GEgVSef-b_G9mEBnubATD2U5pjVAE1Q8XpfWSwCbGg=EC3E3D78".encode('ascii')
#auth_string = "myuser:myapitoken".encode('ascii')
#ATATT3xFfGF0-f9lu6Lf4cxznqREq_bsC2sPbrMw5nIhi63Jt9A3S41oOJ3JRNWsAIa-4nnZ8su1xYTho5jLMCxhSrQBemxO62YLlRIUU0rKId93qMztwOWZvGRrBzo3kM_FbCLZa6u42GEgVSef-b_G9mEBnubATD2U5pjVAE1Q8XpfWSwCbGg=EC3E3D78
auth_base64 = base64.b64encode(auth_string).decode('ascii')

# Set the headers for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + auth_base64
}

#################################################
# Load the validated user stories to JIRA
#################################################


fileName = "results.txt"
with open(fileName, 'r') as file:
    for line in file:
        storyNumber = line.split('.',1)[0]
        storyDescrption = line.split('.',1)[1]
                
        payload = {
            "fields": {
                "project": {
                    "key": "BSOFT"
                },
                "summary": "Chatgpt user story_" + storyNumber,
                "description": storyDescrption,
                "issuetype": {
                    "name": "Story"
                }
            }
        }

        # Make the API request to create the issue
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Check the response status code
        if response.status_code == 201:
            print("Issue created successfully")
        else:
            print("Error creating issue: " + response.text)
