import random as r


def create_deck():
    deck = []
    face_values = ['A', 'J', 'Q', 'K']
    for i in range(4):
        for card in range(2, 11):
            deck.append(str(card))
        for card in face_values:
            deck.append(card)
    r.shuffle(deck)
    return deck


class Player:

    def __init__(self, hand=[], money=100):
        self.hand = hand
        self.score = 0
        self.score = self.set_score()
        self.money = money
        self.bet_value = 0

    def __str__(self):
        current_hand = ''
        for card in self.hand:
            current_hand += str(card) + ' '
        return current_hand + 'score: ' + str(self.score)

    def set_score(self):
        self.score = 0
        face_cards_dict = {'A': 11, 'J': 10, 'Q': 10, 'K': 10,
                           '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                           '8': 8, '9': 9, '10': 10}
        ace_counter = 0
        for card in self.hand:
            self.score += face_cards_dict[card]
            if card == 'A':
                ace_counter += 1
            # For every ace we take away 10 points so that ace would have value
            # of 1
            if self.score > 21 and ace_counter != 0:
                self.score -= 10
                ace_counter -= 1
        return self.score

    def hit(self, card):
        self.hand.append(card)
        self.score = self.set_score()

    def play(self, new_hand):
        self.hand = new_hand
        self.score = self.set_score()

    def bet(self, amount):
        self.money -= amount
        self.bet_value += amount

    def win(self, result):
        if result:
            if self.score == 21 and len(self.hand) == 2:
                print('YOU WON BLACKJACK')
                self.money += 2.5 * self.bet_value
            else:
                print('YOU WON')
                self.money += 2 * self.bet_value
            self.bet_value = 0
        else:
            print('You lost :<')
            self.bet_value = 0

    def has_blackjack(self):
        if self.score == 21 and len(self.hand) == 2:
            return True
        else:
            return False

    def draw(self):
        self.money += self.bet_value
        self.bet_value = 0


def print_house(house):
    print('HOUSE CARDS')
    for card in range(len(house.hand)):
        if card == 0:
            print('X', end=' ')
        elif card == len(house.hand) - 1:
            print(house.hand[card])
        else:
            print(house.hand[card], end=' ')


card_deck = create_deck()
first_hand = [card_deck.pop(), card_deck.pop()]
second_hand = [card_deck.pop(), card_deck.pop()]
player1 = Player(first_hand)
house_player = Player(second_hand)
card_deck = create_deck()
continue_game = True
while continue_game:
    if len(card_deck) < 20:
        card_deck = create_deck()
    first_hand = [card_deck.pop(), card_deck.pop()]
    second_hand = [card_deck.pop(), card_deck.pop()]
    player1.play(first_hand)
    house_player.play(second_hand)
    bet = int(input("Please enter your bet: "))
    player1.bet(bet)
    print_house(house_player)
    print('YOUR CARDS')
    print(player1)
    if player1.has_blackjack():
        if house_player.has_blackjack():
            player1.draw()
        else:
            player1.win(True)
    else:
        while player1.score < 21:
            action = input('Do you want another card?(Y/N): ')
            if action == 'y' or action == 'Y':
                player1.hit(card_deck.pop())
                print('YOUR CARDS')
                print(player1)
                print_house(house_player)
            else:
                break
        while house_player.score < 16:
            print_house(house_player)
            house_player.hit(card_deck.pop())

        if player1.score > 21:
            if house_player.score > 21:
                player1.draw()
            else:
                player1.win(False)
        elif player1.score > house_player.score:
            player1.win(True)
        elif player1.score == house_player.score:
            player1.draw()
        else:
            if house_player.score > 21:
                player1.win(True)
            else:
                player1.win(False)
    print('house hand was: ', house_player)
    print('Your current wallet: ', player1.money)
    play_again = input('Continue the game? (Y/N): ')
    if play_again == 'Y' or play_again == 'y':
        continue_game = True
        print('Continuing the game')
    elif play_again == 'N' or play_again == 'n':
        continue_game = False
        print('The game will be stopped...')

print('Thank you for playing')

