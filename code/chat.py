import urllib.request
import json
import os
from dotenv import load_dotenv
import ssl
import random
import csv
import sys


load_dotenv()

def write_header(output_file=None, header_list=None):
    try:
        with open(output_file, mode='w') as csvfile:
            #write rows
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=header_list)
            writer.writeheader()
    except Exception as e:
        print("failed to write header csv file %s" % (e))
    return

def write_csv(output_file=None, question=None, answer=None, chat_context=None):
    try:
        with open(output_file, mode='a') as csvfile:
            #write rows
            writer = csv.writer(csvfile)
            writer.writerow([question, answer, chat_context])
    except Exception as e:
        print("failed to write csv file %s" % (e))
    return

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

num_of_questions = int(os.getenv("NUM_OF_QUESTIONS"))
output_file = os.getenv("OUTPUT_FILE")
header_list = ['Question', 'Answer', 'Context']
write_header(output_file, header_list)
print("Number of questions: ", num_of_questions)
rand_num = random.randint(1, int(num_of_questions))
print("Random number when invalid prompt will be sent!!!: ", rand_num)
# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
initPrompt = "Generate ", num_of_questions, " different travel questions."
data = {
    "chat_history" : [
        {
            "inputs": { 
            "question": "I have one day in London, what should I do?"
            },
            "outputs": {
            "answer": "You can visit Buckingham Palace."
            }
        }    
    ],
    "question" : initPrompt,
}
chat_context = data
body = str.encode(json.dumps(data))

url = os.getenv("BASE_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT")
#url = 'https://toniletempt-mslearn-0628-imwtp.eastus.inference.ml.azure.com/score'
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
api_key = os.getenv("API_KEY")

if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
#GPT 3.5 header 
#headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'toniletempt-mslearn-0628-ufwyn' }
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': model_deployment }

req = urllib.request.Request(url, body, headers)
try:
    response = urllib.request.urlopen(req)
    result = response.read()
    print(result)
    question_count = 0
    for question in json.loads(result)['answer'].split('\n'):
        question_count += 1
        print(question)
        if question_count == rand_num:
            question = "Tell me how to bake a cake."
        elif question_count > num_of_questions:
            break
        data = {
             "chat_history" : [
                {
                    "inputs": { 
                    "question": "I have one day in London, what should I do?"
                    },
                    "outputs": {
                    "answer": "You can visit Buckingham Palace. You can also visit the London Eye."
                    }
                }    
             ],
            "question" : question,
        }
        body = str.encode(json.dumps(data))
        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)
        result = response.read()
        print("The question was: ", question, ": ", result)
        write_csv(output_file, question, json.loads(result)['answer'], chat_context)

except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))