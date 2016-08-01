__author__ = 'Vikhyat'
"""Player Class keeps the information the player- name, mark, games won, games lost, games drawn. Based on the statictics, it also calculates the score. It also prints all the relevant information related to a player """
class Player(object):
    #Class where the player name, their mark and the information of the score is maintained
    p1_statistics = {'Name':'Player1','Mark':'X','Won':0,'Lost':0,'Draw':0} #A dictionary that maintains all the information of the player
    p2_statistics = {'Name':'Player2','Mark':'O','Won':0,'Lost':0,'Draw':0}

    def __init__(self,name,playing_mark,chance=False):
        #Instantiates the player class (the name, mark and their chance)
        self.name=name
        self.playing_mark=playing_mark
        self.chance=chance

    def get_score(self,statistics):
        #Calculates the score of the player based on their performance
        return (((statistics['Won']*2))+statistics['Draw']-statistics['Lost'])

    def __str__(self,statistics):
        #Prints the complete information of the player
        print ('{}\n Mark: {}\n Score: {}\n Matches won: {}\n Matches lost: {}\n Matches Drawn: {}\n'.format(statistics['Name'],statistics['Mark'],self.get_score(statistics),statistics['Won'],statistics['Lost'],statistics['Draw']))

"""The Deck Class has the TicTacBoard which is initially initialized to the position numbers a player can pick and which are eventually replaced by the marks on the position selected by the player"""
class Deck(object):
    #Class with the Tic-tac-toe board
    Board=[]
    def __init__(self):
        #Instantiates the board list and the lists of individual player is maintained which records the position the player has selected
        self.Board=[0,1,2,3,4,5,6,7,8]
        self.Player1Choices=[]
        self.Player2Choices=[]

    def __str__(self):
        #Prints the board
        return "     |     |   \n  {}  |  {}  |  {}\n_____|_____|_____\n     |     |     \n  {}  |  {}  |  {}\n_____|_____|_____\n     |     |     \n  {}  |  {}  |  {}\n     |     |     \n".format(*self.Board)

"""Creates 2 Players
    Player1 with mark X and is given the first chance
    and Player2 with mark O

    Deck board is initialized and is saved after each game

    Validations-
        The player must enter a position between 0-8
        The player cannot enter a position which has already been marked

    Game over-
        When the board is completely filled (in this case, the game is drawn and each player is given 1 point)
        When either player wins (The winner gets 2 points and the loser looses 1 point

    Each time the players plays the game again, a new object of the players and the deck are created but their previous statistics are maintained
"""
class TicTacToe:
    #Class where objects of the players and the deck is created and where the game logic resides
    DeckList = []
    def __init__(self):
        self.player1= Player("Player1","X",True)                #Object of the Player class created and the values are passed
        self.player2= Player("Player2","O")
        self.player1_chance=self.player1.chance
        self.player2_chance=self.player2.chance
        self.player1_name=self.player1.name
        self.player2_name=self.player2.name
        self.player1_mark=self.player1.playing_mark
        self.player2_mark=self.player2.playing_mark
        self.deck=Deck()
        self.player1_positions = self.deck.Player1Choices
        self.player2_positions = self.deck.Player2Choices
        self.Board=self.deck.Board
        self.p1_stat = self.player1.p1_statistics
        self.p2_stat = self.player2.p2_statistics


    def is_game_over(self,player_positions,playing_mark):
        #Checks if the game is still in play or not
        count=0
        winning_possibilities = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]       #All the winning combinations on the board
        for mark in self.Board:
            #Counts all the 'marks' (the positions occupied by the players) on the board
            if isinstance(mark,str):
                count = count + 1

        if count == 9:
            #If the count of the positions is 9, it means all the positions have been filled and the game is Drawn
            print ("Game board filled. Game draw")
            self.DeckList.extend(self.Board)            #Puts the information of the final board in the list - DeckList
            try:
                #Writes the DeckList to a file
                with open("Decklist.txt","w") as DeckListData:
                    DeckListData.write(str(self.DeckList))
            except IOError as ioerr:
                print(ioerr)
            self.p1_stat["Draw"]+=1                     #Increments the score of the 'Draw column'
            self.p2_stat["Draw"]+=1
            self.player1.__str__(self.p1_stat)          #Prints the Statistics of the player
            self.player2.__str__(self.p2_stat)
            return True

        if len(player_positions)>2:                     #Checks which player won the game
            #Goes in the loop only when the player has entered 3 or more values
            for x in range(8):                      #8 indicates the number of winning possibilities
                if set(winning_possibilities[x]).issubset(player_positions):            #If the winning possibilies' list is a subset of the player's position, the player wins the game
                    if playing_mark == "X":
                        print ("Player 1 won the game\n")
                        self.DeckList.extend(self.Board)                                #Puts the information of the final board in the list - DeckList
                        try:
                            #Writes the DeckList to a file
                            with open("Decklist.txt","w") as DeckListData:
                                DeckListData.write(str(self.DeckList))
                        except IOError as ioerr:
                            print(ioerr)
                        self.p1_stat["Won"]+=1                                          #Increments the score of the 'Won column' of Player1
                        self.p2_stat["Lost"]+=1                                         #Increments the score of the 'Lost column' of Player2
                        self.player1.__str__(self.p1_stat)                              #Prints the Statistics of the player
                        self.player2.__str__(self.p2_stat)
                        return True
                    elif playing_mark == "O":
                        print ("Player2 won the game\n")
                        self.DeckList.extend(self.Board)
                        try:
                            with open("Decklist.txt","w") as DeckListData:
                                DeckListData.write(str(self.DeckList))
                        except IOError as ioerr:
                            print(ioerr)
                        self.p2_stat["Won"]+=1
                        self.p1_stat["Lost"]+=1
                        self.player1.__str__(self.p1_stat)
                        self.player2.__str__(self.p2_stat)
                        return True

    def validate_user_input(self,user_input):
        #Validates the position entered by the player
        if (user_input > 8 or user_input < 0):
            #Checks whether the position is between 0-8
            print("Invalid position")
            return True
        elif (self.Board[user_input]!=user_input):
            #Checks whether the position is occupied or not
            print("Position occupied")
            return True
        else:
            return False

    def get_user_input(self,player_name):
        #Gets the user input in the 'int' datatype
        return int(input("Enter the position " + player_name + ": "))

    def game_logic(self):
        #Switches the turns of the players and calls appropriate functions
        while True:
            if self.player1_chance==True:
                #Checks to see if is the turn of Player 1
                user_input = self.get_user_input(self.player1_name)     #Gets the user input
                val = self.validate_user_input(user_input)      #Validates the user input
                if val:                 #If the value entered by the user is incorrect, it asks the user to enter the value again
                    while (val):        #Called untill enters valid position
                        user_input = self.get_user_input(self.player1_name)
                        val = self.validate_user_input(user_input)
                self.Board[user_input]=self.player1_mark            #Puts the player's mark on the position he specified
                self.player1_positions.append(user_input)           #Puts the position entered by the user in the Player's list
                try:
                #Writing the player's list to a file
                    with open("Player1_Positions.txt","w") as data1:
                        data1.write(str(self.player1_positions))
                except IOError as ioerr:
                    print(ioerr)
                self.player1_chance=False                           #Setting the Player1's chance to false
                self.player2_chance=True                            #Setting the Player2's chance to true
                print(self.deck)                          #Prints the board after each input
                if self.is_game_over(self.player1_positions,self.player1_mark):             #Checks whether the game is over or not
                    break

            if self.player2_chance==True:
                user_input = self.get_user_input(self.player2_name)
                val = self.validate_user_input(user_input)
                if val:
                    while (val):
                        user_input = self.get_user_input(self.player2_name)
                        val = self.validate_user_input(user_input)
                self.Board[user_input]=self.player2_mark
                self.player2_positions.append(user_input)
                try:
                    with open("Player2_Positions.txt","w") as data2:
                        data2.write(str(self.player2_positions))
                except IOError as ioerr:
                   print(ioerr)
                self.player2_chance=False
                self.player1_chance=True
                print(self.deck)
                if self.is_game_over(self.player2_positions,self.player2_mark):
                    break

    def start_game(self):
        #Starts the game by calling the game_logic function
        self.game_logic()
        play = True
        while play:
            #Loop to ask the user to play more or exit
            play_more = input('Do you want to play again? "Y" or "N"\n')
            if play_more == "Y" or play_more == "y":
                new_game = TicTacToe()
                new_game.start_game()
                play = False
            elif play_more == "N" or play_more == "n":
                print('Good bye!')
                play = False
            else:
                print('Invalid option')
                play = True

Game = TicTacToe()              #Object of the TicTacToe class
Game.start_game()               #Starting the game by calling the start_game function