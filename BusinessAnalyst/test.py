#Import open AI OS and System Modules
import openai,os,sys

fileName = "results.txt"
with open(fileName, 'r') as file:
    for line in file:
        print(line.split('.',1)[1])

    

#prompt = "Can you give me user stories for the requirement: and number them" +  returnFileData(sys.argv[1])
