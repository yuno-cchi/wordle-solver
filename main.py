import re # regular expressions, son
import random

# put all (valid) 5 letter English words, ordered by frequency, in a list
with open('ordered_words.txt') as f:
    words = f.read().splitlines()


def flavorText(): # :p
    lis = ["\n\"I learned Regex and all i got was this cool shirt\"\n",
           "\n\"Please go easy on me it's my first hackathon\"\n",
           "\n\"It's not _really_ cheating if I stayed up all night to make this script right?\"\n",
           "\n\"Time complexity of O(h my goodness)\"\n",
           "\n\"I _think_ it's O(nlg(n)) but English is a lot more complicated than that\"\n",
           "\n\"Inspired by 3Blue1Brown!\"\n"]
    print(random.choice(lis))


print("\n\nOptimized(?) Wordle Solver")
flavorText()
print("\nHOW TO USE:")
print("Enter your (lowercase) initial word guess, and then the \"response\" from Wordle")
print("as a 5 char string of LOWERCASE letters corresponding to the color of each letter.")
print("\nThat is to say, if I were to guess STIRS, and the reply from wordle was:")
print("S: green, T: green, I: yellow, R:yellow, S: black")
print("then I would have entered \"stirs\" and then \"ggyyb\"")
print("\nThe script will suggest the next words you can use, and will keep going until")
print("you win or lose.")

# using a regular expression, and iterating over the list of words,
# search for words that fit the wordle hint and add them into an array
def grep(arr, key):
    results = []
    for i in arr:
        if (re.search(key, i)):
            results.append(i)
    return results
            
def printTopWords(arr):
    print("\nTop words: ")
    if (len(arr) > 10):
        for i in range (0,9):
            print(arr[i]) 
    else:
        for i in arr:
            print(i)
            
# class for one of the 5 letter spaces
class Letter:
    def __init__(self, posn):
        # string of letters not included
        self.discardFromPosn = []
        
        # have we solved the letter?
        self.isSolved = False
        
        # if so, what letter was it? (empty string otherwise)
        self.soln = ''
        
        # which position is the word in?
        self.posn = posn
        
# class for the word itself     
class Word:
    
    def __init__(self):
        
        self.let0 = Letter(0)
        self.let1 = Letter(1)
        self.let2 = Letter(2)
        self.let3 = Letter(3)
        self.let4 = Letter(4)
        
        self.let = [self.let0, self.let1, self.let2, self.let3, self.let4]
        self.solns = [self.let0.soln,self.let1.soln,self.let2.soln,self.let3.soln,self.let4.soln]
        
        #list of chars that were yellow
        self.includeInWord = []
        
    def blacklist(self, char:str):
        for i in range(0,5):
            self.let[i].discardFromPosn.append(char)

# adds chars to includ and exclude lists per char depending on wordle reply
def processGuess(guess:str, reply:str, answer:Word):
    # letter 1:
    for i in range(0, 5):
        
        # green: correct guess at correct position    
        if((reply[i] == 'g') and  not(answer.let[i].isSolved)):
            answer.let[i].isSolved = True
            answer.let[i].soln += guess[i]
                    
        # yellow: correct guess at wrong position
        elif (reply[i] == 'y'):
            answer.let[i].discardFromPosn.append(guess[i])
            answer.includeInWord.append(guess[i])
                   
        # black: wrong guess
        if (reply[i] == 'b'):
            isDuplicate = False;
            for j in range(i, 0, -1):
                
                # if there is an unsolved duplicate behind i
                if((guess[j] == guess[i]) and ((reply[j] == 'y') or (reply[j] == 'g'))):
                    isDuplicate = True
                    break
                
            if (not (isDuplicate)):
                answer.blacklist(guess[i])
                    
# generates regex key to search through and filter list of words to check
def keyGen(answer:Word):
    key = "^"

    for i in answer.includeInWord:
        key += "(?=.*"
        key += i
        key += ".*)"
    
    for i in range(0,5):
        if (answer.let[i].isSolved):
            key += answer.let[i].soln
        else:
            key += "[^"
            for ch in answer.let[i].discardFromPosn:
                key += ch
            key += "]"
            
    key += "$"
    return key

word = Word()
lives = 6
weWon = False
wordsToCheck = words

# the meat and potatoes
while(lives > 0):
    print("\n{:d} possible words.".format(len(wordsToCheck)))
    print("\nTry {:d}".format((7-lives)))
    guess = input("Guess: ")
    reply = input("Reply: ")
    
    if(reply == "ggggg"):
        weWon = True
        break
    
    lives -= 1
    
    processGuess(guess, reply, word)
    key = keyGen(word)
    print("regex key generated: /" + key + "/")
    wordsToCheck = grep(wordsToCheck, key)
    
    printTopWords(wordsToCheck)

if(weWon):
    print("\n\nWe did it! :)\n")
else:
    print("\n\nI'm sorry ;-;\n")
 
