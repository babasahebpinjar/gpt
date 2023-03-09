#!/usr/bin/env python3
#Import open AI OS and System Modules
import openai,os,sys

def returnFileData(fileName):
    # Open the file for reading
    with open(fileName, 'r') as file:
        # Read the contents of the file
        contents = file.read()
        # Print the contents of the file
        return(contents)
    

prompt = "Can you give me user stories for the requirement: and number them" +  returnFileData(sys.argv[1])


#prompt = sys.argv[1]
openai.api_key = os.environ['api_key']
#export api_key=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
#export api_key=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
completions = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)
message = completions.choices[0].text
print(message)