from os import fchdir
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents-main.json', 'r') as f:
    intents = json.load(f)

FILE = "training-data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Skye"
user_name = "User"
chat = []
chat.append(("Intro", "Hi there, I'm Skye!"))
print("Skye: Hi there, I'm Skye!")
while True:
    sentence = input(f"{user_name}: ")
    chat.append((user_name, sentence))

    if sentence == "quit":
        break

    sentence = tokenize(sentence)
    x = bag_of_words(sentence, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probabilitys = torch.softmax(output, dim=1)

    prob = probabilitys[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                response = intent['responses'][0]
                print(f"{bot_name}: {response}")
                recommendations = intent["recommendations"]
                print(f"Recommended: {recommendations}")
                chat.append((bot_name, response))
            if tag == "contact sales":
                print()
    else:
        response = "I do not understand, could you please rephrase your question?"
        print(f"{bot_name}: {response}")
        chat.append((bot_name, response))

print(chat)
