from tkinter import *
from random import randint as ranNum
from pygame import mixer       #for music
import scoremanager
from os import path
from sys import platform as _PLATFORM

ASSET_DIR = path.join(path.dirname(path.abspath(__file__)), "mathegameasset")

mixer.init()                 #makes msuic be ready

window = Tk()                # (this creates the window) 
window.title("Afishmetic v 0.3.5 (Linux Test)")                   #title
window.option_add("*Button.activeBackground", "#255ab7")
window.option_add("*Button.highlightThickness", 0)



if _PLATFORM == "win32":
    window.iconbitmap(path.join(ASSET_DIR, "icon.ico"))         #icon (only in top corner. real icon is changed manually rn)
elif _PLATFORM == "linux" or _PLATFORM == "darwin":  #linux and mac have no icon
    window.iconphoto(True, PhotoImage(file=path.join(ASSET_DIR, "sing_clam.png")))  # xd linux has higher quality icon
    

window.resizable(False, False)                       #no resizing the window

mixer.Channel(1).play(mixer.Sound(path.join(ASSET_DIR, "sounds", "gamesong.wav")), loops=99999)   #starts the theme song. plays it 100 times

playerName =""     #this will become your chosen mame #TRANSRIJTS
playerAnswer = -99        #wthis will become your chosen ansewer
ops = []  #these are the operators chosen by the player
clicks = 0 #click counter for def submitClick(): (submitclick is a mess. why not two buttons instead)

level = 1                    #some useful things to keep track of
firstNumA =1
firstNumB =10
secondNumA =3
secondNumB = 12
correctInRow = 0
hardMode = False
devMode = False
codes = 0
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
creditsRolled=1
music = 1
gameStart = False

appendOpListAdd = True           #these are for adding to the list of ops
appendOpListSub = True                #they are used as a toggle to be able to add and remove ops
appendOpListMlt = True
appendOpListDiv = True

ScoreHandler = scoremanager.ScoreManager()  # our highscore manager :D

def toggleMute():              #this is the command that runs on clicking the mute button
    global music
    music+=1                               
    if music%2 == 0:                            
        mixer.Channel(1).set_volume(0)          #sets volume to 0 & closes the clam 
        muteButton.config(i=muteButtonArt)
    else:
        mixer.Channel(1).set_volume(1)            #or sets volume to 1 &opens the clam
        muteButton.config(i=singingArt)

def startButtonClick():     #this is the command that runs on clicking the start bytton
    global playerName
    startButton.place_forget()                   #remove start button & credits button
    creditsButton.place_forget()
    nameInstruc.pack(pady=20)               #places instruction label & input box 
    nameInputBox.pack()                 
    nameInputBox.focus()                     #focus you to the input box
    nameInputBox.bind("<Return>", codeCheckBOUND)    #binds enter key to inp box
    submitButton.place(x=258, y=176)      #placing submit button

def codeCheckBOUND(event=None):
    codeCheck()
def codeCheck():                               #this is the command that runs when you submit your name
    global hardMode, codes, playerName, devMode
    playerName = nameInputBox.get()   
    if 'dev' in playerName:                     #if dev, prints location on click & turns  devMode on
        devMode= True
        window.bind("<Button-1>",devClick) 
    if len(playerName) == 0:                      #if empty, add code
        codes+=1
    if 'hard' in playerName:                        # if hard, turns hm on, add code
        hardMode=True                                       
        codes+=1
    if codes >= 1:   
        nameInputBox.delete(0,END)
        codes = 0                           #on code, empty codes & makes you choose again
        startButtonClick()
    else:
        submitClick()                      #otherwise, runs command

def devClick(event):            #this is the func to make placing things easier when devmode is on
    global devMode
    if devMode == True:
        print("Mouse x=" + str(event.x)+", y="+str(event.y))

def submitBOUND(event=None):
    submitClick()
def submitClick():                                    #this is the command that runs when you click the submit button
    global playerName, clicks, ops, gameStart
    clicks+=1        
    if clicks == 1:                        #first time in the block
        nameInputBox.pack_forget()       
        submitButton.place_forget()    #removes submit button, instructions & box for name
        nameInstruc.pack_forget()      

        playerName = nameInputBox.get()                   #gets name from inputbox ^
        nameTag.config(text=f"you are: {playerName}")  #gives your name to the nametag
        nameTag.place(x=270,y=56)                        #places nametag label
        showOperators()               #then places the screen for selecting your operators

    if clicks > 1:                    #second time in the block. please see def showOperators(): first
        clicks+=1                            #(this is the commmand that runs when you hit submit ops)
        if ops == []:                     
            noOpsPicked.pack(pady=10)           #on no operators selected, tells you no ops selected
        else:                      
            addButton.place_forget()       
            subButton.place_forget()
            divButton.place_forget()
            mltButton.place_forget()           #when operators selected, removes all buttons & labels from sceern
            submitButton.place_forget()
            resetOpsButton.place_forget()  
            nameTag.place_forget()      
            chooseOpInstrc.place_forget()     
            noOpsPicked.pack_forget()          
            submitOpsButton.place_forget()
            if gameStart == False:                 #??? not sure 
                gameStart = True           
                areYouReadyLabel.pack(pady=30)     #places the label & yes button for if you are ready to play
                readyButton.pack(pady=10)    
                readyButton.focus()                                    #ready bytton runs startGame command
                readyButton.bind("<Return>",startGameBOUND)         #binds enter key to yes button ^

def showOperators(): #this is the command that runs when you submit your name
    chooseOpInstrc.place(x=320, y=166)             
    addButton.place(x=293, y= 258)            #these are instructions & the + - * / buttons being placed
    subButton.place(x=333, y= 256)       
    mltButton.place(x=374, y= 257)     
    divButton.place(x=418, y= 260)    
    window.bind("<plus>", addOpBOUND)       #these allow you to hit the symbol to toggle
    window.bind("<minus>", subOpBOUND)
    window.bind("<asterisk>", mulOpBOUND)
    window.bind("<slash>", divOpBOUND)
    
    window.focus()                        #?
    resetOpsButton.place(x=252,y=255)    #places btton for reseting your selections 
    submitOpsButton.place(x=490, y=260) # places button for  submitting your chosen op
    window.bind("<Return>", submitBOUND)  #this binds enter key to submit button^

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
def startGame():        #this is the commmand that runs when you hit "yes" to the ready button 
    global firstNumA, firstNumB, secondNumB, secondNumA, level
    window.unbind("<plus>")        
    window.unbind("<minus>")
    window.unbind("<asterisk>")             #unbinds operator keys so you cannot mess with list mid game
    window.unbind("<slash>")
    window.unbind("<Return>")                           
    areYouReadyLabel.pack_forget()                             #remove ready label& button
    readyButton.pack_forget()                         
    scoreLabel.config(text=f"score: {score}", i=scoreFish1)  #this is a fish displaying your score. *configuring*
    levelLabel.config(text=f"level: {level}")  #level label being configured
    if hardMode == True:
        for a in range(4):
            firstNumA+=1               #if you are in hardmode, its harder. 
            firstNumB+=2
            secondNumA+=1
            secondNumB+=2
            level+=1
            levelLabel.config(text=f"level: {level}")  #makes level label reflect that
    questionLabel.pack()          #places label that will ask question, & box that you'll input answers in
    answerBox.pack()                                      
    submitAnswerButton.pack()            #button for clicking submitANswer - and label displaying level number
    levelLabel.place(x=303,y=203)
    scoreLabel.place(x=435,y=206)                                       #places score label
    placeHearts()                   #places hearts
    questionLoop()                       #starts loop by running "asking the question" (other half is "checking the answer")    

def placeHearts():
    if hardMode == True:
        heart.pack(anchor="se")
        heart2.pack(anchor="se")            #if you are in hardmode, its harder
        heart3.pack(anchor="se")
    else:
        heart.pack(anchor="se")
        heart2.pack(anchor="se")           #places 5 lives for you!
        heart3.pack(anchor="se")
        heart4.pack(anchor="se")
        heart5.pack(anchor="se")

def questionLoop():        #one half of the gameplay loop
    global questionNumber, playerAnswer, correctNum, score, firstNum, secondNum, lenOp, selectedOp, firstNumA, firstNumB, secondNumB,secondNumA  
    firstNum = ranNum(firstNumA,firstNumB)                  #random numbers chosen for question
    secondNum = ranNum(secondNumA,secondNumB)
    lenOp = (len(ops)-1)                    #list start at index 0
    selectedOp = ops[ranNum(0,lenOp)]   #selected a random operator
    if selectedOp =="+":                        # if the selected op is +, itll make the question x - y
        correctNum = firstNum + secondNum
    if selectedOp =="-":                         # for sub we have to take some proactive measures to remove negative answers
        if secondNum > firstNum:
            _temp = firstNum                               #they were unfun to enter
            firstNum = secondNum
            secondNum = _temp
        correctNum = firstNum - secondNum
    if selectedOp =="*":                       
        correctNum = firstNum * secondNum
    if selectedOp =="/":                             #division does tricks to make all #s intergers everytime
        correctNum = firstNum / secondNum
        while correctNum%1!=0 and firstNum != secondNum:         # thats by making sure it has no remader when divided by one
            firstNum=ranNum(1,200)                      
            secondNum=ranNum(3,15)                                             
            correctNum = firstNum / secondNum   
    correctNum = round(correctNum)                       #rounds the answer down to NO decimal places (2 inst of 2.0)
    questionNumber+=1    #adds 1, for obvi- below configs label to print the question
    questionLabel.config(text=f"Q{questionNumber}: {firstNum} {selectedOp} {secondNum}")   
    answerBox.bind("<Return>", checkAnswerBound)         
    answerBox.focus()     #focus in the answer box ^ lets you press enter to answer
    if skips >0:                          #if you have any skips it'll make the skips button (happens every loop bc idk im bad)
        skipButton.bind("<Return>", skipClickBOUND)      #so you can tab to enter to skip ^^
        skipButton.place(x=360,y=265)                  

def checkAnswerBound(event=None):
    checkAnswer()
def checkAnswer():    #the commands that runs when we enter our answer
    global playerAnswer, correctNum, correctAnswers, incorrectAnswers, skips, combo, score, firstNumA, firstNumB, secondNumA, secondNumB, correctInRow, level, devMode
    scoreLabel.config(text=f"score: {score}",fg="white",font = ("Helvetica", 15),)        #configs score every round
    playerAnswer = answerBox.get()          #grabs your answer from the box 
    answerBox.delete(0,END)              #clears your input
    if playerAnswer == str(correctNum):   
        soundCorrectAnswer()
        if ScoreHandler.is_high_score(score):   #if you have highscore, shwo yoy!
            highScoreLabel.place(x=114, y=296)              
        correctAnswers+=1              #if your answer is correct
        combo+=1           #combo up+
        correctInRow+=1 
        score += 10*(((combo)+(level)*0.5))
        score = round(score)   #rounds score to NO decimal places   vvv configs score for uou!
        scoreLabel.config(text=f"score: {score}",fg="white",font = ("Helvetica", 15),)
        if hardMode == True:
            score*=1.05       #woah...big
        fishScoreChanger()   #if your score is large enough, gives you a bigger fish
        if correctInRow == 5:       #if you got 5 correct in a row, the game gets harder
            if level != 10 or hardMode == True:
                for a in range(1):
                    firstNumA+=1
                    firstNumB+=2
                    secondNumA+=1
                    secondNumB+=2
                    level+=1
                    levelLabel.config(text=f"level: {level}") 
                correctInRow=0
    
    elif "skip" in playerAnswer:                             # if you skipped
        skipClick()

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
def skipClick():                             
    global skips, incorrectAnswers, combo, correctInRow
    combo = 0                            #c-c-c-c-combo breaker
    correctInRow = 0
    if skips >= 1 and incorrectAnswers < 5:             #if yoy have 1 or more skips, and less than 5 wrong answwrs
        skips-=1 
        if skips == 0:          #if you have no skips left
            skipButton.config(state=DISABLED, text="")                                     
    elif skips < 1:                     #  if you alreasdy had no skips left
        incorrectAnswer()

def incorrectAnswer():  #               the command the runs when you get the answer wrong
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
        score/=2
        score = round(score)
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

def rollCredits():
    global creditsRolled
    creditsRolled+=1
    if creditsRolled%2==0:
        startButton.place_forget()
        creditLabel.pack()
        creditsButton.config(text="go  back")
    else:
        startButton.place(x=334,y=220)
        creditLabel.pack_forget()
        creditsButton.config(text="CREDITS")

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
    mixer.music.load(path.join(ASSET_DIR, "sounds", "incorrect.wav"))
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=0)
def soundCorrectAnswer():
    mixer.music.load(path.join(ASSET_DIR, "sounds", "correct.wav"))
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=0)
# THIS WILL BE THE ART THAT IS USED THIS BLOCK RIGHT HERE AND NOWHERE ELES
operatorButtonArt = PhotoImage(file=path.join(ASSET_DIR, "button_mushroom_001.png")).subsample(20,20)
windowBgSource = PhotoImage(file=path.join(ASSET_DIR, "background_water_001.png"))
windowBgArt = PhotoImage(width=800, height=600)
windowBgArt.tk.call(
    str(windowBgArt),
    "copy",
    str(windowBgSource),
    "-from", 10, 10, 810, 610,
    "-to", 0, 0,
)
logLabelArt = PhotoImage(file=path.join(ASSET_DIR, "button_log_001.png")).subsample(2,2)
submitButtonArt = PhotoImage(file=path.join(ASSET_DIR, "button_lilypad_001.png")).subsample(4,4)
startButtonArt= PhotoImage(file=path.join(ASSET_DIR, "butterfly_start_button_001.png")).subsample(3,4)
nameTagArt = PhotoImage(file=path.join(ASSET_DIR, "fish_label.png")).subsample(2,2)
chooseOpsArt = PhotoImage(file=path.join(ASSET_DIR, "fish_label_002.png")).subsample(2,2)
readyLabelArt = PhotoImage(file=path.join(ASSET_DIR, "duck_button_art.png")).subsample(2,2)
readyButtonArt = PhotoImage(file=path.join(ASSET_DIR, "fish_003.png")).subsample(2,2)
submitAnswerArt = PhotoImage(file=path.join(ASSET_DIR, "fish_label.png")).subsample(2,2)
heartArt = PhotoImage(file=path.join(ASSET_DIR, "heart.png"))
heartBrokeArt = PhotoImage(file=path.join(ASSET_DIR, "heartbroken.png"))
levelLabelArt = PhotoImage(file=path.join(ASSET_DIR, "level_art.png"))
playAgainArt = PhotoImage(file=path.join(ASSET_DIR, "bird_play_again.png"))
highScoreArt = PhotoImage(file=path.join(ASSET_DIR, "highscore.png")).subsample(2,2)
firstPlaceArt = PhotoImage(file=path.join(ASSET_DIR, "fish_gold.png")).subsample(3,3)
secondPlaceArt = PhotoImage(file=path.join(ASSET_DIR, "fish_silv.png")).subsample(3,3)
thirdPlaceArt = PhotoImage(file=path.join(ASSET_DIR, "fish_bronze.png")).subsample(3,3)
muteButtonArt = PhotoImage(file=path.join(ASSET_DIR, "mute_clam.png")).subsample(2,2)
singingArt = PhotoImage(file=path.join(ASSET_DIR, "sing_clam.png")).subsample(2,2)
scoreFish1 = PhotoImage(file=path.join(ASSET_DIR, "scorefish_001.png"))
scoreFish2= PhotoImage(file=path.join(ASSET_DIR, "scorefish_002.png"))
scoreFish3= PhotoImage(file=path.join(ASSET_DIR, "scorefish_003.png"))
scoreFish4= PhotoImage(file=path.join(ASSET_DIR, "scorefish_004.png"))
scoreFish5= PhotoImage(file=path.join(ASSET_DIR, "scorefish_005.png"))
scoreFish6= PhotoImage(file=path.join(ASSET_DIR, "scorefish_006.png"))
creditArt = PhotoImage(file=path.join(ASSET_DIR, "credit_art.png"))

backgroundLabl = Label(window, image=windowBgArt, border=0, highlightthickness=0) 
backgroundLabl.place(x=0, y=0)
backgroundLabl.lower()
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

creditLabel = Label(window, i=creditArt)

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
                            command=checkAnswer,
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

creditsButton = Button(window, text="CREDITS",
                       command=rollCredits,
                       font=("Helvetica", 15),
                       bg= "#255ab7",
                       i=logLabelArt,
                       border=0,
                       compound="center",
                       fg="#FFFFFF")

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
creditsButton.place(x=300,y=500)
muteButton.place(x=690, y=20)





window.mainloop()       #I AM GOD, CREATOR OF WINDOW 