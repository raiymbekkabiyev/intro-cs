#importing modules required for the project
import random

#Global variables that allow us adapt the game to new size easily
NUM_ROWS=6
NUM_COLS=7

#initializing Card class to assign position and value of the cards, and load corresponding images
class Card:
    def __init__ (self,r,c,v):
        self.r = r
        self.c = c
        self.v = v
        self.s='h'
        self.img = loadImage(str(self.v)+".png")
        self.card_back=loadImage("cardBack.png")
        self.matched = False
        # self.selected = False
    # display function to colour cards once they will be mached, and display hovered cards
    def display(self):
        if self.matched:
            if self.matched == 1:
                fill(255,0,0)
            else:
                fill(0,0,0)
            rect(self.c*105 +5, self.r*105+5, 100, 100)
            image(self.img, 5 + self.c*105, 5 + self.r*105)
        else:
            if self.s=='h': 
                image(self.card_back, 5 + self.c*105, 5 + self.r*105)
            else: 
                image(self.img, 5 + self.c*105, 5 + self.r*105)
        
#deck class with the main functions of board creation and shuffling algorithm
class Deck:
    def __init__(self,numRows,numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.game_over=False
        self.board = []
        # variables to work with the score of the players
        self.chosen_cards_list=[]
        self.player_score=[0,0]
        self.sum_of_scores=0
        self.start_time = 0
        #assigning random starting turn for the player
        self.turn=random.randint(0,len(self.player_score)-1)
        self.state=[]
        self.a=[]
  
    #creating board with 21 different pictures    
    def createBoard(self):
        cnt = 0
        for r in range(self.numRows):
            for c in range(self.numCols):
                self.board.append(Card(r,c,str(cnt)))
                cnt+=1
                if cnt==21: 
                    cnt=0
    #board shuffling: takes 2 random cards and swaps their positions; these algorithm is repeated as many times as we ask when class the method 
    def shuffleBoard(self, num):
        for i in range(num):
            randomRow_card1=random.randint(0,NUM_ROWS-1) 
            randomCol_card1=random.randint(0,NUM_COLS-1) 
            randomCard1=self.getCard(randomRow_card1,randomCol_card1)
            randomRow_card2=random.randint(0,NUM_ROWS-1) 
            randomCol_card2=random.randint(0,NUM_COLS-1)
            randomCard2=self.getCard(randomRow_card2,randomCol_card2)
            if randomRow_card1!=randomRow_card2 and randomCol_card1!=randomCol_card2: 
                #this one swaps objects 
                tmp=randomCard2.v
                randomCard2.v=randomCard1.v
                randomCard1.v=tmp
                #this one swaps images of corresponding objects 
                tmp2=randomCard2.img
                randomCard2.img=randomCard1.img
                randomCard1.img=tmp2
        
    # functions to acquire positions of the card and its corresponding value            
    def getCard (self,r,c):
        for t in self.board:
            if t.r == r and t.c == c:
                return t
        return "No card"
    #check for win game once players will guess all cards on the board,i.e 21 pairs
    def check_for_end_of_game(self):
        self.sum_of_scores=sum(self.player_score)
        if self.sum_of_scores==21: 
            return True

    def getCardByValue (self,v):
        for t in self.board:
            if t.v == v:
                return t
            
    #show text after the win with the player who won
    def windisplay(self):
        fill(100)
        rect (230,660,180,30)
        fill (255)
        text ("Player number %s won" %self.turn, 250,680)
        
     # assingin delay timer                
    def display(self):
        if self.start_time > 0:
            self.start_time -= 1
            return
        background(255)
        c = mouseX // 110
        r = mouseY // 110 
        
        hoverCard=self.getCard(r,c)
        #changing "mouse" colour depending on whcih turn the game has
        if hoverCard!="No card":
            if self.turn==0:
                fill(255,0,0)
                rect(c*105,r*105,110,110)           
            if self.turn==1:
                fill(50,0,0)
                rect(c*105,r*105,110,110)
        #printing some visual texts for user interface to track turn and scores        
        for t in self.board:
            t.display()
        fill (100)
        rect (250,700,120,50)
        fill (255)
        text ("Shuffle", 260,735)
 
        fill(100)
        rect (500,700,200,50)
        fill (255)
        text ("Player number %s turn" %(self.turn+1), 510,730)
 
        fill(50)
        text("Welcome to the memory game",250,650)
        
        fill(100)
        rect (500,640,200,50)
        fill (255)
        text ("Player 1 scores: %s" %self.player_score[0], 550,660)
        text ("Player 2 scores: %s "%self.player_score[1], 550,680)

#creating deck1 object        
deck1=Deck(NUM_ROWS,NUM_COLS)

#setup,back colour,size
def setup():
    size(NUM_COLS*105+5,NUM_ROWS*105+125)
    background(255)
    deck1.createBoard()
def draw():
    deck1.display()
#function once mouse is cliked
def mouseClicked():
    c = mouseX // 110
    r = mouseY // 110

    chosen_card = deck1.getCard(r,c)
    if chosen_card != "No card":
        deck1.chosen_cards_list.append(chosen_card)
        deck1.a.append(chosen_card)
        # deck1.chosen_cards_list[0].s='unh'
        deck1.chosen_cards_list[len(deck1.chosen_cards_list)-1].s='unh'
    
    # for the last two chosen cards, these cards will be revealed and checked for matching
    if len(deck1.chosen_cards_list)==2: 
        deck1.chosen_cards_list[0].s='unh'
        deck1.chosen_cards_list[1].s='unh'

        # delay time of 30 for unmacthed cards
        deck1.display()
        deck1.start_time =30

        #if values of these 2 cards are equal and they have different r value(to avoid clicking on the same card twice), rather they must be with different positions
        if deck1.chosen_cards_list[0].v==deck1.chosen_cards_list[1].v and deck1.chosen_cards_list[0].r!=deck1.chosen_cards_list[1].r: 
            deck1.player_score[deck1.turn]+=1
             # condition for our colouring(display) function above   
            if deck1.turn==0:
                deck1.chosen_cards_list[0].matched = 1
                deck1.chosen_cards_list[1].matched = 1
            else:
                deck1.chosen_cards_list[0].matched = 2
                deck1.chosen_cards_list[1].matched = 2    
            deck1.turn=deck1.turn
       # if the cards are different they will not be shown     
        elif deck1.chosen_cards_list[0].v!=deck1.chosen_cards_list[1].v:      
            deck1.chosen_cards_list[0].s='h'
            deck1.chosen_cards_list[1].s='h'
            #turn change
            deck1.turn=(deck1.turn+1)%(len(deck1.player_score))
        #calling out "end" function and stopping the game once it is True
        if deck1.check_for_end_of_game():
            deck1.windisplay()
            noLoop()
        #reassigning the list to empty list to use it again
        deck1.chosen_cards_list=[]
     # position of the shuffling board   
    if 250 <= mouseX <= 370 and 700 <= mouseY <= 750:
        deck1.board = []
        deck1.createBoard()
        deck1.shuffleBoard(50)
