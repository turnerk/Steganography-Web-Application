from sen_gen import ADJECTIVES, NOUNS, VERBS
import random, string

NUMBER_letters = {'0': 'o', '1':'I', '2':'z', '3':'E', '4': 'A', '5':'s', '6':'G', '7':'L', '8':'B', '9':'P'}

URL = "2hET9im"
URL = "2AWLz7C"

# sentence "The ad1 ad2 n3 made me lol, some ad4 n5 are ad6 [and adx]"
sentence = "The #1 #2 made me #3, some #4 #5 are #6"
for i in range(7, len(URL)+1):
    sentence = sentence + " ##" + str(i)

counter = 1
for char in URL:
    let = char
    if char.isdigit():
        let = NUMBER_letters[char]
    word = ""
    if counter==2 or counter==5:
        while let.lower() not in word:
            word = random.choice(NOUNS)
    elif counter==3:
        while let.lower() not in word:
            word = random.choice(VERBS)
    else:
        while let.lower() not in word:
            word = random.choice(ADJECTIVES)
    word = word.replace(let.lower(), u'\uFEFF'+char, 1)
    sentence = sentence.replace("#"+str(counter), word, 1)
    counter+=1

# capitalize 6 random letters
i=0
while i<6:
    replace = random.choice(string.ascii_letters)
    if replace not in URL:
        i+=1
        sentence = sentence.replace(replace, replace.upper())
print(sentence)
