import random
from random import choices


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS  = 'AEIOU'
VOWEL_COST  = 250


class WOFPlayer():
    def __init__(self,name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []
    
    def addMoney(self,amt):
        self.prizeMoney += amt
        
    def goBankrupt(self):
        self.prizeMoney = 0
        
    def addPrize(self,prize):
        self.prizes.append(prize)
        
    def __str__(self):
        return "{} (${})".format(self.name,self.prizeMoney)

class WOFHumanPlayer(WOFPlayer):
    
    def getMove(self, category, obscuredPhrase, guessed):
        getM_input = input("""
        {} has ${}

        Category: {}
        Phrase:  {}
        Guessed: {}

        Guess a letter, phrase, or type 'exit' or 'pass': """.format(self.name,self.prizeMoney,category,obscuredPhrase,guessed))
        return getM_input

class WOFComputerPlayer(WOFPlayer):
    
    def __init__(self,name,difficulty):
        WOFPlayer.__init__(self,name)
        self.difficulty = difficulty
    
    def smartCoinFlip(self):
        randint = random.randint(1,10)
        
        if randint <= self.difficulty:
            return True
        elif randint > self.difficulty:
            return False

    def getPossibleLetters(self,guessed):
        guess_lst = []
        for i in LETTERS:
            if self.prizeMoney >= VOWEL_COST:
                if i not in guessed:
                    guess_lst.append(i)
                    
            if self.prizeMoney < VOWEL_COST:
                if i not in guessed and i not in VOWELS:
                    guess_lst.append(i)
                    
        return guess_lst

    def difficulty_letter(self,guessed):
        
        sorted_dict =dict([
        ('E',11.1607),	('M',3.0129),
        ('A',8.4966),	('H',3.0034),
        ('R',7.5809),	('G',2.4705),
        ('I',7.5448),	('B',2.0720),
        ('O',7.1635),	('F',1.8121),
        ('T',6.9509),	('Y',1.7779),
        ('N',6.6544),	('W',1.2899),
        ('S',5.7351),	('K',1.1016),
        ('L',5.4893),	('V',1.0074),
        ('C',4.5388),	('X',0.2902),
        ('U',3.6308),	('Z',0.2722),
        ('D',3.3844),	('J',0.1965),
        ('P',3.1671),	('Q',0.1962)])

        for filterkey in guessed:
            if filterkey in sorted_dict:
                sorted_dict.pop(filterkey)   
        sorted_keys=str(sorted_dict.keys())[11:-2].split(',')
        sorted_values=str(sorted_dict.values())[13:-2].split(',')
        sorted_values2 = []
        for i in sorted_values:
            sorted_values2.append(float(i))     

        return (choices(sorted_keys,sorted_values2))
            
    def getMove(self,category, obscuredPhrase, guessed):
        lst_guess = self.getPossibleLetters(guessed)
        if len(lst_guess) == 0:
            return 'pass'
        elif self.smartCoinFlip is True:
            rand_letter = self.difficulty_letter(lst_guess)
        else:            
            rand_letter = random.choice(lst_guess)
        return rand_letter
