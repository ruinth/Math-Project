from tkinter import *
from random import randint as ranNum
from pygame import mixer
import scoremanager

mixer.init()

window = Tk()                #WINDOW (this creates the window)
window.config(bg="#255ab7") #(unnessacarily) makes the background blue (its overwritten w the photo bg)
window.title("The Math Game v 0.3.10")
window.resizable(False, False)

mixer.Channel(1).play(mixer.Sound('mathegameasset\\sounds\\gamesong.wav'), loops=99999)

playerName =""     #this will become your chosen mame #TRANSRIJTS
playerAnswer = -99        #wthis will become your chosen ansewer
ops = []  #these are the operators chosen by the player
clicks = 0 #click counter for def submitClick():
level = 1

firstNumA =1
firstNumB =10
secondNumA =3
secondNumB = 12
correctInRow = 0
hardMode = False
devMode = False
codes = 0

skips = 5               #some useful things to keep track of
correctAnswers = 0 
incorrectAnswers = 0
questionNumber = 0
correctNum = 0
firstNum=0
secondNum=0
score = 0
combo = 0
selectedOp = 0

appendOpListAdd = True           #these are for adding to the list of ops
appendOpListSub = True                #they are used as a toggle to be able to add and remove ops
appendOpListMlt = True
appendOpListDiv = True

gameStart = False
music = 1

ScoreHandler = scoremanager.ScoreManager()  # our highscore manager :D
def toggleMute():
    global music
    music+=1
    if music%2 == 0:
        mixer.Channel(1).set_volume(0)
        muteButton.config(i=muteButtonArt)
    else:
        mixer.Channel(1).set_volume(1)
        muteButton.config(i=singingArt)



def startButtonClick():     #place instuctions & imput box & submit button. remove start button, 
    global playerName
    startButton.place_forget()                   #remove start button
    nameInstruc.pack(pady=20)      #tells u to put name (placing)
    nameInputBox.pack()    #box for ur name (placing)
    nameInputBox.focus() #focus you to the input box
    nameInputBox.bind("<Return>", codeCheckBOUND)      #makes it so you can hit enter (feeling fristy huh?) to subn mit name, making th ebyttib USELESS FUCK DAMN NOOOOOO imj so sorry submitButton </3
    submitButton.place(x=258, y=176)   #submit button (placing)
def codeCheckBOUND(event=None):
    codeCheck()
def codeCheck():
    global hardMode, codes, playerName, devMode
    playerName = nameInputBox.get()
    if 'dev' in playerName:
        devMode= True
        window.bind("<Button-1>",doSomething) #left mouse click
    if len(playerName) == 0:
        codes+=1
    if 'hard' in playerName:
        hardMode=True
        codes+=1
    if codes >= 1:
        nameInputBox.delete(0,END)
        codes = 0
        startButtonClick()
    else:
        submitClick()
def submitBOUND(event=None):
    submitClick()
def submitClick():                                    #this is when you click the submit button
    global playerName, clicks, ops, gameStart
    clicks+=1 #well it was clicked right?
    if clicks == 1:                        #first click
        nameInputBox.pack_forget()        #removes inputBox for name
        submitButton.place_forget()   #removes bthe button to submit
        nameInstruc.pack_forget()       #removes telling you to enter name

        playerName = nameInputBox.get()   #gets name
        nameTag.config(text=f"you are: {playerName}")  #makes a label say that
        nameTag.place(x=270,y=56)                                             #makes said label
        showOperators()               #shows the operators

    if clicks > 1:                                  #second click
        clicks+=1   #see line 41's comment
        if ops == []:                     #if no ops selected, tells you that
            noOpsPicked.pack(pady=10)            #no ops were piked, duh

        else:                        #if ops selected

            addButton.place_forget()       #removes + byttons 
            subButton.place_forget()    #remov - btn
            divButton.place_forget() #remove / btn
            mltButton.place_forget() #remove * btn
            submitButton.place_forget()  #remove submit buttn
            resetOpsButton.place_forget()   #removes reset ops buttn
            nameTag.place_forget()         #removes nametag
            chooseOpInstrc.place_forget()      #removes telling u to choose ops
            noOpsPicked.pack_forget()            #incanse u fucked it all up, its gone now
            submitOpsButton.place_forget()
            if gameStart == False:
                gameStart = True
                areYouReadyLabel.pack(pady=30)    #places label asking if you are ready
                readyButton.pack(pady=10)     #you are going to be ready. only yes button
                readyButton.focus()
                readyButton.bind("<Return>",startGameBOUND)

def showOperators():                                 #places 5 buttons & two labels.
 
    chooseOpInstrc.place(x=320, y=166)               #tells you to choose

    addButton.place(x=293, y= 258)            #these 4 are + - * / buttons being placed
    subButton.place(x=333, y= 256)       
    mltButton.place(x=374, y= 257)     
    divButton.place(x=418, y= 260)    
    window.bind("<plus>", addOpBOUND)                 #these allow you to hit the letter to add or remove it from list instead of clicking
    window.bind("<minus>", subOpBOUND)
    window.bind("<asterisk>", mulOpBOUND)
    window.bind("<slash>", divOpBOUND)
    window.bind("<Return>", submitBOUND)               #this makes enter key work^-^
    window.focus()
    resetOpsButton.place(x=252,y=255)    #resets all buttons to unclicked position  (button place)
    submitOpsButton.place(x=490, y=260) # submits selcected operatoes to lists of ops (button placemnet)

def addOpBOUND(event=None):
    addOp()
def subOpBOUND(event=None):
    subOp()
def mulOpBOUND(event=None):
    mulOp()
def divOpBOUND(event=None):
    divOp()
def addOp():              #these are commands that run when you click th buttons on the operators select screen
    global appendOpListAdd
    if appendOpListAdd == True:               #they check if it is to be added
        ops.append("+")          #if so they add
        addButton.config(relief=SUNKEN, fg = "#3B0404")
        appendOpListAdd = False     #and toggle states internally
    else:
        ops.remove("+")   #otherwise they remove
        addButton.config(relief=RAISED, fg = "#000000")
        appendOpListAdd = True           #& toggle back
def subOp():
    global appendOpListSub
    if appendOpListSub == True:
        ops.append("-")
        subButton.config(relief=SUNKEN, fg = "#3B0404")
        appendOpListSub = False
    else:
        ops.remove("-")
        subButton.config(relief=RAISED, fg = "#000000")
        appendOpListSub = True
def mulOp():
    global appendOpListMlt
    if appendOpListMlt == True:
        ops.append("*")
        mltButton.config(relief=SUNKEN, fg = "#3B0404")
        appendOpListMlt = False
    else:
        ops.remove("*")
        mltButton.config(relief=RAISED, fg = "#000000")
        appendOpListMlt = True
def divOp():
    global appendOpListDiv
    if appendOpListDiv == True:
        ops.append("/")
        divButton.config(relief=SUNKEN, fg = "#3B0404")
        appendOpListDiv = False
    else:
        ops.remove("/")
        divButton.config(relief=RAISED, fg = "#000000")
        appendOpListDiv = True

def resetOpsClick():    #this resets all of the operatos buttons to the unclicked state removes all ops from the opslist
    global appendOpListAdd, appendOpListSub, appendOpListDiv, appendOpListMlt, ops
    appendOpListAdd, appendOpListSub, appendOpListDiv, appendOpListMlt = True,True,True,True   #sets toggle to "to add"
    ops = []                                                                        #empties list
    addButton.config(relief=RAISED, fg = "#000000")
    subButton.config(relief=RAISED, fg = "#000000")             
    mltButton.config(relief=RAISED, fg = "#000000")
    divButton.config(relief=RAISED, fg = "#000000")
def startGameBOUND(event=None):
    startGame()
def startGame():        #ask first question(startubf the loop), switcg ready button for submitAns button, applies entry box for answers 
    global firstNumA, firstNumB, secondNumB, secondNumA, level
    window.unbind("<plus>")        
    window.unbind("<minus>")
    window.unbind("<asterisk>")             #the unbindening   (so it doersnt fuck up and trigger shit it shouldn't)
    window.unbind("<slash>")
    window.unbind("<Return>")                            #startub loop
    areYouReadyLabel.pack_forget()                                #kill ready questions label

    if hardMode == True:
        for a in range(4):
            firstNumA+=1
            firstNumB+=2
            secondNumA+=1
            secondNumB+=2
            level+=1
    questionLoop()  

    placeHearts()

def placeHearts():
    if hardMode == True:
        heart.pack(anchor="se")
        heart2.pack(anchor="se")
        heart3.pack(anchor="se")
    else:
        heart.pack(anchor="se")
        heart2.pack(anchor="se")
        heart3.pack(anchor="se")
        heart4.pack(anchor="se")
        heart5.pack(anchor="se")

def questionLoop():          #places the question label, and generates questions - ranNum & random ops from selected. chnages button seceretly. makes calculates answer
    global questionNumber, playerAnswer, correctNum, score, firstNum, secondNum, lenOp, selectedOp, firstNumA, firstNumB, secondNumB,secondNumA  
    firstNum = ranNum(firstNumA,firstNumB)                  #random numbers chosen for question
    secondNum = ranNum(secondNumA,secondNumB)
    lenOp = (len(ops)-1)                    #because list start at index 0
    selectedOp = ops[ranNum(0,lenOp)]   #this lets me print the question, and test what the operator is for calculating answers

    if selectedOp =="+":
        correctNum = firstNum + secondNum
    if selectedOp =="-":                         #ie if the index selected(operator) is -, itll ensure the answer is x - y
        if secondNum > firstNum:
            _temp = firstNum
            firstNum = secondNum
            secondNum = _temp
        correctNum = firstNum - secondNum
    if selectedOp =="*":
        correctNum = firstNum * secondNum
    if selectedOp =="/":                             # for division we have to do some tricks to make sure it doesn't end up in a decimal most of the time
        correctNum = firstNum / secondNum
        while correctNum%1!=0 and firstNum != secondNum:         # thats making sure it has no remader when divided by one
            firstNum=ranNum(1,200)                       #making one number way bigger
            secondNum=ranNum(3,15)                                               #and one little bigger
            correctNum = firstNum / secondNum   
    correctNum = round(correctNum)                       #this makes it have no ".0" at the end of the answer


    questionNumber+=1                                         #adds one to questions asked, becyase a q was aske d
    questionLabel.config(text=f"Q{questionNumber}: {firstNum} {selectedOp} {secondNum}")  #THIS SETS THE LABEL TO THE QUESTION
    questionLabel.pack()                                                                    # THIS PLACES THE LABEL WITH THE QUESTION

    levelLabel.place(x=303,y=203)
    levelLabel.config(text=f"level: {level}")
    answerBox.pack()                                                                #THIS PLACES THE BOX WHERE YOU ANSWER
    submitAnswerButton.config(text="submit answer", command = checkAnswer)      #configures button to check your answer with the def checkAnswer func // CONTINUES QUESTION / ANSWER LOOP
    submitAnswerButton.pack()                              #places button for you to submit answer\
    answerBox.bind("<Return>", checkAnswerBound)          #this allows for using the enter key to answer as well as submit buton
    answerBox.focus()                 #focus int he box
    scoreLabel.place(x=435,y=206)                                       #places score
    
    readyButton.pack_forget()                         #removes previous button that was forced to be submit answer


    if skips >0:                          #if you have any skips it'll make the skips button 
        skipButton.bind("<Return>", skipClickBOUND)      #so you can tab enter to skip ^*^
        skipButton.place(x=360,y=265)

def checkAnswerBound(event=None):         #for enter key a few lines up
    checkAnswer()
def checkAnswer():                                                #checks you answer, & if & or youtyped any codes in
    global playerAnswer, correctNum, correctAnswers, incorrectAnswers, skips, combo, score, firstNumA, firstNumB, secondNumA, secondNumB, correctInRow, level, devMode
    scoreLabel.config(text=f"score: {score}",fg="white",font = ("Helvetica", 15),)        #configs score every round
    playerAnswer = answerBox.get()                                #grabs your answer from the box 
    answerBox.delete(0,END)                                       #clears box
    scoreLabel.config(i=scoreFish1)

    if playerAnswer == str(correctNum):   
        soundCorrectAnswer()
        if ScoreHandler.is_high_score(score):
            highScoreLabel.place(x=114, y=296)                        #if your answer is correct
        correctAnswers+=1           #correct answe
        combo+=1           #combo up+
        correctInRow+=1 
        score += 10*(combo/2) #score adding
        score = round(score)   #score flattening
        scoreLabel.config(text=f"score: {score}",fg="white",font = ("Helvetica", 15),)
        if hardMode == True:
            score*=1.1
        fishScoreChanger()
        if correctInRow == 5:       #if you got 5 correct, the lowest numbers rise
            for a in range(1):
                firstNumA+=1
                firstNumB+=2
                secondNumA+=1
                secondNumB+=2
                level+=1
            correctInRow=0
        

    elif "skip" in playerAnswer:                             # if you skipped
        combo = 0               #c-c-c-c-combo breaker
        correctInRow = 0
        if skips >= 1:            #and have skips
            skips-=1                                #remove a skip
        if skips <= 0:                     #if you are now out
            skipButton.config(state=DISABLED, text="")
        if skips == 0:                                            #if you were already out
            incorrectAnswer()

    elif playerAnswer != str(correctNum):          #if you are wrong
        combo = 0                       #c-c-c-c-c-combo breaker
        correctInRow = 0             
        incorrectAnswer()
    if hardMode == False:
        if incorrectAnswers < 5:                                      #if you are at less than 5 inc answers
            questionLoop()                  #CONTINUE QUESTION / ANSWER LOOP
    if hardMode == True:
        if incorrectAnswers <3:
            questionLoop()

def skipClickBOUND(event=None):
    skipClick()
def skipClick():                             #for if youre feeling frisky & want skip
    global skips, incorrectAnswers, combo, correctInRow
    combo = 0                            #c-c-c-c-combo breaker
    correctInRow = 0
    if skips >= 1 and incorrectAnswers < 5:             #if yoy have 1 or more skips, and less than 5 wrong answwrs
        skips-=1
        if skips == 0:
            skipButton.config(state=DISABLED, text="")                                           #use a skip
    elif skips < 1:                          #if you have no skips left
        incorrectAnswer()
    questionLoop()                   #repeat loop

def incorrectAnswer():                                                    #on incorrect answer, kills a heart & shows correct answer over score board
    global incorrectAnswers, correctNum, firstNum, secondNum, selectedOp, score
    soundIncorrectAnswer()
    incorrectAnswers+=1
    if incorrectAnswers == 1:
        heart.config(i=heartBrokeArt)
    elif incorrectAnswers == 2:
        heart2.config(i=heartBrokeArt)
    elif incorrectAnswers == 3:
        heart3.config(i=heartBrokeArt)
    elif incorrectAnswers == 4:
        heart4.config(i=heartBrokeArt)
    elif incorrectAnswers == 5:
        heart5.config(i=heartBrokeArt)
    scoreLabel.config(text= f"{firstNum}{selectedOp}{secondNum}={correctNum}", fg="black", font = ("Helvetica", 15),)
    if hardMode == True:
        score=0
        if incorrectAnswers>=3:
            gameLoss()
    else:
        if incorrectAnswers>=5:
            gameLoss()


def fishScoreChanger():
    global score
    if score >= 50:
        scoreLabel.config(i=scoreFish2)
    if score >= 200:
        scoreLabel.config(i=scoreFish3)     
    if score >=  450:
        scoreLabel.config(i=scoreFish4)     
    if score >= 1200:
        scoreLabel.config(i=scoreFish5)
    if score >= 3500:
        scoreLabel.config(i=scoreFish6)

def gameLoss():                                #makes a pretty end screen
    skipButton.config(state = DISABLED, text = "")                          #button bad
    scoreLabel.config(text=f"final score: {score}", fg="#FFFFFF", font = ("Helvetica", 15))               #final score print
    submitAnswerButton.config(text="", state=DISABLED)                  #button turn off
    answerBox.pack_forget()                                 #kill anserr box
    questionLabel.config(text="game over")             #game over rexr
    playAgainButton.place(x=115,y=100)            #place button to play again
    levelLabel.config(text="")                        #removes text from turtle
    if devMode == False:
        ScoreHandler.addHighScore(playerName, score)
    viewScoresButton.place(x=300,y=400)

def highScores():
        global playerName, score
        viewScoresButton.place_forget()
        questionLabel.pack_forget()
        scoreLabel.place_forget()
        heart.pack_forget()
        heart2.pack_forget()
        heart3.pack_forget()
        heart4.pack_forget()
        heart5.pack_forget()
        submitAnswerButton.pack_forget()
        skipButton.place_forget()
        levelLabel.place_forget()
        highScoreLabel.place_forget()
        nameInstruc.config(text="HIGH SCORES")
        nameInstruc.pack()

        ScoreHandler.apply_sort()
        scores = ScoreHandler.high_scores

        labels = [firstPlaceLabel, secondPlaceLabel, thirdPlaceLabel]
        places = ["1st", "2nd", "3rd"]

        for i, label in enumerate(labels):
            if i < len(scores):
                entry = scores[i]
                label.config(text=f"{places[i]}- {entry['name']} ({entry['score']})")
            else:
                label.config(text=f"{places[i]}- ---")
            label.pack()

def playAgain():             #RESETS ALL VARIABLES AND REMOVES ALL PLACED BUTTONS AND LABELS AND FINALLY PLACES START BUTTON
    global playerAnswer, playerName, ops, clicks, skips, correctAnswers, incorrectAnswers, questionNumber, correctNum, firstNum, secondNum, score, combo, selectedOp, appendOpListAdd, appendOpListDiv, appendOpListMlt, appendOpListSub, gameStart
    global firstNumB, firstNumA, secondNumB, secondNumA, correctInRow, hardMode, level, devMode
    questionLabel.pack_forget()
    nameInstruc.config(text="enter player name")
    scoreLabel.place_forget()
    heart5.config(i=heartArt)
    heart4.config(i=heartArt)
    heart3.config(i=heartArt)
    heart2.config(i=heartArt)
    heart.config(i=heartArt)
    heart.pack_forget()
    heart2.pack_forget()
    heart3.pack_forget()
    heart4.pack_forget()
    heart5.pack_forget()
    submitAnswerButton.pack_forget()
    skipButton.place_forget()
    playAgainButton.place_forget()
    levelLabel.place_forget()
    highScoreLabel.place_forget()
    nameInstruc.pack_forget()
    viewScoresButton.place_forget()
    firstPlaceLabel.pack_forget()
    secondPlaceLabel.pack_forget()
    thirdPlaceLabel.pack_forget()
    submitAnswerButton.config(state=ACTIVE, text="submit answer", bg= "#255ab7", border = 0, fg="#FFFFFF") 
    skipButton.config(state=ACTIVE, text="skip")
    firstNumA =1
    firstNumB =10
    secondNumA =3
    secondNumB = 12
    correctInRow = 0
    playerName =""  
    playerAnswer = -99  
    ops = []  
    clicks = 0 
    skips = 5             
    correctAnswers = 0 
    incorrectAnswers = 0
    questionNumber = 0
    correctNum = 0
    firstNum=0
    secondNum=0
    score = 0
    combo = 0
    selectedOp = 0
    level = 1
    appendOpListAdd = True    
    appendOpListSub = True            
    appendOpListMlt = True
    appendOpListDiv = True
    gameStart = False
    hardMode = False
    devMode = False
    startButton.place(x=334,y=220)

def soundIncorrectAnswer():
    mixer.music.load("mathegameasset\\sounds\\incorrect.wav")
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=0)
def soundCorrectAnswer():
    mixer.music.load("mathegameasset\\sounds\\correct.wav")
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=0)
# THIS WILL BE THE ART THAT IS USED THIS BLOCK RIGHT HERE AND NOWHERE ELES
operatorButtonArt = PhotoImage(file="mathegameasset\\MUSHBUTTON001.png").subsample(20,20)
windowBgArt= PhotoImage(file="mathegameasset\\BACKGROUNWATER001.png")
logLabelArt = PhotoImage(file="mathegameasset\\LOGBUTTON001.png").subsample(2,2)
submitButtonArt = PhotoImage(file="mathegameasset\\lilypadbutton001.png").subsample(4,4)
startButtonArt= PhotoImage(file="mathegameasset\\butterflySTARTBUTTON001.png").subsample(3,4) 
nameTagArt = PhotoImage(file="mathegameasset\\fishLabel.png").subsample(2,2) 
chooseOpsArt = PhotoImage(file="mathegameasset\\fishLabel2.png").subsample(2,2) 
readyLabelArt = PhotoImage(file="mathegameasset\\duckbuttonart.png").subsample(2,2) 
readyButtonArt = PhotoImage(file="mathegameasset\\fish3.png").subsample(2,2) 
submitAnswerArt = PhotoImage(file="mathegameasset\\fishLabel.png").subsample(2,2) 

heartArt = PhotoImage(file="mathegameasset\\HEARTS.png")
heartBrokeArt = PhotoImage(file="mathegameasset\\HEARTBROKEN.png")

levelLabelArt = PhotoImage(file="mathegameasset\\levelART.png")
playAgainArt = PhotoImage(file="mathegameasset\\birdplayagin.png")
highScoreArt = PhotoImage(file="mathegameasset\\highscore.png").subsample(2,2)
firstPlaceArt = PhotoImage(file="mathegameasset\\goldFISH.png").subsample(3,3)
secondPlaceArt = PhotoImage(file="mathegameasset\\SILVfish.png").subsample(3,3)
thirdPlaceArt = PhotoImage(file="mathegameasset\\bronzFish.png").subsample(3,3)
muteButtonArt = PhotoImage(file="mathegameasset\\muteClam.png").subsample(2,2)
singingArt = PhotoImage(file="mathegameasset\\singClam.png").subsample(2,2)

scoreFish1 = PhotoImage(file="mathegameasset\\scorefish1.png")
scoreFish2= PhotoImage(file="mathegameasset\\scorefish2.png")
scoreFish3= PhotoImage(file="mathegameasset\\scorefish3.png")
scoreFish4= PhotoImage(file="mathegameasset\\scorefish4.png")
scoreFish5= PhotoImage(file="mathegameasset\\scorefish5.png")
scoreFish6= PhotoImage(file="mathegameasset\\scorefish6.png")

backgroundLabl = Label(window, i=windowBgArt)   #this makes a big label to be the background, and give that label the background art
backgroundLabl.place(x=-5,y=-5)              #places label so its a little out
window.geometry("800x600")                     #WINDOW size 
window.grid()

 #                                            below are entry boxes, labels*, then buttons. tried my best                       *most labels

nameInputBox = Entry(window,                         #input box for name                 (entry)
                     font=("Helvetica", 20),
                     bg = "#2767BB",               #background color
                     fg = "#FFFFFF")               #text color

answerBox = Entry(window,                             #answer box for answering in        (entry)
                  bg = "#2767BB",                   #background color
                  fg = "#FFFFFF",                   #text color
                  font = ("Helvetica", 20),)                          #font size

nameInstruc = Label(window, text="enter player name",  #tells you to enter name below     (label)
                    i=logLabelArt,                   #use art (log)
                    bg = "#255ab7",
                    fg="#FFFFFF",
                    font = ("Helvetica", 15),  
                    compound="center")               #below text

nameTag = Label(window,         #will display player name. empty text for now             (label)
                font = ("Helvetica", 14),
                bg= "#255ab7",                           #background color
                fg="white",                                #text color
                i = nameTagArt,                           #art use (fish)
                compound="center")                         #below text

chooseOpInstrc = Label(window, text="choose your operators", #ask you to choose operators (label)   
                       font = ("Helvetica", 15),             
                       bg = "#255ab7",             #background color
                       i = chooseOpsArt,
                       compound="center",
                       fg = "#000000")            #text color            

noOpsPicked = Label(window, text="no operators chosen", #tells if you have no operators    (label)
                    font = ("Helvetica", 70),
                    bg="green",                      #text color
                    fg= "red")                       #background color 

highScoreLabel = Label(window, text="NEW HIGH SCORE",
                       font=("Helvetica", 15),
                       bg="#255ab7",
                       fg="#000000",
                       i = highScoreArt,
                       compound="center")

questionLabel = Label(window,
                      i = logLabelArt,
                      compound="center",
                      font = ("Helvetica", 15),
                      fg="#FFFFFF",
                      bg= "#255ab7")                        #              will ask question l8r  (label)

scoreLabel = Label(window, text=(f"score: {score}"),  #will display your score             (label)
                   font = ("Helvetica", 15),
                   bg = "#255ab7",                  #background color
                   i = scoreFish1,
                   compound="center",
                   border=0,
                   fg = "#FFFFFF")                  #text color

firstPlaceLabel = Label(window, i = firstPlaceArt, compound="center", border=0, bg= "#255ab7")
secondPlaceLabel = Label(window, i = secondPlaceArt, compound="center",border=0, bg= "#255ab7")
thirdPlaceLabel = Label(window, i = thirdPlaceArt,compound="center",border=0, bg= "#255ab7")

heart = Label(window, i=heartArt, border=0)
heart2 = Label(window, i=heartArt, border=0)
heart3 = Label(window, i=heartArt, border=0)
heart4 = Label(window, i=heartArt, border=0)
heart5 = Label(window, i=heartArt, border=0)

levelLabel = Label(window, text=f"level: {level}",    #will display what lebel you are on  (label)
                    i= levelLabelArt,                  #using turtle art
                    bg="#255ab7",           #water bg
                    border=0,  
                    font = ("Helvetica", 15),
                    compound="center")              #under text

areYouReadyLabel = Label(window, text = "Ready?",  #to ask if you're ready        (label)
                         i = readyLabelArt,
                         font = ("Helvetica", 15),
                         compound="center",
                         bg="#255ab7",
                         fg ="#0018F0")

readyButton = Button(window, text="Yes",      #ready for game button                 (button)
                     command=startGame,            #run command
                    border= 0,
                    i = readyButtonArt,
                    font = ("Helvetica", 15),
                    bg = "#255ab7",
                    fg = "#FFFFFF",
                    compound="center")

muteButton = Button(window, text="",
                    command=toggleMute,
                    bg="#255ab7",
                    i=singingArt,
                    border=0)

skipButton = Button(window, text = "skip",  #skip button                         (button)
                    command=skipClick,              #run command
                    font = ("Helvetica", 15),
                    bg = "#255ab7",               #background color
                    i = submitButtonArt,
                    compound="center",
                    border=0,
                    fg = "#02680B")               #text color
               
submitButton = Button(window, text="submit",       #submit button                         (button)
                      command=codeCheck,          #gives command
                      font = ("Helvetica", 15),
                      bg = "#255ab7", 
                      image = submitButtonArt,      #use art (lily pad)
                      compound="center",            #below text
                      fg = "#02680B",             #text color
                      border = 0)

submitOpsButton = Button(window, text="submit",       #submit button                         (button)
                      command=submitClick,          #gives command
                      font = ("Helvetica", 15),
                      bg = "#255ab7", 
                      image = submitButtonArt,      #use art (lily pad)
                      compound="center",            #below text
                      fg = "#02680B",             #text color
                      border = 0)

resetOpsButton = Button(window, text="reset selections",   #reset ops bytton              (button)
                        command = resetOpsClick,   #runs commd
                        bg = "#255ab7",          #border color
                        font = ("Helvetica", 15),
                        i=logLabelArt,             #use art (log)
                        compound="center",         #art below text
                        fg = "#FFFFFF",             #text color
                        border = 0)

addButton = Button(window, text="+",       # +, -, *, / buttons ( this & following 3)     (button)
                   command=addOp,                  #runs command
                   font = ("Helvetica", 15),
                   bg = "#255ab7", 
                   i=operatorButtonArt,            #use art (mushroom)
                   compound="center",              #under text
                   fg = "#000000",             #text color
                   border = 0)
subButton = Button(window, text="-", 
                   command=subOp, 
                   font = ("Helvetica", 15),
                   bg = "#255ab7", 
                   i=operatorButtonArt,
                   compound="center",
                   fg = "#000000",
                   border=0)
mltButton = Button(window, text="*", 
                   command= mulOp, 
                   font = ("Helvetica", 15),
                   bg = "#255ab7", 
                   i=operatorButtonArt,
                   compound="center",
                   fg = "#000000",
                   border=0)
divButton = Button(window, text="/", 
                   command=divOp, 
                   font = ("Helvetica", 15),
                   bg = "#255ab7", 
                   i=operatorButtonArt, 
                   compound="center",
                   fg = "#000000",
                   border=0)

submitAnswerButton = Button(window, text="submit answer",   #submit answer button       (button)
                            font = ("Helvetica", 15),
                            bg= "#255ab7",          #background  color
                            i = submitAnswerArt,         #red fish
                            compound="center",         #below art
                            border = 0,
                            fg="#FFFFFF")           #text color        

playAgainButton = Button(window, text="play again",      #play agin button            (button)
                         command = playAgain,      #command !    
                         font = ("Helvetica", 15),
                         bg= "#255ab7",       #background colo
                         i=playAgainArt,
                         compound="center",
                         border=0)         #no border

viewScoresButton = Button(window, text="View High Scores",
                         compound="center",
                         font=("Helvetica", 15),
                         border=0,
                         bg="#255ab7",
                         fg="#FFFFFF",
                         i = logLabelArt,
                         command=highScores)

startButton = Button(window,text="click to start",    #button for starting game!        (button)
                     command= startButtonClick,   #runs command
                     font = ("Helvetica", 15),
                     bg = "#255ab7", 
                     image=startButtonArt,        #use art (butterfly)
                     compound="center",           #below text
                     fg= "#FFFFFF",             #text color
                     border = 0,
                     height=100,
                     width=140)

startButton.place(x=334,y=220)  #places the start button, as it needs to be placed
muteButton.place(x=690, y=20)


def doSomething(event):
    global devMode
    if devMode == True:
        print("Mouse coordinates: " + str(event.x)+","+str(event.y))


window.mainloop()       #I AM GOD, CREATOR OF WINDOW 