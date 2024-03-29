import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')

values = {
    'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7,
    'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10,
    'Ace': 11
}

playing = True


class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp =''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)  # card passed on. from Deck.deal()--> single card(suit,rank)
        self.value += values[card.rank]
        if card.rank == 'Ace':  # track aces
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:  # if total value >21 and still have an ace.
            self.value -= 10  # then change many aces to be one instead of 11
            self.aces -= 1


class Chips:
    def __init__(self,total=100):
        self.total = total  # this can be set to a default value or supplied by user
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except:
            print('Sorry please provide an integer')
        else:
            if chips.bet > chips.total:
                print('Sorry, you do not have enough chips! you have {}'.format(chips.total))
            else:
                break


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to an upcoming while loop
    while True:
        x = input('Hit or Stand? Enter h or s ')
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player stand, dealer's turn")
            playing = False
        else:
            print('Sorry i did not understand that, please enter h or s only!')
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand \nFirst card hidden")  # show only one of the dealer's cards
    print(dealer.cards
          [1])
    print("\nPlayer's hand")  # show all 2 cards of player's hand/cards
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    print("\nDealer's hand")
    for card in dealer.cards:
        print(card)
    print(f"Value of Dealer's hand is: {dealer.value}")
    print("\nPlayer's hand")
    for card in player.cards:
        print(card)
    print(f"Value of Dealer's hand is: {player.value}")


def player_busts(player, dealer, chips):
    print('BUST PLAYER!')
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print('PLAYER WINS!')
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print('DEALER WINS!')
    chips.lose_bet()


def dealer_wins(player, dealer, chips):
    print('PLAYER WINS! DEALER BUSTED!')
    chips.win_bet()


def push(player, dealer):
    print('Dealer and Player tie! PUSH')


while True:

    print('WELCOME TO BLACK JACK')

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand,dealer_hand)
    while playing:
        hit_or_stand(deck,player_hand)

        show_some(player_hand,dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        show_all(player_hand,dealer_hand)

        if dealer_hand.value < 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)

    print('\n Player total chips are at: {}'.format(player_chips.total))

    new_game = input('would you like to play another hand? [y or n] 100 ')
    if new_game[0].lower() == 'y':
        playing = True
        continue
    elif new_game != 'y' or new_game != 'n':
        print('Sorry i did not understand')
        break
    elif new_game[0].lower() != 'n':
        print('Sorry i did not understand')
        break
    else:
        print('THANK YOU FOR PLAYING!')
        break
