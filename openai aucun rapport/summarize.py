import os
import openai

# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"


#open text file in read mode
# text_file = open("/home/alexandre/Documents/Sites/Python/six_qui_prend/openai aucun rapport/text_ori_2.txt", "r")
file_name = "deep_work"
text_file = open(f"/home/alexandre/Documents/Sites/Python/six_qui_prend/openai aucun rapport/files/{file_name}.txt", "r")
 
#read whole file to a string
data = text_file.read()
 
#close file
text_file.close()

response = openai.Completion.create(
  model="text-davinci-002",
  prompt=data,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response.choices[0].text)

with open(f"openai aucun rapport/files/{file_name}_summarized.txt", 'w') as f:
  f.write(response.choices[0].text)

