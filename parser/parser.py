import sys
#line by line input
#parse it.
#incorrect grammar wrapper


#grammer:
#( do <movement> (<funcBody>))



#movements
#yaw pitch roll move
#gate_task
# have task mappings
ACTION_MAP = ["move", "yaw", "pitch", "roll", "gate"]

SIMPLE_ACTION = ["move", "yaw", "pitch", "roll"]

TERMINALS = ['(',')']

class Tokenizer:
    def __init__(self, string):
        self.tokens = string.split(" ")
        self.currIndex = 0
    def skipToken(self):
        self.currIndex = self.currIndex + 1
        
    def getToken(self):
        if self.currIndex >= len(self.tokens):
            return "EOF"
        else:
            return self.tokens[self.currIndex]  

    def peek(self):
        if self.currIndex + 1 >= len(self.tokens):
            return self.tokens[self.currIndex + 1]
        else:
            return None  

class Singleton:
    tok_instance = 0
    def __init__(self, string):
        Singleton.inputStr = string

    @classmethod
    def get_instance(cls):
        if(Singleton.tok_instance == 0):
            Singleton.tok_instance = Tokenizer(Singleton.inputStr)
        return Singleton.tok_instance



class SimpleAction:
    def __init__(self):
        self.action = "None"
        self.parameters = {}
        self.tokenizer = Singleton.get_instance()

    def parseAction(self):
        #first is action's name
        
        if self.tokenizer.getToken() in TERMINALS:
            print(f"Invalid Token: Expected action descriptor, got terminal symbol [{self.tokenizer.getToken()}]")
            return False
        self.action = self.tokenizer.getToken()
        self.tokenizer.skipToken()

        while self.tokenizer.getToken() != ')':
            if self.tokenizer.getToken() != '(':
                print(f"Invalid Token: Expected End of Action [)] or start of next param [(], got [{self.tokenizer.getToken()}]")
                return False
            #this is a parameter! bc it has to be (
            self.tokenizer.skipToken()
            parameterObj = Parameter()
            thisParamSet = parameterObj.parseParameter()
            if thisParamSet is None: return False
            self.parameters[str(thisParamSet[0])] = thisParamSet[1] #assign this dictionary value
            


            if self.tokenizer.getToken() != ')':
                print(f"Invalid Token: Expected End of Parameter [(], got [{self.tokenizer.getToken()}]")
                return False
            self.tokenizer.skipToken()
        return True

            
            #this is a parameter!
        
        #No else, bc if no parameter we just stop.

class Parameter:
    def __init__(self):
        self.num = -1
        self.tokenizer = Singleton.get_instance()
        self.name = None
        self.value = None
    def parseParameter(self):
        self.name = self.tokenizer.getToken()

        self.tokenizer.skipToken()

        if self.tokenizer.getToken() != 'lambda':
            print(f"Invalid Token: Expected [lambda] for paramater, got [{self.tokenizer.getToken()}]")
            return None

        self.tokenizer.skipToken() #lambda -> (
        self.tokenizer.skipToken() #( -> $no
        self.tokenizer.skipToken() #$no -> (
        self.tokenizer.skipToken() #( -> no

        self.value = self.tokenizer.getToken() #no

        self.tokenizer.skipToken()
        if self.tokenizer.getToken() != ')':
            print(f"Invalid Token: Expected end of number [)], got [{self.tokenizer.getToken()}]")
            return None
        self.tokenizer.skipToken()
        if self.tokenizer.getToken() != ')':
            print(f"Invalid Token: Expected end of lambda expression [)], got [{self.tokenizer.getToken()}]")
            return None
        self.tokenizer.skipToken()
        return [self.name, self.value]



class Sequence:
    def __init__(self):
        ###
        self.actions = []
        self.tokenizer = Singleton.get_instance()

    def parseSequence(self):
        #paren
        if self.tokenizer.getToken() != '(':
            print(f"Invalid Token: Expected [(], got [{self.tokenizer.getToken()}]")
            return False
        self.tokenizer.skipToken()
        
        #"seq"
        if self.tokenizer.getToken() != 'seq':
            print(f"Invalid Token: Expected [seq], got [{self.tokenizer.getToken()}]")
            return False   
        self.tokenizer.skipToken()

        counter = 0
        #<actionword>
        while self.tokenizer.getToken() != ')':
            #openparen for action
            #Do we check if this is a valid action? Or no?
            if self.tokenizer.getToken() != '(':
                print(f"Invalid Token. Expected [(] for an action call, got [{self.tokenizer.getToken()}]")
                return False
            self.tokenizer.skipToken()

            childAction = SimpleAction()
            okay = childAction.parseAction()
            help = False

            if not okay:
                print('mf error')

                return help

            self.actions.append(childAction)

            if self.tokenizer.getToken() != ')':
                print(f"Invalid Token. Expected [)] for end of action, got [{self.tokenizer.getToken()}]")
                return False
            self.tokenizer.skipToken()

            #unlikely scenario of infinite loop limiting
            counter = counter + 1
            if counter >= 200:
                return False
        
        #once we're here, we're guaranteed that the token is a ). end of sequence.
        return True

############################################################################################################


#These two methods you want to use!
def getActionTree(logical_form_text):
    Singleton(logical_form_text)
    program = Sequence()
    program.parseSequence()
    if program == False: print('Failed to parse program') 
    return program


def printActionTree(program):
    #Print out actions
    for action in program.actions:
        print(f"Action: {action.action}, Parameters: {action.parameters}")




###############################################################
#Running Code
if len(sys.argv) < 2:
    print("ERROR: Missing 1 required argument: <filename>")
    exit()
filename = sys.argv[1] 
f = open(filename, "r")
text = f.read()
print(text)


#Tokenizer stuff
Singleton(text)
program = Sequence()
program.parseSequence()

#Check to make sure no errors (if any errors, this will be true)
if program == False: print('Failed to parse program') 

#Print out actions
for action in program.actions:
    print(f"Action: {action.action}, Parameters: {action.parameters}")

    
