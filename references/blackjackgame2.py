import numpy as np


class BlackJack:
    print('| | ----------------------------------------------------------------------------------------------------------------------------')
    print('| | Welcome to the casino, do you have your credit card with you? Your starting amount is $100, which you can use freely.')
    print('| |-----------------------------------------------------------------------------------------------------------------------------')
    # cards
    suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    values = ('ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king')

    def __init__(self):
        test_version = False

        ask_number_of_players = False
        ask_names = False
        self.ask_bet = False

        if not test_version:
            ask_number_of_players = True
            ask_names = True
            self.ask_bet = True
        else:
            print('| |')
            print('TEST VERSION')

        self.number_of_players = 3

        if ask_number_of_players:
            self.ask_number_of_players()

        self.original_number_of_players = self.number_of_players
        self.balance = [100] * (self.number_of_players + 1)
        self.old_balance = [0] * (self.number_of_players + 1)
        self.new_balance = [0] * (self.number_of_players + 1)
        self.names = [''] * self.number_of_players
        self.names.append('The dealer')
        self.names_filtered = [''] * (self.number_of_players + 1)

        for i in range(self.number_of_players):
            self.names[i] = 'Player ' + str(i)

        self.bank_account_number = [''] * self.number_of_players
        self.pin_code = [0] * self.number_of_players

        if ask_names:
            self.ask_names()

        self.original_names = [''] * (self.number_of_players + 1)

        for i in range(self.number_of_players + 1):
            self.names_filtered[i] = self.names[i]
            self.original_names[i] = self.names[i]

        self.deck = self.create_deck()
        self.shuffle_deck()
        self.game()

        if not test_version:
            self.scam()

    def game(self):
        self.insurance = False
        self.turn = 0
        self.points_list = [0] * (self.number_of_players + 1)
        self.best_score = [0] * (self.number_of_players + 1)
        self.card_count = [0] * (self.number_of_players + 1)
        self.ace_count = [0] * (self.number_of_players + 1)
        self.blackjack = [False] * (self.number_of_players + 1)
        self.alive = [True] * (self.number_of_players + 1)
        self.won = [False] * (self.number_of_players + 1)
        self.split = [False] * (self.number_of_players + 1)

        self.turn_order = []
        self.ace_list = []
        self.value_list = []
        self.insurance_response = [True] * (self.number_of_players + 1)
        self.stood = [False] * (self.number_of_players + 1)

        self.bet = [5] * (self.number_of_players + 1)
        self.winnings = [0] * (self.number_of_players + 1)
        self.status = [''] * (self.number_of_players + 1)
        self.old_balance_display = [''] * (self.number_of_players + 1)
        self.new_balance_display = [''] * (self.number_of_players + 1)
        self.bet_display = [''] * (self.number_of_players + 1)
        self.winnings_display = [''] * (self.number_of_players + 1)

        self.bet[self.number_of_players] = 'n/a'
        self.winnings[self.number_of_players] = 'n/a'
        self.balance[self.number_of_players] = 'n/a'
        self.old_balance[self.number_of_players] = 'n/a'
        self.new_balance[self.number_of_players] = 'n/a'

        if self.ask_bet:
            self.ask_bet_amount()

        for i in range(len(self.balance)):
            if i == self.number_of_players:
                continue
            self.old_balance[i] = self.balance[i]
            self.balance[i] -= self.bet[i]

        print("| |")
        print('| | The cards are being shuffled.')
        print("| |")
        self.initial_deal()
        self.check_blackjack()
        self.offer_insurance()
        self.resolve_standoff()

        self.handle_split()

        if not self.blackjack[-1]:
            self.payout()
            print('| |')
            self.player_choice()
            print('| |')
            self.dealer_play()
            self.determine_winner()
            print('| |')

        self.clear_table()
        self.play_again()

    def scam(self, iteration=0):
        if iteration == 0:
            print('| |')
            print('| | Your balances will be transferred to your accounts.')
            print('| |')
        for i in range(iteration, self.number_of_players):
            answer1 = input('| | Dear ' + self.names[i] + '. What is your bank account number? \n| | ')
            answer2 = input('| | PIN code? \n| | ')

            self.bank_account_number[i] = answer1
            try:
                self.pin_code[i] = int(answer2)
            except:
                print('| | Dear ' + self.names[i] + '. Your bank details were not found in our database. Would you kindly re-enter them?')
                self.scam(i)
                break

    def play_again(self, iteration=0):
        answer = input('| | Would you like to play again? \n| | ')
        if answer == 'y':
            self.deck = self.create_deck()
            self.shuffle_deck()
            self.game()
        elif answer == 'n':
            print('| | We look forward to seeing you again soon at Emiel\'s Casino')
        else:
            print("| | answer: y/n")
            self.play_again()

    def payout(self):
        for i in range(self.number_of_players):
            if self.blackjack[i]:
                self.balance[i] += (3 * self.bet[i])
                self.winnings[i] = (2 * self.bet[i])
                print('| | Wow, dear ' + str(self.names[i]) + ', you have BLACKJACK, you receive triple your bet, that is $' + str(self.bet[i] * 3) + ' and your balance is now: $' + str(self.balance[i]))

    def resolve_standoff(self):
        if self.insurance:
            print('| |')
            print('| | The dealer\'s face-down card is: ' + self.deck_to_string(2 * self.original_number_of_players + 1))
            print('| |')
            self.print_hand(self.number_of_players)
            if self.blackjack[-1]:
                for i in range(self.number_of_players):
                    if self.blackjack[i]:
                        self.winnings[i] = 0
                        self.balance[i] += self.bet[i]
                        print('| | There is a standoff with player ' + str(i + 1) + ', you keep your bet, your balance is now: $' + str(self.balance[i]))
                    else:
                        print('| | Dear ' + str(self.names[i]) + ', you lose, your balance is now: $' + str(self.balance[i]))
                        self.winnings[i] = -self.bet[i]

    def offer_insurance(self, iteration=0):
        dealer_face_up_card = len(self.deck) - 2

        if self.value_list[dealer_face_up_card] == 1 or self.value_list[dealer_face_up_card] == 10:
            print('| | Insurance')
            print('| | ------------')
            print('| | The house has a chance of blackjack, do you want to continue playing? You will get your bet back if you stop now')

            self.insurance = True
            for i in range(iteration, self.number_of_players):
                if self.blackjack[i]:
                    continue
                answer = input('| | Dear ' + str(self.names[i]) + ', do you wish to continue playing?\n| | ')
                if answer == 'y':
                    self.insurance_response[i] = True
                elif answer == 'n':
                    self.bet[i] = 0
                    self.winnings[i] = 0
                    self.balance[i] = self.old_balance[i]
                    self.insurance_response[i] = False
                else:
                    print("| | Answer: y/n")
                    self.offer_insurance(i)
                    break

    def print_initial_cards(self, message=0):
        card_list = [''] * len(self.deck)
        card1 = [''] * (self.number_of_players + 1)
        card2 = [''] * (self.number_of_players + 1)
        filler = 16
        s = ['-' * filler] * (self.number_of_players + 1)

        for i in range(len(self.deck)):
            card_list[i] = self.deck_to_string(i)

        for i in range(self.number_of_players + 1):
            card1[i] = card_list[2 * i]
            card2[i] = card_list[2 * i + 1]

        if message == 0:
            print('| |')
            for i in range(0, self.number_of_players + 1):
                s[i] = '-' * (filler - len(self.names[i]))
                if i == self.number_of_players:
                    print('| | Dealer\t\t\t: ' + card1[i] + ', ' + card2[i] + '\t(' + str(self.points_list[i]) + ')')
                else:
                    print('| | ' + self.names[i] + '\t' + s[i] + ': ' + card1[i] + ', ' + card2[i] + '\t(' + str(self.points_list[i]) + ')')
        else:
            print('| |')
            print('| | Players and their initial cards are:')
            print('| |')
            for i in range(0, self.number_of_players + 1):
                s[i] = '-' * (filler - len(self.names[i]))
                if i == self.number_of_players:
                    print('| | Dealer\t\t\t: ' + card1[i] + ', ' + card2[i] + '\t(' + str(self.points_list[i]) + ')')
                else:
                    print('| | ' + self.names[i] + '\t' + s[i] + ': ' + card1[i] + ', ' + card2[i] + '\t(' + str(self.points_list[i]) + ')')

    def print_hand(self, player_number):
        print('| | ' + self.names[player_number] + '\'s cards are: ')
        print('| | ---------------------')
        for i in range(len(self.deck)):
            if self.turn_order[i] == player_number:
                print('| | ' + self.deck_to_string(i))

    def check_blackjack(self):
        for i in range(0, self.number_of_players + 1):
            if self.points_list[i] == 21:
                self.blackjack[i] = True
                self.status[i] = 'blackjack'
                if i == self.number_of_players:
                    print('| | The dealer has blackjack!')
                else:
                    print('| | Player ' + str(i + 1) + ' (' + self.names[i] + ') has blackjack!')

    def initial_deal(self):
        self.shuffle_deck()
        self.deal_initial_cards()
        self.calculate_initial_points()
        self.print_initial_cards()

    def deal_initial_cards(self):
        for i in range(2 * (self.number_of_players + 1)):
            self.draw_card(i % (self.number_of_players + 1))

    def calculate_initial_points(self):
        for i in range(0, len(self.deck)):
            player_number = self.turn_order[i]
            card_value = self.value_list[i]
            self.points_list[player_number] += card_value

            if card_value == 1:
                self.ace_list.append(i)
                self.ace_count[player_number] += 1

            if self.points_list[player_number] > 21 and self.ace_count[player_number] > 0:
                self.points_list[player_number] -= 10
                self.ace_count[player_number] -= 1

    def ask_number_of_players(self):
        answer = input('| | How many players?\n| | ')
        try:
            self.number_of_players = int(answer)
            if self.number_of_players < 1 or self.number_of_players > 6:
                raise ValueError
        except ValueError:
            print('| | Please enter a number between 1 and 6.')
            self.ask_number_of_players()

    def ask_names(self):
        for i in range(0, self.number_of_players):
            self.names[i] = input('| | Player ' + str(i + 1) + ', what is your name?\n| | ')

    def ask_bet_amount(self):
        for i in range(0, self.number_of_players):
            answer = input('| | ' + self.names[i] + ', how much do you want to bet? (Min $5)\n| | ')
            try:
                bet = int(answer)
                if bet < 5:
                    raise ValueError
                self.bet[i] = bet
            except ValueError:
                print('| | Please enter a valid bet amount (Min $5).')
                self.ask_bet_amount()

    def create_deck(self):
        deck = []
        for suit in range(4):
            for value in range(13):
                deck.append((suit, value))
        return deck

    def deck_to_string(self, index):
        suit = self.suits[self.deck[index][0]]
        value = self.values[self.deck[index][1]]
        return value + ' of ' + suit

    def draw_card(self, player_number):
        if not self.deck:
            print("| | The deck is empty. Reshuffling...")
            self.deck = self.create_deck()
            self.shuffle_deck()
        card = self.deck.pop()
        self.turn_order.append(player_number)
        self.value_list.append(card[1] + 1 if card[1] < 10 else 10)

    def shuffle_deck(self):
        np.random.shuffle(self.deck)

    def clear_table(self):
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.turn_order = []
        self.ace_list = []
        self.value_list = []

    def handle_split(self):
        pass

    def player_choice(self):
        pass

    def dealer_play(self):
        pass

    def determine_winner(self):
        pass


if __name__ == "__main__":
    BlackJack()
