# Simple Eliza Clone
# Based on Haskell implementation by Tim Hunter

def give_response(input):
    if input.startswith("I need "):
        return "Why do you need " + reflect(after(input,"I need ")) + "?"
    elif input.startswith("I am "):
        return "Do you enjoy being " + reflect(after(input,"I am ")) + "?"
    elif input.startswith("I can't "):
        return "Perhaps you could " + reflect(after(input,"I can't ")) + " if you tried."
    elif input.startswith("I never "):
        return "You really never " + reflect (after(input,"I never ")) + "?"
    elif input.startswith("I don't "):
        return "Do you want to " + reflect (after(input,"I don't ")) + "?"
    elif input.startswith("I feel "):
        return "When do you usually feel " + reflect(after(input,"I feel ")) +  "?"
    elif input.startswith("You don't "):
        return "Do you really think I don't " + reflect(after(input,"You don't ")) + "?"
    elif input.startswith("You are "):
        return "I may be " + reflect(after(input,"You are ")) + " --- what do you think?"
    elif input.startswith("You "):
        return "Why do you say that about me?"
    elif input.startswith("Because "):
        return "Is that the real reason?"
    elif "family" in input:
        return "I see ... tell me more about your family."
    elif "computer" in input:
        return "How do computers make you feel?"
    #Handle case when input has is
    #Problem 1: If the user tries to expain something, for instance, "this is since I was tired" the output is "Why is this since i were tired?"
    #Problem 2: If input is grammatically wrong, for instance, "salad is a john" gives "Why is salad a john?"
    #Problem 3: If the user asks a question,for instance," is the cat here" gives "Why is the cat here?"
    #
    elif " is " in input:
        return "Why is " + reflect(before(input," is ")) + " "+ reflect(after(input," is ")) + "?"
    elif input == "Yes":
        return "You seem very certain ... how can you be so sure?"
    elif input == "No":
        return "Why not?"
    #Handle mod 3
    elif len(input) % 3 == 0:
        return "Could you elaborate on that?"
    #Handle mod 3 - 2
    elif (len(input) - 2) % 3 == 0:
        return "What do you feel about it?"
    #Handle mod 3 - 1
    elif (len(input) - 1) % 3 == 0:
        return "Do you want to talk about it?"
    else:
        return "How can I help?"

#The after function takes a string and a prefix (which is assumed to start the string),
#and returns the portion of the string that follows the prefix
def after(string, prefix):
    return string.split(prefix)[1]

#before returns the portion of the string preceding the prefix
def before(string, prefix):
    return string.split(prefix)[0]

def reflect(string):
    return ' '.join([reflect_word(word) for word in string.split()])

def reflect_word(word):
    if word == "I":
        return "you"
    elif word == "me":
        return "you"
    elif word == "you":
        return "me"
    elif word == "am":
        return "are"
    elif word == "was":
        return "were"
    elif word == "my":
        return "your"
    elif word == "your":
        return "my"
    elif word == "myself":
    	return "yourself"
    else:
        return word

ui = input("Hello! I am the psychotherapist. Please describe your problems to me.\n> ")
while not ui == "quit":
      output = give_response(ui)
      print(output + "\n")
      ui = input("> ")
print("Thank you. That will be $150. Have a nice day!\n")


