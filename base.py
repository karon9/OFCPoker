import string, math, random
import itertools

class Card(object):
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

    SUITS = ('S', 'D', 'H', 'C')

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # string型を定義
    def __str__(self):
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit

    # 比較演算子
    def __eq__(self, other):
        return (self.rank == other.rank and self.suit == other.suit)

    def __ne__(self, other):
        return (self.rank != other.rank or self.suit != other.suit)

    def __lt__(self, other):
        return (self.rank < other.rank)

    def __le__(self, other):
        return (self.rank <= other.rank)

    def __gt__(self, other):
        return (self.rank > other.rank)

    def __ge__(self, other):
        return (self.rank >= other.rank)


class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                card = Card(rank, suit)
                self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def deal(self):
        """
        カードを配るからデックからカードを消すよ
        """
        if len(self) == 0:
            return None
        else:
            return self.deck.pop(0)


class FantasyLand(object):
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.myhand = []
        self.top_hand = []
        self.middle_hand = []
        self.bottom_hand = []
        self.max = 0
        self.hands = [self.top_hand, self.middle_hand, self.bottom_hand]
        self.tlist = []  # create a list to store total_point
        self.royalties = []  # OFCPokerの役のポイント
        numCards_in_Hand = 14
        for i in range(numCards_in_Hand):
            self.myhand.append(self.deck.deal())

    def play(self):
        sortedHand = sorted(self.myhand, reverse=True)
        myhand = ''
        for card in sortedHand:
            myhand = myhand + str(card) + ' '
        print('MyHand' + ':' + myhand)  # ハンドを表示させるよ
        for i in range(3):
            self.top_hand.append(self.myhand.pop(0))
        for i in range(5):
            self.middle_hand.append(self.myhand.pop(0))
        for i in range(5):
            self.bottom_hand.append((self.myhand.pop(0)))
        for hand in self.hands:
            sortedHand = sorted(hand, reverse=True)
            hand_str = ''
            for card in sortedHand:
                hand_str = hand_str + str(card) + ' '
            print('hand' + ':' + hand_str)

    def combination(self):
        hand = ''
        count = 0
        sortedHand = sorted(self.myhand, reverse=True)
        for card in sortedHand:  # 組み合わせの出力
            hand = hand + str(card) + ' '
        print(hand)
        print('yes or no?')
        input()
        for combination in itertools.combinations(self.myhand, 5):
            hand = ''
            myhand = self.myhand
            # for card in combination:  # 組み合わせの出力
            #     hand = hand + str(card) + ' '
            # print(f'BottomHand:{hand}')
            self.bottom_hand = combination
            myhand_last = list(filter(lambda x: x not in list(combination), myhand))  # myhandから一つの組み合わせを削除
            for combination_last in itertools.combinations(myhand_last, 5):
                hand = ''
                # for card in combination_last:
                #     hand = hand + str(card) + ' '
                # print(f'MiddleHand:{hand}')
                self.middle_hand = combination_last
                myhand_last_last = list(filter(lambda x: x not in list(combination_last), myhand_last))
                for combination_last_last in itertools.combinations(myhand_last_last, 3):
                    hand = ''
                    # for card in combination_last_last:
                    #     hand = hand + str(card) + ' '
                    # print(f'TopHand:{hand}')
                    self.top_hand = combination_last_last
                    self.hands = [self.top_hand, self.middle_hand, self.bottom_hand]  # これがないとfor内ではhandsは定義できない
                    count += 1
                    print(f'\ncombination:{count}')
                    for hand in self.hands:
                        sortedHand = sorted(hand, reverse=True)
                        hand_str = ''
                        for card in sortedHand:
                            hand_str = hand_str + str(card) + ' '
                        print('hand' + ':' + hand_str)
                    self.search(self.hands)
                print('\n')
            print('\n')
        print('\n----------------------------------------------------')
        print(f'max:{self.max}')
        for hand in self.max_hands:
            sortedHand = sorted(hand, reverse=True)
            hand_str = ''
            for card in sortedHand:
                hand_str = hand_str + str(card) + ' '
            print('hand' + ':' + hand_str)

    def search(self, hands):
        self.isRoyal(hands)
        flag = False
        if self.tlist[0] < self.tlist[1] < self.tlist[2]:
            flag = True
            print(flag)
            print(f'sum:{sum(self.royalties)}')
            if self.max < sum(self.royalties):
                self.max = sum(self.royalties)
                self.max_hands = hands
        else:
            print(flag)
        self.tlist = []
        self.royalties = []

    def point(self, hand):  # point()function to calculate partial score
        sortedHand = sorted(hand, reverse=True)
        c_sum = 0
        ranklist = []
        for card in sortedHand:
            ranklist.append(card.rank)
        if self.state == 0:
            c_sum = ranklist[0] * 13 ** 4 + ranklist[1] * 13 ** 3 + ranklist[
                2] * 13 ** 2 + 14 * 13 + 14  # topとmiddleの3枚が同じならOut
        else:
            c_sum = ranklist[0] * 13 ** 4 + ranklist[1] * 13 ** 3 + ranklist[2] * 13 ** 2 + ranklist[3] * 13 + ranklist[
                4]
        return c_sum

    def isRoyal(self,
                hands):  # returns the total_point and prints out 'Royal Flush' if true, if false, pass down to isStraightFlush(hand)
        for self.state, hand in enumerate(hands):  # self.staeは現在どのhandの位置にいるか
            sortedHand = sorted(hand, reverse=True)
            if self.state == 0:  # top_handはisThreeに強制
                self.isThree(sortedHand)
            else:
                flag = True
                h = 10
                Cursuit = sortedHand[0].suit
                Currank = 14
                total_point = h * 13 ** 5 + self.point(sortedHand)
                for card in sortedHand:
                    if card.suit != Cursuit or card.rank != Currank:
                        flag = False
                        break
                    else:
                        Currank -= 1
                if flag:
                    print('Royal Flush')
                    self.tlist.append(total_point)
                    if self.state == 1:
                        self.royalties.append(50)
                    if self.state == 2:
                        self.royalties.append(25)

                else:
                    self.isStraightFlush(sortedHand)

    def isStraightFlush(self,
                        hand):  # returns the total_point and prints out 'Straight Flush' if true, if false, pass down to isFour(hand)
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 9
        Cursuit = sortedHand[0].suit
        Currank = sortedHand[0].rank
        total_point = h * 13 ** 5 + self.point(sortedHand)
        for card in sortedHand:
            if card.suit != Cursuit or card.rank != Currank:
                flag = False
                break
            else:
                Currank -= 1
        if flag:
            print('Straight Flush')
            self.tlist.append(total_point)
            if self.state == 1:
                self.royalties.append(30)
            if self.state == 2:
                self.royalties.append(15)
        else:
            self.isFour(sortedHand)

    def isFour(self,
               hand):  # returns the total_point and prints out 'Four of a Kind' if true, if false, pass down to isFull()
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 8
        Currank = sortedHand[
            1].rank  # since it has 4 identical ranks,the 2nd one in the sorted listmust be the identical rank
        count = 0
        total_point = h * 13 ** 5 + self.point(sortedHand)
        for card in sortedHand:
            if card.rank == Currank:
                count += 1
        if not count < 4:
            flag = True
            print('Four of a Kind')
            self.tlist.append(total_point)
            if self.state == 1:
                self.royalties.append(20)
            if self.state == 2:
                self.royalties.append(10)

        else:
            self.isFull(sortedHand)

    def isFull(self,
               hand):  # returns the total_point and prints out 'Full House' if true, if false, pass down to isFlush()
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 7
        total_point = h * 13 ** 5 + self.point(sortedHand)
        mylist = []  # create a list to store ranks
        for card in sortedHand:
            mylist.append(card.rank)
        rank1 = sortedHand[0].rank  # The 1st rank and the last rank should be different in a sorted list
        rank2 = sortedHand[-1].rank
        num_rank1 = mylist.count(rank1)
        num_rank2 = mylist.count(rank2)
        if (num_rank1 == 2 and num_rank2 == 3) or (num_rank1 == 3 and num_rank2 == 2):
            flag = True
            print('Full House')
            self.tlist.append(total_point)
            if self.state == 1:
                self.royalties.append(12)
            if self.state == 2:
                self.royalties.append(6)

        else:
            flag = False
            self.isFlush(sortedHand)

    def isFlush(self,
                hand):  # returns the total_point and prints out 'Flush' if true, if false, pass down to isStraight()
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 6
        total_point = h * 13 ** 5 + self.point(sortedHand)
        Cursuit = sortedHand[0].suit
        for card in sortedHand:
            if not (card.suit == Cursuit):
                flag = False
                break
        if flag:
            print('Flush')
            self.tlist.append(total_point)
            if self.state == 1:
                self.royalties.append(8)
            if self.state == 2:
                self.royalties.append(4)

        else:
            self.isStraight(sortedHand)

    def isStraight(self, hand):
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 5
        total_point = h * 13 ** 5 + self.point(sortedHand)
        Currank = sortedHand[0].rank  # this should be the highest rank
        for card in sortedHand:
            if card.rank != Currank:
                flag = False
                break
            else:
                Currank -= 1
        if flag:
            print('Straight')
            self.tlist.append(total_point)
            if self.state == 1:
                self.royalties.append(4)
            if self.state == 2:
                self.royalties.append(2)

        else:
            self.isThree(sortedHand)

    def isThree(self, hand):
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 4
        total_point = h * 13 ** 5 + self.point(sortedHand)
        Currank = sortedHand[2].rank  # In a sorted rank, the middle one should have 3 counts if flag=True
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(Currank) == 3:
            flag = True
            print("Three of a Kind")
            self.tlist.append(total_point)
            if self.state == 0:
                score = Currank - 10 + 1
                self.royalties.append(score)
            if self.state == 1:
                self.royalties.append(2)

        else:
            flag = False
            if self.state == 0:
                self.isOne(sortedHand)
            else:
                self.isTwo(sortedHand)

    def isTwo(self, hand):  # returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 3
        total_point = h * 13 ** 5 + self.point(sortedHand)
        rank1 = sortedHand[
            1].rank  # in a five cards sorted group, if isTwo(), the 2nd and 4th card should have another identical rank
        rank2 = sortedHand[3].rank
        mylist = []
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(rank1) == 2 and mylist.count(rank2) == 2:
            flag = True
            print("Two Pair")
            self.tlist.append(total_point)
            if self.state == 1:
                self.royalties.append(0)
            if self.state == 2:
                self.royalties.append(0)

        else:
            flag = False
            self.isOne(sortedHand)

    def isOne(self, hand):  # returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 2
        total_point = h * 13 ** 5 + self.point(sortedHand)
        mylist = []  # create an empty list to store ranks
        mycount = []  # create an empty list to store number of count of each rank
        for card in sortedHand:
            mylist.append(card.rank)
        for each in mylist:
            count = mylist.count(each)
            if count == 2:
                pair = each
            mycount.append(count)
        if mycount.count(2) == 2:  # There should be only 2 identical numbers
            flag = True
            print("One Pair")
            self.tlist.append(total_point)
            if self.state == 0:
                score = pair - 6 + 1
                if score < 0:
                    score = 0
                self.royalties.append(score)
            if self.state == 1:
                self.royalties.append(0)
            if self.state == 2:
                self.royalties.append(0)

        else:
            flag = False
            self.isHigh(sortedHand)

    def isHigh(self, hand):  # returns the total_point and prints out 'High Card'
        sortedHand = sorted(hand, reverse=True)
        flag = True
        h = 1
        total_point = h * 13 ** 5 + self.point(sortedHand)
        mylist = []  # create a list to store ranks
        for card in sortedHand:
            mylist.append(card.rank)
        print("High Card")
        self.tlist.append(total_point)
        if self.state == 1 and 7 < sortedHand[0].rank < 10:  # 2-7_low_middle_handのpoint
            score = 10 - sortedHand[0].rank
            self.royalties.append(score)
        if self.state == 1 and sortedHand[0].rank == 7:
            self.royalties.append(4)
        else:
            self.royalties.append(0)
if __name__ == "__main__":
    # while True:
    # flag = False
    # game.play()
    # game.isRoyal(game.hands)
    # print(game.tlist)
    # if game.tlist[0] < game.tlist[1] < game.tlist[2]:
    #     flag = True
    #     print(flag)
    # else:
    #     print(flag)
    # print('\n')
    # print(game.royalties)
    # if flag:
    #     print(f'sum:{sum(game.royalties)}')
    game = FantasyLand()
    game.combination()
