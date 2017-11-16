from string import Template

sentence = Template("""$num1 This is the most $loc1 $num2 $loc2 I have ever seen! $num3 my $num4 $loc3 friends won\'t $num5 $loc4 this. they are $num6 years old and very $loc5 to me $num7 but I $loc6 them.""")


adjList = ["crazy", "sick", "dumb", "quirky", "silly", "woke", "fabulous", "gorgeous", "unholy"," juvenile", "sexy", "ditzy", "precious", "wavy", "foxy"]
verbList = ["believe", "guess", "comprehend", "fathom", "quit", "love", "yield to", "make", "jeer to", "flex", "woo","brawl"]
nounList = ["video", "clippy", "picture", "post", "status", "zone", "rendition", "quiz", "jackpot", "game", "hoax"]

URL = "2z5CjRv"
URL = "2hET9im"
numCount = 1
locCount = 1
values = {}
string = sentence.safe_substitute(values)

# Get rid of extra nums that weren't used
def stripExtra(sentence):

	for i in range(8):
		if i != 6:
			sentence = sentence.replace('$num{0}'.format(i), '')
		else:
			sentence = sentence.replace('$num6', '80')

	if '$loc5' in sentence:
		sentence = sentence.replace('$loc5', 'weird')
	if '$loc6' in sentence:
		sentence = sentence.replace('$loc6', 'love')
	return sentence

for char in URL:
	if(char.isdigit()):
		# Make sure numbers stay in line with letters
		if numCount < locCount:
			numCount = locCount + 1
		# Add digit from URL into current $num location
		values['num{0}'.format(numCount)] = u'#\uFEFF' + char
		string = sentence.safe_substitute(values)
		numCount+=1
	else:
		# If there are still openings, add either a noun, adj, or verb depending on location
		if string.find('$loc{0}'.format(locCount)) != -1:
			if locCount == 1 or locCount == 3 or locCount == 5:
				for word in adjList:
					# Have to check if char from URL is uppercase
					if char in word or char.lower() in word:
						if char.isupper():
							# Have to lowercase the char to find in word, then change back to uppercase
							newWord = (word[:word.find(char.lower())] + u'\uFEFF' + word[word.find(char.lower()):]).replace(char.lower(), char.upper())
							values['loc{0}'.format(locCount)] = newWord
						else:
							newWord = word[:word.find(char)] + u'\uFEFF' + word[word.find(char):]
							values['loc{0}'.format(locCount)] = newWord
						string = sentence.safe_substitute(values)
						adjList.remove(word)
						break
				locCount+=1
			elif locCount == 2:
				for word in nounList:
					if char in word or char.lower() in word:
						if char.isupper():
							newWord = (word[:word.find(char.lower())] + u'\uFEFF' + word[word.find(char.lower()):]).replace(char.lower(), char.upper())
							values['loc{0}'.format(locCount)] = newWord
						else:
							newWord = word[:word.find(char)] + u'\uFEFF' + word[word.find(char):]
							values['loc{0}'.format(locCount)] = newWord
						string = sentence.safe_substitute(values)
						nounList.remove(word)
						break
				locCount+=1
			elif locCount == 4 or locCount == 6:
				for word in verbList:
					if char in word or char.lower() in word:
						if char.isupper():
							newWord = (word[:word.find(char.lower())] +u'\uFEFF' + word[word.find(char.lower()):]).replace(char.lower(), char.upper())
							values['loc{0}'.format(locCount)] = newWord
						else:
							newWord = word[:word.find(char)] + u'\uFEFF' + word[word.find(char):]
							values['loc{0}'.format(locCount)] = newWord
						string = sentence.safe_substitute(values)
						verbList.remove(word)
						break
				locCount+=1

string = stripExtra(string)
print(string)
