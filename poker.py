from copy import deepcopy
from random import choices
from time import time

# cards [2, 3]
# hands [cards, card]
# level 1: high card
# level 2: one pair
# level 3: two pairs
# level 4: three of a kind
# level 5: straight
# level 6: flush
# level 7: full
# level 8: four of a kind
# level 9: straight flush

# result [level, [five best cards by descending order except for full where we put three of a kind first and for the ace when it's like a 1 in a straight]]


def check_straight_flush(seven_cards):
    results = []
    for card in seven_cards:
        # a straight cannot start with a J, Q or K
        if card[0] not in [11, 12, 13]:
            if card[0] == 14:
                if [2, card[1]] in seven_cards and [3, card[1]] in seven_cards and [4, card[1]] in seven_cards and [5, card[1]] in seven_cards:
                    results.append([9, [[5, card[1]], [4, card[1]], [3, card[1]], [2, card[1]], card]])
            else:
                straight_draw = [card]
                keep_searching = True
                while keep_searching and len(straight_draw) <= 4:
                    if [straight_draw[-1][0] + 1, straight_draw[-1][1]] in seven_cards:
                        straight_draw.append([straight_draw[-1][0] + 1, straight_draw[-1][1]])
                    else:
                        keep_searching = False
                if len(straight_draw) == 5:
                    straight_draw.reverse()
                    results.append([9, straight_draw])
    if results:
        return sorted(results, reverse=True)
    else:
        return None


def check_four(seven_cards):
    results = []
    for card in seven_cards:
       if [card[0], 0] in seven_cards and [card[0], 1] in seven_cards and [card[0], 2] in seven_cards and [card[0], 3] in seven_cards:
            seven_cards_copy = deepcopy(seven_cards)
            seven_cards_copy.remove([card[0], 3])
            seven_cards_copy.remove([card[0], 2])
            seven_cards_copy.remove([card[0], 1])
            seven_cards_copy.remove([card[0], 0])
            fifth_best_card = max(seven_cards_copy)
            result = [8, [[card[0], 3], [card[0], 2], [card[0], 1], [card[0], 0], fifth_best_card]]
            if result not in results:
                results.append(result)
    if results:
        return sorted(results, reverse=True)
    else:
        return None


def check_full(seven_cards):
    results = []
    for card in seven_cards:
        three_draw = [card_el for card_el in seven_cards if card_el[0] == card[0]]
        # there cannot be a four of a kind because the hand would not pass in this function if there is a four of a kind
        if len(three_draw) == 3:
            seven_cards_copy = deepcopy(seven_cards)
            seven_cards_copy.remove(three_draw[0])
            seven_cards_copy.remove(three_draw[1])
            seven_cards_copy.remove(three_draw[2])
            for card_left in seven_cards_copy:
                for other_card in seven_cards_copy:
                    if other_card != card_left:
                        if other_card[0] == card_left[0]:
                            result = [7, sorted(three_draw, reverse=True) + sorted([card_left, other_card], reverse=True)]
                            if result not in results:
                                results.append(result)
    if results:
        return sorted(results, reverse=True)
    else:
        return None


def check_flush(seven_cards):
    results = []
    for card in seven_cards:
        flush_draw = [card_el for card_el in seven_cards if card_el[1] == card[1]]
        if len(flush_draw) >= 5:
            flush_draw = sorted(flush_draw, reverse=True)
            while len(flush_draw) >= 6:
                flush_draw.pop()
            result = [6, flush_draw]
            if result not in results:
                results.append(result)
    if results:
        return sorted(results, reverse=True)
    else:
        return None


def check_straight(seven_cards):
    results = []
    for card in seven_cards:
        # a straight cannot start with a J, Q or K
        if card[0] not in [11, 12, 13]:
            straight_draw = [card]
            keep_searching = True
            if card[0] == 14:
                # looking for a 2
                next_possible_cards = [card_el for card_el in seven_cards if card_el[0] == 2]
                if next_possible_cards:
                    straight_draw.append(sorted(next_possible_cards, reverse=True)[0])
            while keep_searching and len(straight_draw) <= 4:
                next_possible_cards = [card_el for card_el in seven_cards if card_el[0] == straight_draw[-1][0] + 1]
                if next_possible_cards:
                    straight_draw.append(sorted(next_possible_cards, reverse=True)[0])
                else:
                    keep_searching = False
            if len(straight_draw) == 5:
                straight_draw.reverse()
                results.append([5, straight_draw])
    if results:
        return sorted(results, reverse=True)
    else:
        return None


def check_three(seven_cards):
    results = []
    for card in seven_cards:
        three_draw = [card_el for card_el in seven_cards if card_el[0] == card[0]]
        # there cannot be a four of a kind because the hand would not pass in this function if there is a four of a kind
        if len(three_draw) == 3:
            seven_cards_copy = deepcopy(seven_cards)
            seven_cards_copy.remove(three_draw[0])
            seven_cards_copy.remove(three_draw[1])
            seven_cards_copy.remove(three_draw[2])
            fourth_best_card = max(seven_cards_copy)
            seven_cards_copy.remove(fourth_best_card)
            fifth_best_card = max(seven_cards_copy)
            result = [4, sorted(three_draw, reverse=True) + [fourth_best_card, fifth_best_card]]
            if result not in results:
                results.append(result)
    if results:
        return sorted(results, reverse=True)
    else:
        return None

def check_two_pairs(seven_cards):
    results = []
    for card in seven_cards:
        for other_card in seven_cards:
            if other_card != card:
                if other_card[0] == card[0]:
                    seven_cards_copy = deepcopy(seven_cards)
                    seven_cards_copy.remove(card)
                    seven_cards_copy.remove(other_card)
                    for third_card in seven_cards_copy:
                        for fourth_card in seven_cards_copy:
                            if fourth_card != third_card:
                                if fourth_card[0] == third_card[0]:
                                    another_seven_cards_copy = deepcopy(seven_cards_copy)
                                    another_seven_cards_copy.remove(third_card)
                                    another_seven_cards_copy.remove(fourth_card)
                                    fifth_best_card = max(another_seven_cards_copy)
                                    result = [3, sorted([card, other_card, third_card, fourth_card], reverse=True) + [fifth_best_card]]
                                    if result not in results:
                                        results.append(result)
    if results:
        return sorted(results, reverse=True)
    else:
        return None


def check_pair(seven_cards):
    results = []
    for card in seven_cards:
        for other_card in seven_cards:
            if other_card != card:
                if other_card[0] == card[0]:
                    seven_cards_copy = deepcopy(seven_cards)
                    seven_cards_copy.remove(card)
                    seven_cards_copy.remove(other_card)
                    third_best_card = max(seven_cards_copy)
                    seven_cards_copy.remove(third_best_card)
                    fourth_best_card = max(seven_cards_copy)
                    seven_cards_copy.remove(fourth_best_card)
                    fifth_best_card = max(seven_cards_copy)
                    result = [2, sorted([card, other_card], reverse=True) + [third_best_card, fourth_best_card, fifth_best_card]]
                    if result not in results:
                        results.append(result)
    if results:
        return sorted(results, reverse=True)
    else:
        return None


def get_result(hand, board):
    seven_cards = hand + board
    # check for straight flush
    results = check_straight_flush(seven_cards)
    if results:
        return results[0]
    # check for four of a kind
    results = check_four(seven_cards)
    if results:
        return results[0]
    # check for full
    results = check_full(seven_cards)
    if results:
        return results[0]
    # check for flush
    results = check_flush(seven_cards)
    if results:
        return results[0]
    # check for straight
    results = check_straight(seven_cards)
    if results:
        return results[0]
    # check for three
    results = check_three(seven_cards)
    if results:
        return results[0]
    # check for two pairs
    results = check_two_pairs(seven_cards)
    if results:
        return results[0]
    # check for pair
    results = check_pair(seven_cards)
    if results:
        return results[0]
    # if none of those worked, we just return the 5 best cards sorted by descending order
    return [1, sorted(hand + board, reverse=True)[:5]]


def compare_hands(h1, h2, board):
    res1 = get_result(h1, board)
    res2 = get_result(h2, board)
    if res1[0] > res2[0]:
        return 1
    else:
        if res2[0] > res1[0]:
            return 2
        else:
            if res1[1][0][0] > res2[1][0][0]:
                return 1
            else:
                if res2[1][0][0] > res1[1][0][0]:
                    return 2
                else:
                    if res1[1][1][0] > res2[1][1][0]:
                        return 1
                    else:
                        if res2[1][1][0] > res1[1][1][0]:
                            return 2
                        else:
                            if res1[1][2][0] > res2[1][2][0]:
                                return 1
                            else:
                                if res2[1][2][0] > res1[1][2][0]:
                                    return 2
                                else:
                                    if res1[1][3][0] > res2[1][3][0]:
                                        return 1
                                    else:
                                        if res2[1][3][0] > res1[1][3][0]:
                                            return 2
                                        else:
                                            if res1[1][4][0] > res2[1][4][0]:
                                                return 1
                                            else:
                                                if res2[1][4][0] > res1[1][4][0]:
                                                    return 2
                                                else:
                                                    return 0


def generate_board(h1, h2):
    pack_of_cards = [[i, j] for i in range(2, 15) for j in range(4)]
    pack_of_cards.remove(h1[0])
    pack_of_cards.remove(h1[1])
    pack_of_cards.remove(h2[0])
    pack_of_cards.remove(h2[1])
    return choices(pack_of_cards, k=5)


def compare_hands_statiscally(h1, h2):
    t1 = time()
    h1_wins = 0
    draw = 0
    h2_wins = 0
    for i in range(10000):
        board = generate_board(h1, h2)
        result = compare_hands(h1, h2, board)
        if result == 1:
            h1_wins += 1
        else:
            if result == 2:
                h2_wins += 1
            else:
                draw += 1
    t2 = time()
    print(t2 - t1)
    print('Hand 1 wins: {}'.format(h1_wins))
    print('Draws: {}'.format(draw))
    print('Hand 2 wins: {}'.format(h2_wins))

compare_hands_statiscally([[14, 0], [13, 0]], [[2, 2], [2, 3]])
