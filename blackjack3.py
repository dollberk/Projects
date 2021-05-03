import random
import sys
from collections import namedtuple, defaultdict
import csv


class Hand:

    def __init__(self, cards=None):
        self.cards = []
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
            total, soft_ace_count = self.score()

    def __str__(self):
        return "Cards in hand: {self.cards}"

    def add_card(self):
        # returns a random number symbolic of cards in a deck
        if self.score()[0] < 21:
            self.cards.append(random.randint(1, 13))
            total, soft_ace_count = self.score()

    def is_blackjack(self):
        if len(self.cards) == 2 and self.score()[1] == 1 and self.score()[0] == 21:
            return True
        else:
            return False

    def is_bust(self):
        if self.score()[0] > 21:
            return True
        else:
            return False

    def score(self):
        Score = namedtuple("Score", "total soft_act_count")
        weighted_cards = []
        card_total = 0
        soft_ace_count = 0

        # creates a separate list for the weights of the cards
        for x in self.cards:

            # for royals (king, queen, jack) whose value is 10
            if x > 10:
                weighted_cards.append(10)

            # for aces whose value is initially 11
            elif x == 1:
                weighted_cards.append(11)
                # count the value of aces representing the value 11
                soft_ace_count += 1

            else:
                # card value = weighted value
                weighted_cards.append(x)

        # if an ace is present in the hand
        if 1 in self.cards:

            card_total = sum(weighted_cards)

            # loops through cards to make sure soft aces can be converted
            # to avoid busting
            while 11 in weighted_cards and card_total > 21:
                # removes each 11-valued ace to replace with a 1-valued ace
                weighted_cards.remove(11)
                weighted_cards.append(1)
                # lowers soft ace count when an 11 is replaced with a 1
                soft_ace_count -= 1

        card_total = sum(weighted_cards)

        return Score(card_total, soft_ace_count)


class Strategy:

    def __init__(self, stand_on_value, stand_on_soft):
        self.hand = Hand()
        self.stand_on_value = stand_on_value
        self.stand_on_soft = stand_on_soft

    def __repr__(self):
        return "(%d, %d)" % (self.stand_on_value, self.stand_on_soft)

    def __str__(self):
        if self.stand_on_soft:
            return "S" + str(self.stand_on_value)
        else:
            return "H" + str(self.stand_on_value)

    def stand(self, hand):
        Stand = namedtuple("Stand", "stand total")
        total, soft_ace_count = Hand.score(hand)
        # when soft aces are present and stand value has been met
        # but can exchange soft aces for hard
        if total >= self.stand_on_value and self.stand_on_soft is False and soft_ace_count > 0:
            # print("False, hit it")
            return Stand(False, total)

        # when stand on value has been met and
        # 1) stand on soft is true or
        # 2) stand on soft is false but there are no soft aces
        elif total >= self.stand_on_value:
            return Stand(True, total)

        else:
            return Stand(False, total)

    def play(self):

        hand_score = self.hand.score()
        while hand_score[0] < 21:
            if (self.stand_on_soft and hand_score[0] >= self.stand_on_value) or self.stand(self.hand)[0]:
                return self.hand
            else:
                Hand.add_card(self.hand)

        else:
            return self.hand


def main():

    #check that all arguments are present but no more
    if len(sys.argv) != 2:
        raise ValueError("Please include the number of simulations")

    #check that value entered is an integer greater than 0
    num_simulations = int(sys.argv[1])
    if not num_simulations > 0:
        raise TypeError("Please input an integer above 0 for number of simulations to be performed")

    #create nested default dictionary
    percent_dict = defaultdict(lambda: defaultdict(float))

    #loop through all stand on values for player
    for x in range(13, 21):

        # create key in dict that is "P-S + x" i.e. P-S13, P-S14
        # added tab for spacing in .txt file
        player_soft_x = 'P-S' + str(x) + '\t'
        # create key in dict that is "P-H + x" i.e. P-H13, P-H14
        player_hard_x = 'P-H' + str(x) + '\t'

        #loops through all stand on values for dealer
        for w in range(13, 21):

            # create key in dict that is "D-S + w" i.e. D-S13
            dealer_soft_w = 'D-S' + str(w)
            # creat key in dict that is "D-H + w" i.e. D-H13
            dealer_hard_w = 'D-H' + str(w)

            y = 0

            # perform number of simulations for hard and soft hands
            # of both the player and the dealer
            while y < num_simulations:

                # play hand when stand_on_soft is true
                # for player
                player_soft_total = Strategy(x, "soft")
                p_soft_hand = player_soft_total.play()
                # for dealer
                dealer_soft_total = Strategy(w, "soft")
                d_soft_hand = dealer_soft_total.play()

                # play hand when stand_on_soft is false
                # for player
                player_hard_total = Strategy(x, "hard")
                p_hard_hand = player_hard_total.play()
                # for dealer
                dealer_hard_total = Strategy(w, "hard")
                d_hard_hand = dealer_hard_total.play()

                #player soft hand is blackjack and dealer soft hand is not
                if p_soft_hand.is_blackjack() and not d_soft_hand.is_blackjack():
                    percent_dict[player_soft_x][dealer_soft_w] += 1

                #player soft hand is blackjack and dealer hard hand is not
                elif p_soft_hand.is_blackjack() and not d_hard_hand.is_blackjack():
                    percent_dict[player_soft_x][dealer_hard_w] += 1

                #dealer soft hand busts against player soft hand
                elif d_soft_hand.is_bust() and not p_soft_hand.is_bust():
                    percent_dict[player_soft_x][dealer_soft_w] += 1

                #dealer hard hand busts against player soft hand
                elif d_hard_hand.is_bust() and not p_soft_hand.is_bust():
                    percent_dict[player_soft_x][dealer_hard_w] += 1

                #player soft hand is greater than dealer soft hand
                elif not p_soft_hand.is_bust() and p_soft_hand.score()[0] > d_soft_hand.score()[0]:
                    percent_dict[player_soft_x][dealer_soft_w] += 1

                #player soft hand is greater than dealer hard hand
                elif not p_soft_hand.is_bust() and p_soft_hand.score()[0] > d_hard_hand.score()[0]:
                    percent_dict[player_soft_x][dealer_hard_w] += 1

                #player hard hand is blackjack and dealer soft hand is not
                if p_hard_hand.is_blackjack() and not d_soft_hand.is_blackjack():
                    percent_dict[player_hard_x][dealer_soft_w] += 1

                #player hard hand is blackjack and dealer hard hand is not
                elif p_hard_hand.is_blackjack() and not d_hard_hand.is_blackjack():
                    percent_dict[player_hard_x][dealer_hard_w] += 1

                #dealer soft hand busts against player hard hand
                elif d_soft_hand.is_bust() and not p_hard_hand.is_bust():
                    percent_dict[player_soft_x][dealer_soft_w] += 1

                #dealer hard hand busts against player hard hand
                elif d_hard_hand.is_bust() and not p_hard_hand.is_bust():
                    percent_dict[player_hard_x][dealer_hard_w] += 1

                #player hard hand is greater than dealer soft hand
                elif not p_hard_hand.is_bust() and p_hard_hand.score()[0] > d_soft_hand.score()[0]:
                    percent_dict[player_hard_x][dealer_soft_w] += 1

                #player hard hand is greater than dealer hard hand
                elif not p_hard_hand.is_bust() and p_hard_hand.score()[0] > d_hard_hand.score()[0]:
                    percent_dict[player_hard_x][dealer_soft_w] += 1

                y += 1
            w += 1

        for a in range(13, 21):
            #added default 0s for simulations in which no hand hit a particular total
            #i.e. S20 may never need to create a dict key 13 as no hand will stop at 13
            b = "D-S" + str(a)
            c = "D-H" + str(a)
            if b not in percent_dict[player_soft_x].keys():
                 percent_dict[player_soft_x][b]

            if b not in percent_dict[player_hard_x].keys():
                 percent_dict[player_hard_x][b]

            if c not in percent_dict[player_soft_x].keys():
                 percent_dict[player_soft_x][c]
                                                           
            if c not in percent_dict[player_hard_x].keys():
                 percent_dict[player_hard_x][c]
                
            a += 1

        for z in percent_dict[player_soft_x]:
            #avg each simulation total for player soft hands
            percent_dict[player_soft_x][z] = percent_dict[player_soft_x][z]/num_simulations

        for t in percent_dict[player_hard_x]:
            #avg each simulation total for player hard hands
            percent_dict[player_hard_x][t] = percent_dict[player_hard_x][t]/num_simulations

        x += 1

    #headers
    header = ["D-S13", "D-H13", "D-S14", "D-H14", "D-S15", "D-H15", "D-S16", "D-H16", "D-S17", "D-H17", "D-S18", "D-H18", "D-S19",  "D-H19", "D-S20", "D-H20"]

    #csv writer to create txt file
    with open("test.txt", "w", newline="") as f:
        wr = csv.writer(f, delimiter='\t')
        #write headers
        wr.writerow(["P-Strategy", *header])
        #write each line in the order of which header its key corresponds to
        for m, n in percent_dict.items():
            wr.writerow([m]+[n.get(i, '') for i in header])


if __name__ == "__main__":
    main()
