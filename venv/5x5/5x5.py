
import random
import copy


## Currently building
# Select best option [V]
# Destroy the board [in progress]
# Game results [In progress]

######################
# Class to Create Cards
#####################
class Card:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def name_card(self):
        return self.value + self.type

    def create_all_cards(vals, types):
        all_cards = [Card(value, type) for value in vals for type in types]
        return all_cards


############
## Class to create deck of cards
############

class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.amount = len(self.cards)

    def show_all_cards(self):
        for card in self.cards:
            print(Card.name_card(card))

    def show_top_card(self):
        top_card = self.cards[-1]
        print(f'The top card is : {Card.name_card(top_card)}')
        self.amount = len(self.cards)
        return Card.name_card(top_card)

    def draw_top_card(self):
        drawn_top_card = self.cards.pop()
        self.amount = len(self.cards)  # after drawing, update amount of cards in deck
        return drawn_top_card

    def draw_random_card(self):
        drawn_random_card = random.choice(self.cards)
        self.cards.remove(drawn_random_card)
        self.amount = len(self.cards)  # after drawing, update amount of cards in deck
        return drawn_random_card

    def shuffle(self):
        random.shuffle(self.cards)

    def add_cards(self, added_cards):
        self.cards.append(added_cards)
        self.amount = len(self.cards)  # after adding card(s), update amount of cards in deck


################
##Create Board
################

class Board:
    def __init__(self, amount_of_columns=9, amount_of_rows=8):
        self.board = []
        self.amount_of_rows = amount_of_rows
        self.amount_of_columns = amount_of_columns
        self.possible_values = []
        self.begin_cards = [(3,4),(4,4)]
        for i in range(0, amount_of_rows):
            self.board.append([[] for x in range(0, amount_of_columns)])

    def print_board(self):
        for row in self.board:
            print(row)

    def print_playable_options(self,playable_options_list):
        temp_board = copy.deepcopy(self.board)
        for row,column in playable_options_list:
            temp_board[row][column] = 'Position'
        for row in temp_board:
            print(row)

    def print_postition(self,position):
        # Print specifc place on board
        temp_board = copy.deepcopy(self.board)
        temp_board[position[0]][position[1]] = 'Position'
        for row in temp_board:
            print(row)

    def create_start(self):
        self.board[3][4] = deck.draw_random_card().name_card()
        self.board[4][4] = deck.draw_top_card().name_card()

    def playing_options(self):
        all_options = []
        for row_count, value in enumerate(self.board):
            all_options_row = []
            for column_count, place in enumerate(value):
                if place != []:
                    _place = (row_count, column_count)
                    _possible_place = (row_count - 1, column_count)
                    _options = []
                    _options_for_card = [(row_count - 1, column_count), (row_count, column_count + 1),
                                         (row_count + 1, column_count),
                                         (row_count, column_count - 1)]
                    all_options.append(_options_for_card)

        possible_values = []
        for list in all_options:
            for option in list:
                found_value = self.board[option[0]][option[1]]
                if found_value == []:
                    possible_values.append(option)
        self.possible_values = possible_values
        return possible_values

    def play_card(self,position):
        self.playing_options()
        if position in self.possible_values:
            self.board[position[0]][position[1]] = deck.draw_top_card().name_card()
        else:
            print(f'{position} is not a valid place to place a card. Valid places are {self.possible_values}')

    def surroudning_spaces(self,position):
        self.playing_options()

        if position in self.possible_values:
            row_count = position[0]
            column_count = position[1]
            surrounding_spaces =[]
            _surrounding_spaces = [(row_count - 1, column_count), (row_count, column_count + 1),
                                 (row_count + 1, column_count),
                                 (row_count, column_count - 1)]
            # FIX HERE SURROUNDING SPACES
            print('fix test here')
            for space in _surrounding_spaces:
                if (space[0] or space[1]) > 0 :
                    if space[0] < self.amount_of_rows:
                        if space[1] <self.amount_of_columns:
                            surrounding_spaces.append(space)
            return surrounding_spaces
        else:
            print(f'{position} is not a valid place to place a card. Valid places are {self.possible_values}')

    def surroudning_card_values(self,position):
        surrounding_spaces = self.surroudning_spaces(position)
        surroudning_card_values = []
        for space in surrounding_spaces:
            if self.board[space[0]][space[1]] != []:
                surroudning_card_values.append(self.board[space[0]][space[1]])
        return surroudning_card_values

    def select_game(self,position):
        self.playing_options()
        surrounding_spaces = self.surroudning_spaces(position)
        spaces_with_values = 0
        cards_for_games = []
        for space in surrounding_spaces:
            if self.board[space[0]][space[1]] != []:
                spaces_with_values +=1
                cards_for_games.append(self.board[space[0]][space[1]])
        if spaces_with_values == 1:
            print('We play higher lower')
            game = 'Higer Lower'
            print(f'Card(s) for this game: {cards_for_games}')
        elif spaces_with_values == 2:
            print('We play binnen/buiten')
            game = 'Binnen Buiten'
            print(f'Card(s) for this game: {cards_for_games}')
        elif spaces_with_values == 3 :
            print('We play heb je m al of niet')
            game = 'Heb ik hem al'
            print(f'Card(s) for this game: {cards_for_games}')
        elif spaces_with_values == 4:
            print('We play heb je m al of niet')
            game = 'Heb ik hem al'
            print(f'Card(s) for this game: {cards_for_games}')
        return game

    # Function to calculate all odds
    def calculate_all_odds(self):
        playable_options_list = self.playing_options()
        odds_result_dict = {}
        for row, column in playable_options_list:
            select_game = self.select_game((row,column))
            surrounding_spaces = self.surroudning_spaces((row, column))
            surroudning_card_values = self.surroudning_card_values((row, column))
            # Calculate odds
            if select_game == 'Higer Lower':
                odds = higher_lowers_odds(surroudning_card_values[0])
                print(f'Odds Higer Lower : {odds}')
                odds_result_dict[(row,column)] = odds
            elif select_game == 'Binnen Buiten':
                print(f'Surrounding: {surroudning_card_values}')
                odds = binnen_buiten_odds(surroudning_card_values[0],surroudning_card_values[1])
                odds_result_dict[(row, column)] = odds
                print(f'Odds Binnen Buiten : {odds}')
            elif select_game == 'Heb ik hem al':
                print(f'Surrounding: {surroudning_card_values}')
                odds = heb_ik_of_heb_ik_niet(surroudning_card_values[0],surroudning_card_values[1],surroudning_card_values[2])
                odds_result_dict[(row, column)] = odds
                print(f'Odds Binnen Buiten : {odds}')
        return odds_result_dict

    def print_all_odds(self,dict_df):
        temp_board = copy.deepcopy(self.board)
        for key, value in option_dict.items():
            temp_board[key[0]][key[1]] = value
        for row in temp_board:
            print(row)



    def play_card(self,position):
        self.playing_options()
        surrounding_spaces = self.surroudning_spaces(position)
        spaces_with_values = 0
        cards_for_games = []
        for space in surrounding_spaces:
            if self.board[space[0]][space[1]] != []:
                spaces_with_values +=1
                cards_for_games.append(self.board[space[0]][space[1]])


        if spaces_with_values == 1:
            print('We play higher lower')
            print(f'Your card {cards_for_games}')
        elif spaces_with_values == 2:
            print('We play binnen/buiten')
            print(f'Your cards f{cards_for_games}')
        elif spaces_with_values == 3 :
            print('We play heb je m al of niet')
            print(f'Your cards f{cards_for_games}')
        elif spaces_with_values == 4:
            print('We play heb je m al of niet')
            print(f'Your cards f{cards_for_games}')
        else:
            print('ERROR ')

        # Set card on the board
        self.board[position[0]][position[1]] = deck.draw_top_card().name_card()

            #print(len(self.board[space[0]][space[1]]))
        #print(surrounding_spaces)

    def best_position_to_play(self):
        options_dict = self.calculate_all_odds()
        best_position = max(options_dict, key=options_dict.get)
        return best_position

    def destory_board (self,position):
        print(f'Postition {position}')
        begin_cards = self.begin_cards
        destroy = ''
        # Count amount of cards in row
        row_value = position[0]
        row_count = 0
        for column_value in range(0,len(self.board)):
            if (row_value,column_value) not in begin_cards:
                if self.board[row_value][column_value] != []:
                    row_count += 1
            else:
                print(f'Row cannot be deleted for {position}')
                destroy = 'Column'
        # Count amount of cards in column
        column_value = position[1]
        column_count = 0
        for row_value in range(0,len(self.board)):
            print(row_value, column_value)
            if (row_value, column_value) not in begin_cards:
                if self.board[row_value][column_value] != []:
                    column_count += 1
            else:
                destroy = 'Row'

        if destroy != '':
            if row_count >=  column_count:
                destroy = 'Row'
            else:
                destroy = 'Column'
        print(f'We are destroying {destroy}')

        # Now destory the board
        if destroy == 'Row':
            row_value = position[0]
            for column_value in range(0, len(self.board)):
                if (row_value, column_value) not in begin_cards:
                    if self.board[row_value][column_value] != []:
                        self.board[row_value][column_value] = []
        else:
            column_value = position[1]
            column_count = 0
            for row_value in range(0, len(self.board)):
                print(row_value, column_value)
                if (row_value, column_value) not in begin_cards:
                    if self.board[row_value][column_value] != []:
                        self.board[row_value][column_value] = []











#####################
## Functions for game odds
######################

# Odds for higher lower, returns odds and what to play (lower/higer)
def higher_lowers_odds(card1):
    index_value_card1 = vals.index(card1[:-1]) + 1
    correct_chance_odds = (index_value_card1) / (len(vals) +1)
    higher_or_lower = 'Lower'
    if correct_chance_odds < 0.5:
        correct_chance_odds = 1 - correct_chance_odds
        higher_or_lower = 'Higher'
    return round(correct_chance_odds,4), higher_or_lower

def higher_lower_results(card1,card2,prediction):
    if prediction == 'Higher':
        if card1 > card2:
            correct = True
        else:
            correct = False
    else:
        if card1 < card2:
            correct = True
        else:
            correct = False

# Odds for binnen buiten, returns odds and what to play (binnen/buiten)
def binnen_buiten_odds(card1,card2):
    index_value_card1 = vals.index(card1[:-1])
    index_value_card2 = vals.index(card2[:-1])
    max_card = max(index_value_card1, index_value_card2)
    min_card = min(index_value_card1, index_value_card2)
    odds_binnen = (max_card-min_card-1) / len(vals)
    odds_buiten = ((14 - max_card) + (min_card - 2)) / len(vals)
    odds_paal = 2 / len(vals)
    correct_chance_odds = max(odds_binnen, odds_paal, odds_buiten)
    if odds_binnen > odds_buiten:
        to_play = 'Binnen'
    else:
        to_play = 'Buiten'
    return round(correct_chance_odds, 4), to_play


def heb_ik_of_heb_ik_niet(card1, card2, card3):
    card1_type = card1[-1:]
    card2_type = card2[-1:]
    card3_type = card3[-1:]
    all_card_types = [card1_type, card2_type, card3_type]
    all_card_types_values = len(set(all_card_types))
    correct_chance_odds = all_card_types_values / len(types)
    if correct_chance_odds < 0.5:
        correct_chance_odds = 1 - correct_chance_odds
        to_play = 'Heb ik niet'
    else:
        to_play = 'Heb ik'
    return round(correct_chance_odds, 4), to_play





########################
## Run functions
######################

# Cards in this game
vals = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King','Ace']
types = ['♥', '♦', '♠', '♣']

# Create a deck of cards
all_possible_cards = Card.create_all_cards(vals, types)
deck = Deck(all_possible_cards)

deck.shuffle()
card1 = deck.draw_random_card()


# Create board
test_board = Board(9, 9)
test_board.create_start()
test_board.print_board()




#finish this

deck.shuffle()
# Populate board
test_board.play_card((3,3))
test_board.play_card((4,5))
test_board.play_card((4,6))
test_board.play_card((3,6))
test_board.print_board()


playable_options_list = test_board.playing_options()
option_dict = test_board.calculate_all_odds()

test_board.print_all_odds(option_dict)
# Select best option for option dict

# Select where to play
test_board.best_position_to_play()


## Function to play
# Start with Creating the board
# Starting pos (4,4, 4,5)
simulate_board = Board(9, 9)
# Create a start for the board
simulate_board.create_start()

# Create a start for the board
simulate_board.print_board()

# Select where to play
best_card = simulate_board.best_position_to_play()

simulate_board.print_board()

amount_of_cards_to_play = 6
for i in range (0,amount_of_cards_to_play):
    best_card = simulate_board.best_position_to_play()
    simulate_board.play_card((best_card))


simulate_board.play_card(())

simulate_board.playing_options()