import requests
import json
import base64

##############################################
# Login and Authenication Details
##############################################

# Set up the API endpoint URL and payload data
#url = "https://your-jira-instance/rest/api/2/issue/"
url = "https://babatestsite.atlassian.net/rest/api/2/issue"
#ajd9460c-4297-1490-76a6-4k9da4a45686
#ATCTT3xFfGN08if7_THS1tRAU8_habbvd93kYhK5AUL22MJUzyp3Zk0cCD1ac65nSlvXavtgmohGgQx7f02Wz_aDAvc2tGk5_ASuRlIcUkABayYS-qcVm9KP8SkMhhElusqmJd3d9E1HTvAj85fK2J7kGqNW7W2W6tjGvPgTFSksmWEuKO81N_4=823C1C0E

# Encode your Jira username and API token in base64
#auth_string = "babasahebpinjar@gmail.com:ATATT3xFfGF0-f9lu6Lf4cxznqREq_bsC2sPbrMw5nIhi63Jt9A3S41oOJ3JRNWsAIa-4nnZ8su1xYTho5jLMCxhSrQBemxO62YLlRIUU0rKId93qMztwOWZvGRrBzo3kM_FbCLZa6u42GEgVSef-b_G9mEBnubATD2U5pjVAE1Q8XpfWSwCbGg=EC3E3D78".encode('ascii')

auth_string = "babasahebpinjar@gmail.com:ATCTT3xFfGN08if7_THS1tRAU8_habbvd93kYhK5AUL22MJUzyp3Zk0cCD1ac65nSlvXavtgmohGgQx7f02Wz_aDAvc2tGk5_ASuRlIcUkABayYS-qcVm9KP8SkMhhElusqmJd3d9E1HTvAj85fK2J7kGqNW7W2W6tjGvPgTFSksmWEuKO81N_4=823C1C0E".encode('ascii')
auth_string = "babasahebpinjar@gmail.com:ATATT3xFfGF0kzmWW-72vvJUYQmk7ozmMdO5nZhYRy2SlVSoTT16kQgfAbTc441lflnAbBNUOwt8dNoZf-MLZLHoNFyr8KhGxu7FfnT3aArhd6ogzg6WmXVMLbZ-AVcRuEJ4Pr8qMAz7TLsJAsppRXkiTYR7TQK2Tx9kawSSdIBMSvKVWOt0Qd0=16A6B4E8".encode('ascii')
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
