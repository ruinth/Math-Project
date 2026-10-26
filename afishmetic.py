from tkinter import *
from random import randint as ranNum
from pygame import mixer       #for music
import scoremanager
from os import path
from sys import platform as _PLATFORM

ASSET_DIR = path.join(path.dirname(path.abspath(__file__)), "mathegameasset")

mixer.init()                 #makes msuic be ready

window = Tk()                # (this creates the window) 
window.title("Afishmetic v 0.3.6 (now_in_snake_case)")                   #title
window.option_add("*Button.activeBackground", "#255ab7")
window.option_add("*Button.highlightThickness", 0)



if _PLATFORM == "win32":
    window.iconbitmap(path.join(ASSET_DIR, "icon.ico"))         #icon (only in top corner. real icon is changed manually rn)
elif _PLATFORM == "linux" or _PLATFORM == "darwin":  #linux and mac have no icon
    window.iconphoto(True, PhotoImage(file=path.join(ASSET_DIR, "sing_clam.png")))  # xd linux has higher quality icon
    

window.resizable(False, False)                       #no resizing the window

mixer.Channel(1).play(mixer.Sound(path.join(ASSET_DIR, "sounds", "gamesong.wav")), loops=99999)   #starts the theme song. plays it 100 times

player_name =""     #this will become your chosen mame #TRANSRIJTS
player_answer = -99        #wthis will become your chosen ansewer
operator_list = []  #these are the operators chosen by the player
clicks = 0 #click counter for def submit_click(): (submitclick is a mess. why not two buttons instead)

level = 1                    #some useful things to keep track of
first_num_a =1
first_num_b =10
second_num_a =3
second_num_b = 12
correct_in_a_row = 0
hard_mode = False
dev_mode = False
codes = 0
skips = 5               
correct_answers = 0 
incorrect_answers = 0
question_number = 0
correct_number = 0
first_q_number=0
second_q_number=0
score = 0
combo = 0
selected_operator = 0
credits_rolled=1
music = 1
game_start = False

append_add_to_list = True           #these are for adding to the list of operator_list
append_sub_to_list = True                #they are used as a toggle to be able to add and remove operator_list
append_mlt_to_list = True
append_div_to_list = True

score_handler = scoremanager.ScoreManager()  # our highscore manager :D

def toggle_music_mute():              #this is the command that runs on clicking the mute button
    global music
    music+=1                               
    if music%2 == 0:                            
        mixer.Channel(1).set_volume(0)          #sets volume to 0 & closes the clam 
        mute_button.config(i=mute_button_art)
    else:
        mixer.Channel(1).set_volume(1)            #or sets volume to 1 &opens the clam
        mute_button.config(i=sing_button_art)

def on_start_button_click():     #this is the command that runs on clicking the start bytton
    global player_name
    start_game_button.place_forget()                   #remove start button & credits button
    credits_button.place_forget()
    name_instructions.pack(pady=20)               #places instruction label & input box 
    name_entry_box.pack()                 
    name_entry_box.focus()                     #focus you to the input box
    name_entry_box.bind("<Return>", code_check_bound)    #binds enter key to inp box
    submit_button.place(x=258, y=176)      #placing submit button

def code_check_bound(event=None):
    code_check()
def code_check():                               #this is the command that runs when you submit your name
    global hard_mode, codes, player_name, dev_mode
    player_name = name_entry_box.get()   
    if 'dev' in player_name:                     #if dev, prints location on click & turns  dev_mode on
        dev_mode= True
        window.bind("<Button-1>",dev_click) 
    if len(player_name) == 0:                      #if empty, add code
        codes+=1
    if 'hard' in player_name:                        # if hard, turns hm on, add code
        hard_mode=True                                       
        codes+=1
    if codes >= 1:   
        name_entry_box.delete(0,END)
        codes = 0                           #on code, empty codes & makes you choose again
        on_start_button_click()
    else:
        submit_click()                      #otherwise, runs command

def dev_click(event):            #this is the func to make placing things easier when devmode is on
    global dev_mode
    if dev_mode == True:
        print("Mouse x=" + str(event.x)+", y="+str(event.y))

def submit_click_bound(event=None):
    submit_click()
def submit_click():                                    #this is the command that runs when you click the submit button
    global player_name, clicks, operator_list, game_start
    clicks+=1        
    if clicks == 1:                        #first time in the block
        name_entry_box.pack_forget()       
        submit_button.place_forget()    #removes submit button, instructions & box for name
        name_instructions.pack_forget()      

        player_name = name_entry_box.get()                   #gets name from inputbox ^
        name_tag.config(text=f"you are: {player_name}")  #gives your name to the nametag
        name_tag.place(x=270,y=56)                        #places nametag label
        show_operators()               #then places the screen for selecting your operators

    if clicks > 1:                    #second time in the block. please see def show_operators(): first
        clicks+=1                            #(this is the commmand that runs when you hit submit operator_list)
        if operator_list == []:                     
            no_operators_chosen.pack(pady=10)           #on no operators selected, tells you no operator_list selected
        else:                      
            add_button.place_forget()       
            sub_button.place_forget()
            div_button.place_forget()
            mlt_button.place_forget()           #when operators selected, removes all buttons & labels from sceern
            submit_button.place_forget()
            reset_chosen_ops_button.place_forget()  
            name_tag.place_forget()      
            choose_operators_instructions.place_forget()     
            no_operators_chosen.pack_forget()          
            submit_chosen_ops_button.place_forget()
            if game_start == False:                 #??? not sure 
                game_start = True           
                are_you_ready_label.pack(pady=30)     #places the label & yes button for if you are ready to play
                ready_button.pack(pady=10)    
                ready_button.focus()                                    #ready bytton runs start_game command
                ready_button.bind("<Return>",start_game_bound)         #binds enter key to yes button ^

def show_operators(): #this is the command that runs when you submit your name
    choose_operators_instructions.place(x=320, y=166)             
    add_button.place(x=293, y= 258)            #these are instructions & the + - * / buttons being placed
    sub_button.place(x=333, y= 256)       
    mlt_button.place(x=374, y= 257)     
    div_button.place(x=418, y= 260)    
    window.bind("<plus>", add_to_list_bound)       #these allow you to hit the symbol to toggle
    window.bind("<minus>", sub_to_list_bound)
    window.bind("<asterisk>", mlt_to_list_bound)
    window.bind("<slash>", div_to_list_bound)
    
    window.focus()                        #?
    reset_chosen_ops_button.place(x=252,y=255)    #places btton for reseting your selections 
    submit_chosen_ops_button.place(x=490, y=260) # places button for  submitting your chosen op
    window.bind("<Return>", submit_click_bound)  #this binds enter key to submit button^

def add_to_list_bound(event=None):
    add_to_list()
def sub_to_list_bound(event=None):
    sub_to_list()
def mlt_to_list_bound(event=None):
    mlt_to_list()
def div_to_list_bound(event=None):
    div_to_list()
def add_to_list():              #these are commands that run when you click th buttons on the operators select screen
    global append_add_to_list
    if append_add_to_list == True:               #they check if it is to be added
        operator_list.append("+")          #if so they add
        add_button.config(relief=SUNKEN, fg = "#3B0404")
        append_add_to_list = False     #and toggle states internally
    else:
        operator_list.remove("+")   #otherwise they remove
        add_button.config(relief=RAISED, fg = "#000000")
        append_add_to_list = True           #& toggle back
def sub_to_list():
    global append_sub_to_list
    if append_sub_to_list == True:
        operator_list.append("-")
        sub_button.config(relief=SUNKEN, fg = "#3B0404")
        append_sub_to_list = False
    else:
        operator_list.remove("-")
        sub_button.config(relief=RAISED, fg = "#000000")
        append_sub_to_list = True
def mlt_to_list():
    global append_mlt_to_list
    if append_mlt_to_list == True:
        operator_list.append("*")
        mlt_button.config(relief=SUNKEN, fg = "#3B0404")
        append_mlt_to_list = False
    else:
        operator_list.remove("*")
        mlt_button.config(relief=RAISED, fg = "#000000")
        append_mlt_to_list = True
def div_to_list():
    global append_div_to_list
    if append_div_to_list == True:
        operator_list.append("/")
        div_button.config(relief=SUNKEN, fg = "#3B0404")
        append_div_to_list = False
    else:
        operator_list.remove("/")
        div_button.config(relief=RAISED, fg = "#000000")
        append_div_to_list = True

def reset_operators_click():    #this resets all of the operatos buttons to the unclicked state removes all operator_list from the opslist
    global append_add_to_list, append_sub_to_list, append_div_to_list, append_mlt_to_list, operator_list
    append_add_to_list, append_sub_to_list, append_div_to_list, append_mlt_to_list = True,True,True,True   #sets toggle to "to add"
    operator_list = []                                                                        #empties list
    add_button.config(relief=RAISED, fg = "#000000")
    sub_button.config(relief=RAISED, fg = "#000000")             
    mlt_button.config(relief=RAISED, fg = "#000000")
    div_button.config(relief=RAISED, fg = "#000000")

def start_game_bound(event=None):
    start_game()
def start_game():        #this is the commmand that runs when you hit "yes" to the ready button 
    global first_num_a, first_num_b, second_num_b, second_num_a, level
    window.unbind("<plus>")        
    window.unbind("<minus>")
    window.unbind("<asterisk>")             #unbinds operator keys so you cannot mess with list mid game
    window.unbind("<slash>")
    window.unbind("<Return>")                           
    are_you_ready_label.pack_forget()                             #remove ready label& button
    ready_button.pack_forget()                         
    score_label.config(text=f"score: {score}", i=score_fish_01_art)  #this is a fish displaying your score. *configuring*
    level_label.config(text=f"level: {level}")  #level label being configured
    if hard_mode == True:
        for a in range(4):
            first_num_a+=1               #if you are in hardmode, its harder. 
            first_num_b+=2
            second_num_a+=1
            second_num_b+=2
            level+=1
            level_label.config(text=f"level: {level}")  #makes level label reflect that
    question_label.pack()          #places label that will ask question, & box that you'll input answers in
    answer_entry_box.pack()                                      
    submit_answer_button.pack()            #button for clicking submitANswer - and label displaying level number
    level_label.place(x=303,y=203)
    score_label.place(x=435,y=206)                                       #places score label
    place_hearts()                   #places hearts
    question_loop()                       #starts loop by running "asking the question" (other half is "checking the answer")    

def place_hearts():
    if hard_mode == True:
        heart_1.pack(anchor="se")
        heart_2.pack(anchor="se")            #if you are in hardmode, its harder
        heart_3.pack(anchor="se")
    else:
        heart_1.pack(anchor="se")
        heart_2.pack(anchor="se")           #places 5 lives for you!
        heart_3.pack(anchor="se")
        heart_4.pack(anchor="se")
        heart_5.pack(anchor="se")

def question_loop():        #one half of the gameplay loop
    global question_number, player_answer, correct_number, score, first_q_number, second_q_number, lenOp, selected_operator, first_num_a, first_num_b, second_num_b,second_num_a  
    first_q_number = ranNum(first_num_a,first_num_b)                  #random numbers chosen for question
    second_q_number = ranNum(second_num_a,second_num_b)
    lenOp = (len(operator_list)-1)                    #list start at index 0
    selected_operator = operator_list[ranNum(0,lenOp)]   #selected a random operator
    if selected_operator =="+":                        # if the selected op is +, itll make the question x - y
        correct_number = first_q_number + second_q_number
    if selected_operator =="-":                         # for sub we have to take some proactive measures to remove negative answers
        if second_q_number > first_q_number:
            _temp = first_q_number                               #they were unfun to enter
            first_q_number = second_q_number
            second_q_number = _temp
        correct_number = first_q_number - second_q_number
    if selected_operator =="*":                       
        correct_number = first_q_number * second_q_number
    if selected_operator =="/":                             #division does tricks to make all #s intergers everytime
        correct_number = first_q_number / second_q_number
        while correct_number%1!=0 and first_q_number != second_q_number:         # thats by making sure it has no remader when divided by one
            first_q_number=ranNum(1,200)                      
            second_q_number=ranNum(3,15)                                             
            correct_number = first_q_number / second_q_number   
    correct_number = round(correct_number)                       #rounds the answer down to NO decimal places (2 inst of 2.0)
    question_number+=1    #adds 1, for obvi- below configs label to print the question
    question_label.config(text=f"Q{question_number}: {first_q_number} {selected_operator} {second_q_number}")   
    answer_entry_box.bind("<Return>", check_answer_bound)         
    answer_entry_box.focus()     #focus in the answer box ^ lets you press enter to answer
    if skips >0:                          #if you have any skips it'll make the skips button (happens every loop bc idk im bad)
        skip_button.bind("<Return>", skip_click_bound)      #so you can tab to enter to skip ^^
        skip_button.place(x=360,y=265)                  

def check_answer_bound(event=None):
    check_answer()
def check_answer():    #the commands that runs when we enter our answer
    global player_answer, correct_number, correct_answers, incorrect_answers, skips, combo, score, first_num_a, first_num_b, second_num_a, second_num_b, correct_in_a_row, level, dev_mode
    score_label.config(text=f"score: {score}",fg="white",font = ("Helvetica", 15),)        #configs score every round
    player_answer = answer_entry_box.get()          #grabs your answer from the box 
    answer_entry_box.delete(0,END)              #clears your input
    if player_answer == str(correct_number):   
        play_correct_sound()
        if score_handler.is_high_score(score):   #if you have highscore, shwo yoy!
            high_score_label.place(x=114, y=296)              
        correct_answers+=1              #if your answer is correct
        combo+=1           #combo up+
        correct_in_a_row+=1 
        score += 10*(((combo)+(level)*0.5))
        score = round(score)   #rounds score to NO decimal places   vvv configs score for uou!
        score_label.config(text=f"score: {score}",fg="white",font = ("Helvetica", 15),)
        if hard_mode == True:
            score*=1.05       #woah...big
        fish_score_changer()   #if your score is large enough, gives you a bigger fish
        if correct_in_a_row == 5:       #if you got 5 correct in a row, the game gets harder
            if level != 10 or hard_mode == True:
                for a in range(1):
                    first_num_a+=1
                    first_num_b+=2
                    second_num_a+=1
                    second_num_b+=2
                    level+=1
                    level_label.config(text=f"level: {level}") 
                correct_in_a_row=0
    
    elif "skip" in player_answer:                             # if you skipped
        skip_click()

    elif player_answer != str(correct_number):          #if you are wrong
        combo = 0                       #c-c-c-c-c-combo breaker
        correct_in_a_row = 0             
        incorrect_answer()

    if hard_mode == False:
        if incorrect_answers < 5:                                      #if you are at less than 5 inc answers
            question_loop()                  #CONTINUE QUESTION / ANSWER LOOP
    if hard_mode == True:
        if incorrect_answers <3:
            question_loop()

def skip_click_bound(event=None):
    skip_click()
def skip_click():                             
    global skips, incorrect_answers, combo, correct_in_a_row
    combo = 0                            #c-c-c-c-combo breaker
    correct_in_a_row = 0
    if skips >= 1 and incorrect_answers < 5:             #if yoy have 1 or more skips, and less than 5 wrong answwrs
        skips-=1 
        if skips == 0:          #if you have no skips left
            skip_button.config(state=DISABLED, text="")                                     
    elif skips < 1:                     #  if you alreasdy had no skips left
        incorrect_answer()

def incorrect_answer():  #               the command the runs when you get the answer wrong
    global incorrect_answers, correct_number, first_q_number, second_q_number, selected_operator, score
    play_incorrect_sound()
    incorrect_answers+=1               
    if incorrect_answers == 1:
        heart_1.config(i=heart_broken_art)
    elif incorrect_answers == 2:
        heart_2.config(i=heart_broken_art)
    elif incorrect_answers == 3:
        heart_3.config(i=heart_broken_art)
    elif incorrect_answers == 4:
        heart_4.config(i=heart_broken_art)
    elif incorrect_answers == 5:
        heart_5.config(i=heart_broken_art)
    score_label.config(text= f"{first_q_number}{selected_operator}{second_q_number}={correct_number}", fg="black", font = ("Helvetica", 15),)
    if hard_mode == True:
        score/=2
        score = round(score)
        if incorrect_answers>=3:
            game_loss()
    else:
        if incorrect_answers>=5:
            game_loss()

def fish_score_changer():
    global score
    if score >= 50:
        score_label.config(i=score_fish_02_art)
    if score >= 200:
        score_label.config(i=score_fish_03_art)     
    if score >=  450:
        score_label.config(i=score_fish_04_art)     
    if score >= 1200:
        score_label.config(i=score_fish_05_art)
    if score >= 3500:
        score_label.config(i=score_fish_06_art)

def game_loss():                                #makes a pretty end screen
    skip_button.config(state = DISABLED, text = "")                          #button bad
    score_label.config(text=f"final score: {score}", fg="#FFFFFF", font = ("Helvetica", 15))               #final score print
    submit_answer_button.config(text="", state=DISABLED)                  #button turn off
    answer_entry_box.pack_forget()                                 #kill anserr box
    question_label.config(text="game over")             #game over rexr
    play_again_button.place(x=115,y=100)            #place button to play again
    level_label.config(text="")                        #removes text from turtle
    if dev_mode == False:
        score_handler.addHighScore(player_name, score)
    view_scores_button.place(x=300,y=400)

def roll_credits():
    global credits_rolled
    credits_rolled+=1
    if credits_rolled%2==0:
        start_game_button.place_forget()
        credits_label.pack()
        credits_button.config(text="go  back")
    else:
        start_game_button.place(x=334,y=220)
        credits_label.pack_forget()
        credits_button.config(text="CREDITS")

def high_scores():
        global player_name, score
        view_scores_button.place_forget()
        question_label.pack_forget()
        score_label.place_forget()
        heart_1.pack_forget()
        heart_2.pack_forget()
        heart_3.pack_forget()
        heart_4.pack_forget()
        heart_5.pack_forget()
        submit_answer_button.pack_forget()
        skip_button.place_forget()
        level_label.place_forget()
        high_score_label.place_forget()
        name_instructions.config(text="HIGH SCORES")
        name_instructions.pack()

        score_handler.apply_sort()
        scores = score_handler.high_scores

        labels = [first_place_label, second_place_label, third_place_label]
        places = ["1st", "2nd", "3rd"]

        for i, label in enumerate(labels):
            if i < len(scores):
                entry = scores[i]
                label.config(text=f"{places[i]}- {entry['name']} ({entry['score']})")
            else:
                label.config(text=f"{places[i]}- ---")
            label.pack()

def play_again():             #RESETS ALL VARIABLES AND REMOVES ALL PLACED BUTTONS AND LABELS AND FINALLY PLACES START BUTTON
    global player_answer, player_name, operator_list, clicks, skips, correct_answers, incorrect_answers, question_number, correct_number, first_q_number, second_q_number, score, combo, selected_operator, append_add_to_list, append_div_to_list, append_mlt_to_list, append_sub_to_list, game_start
    global first_num_b, first_num_a, second_num_b, second_num_a, correct_in_a_row, hard_mode, level, dev_mode
    question_label.pack_forget()
    name_instructions.config(text="enter player name")
    score_label.place_forget()
    heart_5.config(i=heart_art)
    heart_4.config(i=heart_art)
    heart_3.config(i=heart_art)
    heart_2.config(i=heart_art)
    heart_1.config(i=heart_art)
    heart_1.pack_forget()
    heart_2.pack_forget()
    heart_3.pack_forget()
    heart_4.pack_forget()
    heart_5.pack_forget()
    submit_answer_button.pack_forget()
    skip_button.place_forget()
    play_again_button.place_forget()
    level_label.place_forget()
    high_score_label.place_forget()
    name_instructions.pack_forget()
    view_scores_button.place_forget()
    first_place_label.pack_forget()
    second_place_label.pack_forget()
    third_place_label.pack_forget()
    submit_answer_button.config(state=ACTIVE, text="submit answer", bg= "#255ab7", border = 0, fg="#FFFFFF") 
    skip_button.config(state=ACTIVE, text="skip")
    first_num_a =1
    first_num_b =10
    second_num_a =3
    second_num_b = 12
    correct_in_a_row = 0
    player_name =""  
    player_answer = -99  
    operator_list = []  
    clicks = 0 
    skips = 5             
    correct_answers = 0 
    incorrect_answers = 0
    question_number = 0
    correct_number = 0
    first_q_number=0
    second_q_number=0
    score = 0
    combo = 0
    selected_operator = 0
    level = 1
    append_add_to_list = True    
    append_sub_to_list = True            
    append_mlt_to_list = True
    append_div_to_list = True
    game_start = False
    hard_mode = False
    dev_mode = False
    start_game_button.place(x=334,y=220)
    credits_button.place(x=300,y=500)

def play_incorrect_sound():
    mixer.music.load(path.join(ASSET_DIR, "sounds", "incorrect.wav"))
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=0)
def play_correct_sound():
    mixer.music.load(path.join(ASSET_DIR, "sounds", "correct.wav"))
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=0)
# THIS WILL BE THE ART THAT IS USED THIS BLOCK RIGHT HERE AND NOWHERE ELES
operator_button_art = PhotoImage(file=path.join(ASSET_DIR, "button_mushroom_001.png")).subsample(20,20)
window_background_source = PhotoImage(file=path.join(ASSET_DIR, "background_water_001.png"))
window_background_art = PhotoImage(width=800, height=600)
window_background_art.tk.call(
    str(window_background_art),
    "copy",
    str(window_background_source),
    "-from", 10, 10, 810, 610,
    "-to", 0, 0,
)
log_label_art = PhotoImage(file=path.join(ASSET_DIR, "button_log_001.png")).subsample(2,2)
submit_button_art = PhotoImage(file=path.join(ASSET_DIR, "button_lilypad_001.png")).subsample(4,4)
start_button_art= PhotoImage(file=path.join(ASSET_DIR, "butterfly_start_button_001.png")).subsample(3,4)
name_tag_art = PhotoImage(file=path.join(ASSET_DIR, "fish_label.png")).subsample(2,2)
choose_operators_art = PhotoImage(file=path.join(ASSET_DIR, "fish_label_002.png")).subsample(2,2)
ready_art = PhotoImage(file=path.join(ASSET_DIR, "duck_button_art.png")).subsample(2,2)
ready_button_art = PhotoImage(file=path.join(ASSET_DIR, "fish_003.png")).subsample(2,2)
submit_answer_art = PhotoImage(file=path.join(ASSET_DIR, "fish_label.png")).subsample(2,2)
heart_art = PhotoImage(file=path.join(ASSET_DIR, "heart.png"))
heart_broken_art = PhotoImage(file=path.join(ASSET_DIR, "heartbroken.png"))
level_label_art = PhotoImage(file=path.join(ASSET_DIR, "level_art.png"))
leplay_again_art = PhotoImage(file=path.join(ASSET_DIR, "bird_play_again.png"))
high_score_art = PhotoImage(file=path.join(ASSET_DIR, "highscore.png")).subsample(2,2)
first_place_art = PhotoImage(file=path.join(ASSET_DIR, "fish_gold.png")).subsample(3,3)
second_place_art = PhotoImage(file=path.join(ASSET_DIR, "fish_silv.png")).subsample(3,3)
third_place_art = PhotoImage(file=path.join(ASSET_DIR, "fish_bronze.png")).subsample(3,3)
mute_button_art = PhotoImage(file=path.join(ASSET_DIR, "mute_clam.png")).subsample(2,2)
sing_button_art = PhotoImage(file=path.join(ASSET_DIR, "sing_clam.png")).subsample(2,2)
score_fish_01_art = PhotoImage(file=path.join(ASSET_DIR, "scorefish_001.png"))
score_fish_02_art= PhotoImage(file=path.join(ASSET_DIR, "scorefish_002.png"))
score_fish_03_art= PhotoImage(file=path.join(ASSET_DIR, "scorefish_003.png"))
score_fish_04_art= PhotoImage(file=path.join(ASSET_DIR, "scorefish_004.png"))
score_fish_05_art= PhotoImage(file=path.join(ASSET_DIR, "scorefish_005.png"))
score_fish_06_art= PhotoImage(file=path.join(ASSET_DIR, "scorefish_006.png"))
credit_art = PhotoImage(file=path.join(ASSET_DIR, "credit_art.png"))

background_label = Label(window, image=window_background_art, border=0, highlightthickness=0) 
background_label.place(x=0, y=0)
background_label.lower()
window.geometry("800x600")                     #WINDOW size 
window.grid()
 #                                            below are entry boxes, labels*, then buttons. tried my best                       *most labels

name_entry_box = Entry(window,                         #input box for name                 (entry)
                     font=("Helvetica", 20),
                     bg = "#2767BB",               #background color
                     fg = "#FFFFFF")               #text color

answer_entry_box = Entry(window,                             #answer box for answering in        (entry)
                  bg = "#2767BB",                   #background color
                  fg = "#FFFFFF",                   #text color
                  font = ("Helvetica", 20),)                          #font size

name_instructions = Label(window, text="enter player name",  #tells you to enter name below     (label)
                    i=log_label_art,                   #use art (log)
                    bg = "#255ab7",
                    fg="#FFFFFF",
                    font = ("Helvetica", 15),  
                    compound="center")               #below text

name_tag = Label(window,         #will display player name. empty text for now             (label)
                font = ("Helvetica", 14),
                bg= "#255ab7",                           #background color
                fg="white",                                #text color
                i = name_tag_art,                           #art use (fish)
                compound="center")                         #below text

choose_operators_instructions = Label(window, text="choose your operators", #ask you to choose operators (label)   
                       font = ("Helvetica", 15),             
                       bg = "#255ab7",             #background color
                       i = choose_operators_art,
                       compound="center",
                       fg = "#000000")            #text color            

no_operators_chosen = Label(window, text="no operators chosen", #tells if you have no operators    (label)
                    font = ("Helvetica", 70),
                    bg="green",                      #text color
                    fg= "red")                       #background color 

high_score_label = Label(window, text="NEW HIGH SCORE",
                       font=("Helvetica", 15),
                       bg="#255ab7",
                       fg="#000000",
                       i = high_score_art,
                       compound="center")

question_label = Label(window,
                      i = log_label_art,
                      compound="center",
                      font = ("Helvetica", 15),
                      fg="#FFFFFF",
                      bg= "#255ab7")                        #              will ask question l8r  (label)

score_label = Label(window, text=(f"score: {score}"),  #will display your score             (label)
                   font = ("Helvetica", 15),
                   bg = "#255ab7",                  #background color
                   i = score_fish_01_art,
                   compound="center",
                   border=0,
                   fg = "#FFFFFF")                  #text color

first_place_label = Label(window, i = first_place_art, compound="center", border=0, bg= "#255ab7")
second_place_label = Label(window, i = second_place_art, compound="center",border=0, bg= "#255ab7")
third_place_label = Label(window, i = third_place_art,compound="center",border=0, bg= "#255ab7")

heart_1 = Label(window, i=heart_art, border=0)
heart_2 = Label(window, i=heart_art, border=0)
heart_3 = Label(window, i=heart_art, border=0)
heart_4 = Label(window, i=heart_art, border=0)
heart_5 = Label(window, i=heart_art, border=0)

credits_label = Label(window, i=credit_art)

level_label = Label(window, text=f"level: {level}",    #will display what lebel you are on  (label)
                    i= level_label_art,                  #using turtle art
                    bg="#255ab7",           #water bg
                    border=0,  
                    font = ("Helvetica", 15),
                    compound="center")              #under text

are_you_ready_label = Label(window, text = "Ready?",  #to ask if you're ready        (label)
                         i = ready_art,
                         font = ("Helvetica", 15),
                         compound="center",
                         bg="#255ab7",
                         fg ="#0018F0")

ready_button = Button(window, text="Yes",      #ready for game button                 (button)
                     command=start_game,            #run command
                    border= 0,
                    i = ready_button_art,
                    font = ("Helvetica", 15),
                    bg = "#255ab7",
                    fg = "#FFFFFF",
                    compound="center")

mute_button = Button(window, text="",
                    command=toggle_music_mute,
                    bg="#255ab7",
                    i=sing_button_art,
                    border=0)

skip_button = Button(window, text = "skip",  #skip button                         (button)
                    command=skip_click,              #run command
                    font = ("Helvetica", 15),
                    bg = "#255ab7",               #background color
                    i = submit_button_art,
                    compound="center",
                    border=0,
                    fg = "#02680B")               #text color
               
submit_button = Button(window, text="submit",       #submit button                         (button)
                      command=code_check,          #gives command
                      font = ("Helvetica", 15),
                      bg = "#255ab7", 
                      image = submit_button_art,      #use art (lily pad)
                      compound="center",            #below text
                      fg = "#02680B",             #text color
                      border = 0)

submit_chosen_ops_button = Button(window, text="submit",       #submit button                         (button)
                      command=submit_click,          #gives command
                      font = ("Helvetica", 15),
                      bg = "#255ab7", 
                      image = submit_button_art,      #use art (lily pad)
                      compound="center",            #below text
                      fg = "#02680B",             #text color
                      border = 0)

reset_chosen_ops_button = Button(window, text="reset selections",   #reset operator_list bytton              (button)
                        command = reset_operators_click,   #runs commd
                        bg = "#255ab7",          #border color
                        font = ("Helvetica", 15),
                        i=log_label_art,             #use art (log)
                        compound="center",         #art below text
                        fg = "#FFFFFF",             #text color
                        border = 0)

add_button = Button(window, text="+",       # +, -, *, / buttons ( this & following 3)     (button)
                   command=add_to_list,                  #runs command
                   font = ("Helvetica", 15),
                   bg = "#255ab7", 
                   i=operator_button_art,            #use art (mushroom)
                   compound="center",              #under text
                   fg = "#000000",             #text color
                   border = 0)
sub_button = Button(window, text="-", 
                   command=sub_to_list, 
                   font = ("Helvetica", 15),
                   bg = "#255ab7", 
                   i=operator_button_art,
                   compound="center",
                   fg = "#000000",
                   border=0)
mlt_button = Button(window, text="*", 
                   command= mlt_to_list, 
                   font = ("Helvetica", 15),
                   bg = "#255ab7", 
                   i=operator_button_art,
                   compound="center",
                   fg = "#000000",
                   border=0)
div_button = Button(window, text="/", 
                   command=div_to_list, 
                   font = ("Helvetica", 15),
                   bg = "#255ab7", 
                   i=operator_button_art, 
                   compound="center",
                   fg = "#000000",
                   border=0)

submit_answer_button = Button(window, text="submit answer",   #submit answer button       (button)
                            font = ("Helvetica", 15),
                            command=check_answer,
                            bg= "#255ab7",          #background  color
                            i = submit_answer_art,         #red fish
                            compound="center",         #below art
                            border = 0,
                            fg="#FFFFFF")           #text color        

play_again_button = Button(window, text="play again",      #play agin button            (button)
                         command = play_again,      #command !    
                         font = ("Helvetica", 15),
                         bg= "#255ab7",       #background colo
                         i=leplay_again_art,
                         compound="center",
                         border=0)         #no border

view_scores_button = Button(window, text="View High Scores",
                         compound="center",
                         font=("Helvetica", 15),
                         border=0,
                         bg="#255ab7",
                         fg="#FFFFFF",
                         i = log_label_art,
                         command=high_scores)

credits_button = Button(window, text="CREDITS",
                       command=roll_credits,
                       font=("Helvetica", 15),
                       bg= "#255ab7",
                       i=log_label_art,
                       border=0,
                       compound="center",
                       fg="#FFFFFF")

start_game_button = Button(window,text="click to start",    #button for starting game!        (button)
                     command= on_start_button_click,   #runs command
                     font = ("Helvetica", 15),
                     bg = "#255ab7", 
                     image=start_button_art,        #use art (butterfly)
                     compound="center",           #below text
                     fg= "#FFFFFF",             #text color
                     border = 0,
                     height=100,
                     width=140)

start_game_button.place(x=334,y=220)  #places the start button, as it needs to be placed
credits_button.place(x=300,y=500)
mute_button.place(x=690, y=20)





window.mainloop()       #I AM GOD, CREATOR OF WINDOW 