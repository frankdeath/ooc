#!/usr/bin/env python
# file:         calc.py
# usage:        calc.py <hole_cards> <flop>
# description:  This script calculates probabilities.
# author:       Kevin Peterson
# created:      June 10, 2004
# matured:      July 26, 2004

#  sys.argv[0] = ./calibrate.py
#  sys.argv[1] = <hole_cards>
#  sys.argv[2] = <flop>
#  sys.argv[3] = <turn>
#  sys.argv[4] = <river>

import sys

full_deck = [1] * 52
hand_type = {0:'No Pair        ', 1:'One Pair       ', 2:'Two Pair       ', 3:'Three of a Kind', 4:'Straight       ', 5:'Flush          ', 6:'Full House     ', 7:'Four of a Kind ', 8:'Straight Flush ', 9:'Five of a Kind'}
denom = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
suits = {'s':0, 'h':1, 'd':2, 'c':3}
d = {0:'2', 1:'3', 2:'4', 3:'5', 4:'6', 5:'7', 6:'8', 7:'9', 8:'T', 9:'J', 10:'Q', 11:'K', 12:'A'}
s = {0:'s', 1:'h', 2:'d', 3:'c'}
rank_dict = {0:'2', 1:'3', 2:'4', 3:'5', 4:'6', 5:'7', 6:'8', 7:'9', 8:'T', 9:'J', 10:'Q', 11:'K', 12:'A'} 
suit_dict = {0:'s', 1:'h', 2:'d', 3:'c'}
suit_names = {0:'spades', 1:'hearts', 2:'diamonds', 3:'clubs'}

min_hand = 0

def hand2array(string, array):
    length=len(string)/2
    for i in range(1,length+1):
      finish=i*2
      start=finish-2
      card=string[start:finish]
      array.append(denom[card[0]]+13*suits[card[1]])

def combinations(hand, output_array):
    for i in range(len(hand)):
        k=i+1
        sliced_hand=hand[k:]
        for j in range(len(sliced_hand)):
            output_array.append([hand[i],sliced_hand[j]])

def b_combos(flop, turn, river, output_array):
    if turn == 53:
        board = flop
    elif river == 53:
        board = flop
        board.append(turn)
    else:
        board = flop
        board.append(turn)
        board.append(river)

    for i in range(len(board)):
        slice_index_1 = i + 1
        slice_1 = board[slice_index_1:]
        for j in range(len(slice_1)):
            slice_index_2 = j + 1
            slice_2 = slice_1[slice_index_2:]
            for k in range(len(slice_2)):
                x = i
                y = j + slice_index_1
                z = k + slice_index_1 + slice_index_2
                output_array.append([board[x], board[y], board[z]])

def correct_deck(hand, deck):
    for card in hand:
        deck[card] = 0
    return deck

def value_count(hand):
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for card in hand:
        value = card % 13
        count[value] = count[value] + 1
    return count

def suit_count(hand):
    count = [0, 0, 0, 0]
    for card in hand:
        suit = card / 13
        count[suit] = count[suit] + 1
    return count

def straight_chk(hand):
    # hand will always have 5 cards in it (will differ for hold'em)
    straight = 0
    # assume hand is already sorted
    gaps = []
    for i in range(len(hand)-1):
        reduced = hand[i+1] - ( hand[i] + 1 )
        gaps.append(reduced)

    # if don't have a pair, then a straight is possible
    if gaps.count(-1) == 0:
        num_suits = suit_count(hand)
        # if checking for a straight, all will appear to be the same suit
        # if checking for a straight flush, this will remove suit spill-over
        if num_suits.count(5) == 1:
            zero_count = gaps.count(0)
            # normal straight check
            if zero_count == 4:
                straight = 1
            # low A straight check
            if zero_count == 3 and gaps == [0, 0, 0, 8]:
                straight = 1

    return straight

def hand_evaluation(hand_combos, flop, turn, river, minHand=0):
    # this needs to be highly optimized - don't check for hands lower than min hand
    max_hand = minHand
    board_combos = []
    # the lack of a colon in the following line was causing the problem
    b_combos(flop[:], turn, river, board_combos)
    for hand_combo in hand_combos:
        for board_combo in board_combos:
            hand = hand_combo + board_combo
            hand.sort()
            v_c = value_count(hand[:])
            h_s = [ x/13 for x in hand ]
            h_v = [ x%13 for x in hand ]
            s_c = suit_count(hand[:])
            h_v.sort()
            # Straight flush
            if minHand < 8 and straight_chk(hand[:]) > 0:
                type = 8
            # 4 of a Kind
            elif minHand < 7 and v_c.count(4) > 0:
                type = 7
            # Full House
            elif minHand < 6 and v_c.count(3) > 0 and v_c.count(2) > 0:
                type = 6
            # Flush
            elif minHand < 5 and s_c.count(5) > 0:
                type = 5
            # Straight (used modified sorted denom)
            elif minHand < 4 and straight_chk(h_v[:]) > 0: 
                type = 4
            # 3 of a Kind
            elif minHand < 3 and v_c.count(3) > 0:
                type = 3
            # 2 Pair
            elif minHand < 2 and v_c.count(2) > 1:
                type = 2
            # 1 Pair
            elif minHand < 1 and v_c.count(2) > 0:
                type = 1
            # No Pair
            else:
                type = 0
            if type > max_hand:
                max_hand = type
    return max_hand

def calc_stats(total_count, type_counts):
    odds = [0] * 10
    probability = [0] * 10
    for i in range(9):
        if type_counts[i] != 0:
            odds[i] = float(total_count) / type_counts[i] - 1
            probability[i] = type_counts[i] / float(total_count) * 100
    return (odds, probability)

def calculate_river(hole, board):
    combo_array = []
    combinations(hole, combo_array)

    flop = board[:3]
    turn = board[3]
    river = board[4]

    final_hand = hand_evaluation(combo_array[:], flop, turn, river)

    final_counter = 1
    final_type_counter = [0] * 10
    final_type_counter[final_hand] = 1
    
    #print final_type_counter
    final_odds, final_prob = calc_stats(final_counter, final_type_counter)
    #print final_odds, final_prob
    better_hand_array, better_hand_list = better_hands(hole, board, final_hand)
    #print better_hand_array

    global min_hand
    min_hand = final_hand

    return ((final_counter, final_type_counter, final_odds, final_prob), (better_hand_array, better_hand_list))

def calculate_turn(hole, board):
    combo_array = []
    combinations(hole, combo_array)

    flop = board[:3]
    turn = board[3]
    
    current_deck = correct_deck(hole, full_deck[:])
    current_deck = correct_deck(board, current_deck[:])

    river_card_index = 6
    river_type_counter = [0] * 10
    river_counter = 0

    # Determine minimum post-flop hand
    min_hnd = hand_evaluation(combo_array[:], flop, turn, 53)

    # Enumerate all possible hands
    for river_card in range(len(current_deck)):
        if current_deck[river_card] == 1:
            # Test for hands
            river = river_card
            type = hand_evaluation(combo_array[:], flop, turn, river, min_hnd)
            if type < min_hnd:
                print "ADDING A RIVER CARD MADE MY HAND LOWER"
                type = min_hnd
            ##print current_hand, hand_type[type]
            river_type_counter[type] = river_type_counter[type] + 1
            river_counter = river_counter + 1
            ###print "river_counter", river_counter

    river_odds, river_prob = calc_stats(river_counter, river_type_counter)

    better_hand_array, better_hand_list = better_hands(hole, board, min_hnd)

    global min_hand
    min_hand = min_hnd

    return ((river_counter, river_type_counter, river_odds, river_prob), (better_hand_array, better_hand_list))

def calculate_flop(hole, flop):
    combo_array = []
    combinations(hole, combo_array)

    current_deck = correct_deck(hole, full_deck[:])
    current_deck = correct_deck(flop, current_deck[:])

    turn_card_index = 5
    river_card_index = 6

    turn_type_counter = [0] * 10
    river_type_counter = [0] * 10

    turn_counter = 0
    river_counter = 0

    # Determine minimum post-flop hand
    min_hnd = hand_evaluation(combo_array[:], flop, 53, 53)

    # Enumerate all possible hands
    for turn_card in range(len(current_deck)):
        if current_deck[turn_card] == 1:
            slice_index = turn_card + 1
            # Test for hands
            type = hand_evaluation(combo_array[:], flop, turn_card, 53, min_hnd)
            if type < min_hnd:
                print "ERROR - ADDING A TURN CARD MADE MY HAND LOWER"
                type = min_hnd
            turn_type_counter[type] = turn_type_counter[type] + 1
            turn_counter = turn_counter + 1
            sliced_deck = current_deck[slice_index:]
            for river_card in range(len(sliced_deck)):
                if sliced_deck[river_card] == 1:
                    # Test for hands
                    river = river_card + slice_index
                    type = hand_evaluation(combo_array[:], flop, turn_card, river, min_hnd)
                    if type < min_hnd:
                        print "ERROR - ADDING A RIVER CARD MADE MY HAND LOWER"
                        type = min_hnd
                    river_type_counter[type] = river_type_counter[type] + 1
                    river_counter = river_counter + 1
                    ###print "river_counter", river_counter

    turn_odds, turn_prob = calc_stats(turn_counter, turn_type_counter)
    river_odds, river_prob = calc_stats(river_counter, river_type_counter)

    better_hand_array, better_hand_list = better_hands(hole, flop, min_hnd)

    global min_hand
    min_hand = min_hnd
    return ((turn_counter, turn_type_counter, turn_odds, turn_prob), (river_counter, river_type_counter, river_odds, river_prob), (better_hand_array, better_hand_list))

# better hands will be called from calculate_turn and calculate_flop
def better_hands(h, b, hand_int):
	hand_type_counter = [0] * 9
	hand_list = [""] * 9

	br = [x%13 for x in b]
	bs = [x/13 for x in b]
	hr = [x%13 for x in h]
	hs = [x/13 for x in h]

	brc = value_count(b)
	bsc = suit_count(b)
	hrc = value_count(h)
	hsc = suit_count(h)

	#combos = []
	#combinations(h, combos)

	#hand_int = hand_evaluation(combos, b[:3], b[3], b[4])
	#print
	#print hand_int, hand_type[hand_int]
	#print

	possible_flush = False
	# suit, number
	flush_suit = (-1, 0)

	#print "board", [rank_dict[x%13]+suit_dict[x/13] for x in b]
	#print "hand", [rank_dict[x%13]+suit_dict[x/13] for x in h]
	#print

	### Note: this algorithm may not exclude hands that are not possible based
	### on the cards you're holding in your hand.  The straight flush calculation
	### has been corrected for this.
	if 8 >= hand_int:
		#print "** Straight Flush **"
		
		# determine if there are 3 of the same suit
		for i in range(len(bsc)):
			if bsc[i] >= 3:
				possible_flush = True
				flush_suit = (i, bsc[i])
				break

		if possible_flush:
			# create an array of the flush cards
			flush_ranks = []
			for i in range(len(b)):
				if bs[i] == flush_suit[0]:
					flush_ranks.append(br[i])

			# hand ranks of flush suit cards
			hand_flush_ranks = []
			for i in range(len(h)):
				if hs[i] == flush_suit[0]:
					hand_flush_ranks.append(hr[i])
			#print [rank_dict[x] for x in hand_flush_ranks]

			# determine if flush cards can make a straight
			all = range(13)
			for i in range(13):
				try:
					index = flush_ranks.index(i)
				except ValueError, status:
					index = -1
				if index == -1:
					all[i] = -1

			all.reverse()
			
			if all[0] == 12:
				all = all + [12]

			for i in range(len(all)-4):
				temp_h = all[i:i+5]
				num = temp_h.count(-1)
				high = -1
				if i == 0:
					if num <= 2:
						high = 12
				else:
					if num < 2 or (num == 2 and (all[i+4] == -1 or all[i-1] == -1)):
						high = 12 - i

				if high != -1:
					# find holes
					others = temp_h[:]
					
					gap_cards = []
					count = temp_h.count(-1)
					for j in range(count):
						index = temp_h.index(-1)
						value = 12 - i - index
						temp_h[index] = value
						gap_cards.append(value)
					for k in range(others.count(-1)):
						others.pop(others.index(-1))
					if count == 2:
						# you have a straight flush if you have both cards, however if you have one of the two,
						# you prevent someone else from having it.
						hand_sf_card_count = hand_flush_ranks.count(gap_cards[0]) + hand_flush_ranks.count(gap_cards[1])
						if hand_int == 8 and hand_sf_card_count == 2:
							break
						elif hand_int == 8 and hand_sf_card_count == 1:
							continue
						else:
							hand_type_counter[8] = hand_type_counter[8] + 1
							#print "a %s-high straight flush is possible if you hold %s of %s" % (rank_dict[high], [rank_dict[x] for x in gap_cards], suit_names[flush_suit[0]])
							#print "%i. %s-high straight flush" % (hand_type_counter[8], rank_dict[high])
							hand_list[8] = hand_list[8] + "%i. %s-high straight flush\n" % (hand_type_counter[8], rank_dict[high])
					else:
						dummy_variable = 1
						#print "ERROR"
		else:
			dummy_variable = 1
			#print ""
		
	if 7 >= hand_int:
		#print "** Four of a kind **"

		hand = br[:]
		hand.sort()

		# assume hand is already sorted
		gaps = []
		for i in range(len(hand)-1):
			reduced = hand[i+1] - ( hand[i] + 1 )
			gaps.append(reduced)

		multiples = []
		if gaps.count(-1) > 0:
			# a four-of-a-kind is possible (unless all four are on the board)
			for i in range(len(gaps)):
				if gaps[i] == -1:
					multiples.append(hand[i])
			multiples.reverse()

			last = -1
			for i in multiples:
				if i != last:
					num = hand.count(i)
					if num == 2:
						if hand_int == 7 and hr.count(i) == 2:
							break
						elif hr.count(i) == 1:
							continue
						else:
							hand_type_counter[7] = hand_type_counter[7] + 1
							#print "if you have two %s's you have four of a kind" % rank_dict[i]
							#print "%i. four %s's" % (hand_type_counter[7], rank_dict[i])
							hand_list[7] = hand_list[7] + "%i. four %s's\n" % (hand_type_counter[7], rank_dict[i])
					if num == 3:
						if hand_int == 7 and hr.count(i) == 1:
							break
						else:
							hand_type_counter[7] = hand_type_counter[7] + 1
							#print "if you have one %s you have a four of a kind" % rank_dict[i]
							#print "%i. four %s's" % (hand_type_counter[7], rank_dict[i])
							hand_list[7] = hand_list[7] + "%i. four %s's\n" % (hand_type_counter[7], rank_dict[i])
					if num == 4:
						dummy_variable = 1
						#print ""
				last = i
		else:
			dummy_variable = 1
			#print ""

	if 6 >= hand_int:
		#print "** Full House **"
		# to have a full house you MUST use a pair on the board
		have_pair = 13 - brc.count(0) - brc.count(1)
		if have_pair > 0:
			loop_list = []
			bpairs = []
			more = (-1, -1)
			# three and four (more) are an integer since you can only have one of them on the board
			for i in range(len(brc)):
				if brc[i] >= 2:
					bpairs.append(i)
				if brc[i] >= 3:
					more = (brc[i], i)
				if brc[i] > 0:
					loop_list.append((i, brc[i]))

			loop_list.reverse()
			max_board_pair = max(bpairs)

			for index, number in loop_list:
				if number == 1:
					# this may fail when have 3-of-a-kind on the board
					if more[1] == -1:
						if hand_int == 6 and hr.count(index) > 1:
							break
						else:
							hand_type_counter[6] = hand_type_counter[6] + 1
							#print "a full house, %s's over %s's if you have pocket %s's" % (rank_dict[index], rank_dict[max_board_pair], rank_dict[index])
							#print "%i. %s's over %s's" % (hand_type_counter[6], rank_dict[index], rank_dict[max_board_pair])
							hand_list[6] = hand_list[6] + "%i. %s's over %s's\n" % (hand_type_counter[6], rank_dict[index], rank_dict[max_board_pair])
				break_flag = 0
				if number == 2:
					new_list = loop_list[:]
					# remove the pair from the list
					new_list.pop(new_list.index((index, number)))
					# loop over remaining cards
					for x, y in new_list:
						if y == 1:
							if hand_int == 6 and hr.count(index) > 0 and hr.count(x) > 0:
								break_flag = 1
								break
							else:						
								hand_type_counter[6] = hand_type_counter[6] + 1
								#print "a full house, %s's over %s's if you have %s & %s" % (rank_dict[index], rank_dict[x], rank_dict[index], rank_dict[x])
								#print "%i. %s's over %s's" % (hand_type_counter[6], rank_dict[index], rank_dict[x])
								hand_list[6] = hand_list[6] + "%i. %s's over %s's\n" % (hand_type_counter[6], rank_dict[index], rank_dict[x])
						# TEST THIS CASE
						if y == 2:
							if index > x:
								if hand_int == 6 and hr.count(index) > 0 and hr.count(x) > 0:
									break_flag = 1
									break
								else:						
									hand_type_counter[6] = hand_type_counter[6] + 1
									#print "a full house, %s's over %s's if you have %s & %s" % (rank_dict[index], rank_dict[x], rank_dict[index], rank_dict[x])
									#print "%i. %s's over %s's" % (hand_type_counter[6], rank_dict[index], rank_dict[x])
									hand_list[6] = hand_list[6] + "%i. %s's over %s's\n" % (hand_type_counter[6], rank_dict[index], rank_dict[x])
							if index < x:
								if hand_int == 6 and hr.count(index) > 0 and hr.count(x) > 0:
									break_flag = 1
									break
								else:						
									hand_type_counter[6] = hand_type_counter[6] + 1
									#print "a full house, %s's over %s's if you have %s & %s" % (rank_dict[x], rank_dict[index], rank_dict[x], rank_dict[index])
									#print "%i. %s's over %s's" % (hand_type_counter[6], rank_dict[x], rank_dict[index])
									hand_list[6] = hand_list[6] + "%i. %s's over %s's\n" % (hand_type_counter[6], rank_dict[x], rank_dict[index])
					if break_flag == 1:
						break
				if number == 3:
					brc_reversed = brc[:]
					brc_reversed.reverse()

					for i in range(len(brc_reversed)):
						#print i, brc_reversed[i], 12-i
						actual_rank = 12 - i
						if brc_reversed[i] == 0:
							if hand_int == 6 and hr.count(actual_rank) > 1:
								break_flag = 1
								break
							else:
								hand_type_counter[6] = hand_type_counter[6] + 1
								#print "a full house, %s's over %s's if you have pocket %s's" % (rank_dict[index], rank_dict[actual_rank], rank_dict[actual_rank])
								#print "%i. %s's over %s's" % (hand_type_counter[6], rank_dict[index], rank_dict[actual_rank])
								hand_list[6] = hand_list[6] + "%i. %s's over %s's\n" % (hand_type_counter[6], rank_dict[index], rank_dict[actual_rank])
						if brc_reversed[i] == 1:
							if index > actual_rank: 
								if hand_int == 6 and hr.count(actual_rank) > 1:
									break_flag = 1
									break
								else:
									hand_type_counter[6] = hand_type_counter[6] + 1
									#print "a full house, %s's over %s's if you have pocket %s's" % (rank_dict[index], rank_dict[actual_rank], rank_dict[actual_rank])
									#print "%i. %s's over %s's" % (hand_type_counter[6], rank_dict[index], rank_dict[actual_rank])
									hand_list[6] = hand_list[6] + "%i. %s's over %s's\n" % (hand_type_counter[6], rank_dict[index], rank_dict[actual_rank])
							if index < actual_rank:
								if hand_int == 6 and hr.count(actual_rank) > 1:
									break_flag = 1
									break
								else:
									hand_type_counter[6] = hand_type_counter[6] + 1
									#print "a full house, %s's over %s's if you have pocket %s's" % (rank_dict[actual_rank], rank_dict[index], rank_dict[actual_rank])
									#print "%i. %s's over %s's" % (hand_type_counter[6], rank_dict[actual_rank], rank_dict[index])
									hand_list[6] = hand_list[6] + "%i. %s's over %s's\n" % (hand_type_counter[6], rank_dict[actual_rank], rank_dict[index])
					if break_flag == 1:
						break
		else:
			dummy_variable = 1
			#print ""

	if 5 >= hand_int:
		#print "** Flush **"

		suit_cards = []
		for i in range(len(bsc)):
			if bsc[i] >= 3:
				suit = i
				for j in range(len(bs)):
					if bs[j] == suit:
						suit_cards.append(br[j])
				break
		if len(suit_cards) >= 3:
			high_cards = range(13)[max(suit_cards):]
			high_cards.reverse()

			hand_suit_cards = []
			for j in range(len(hs)):
				if hs[j] == suit:
					hand_suit_cards.append(hr[j])

			for i in range(len(high_cards)):
				if i != len(high_cards) - 1:
					if hand_int == 5 and hand_suit_cards.count(high_cards[i]) and len(hand_suit_cards) > 1:
						break
					else:
						hand_type_counter[5] = hand_type_counter[5] + 1
						#print "a %s-high flush is possible if you hold %s%s and another %s" % (rank_dict[high_cards[i]], rank_dict[high_cards[i]], suit_dict[suit], suit_names[suit][:-1])
						#print "%i. %s-high flush" % (hand_type_counter[5], rank_dict[high_cards[i]])
						hand_list[5] = hand_list[5] + "%i. %s-high flush\n" % (hand_type_counter[5], rank_dict[high_cards[i]])
				if i == len(high_cards) - 1:
					if hand_int == 5 and len(hand_suit_cards) > 1:
						break
					else:
						hand_type_counter[5] = hand_type_counter[5] + 1
						#print "a %s-high flush is possible if you hold two %s below %s%s" % (rank_dict[high_cards[i]], suit_names[suit], rank_dict[high_cards[i]], suit_dict[suit])
						#print "%i. %s-high flush" % (hand_type_counter[5], rank_dict[high_cards[i]])
						hand_list[5] = hand_list[5] + "%i. %s-high flush\n" % (hand_type_counter[5], rank_dict[high_cards[i]])
		else:
			dummy_variable = 1
			#print ""

	if 4 >= hand_int:
		#print "** Straight **"
		all = range(13)
		for i in range(13):
			try:
				index = br.index(i)
			except ValueError, status:
				index = -1
			if index == -1:
				all[i] = -1

		all.reverse()


		if all[0] == 12:
			all = all + [12]

		for i in range(len(all)-4):
			h = all[i:i+5]
			num = h.count(-1)
			high = -1
			if i == 0:
				if num <= 2:
					high = 12
			else:
				if num < 2 or (num == 2 and (all[i+4] == -1 or all[i-1] == -1)):
					high = 12 - i

			if high != -1:
				# find holes
				others = h[:]
				gap_cards = []

				count = h.count(-1)
				for j in range(count):
					index = h.index(-1)
					value = 12 - i - index
					h[index] = value
					gap_cards.append(value)

				for k in range(others.count(-1)):
					others.pop(others.index(-1))

				if count == 2:			
					if hand_int == 4 and hr.count(gap_cards[0]) >= 1 and hr.count(gap_cards[1]) >= 1:
						break
					else:
						hand_type_counter[4] = hand_type_counter[4] + 1
						#print "a %s-high straight is possible if you hold %s & %s" % (rank_dict[high], rank_dict[gap_cards[0]], rank_dict[gap_cards[1]])
						#print "%i. %s-high straight" % (hand_type_counter[4], rank_dict[high])
						hand_list[4] = hand_list[4] + "%i. %s-high straight\n" % (hand_type_counter[4], rank_dict[high])
				elif count == 1:
					if hand_int == 4 and hr.count(gap_cards[0]) >= 1:
						num = 0
						for x in others:
							if hr.count(x) > 0:
								num = num + 1
						if num > 0:
							break
					else:
						hand_type_counter[4] = hand_type_counter[4] + 1
						#print "a %s-high straight is possible if you hold %s and one of the following %s" % (rank_dict[high], rank_dict[gap_cards[0]], [rank_dict[x] for x in others])
						#print "%i. %s-high straight" % (hand_type_counter[4], rank_dict[high])
						hand_list[4] = hand_list[4] + "%i. %s-high straight\n" % (hand_type_counter[4], rank_dict[high])
				elif count == 0:
					if hand_int == 4:
						num = 0
						for x in others:
							if hr.count(x) > 0:
								num = num + 1
						if num > 0:
							break
					else:
						hand_type_counter[4] = hand_type_counter[4] + 1
						#print "a %s-high straight is possible if you hold two of the following %s" % (rank_dict[high], [rank_dict[x] for x in others])
						#print "%i. %s-high straight" % (hand_type_counter[4], rank_dict[high])
						hand_list[4] = hand_list[4] + "%i. %s-high straight\n" % (hand_type_counter[4], rank_dict[high])
				else:
					print "ERROR"

	if 3 >= hand_int:
		#print "** Three of a Kind **"
		loop_list = []
		isboardpair = False

		for i in range(len(brc)):
			if brc[i] > 0:
				loop_list.append((i, brc[i]))
			if brc[i] == 2:
				isboardpair = True

		loop_list.reverse()
		#print loop_list
		for index, number in loop_list:
			if number == 1:
				if hand_int == 3 and hr.count(index) == 2:
					break
				elif isboardpair == True:
					# if there is a board pair, then a pocket pair that matches the board gives you a full house
					continue
				else:
					hand_type_counter[3] = hand_type_counter[3] + 1
					#print "three %s's if you have pocket %s's" % (rank_dict[index], rank_dict[index])
					#print "A %i. three %s's" % (hand_type_counter [3], rank_dict[index])
					hand_list[3] = hand_list[3] + "%i. three %s's\n" % (hand_type_counter [3], rank_dict[index])
			if number == 2:
				if hand_int == 3 and hr.count(index) == 1:
					break
				else:
					hand_type_counter[3] = hand_type_counter[3] + 1
					#print "three %s's if you have one %s" % (rank_dict[index], rank_dict[index])
					#print "B %i. three %s's" % (hand_type_counter [3], rank_dict[index])
					hand_list[3] = hand_list[3] + "%i. three %s's\n" % (hand_type_counter [3], rank_dict[index])
			if number == 3:
				if hand_int == 3:
					break
				else:
					hand_type_counter[3] = hand_type_counter[3] + 1
					#print "three %s's are on the board" % rank_dict[index]
					#print "C %i. three %s's" % (hand_type_counter [3], rank_dict[index])
					hand_list[3] = hand_list[3] + "%i. three %s's\n" % (hand_type_counter [3], rank_dict[index])

	if 2 >= hand_int:
		#print "** Two Pair **"
		isboardpair = False
		brc_reversed = brc[:]
		brc_reversed.reverse()

		board_ranks = br[:]
		board_ranks.sort()
		board_ranks.reverse()

		## make sure this is used everywhere it is needed.
		# need a flag because for loops are too complicated to use simple breaks.
		break_flag = 0

		# is there a pair on the board?
		if brc.count(2) > 0:
			isboardpair = True
			# this doesn't get the highest pair
			boardpairindex = 12 - brc_reversed.index(2)
		if isboardpair == False:
			# if there isn't a board pair, then you must have two cards that match the board
			for i in range(len(board_ranks)):
				for j in range(len(board_ranks[i+1:])):
					if break_flag == 0:
						if hand_int == 2 and hr.count(board_ranks[i]) == 1 and hr.count(board_ranks[i+1:][j]) == 1:
							break_flag = 1
							break
						else:
							hand_type_counter[2] = hand_type_counter[2] + 1
							#print "Two pair, %s's and %s's if you have %s %s" % (rank_dict[board_ranks[i]], rank_dict[board_ranks[i+1:][j]], rank_dict[board_ranks[i]], rank_dict[board_ranks[i+1:][j]])
							#print "%i. %s's and %s's" % (hand_type_counter[2], rank_dict[board_ranks[i]], rank_dict[board_ranks[i+1:][j]])
							hand_list[2] = hand_list[2] + "%i. %s's and %s's\n" % (hand_type_counter[2], rank_dict[board_ranks[i]], rank_dict[board_ranks[i+1:][j]])
					else:
						break
		else:
			for i in range(len(brc_reversed)):
				real_index = 12 - i
				if brc_reversed[i] == 0:
					# could consolidate the following tree into three branches rather than four
					if real_index > boardpairindex:
						if hand_int == 2 and hr.count(real_index) == 2:
							break
						else:
							hand_type_counter[2] = hand_type_counter[2] + 1
							#print "two pair, %s's and %s's if you have pocket %s's" % (rank_dict[real_index], rank_dict[boardpairindex], rank_dict[real_index])
							#print "%i. %s's and %s's" % (hand_type_counter[2], rank_dict[real_index], rank_dict[boardpairindex])
							hand_list[2] = hand_list[2] + "%i. %s's and %s's\n" % (hand_type_counter[2], rank_dict[real_index], rank_dict[boardpairindex])
					elif real_index < boardpairindex:
						if hand_int == 2 and hr.count(real_index) == 2:
							break
						else:
							hand_type_counter[2] = hand_type_counter[2] + 1
							#print "two pair, %s's and %s's if you have pocket %s's" % (rank_dict[boardpairindex], rank_dict[real_index], rank_dict[real_index])
							#print "%i. %s's and %s's" % (hand_type_counter[2], rank_dict[boardpairindex], rank_dict[real_index])
							hand_list[2] = hand_list[2] + "%i. %s's and %s's\n" % (hand_type_counter[2], rank_dict[boardpairindex], rank_dict[real_index])
				if brc_reversed[i] == 1:
					### only care about lower board cards because higher ones have already been counted
					### two board pairs don't matter for omaha since you can only use 3 board cards
					if real_index > boardpairindex:
						lower_board_cards = board_ranks[board_ranks.index(12-i)+1:]
						for j in range(len(lower_board_cards)):
							# could consolidate the following tree into three branches rather than four
							if lower_board_cards[j] > boardpairindex:
								if hand_int == 2 and hr.count(real_index) == 1 and hr.count(lower_board_cards[j]):
									break
								else:
									hand_type_counter[2] = hand_type_counter[2] + 1
									#print "two pair, %s's and %s's if you hold %s %s" % (rank_dict[real_index], rank_dict[lower_board_cards[j]], rank_dict[real_index], rank_dict[lower_board_cards[j]])
									#print "%i. %s's and %s's" % (hand_type_counter[2], rank_dict[real_index], rank_dict[lower_board_cards[j]])
									hand_list[2] = hand_list[2] + "%i. %s's and %s's\n" % (hand_type_counter[2], rank_dict[real_index], rank_dict[lower_board_cards[j]])
							else:
								if hand_int == 2 and hr.count(real_index) == 1 and hr.count(lower_board_cards[j]):
									break
								else:
									hand_type_counter[2] = hand_type_counter[2] + 1
									#print "two pair, %s's and %s's if you hold one %s" % (rank_dict[real_index], rank_dict[boardpairindex], rank_dict[real_index])
									#print "%i. %s's and %s's" % (hand_type_counter[2], rank_dict[real_index], rank_dict[boardpairindex])
									hand_list[2] = hand_list[2] + "%i. %s's and %s's\n" % (hand_type_counter[2], rank_dict[real_index], rank_dict[boardpairindex])
					elif real_index < boardpairindex:
						if hand_int == 2 and hr.count(real_index) == 1:
							break
						else:
							hand_type_counter[2] = hand_type_counter[2] + 1
							#print "two pair, %s's and %s's if you hold one %s" % (rank_dict[boardpairindex], rank_dict[real_index], rank_dict[real_index])
							#print "%i. %s's and %s's" % (hand_type_counter[2], rank_dict[boardpairindex], rank_dict[real_index])
							hand_list[2] = hand_list[2] + "%i. %s's and %s's\n" % (hand_type_counter[2], rank_dict[boardpairindex], rank_dict[real_index])

	if 1 >= hand_int:
		#print "** One Pair **"
		pair_on_board = brc.count(2)
		brc_reversed = brc[:]
		brc_reversed.reverse()

		for i in range(len(brc_reversed)):
			index = 12 - i
			if brc_reversed[i] == 0:
				# if you have a pair and it matches the current one, then you're done.
				if hand_int == 1 and hr.count(index) >= 2:
					break
				else:
					# if not then current hand is better than yours, continue.
					hand_type_counter[1] = hand_type_counter[1] + 1
					#print "pair of %s's if you have pocket %s's" % (rank_dict[index], rank_dict[index])
					#print "%i. pair of %s's" % (hand_type_counter[1], rank_dict[index])
					hand_list[1] = hand_list[1] + "%i. pair of %s's\n" % (hand_type_counter[1], rank_dict[index])
			if brc_reversed[i] == 1:
				if hand_int == 1 and hr.count(index) == 1:
					break
				else:
					hand_type_counter[1] = hand_type_counter[1] + 1
					#print "pair of %s's if you have one %s" % (rank_dict[index], rank_dict[index])
					#print "%i. pair of %s's" % (hand_type_counter[1], rank_dict[index])
					hand_list[1] = hand_list[1] + "%i. pair of %s's\n" % (hand_type_counter[1], rank_dict[index])
			if brc_reversed[i] == 2:
				# if you have a pair, then the board pair is your hand (therefore not higher)
				if hand_int == 1:
					break
				else:
					hand_type_counter[1] = hand_type_counter[1] + 1
					#print "pair of %s's is on the board" % rank_dict[index]
					#print "%i. pair of %s's" % (hand_type_counter[1], rank_dict[index])
					hand_list[1] = hand_list[1] + "%i. pair of %s's\n" % (hand_type_counter[1], rank_dict[index])
					break
					# should i break after the board pair?
					# it's not possible to have a single pair lower than the board pair
					# if you do, then you have two pair.

	if 0 >= hand_int:
		#print "** High Card **"
		high_board_card = max(br)
		possible_high_cards = range(13)[high_board_card:]
		possible_high_cards.reverse()

		for i in range(len(possible_high_cards)):
			if i != len(possible_high_cards) - 1:
				if hand_int == 0 and max(hr) == possible_high_cards[i]:
					break
				else:
					hand_type_counter[0] = hand_type_counter[0] + 1
					#print "%s high if you have one %s" % (rank_dict[possible_high_cards[i]], rank_dict[possible_high_cards[i]])
					#print "%i. %s high" % (hand_type_counter[0], rank_dict[possible_high_cards[i]])
					hand_list[0] = hand_list[0] + "%i. %s high\n" % (hand_type_counter[0], rank_dict[possible_high_cards[i]])
			else:
				if hand_int == 0 and max(hr) == possible_high_cards[i]:
					break
				else:
					# since this is the worst hand, you should never be able to have a hand below it.  Delete everything below.
					hand_type_counter[0] = hand_type_counter[0] + 1
					#print "%s high if you have all lower cards" % rank_dict[possible_high_cards[i]]
					#print "%i. %s high" % (hand_type_counter[0], rank_dict[possible_high_cards[i]])
					hand_list[0] = hand_list[0] + "%i. %s high\n" % (hand_type_counter[0], rank_dict[possible_high_cards[i]])

	#print hand_list
	return (hand_type_counter, hand_list)

def hutchison(hole):
    suit_awards = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 2.0, 2.5, 3.0, 4.0)
    pair_awards = (4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 5.0, 6.0, 6.0, 7.0, 8.0, 9.0)
    points = 0.0
    # hand needs to be sorted for first to work
    hole.sort()

    # FIRST
    ranks = [ x%13 for x in hole ]
    suits = [ x/13 for x in hole ]
    suits_reversed = suits[:]
    suits_reversed.reverse()
    total = 0
    for i in range(4):
        count = suits.count(i)
        if count > 1:
            reverse_index = suits_reversed.index(i)
            actual_index = 3 - reverse_index
            # find the rank of the highest suited card
            high = ranks[actual_index]
            points = points + suit_awards[high]
        if count == 4:
            points = points - 2.0
        total = total + count
        if total == 4:
            break

    # SECOND
    ranks_sorted = ranks[:]
    ranks_sorted.sort()
    gaps = []
    for i in range(3):
        reduced = ranks_sorted[i+1] - ( ranks_sorted[i] + 1 )
        gaps.append(reduced)
    # [-1, -1, -1] four of a kind
    # [-1, -1, x] or [x, -1, -1] three of a kind
    # [-1, x, -1] two pair
    num_pairs = gaps.count(-1)
    if ( num_pairs == 1 ) or ( num_pairs == 2 and gaps[1] != -1 ):
        for i in range(3):
            if gaps[i] == -1:
                pair = ranks_sorted[i]
                #print "pair", pair
                points = points + pair_awards[pair]

    # THIRD
    # make a can-make-straight array for easier evaluation
    can_make_straight = [0] * 3
    for i in range(len(gaps)):
        # for calculation purposes, if couples straddling 6 don't count as a straight
        if gaps[i] != -1 and gaps[i] < 4 and (ranks_sorted[i] >= 4 or ranks_sorted[i+1] <= 4):
            can_make_straight[i] = 1
    # email hutchison and get definitive answer on this
    count = can_make_straight.count(1)
    deduction = (0.0, 1.0, 1.0, 2.0)
    penalty = 0.0
    # 4 cards six and above
    if count == 3 and ranks_sorted[0] > 3:
        points = points + 12.0
    # 3 cards six and above
    elif count == 2 and ranks_sorted[1] > 3 and can_make_straight[0] == 0:
        points = points + 7.0
    else:
        # this is where it gets sketchy
        for i in range(len(can_make_straight)):
            if can_make_straight[i] == 1:
                # Any two cards SIX through KING
                if ranks_sorted[i] > 3 and ranks_sorted[i+1] < 12:
                    points = points + 4.0
                # Any two cards TWO through SIX
                if ranks_sorted[i+1] < 5:
                    points = points + 2.0
                # An ACE with a King, Queen, Jack or Ten
                if ranks_sorted[i] > 7 and ranks_sorted[i+1] == 12:
                    points = points + 2.0
        # An ACE with a Two, Three, Four, or Five
        if ranks_sorted[3] == 12:
            for i in range(3):
                if ranks_sorted[i] < 4:
                    penalty = deduction[ranks_sorted[i]]
                    points = points + 1.0

    # for gap of A-5 straight
    points = points - penalty
    # subtract for size of other gaps
    if can_make_straight.count(1) > 0 and gaps.count(3) > 0 and penalty != 2.0:
        points = points - 2.0
    if can_make_straight.count(1) > 0 and ( gaps.count(2) > 0 or gaps.count(1) > 0 ) and penalty != 1.0:
        points = points - 1.0
    return points

def display_output_flop(results):
    print ""
    print "%s %s %s %s | %s %s %s - %s" % (sys.argv[1][0:2], sys.argv[1][2:4], sys.argv[1][4:6], sys.argv[1][6:8], sys.argv[2][0:2], sys.argv[2][2:4], sys.argv[2][4:6], hand_type[min_hand])

    print ""
    print "TURN"
    print ""
    print "Hand\t\tout of %d\tOdds 1:\t\tProbability\t# better" % results[0][0]
    temp = range(9)
    temp.reverse()
    for i in temp:
        print "%s\t%d\t\t%.2f\t\t%.2f\t\t%i" % (hand_type[i], results[0][1][i], results[0][2][i], results[0][3][i], results[2][0][i])
    print ""
    print "RIVER"
    print ""
    print "Hand\t\tout of %d\tOdds 1:\t\tProbability\t# better" % results[1][0]
    temp = range(9)
    temp.reverse()
    for i in temp:
        print "%s\t%d\t\t%.2f\t\t%.2f\t\t%i" % (hand_type[i], results[1][1][i], results[1][2][i], results[1][3][i], results[2][0][i])
    print ""

def display_output_turn(results):
    print ""
    print "%s %s %s %s | %s %s %s | %s - %s" % (sys.argv[1][0:2], sys.argv[1][2:4], sys.argv[1][4:6], sys.argv[1][6:8], sys.argv[2][0:2], sys.argv[2][2:4], sys.argv[2][4:6], sys.argv[3], hand_type[min_hand])

    print ""
    print "RIVER"
    print ""
    print "Hand\t\tout of %d\tOdds 1:\t\tProbability\t# better" % results[0][0]
    temp = range(9)
    temp.reverse()
    for i in temp:
        print "%s\t%d\t\t%.2f\t\t%.2f\t\t%i" % (hand_type[i], results[0][1][i], results[0][2][i], results[0][3][i], results[1][0][i])
    print ""

def display_output_river(results):
    print ""
    print "%s %s %s %s | %s %s %s | %s | %s - %s" % (sys.argv[1][0:2], sys.argv[1][2:4], sys.argv[1][4:6], sys.argv[1][6:8], sys.argv[2][0:2], sys.argv[2][2:4], sys.argv[2][4:6], sys.argv[3], sys.argv[4], hand_type[min_hand])

    print ""
    print "SHOWDOWN"
    print ""
    print "Hand\t\tout of %d\tOdds 1:\t\tProbability\t# better" % results[0][0]
    temp = range(9)
    temp.reverse()
    for i in temp:
        print "%s\t%d\t\t%.2f\t\t%.2f\t\t%i" % (hand_type[i], results[0][1][i], results[0][2][i], results[0][3][i], results[1][0][i])
    print ""

def main(hole_string, flop_string, turn_string, river_string):
    hole = []
    hand2array(hole_string,hole)
    if flop_string == "":
        print "hutchison index =", hutchison(hole)
    elif turn_string == "":
        flop = []
        hand2array(flop_string,flop)
        results = calculate_flop(hole, flop)
        #print results
        display_output_flop(results)
    elif river_string == "":
        flop = []
        turn = []
        hand2array(flop_string, flop)
        hand2array(turn_string,turn)
        board = flop + turn
        #print "turn_string", turn_string
        #print "turn", turn
        results = calculate_turn(hole, board)
        #print results
        display_output_turn(results)
    else:
        # do river stuff here
        flop = []
        turn = []
        river = []
        hand2array(flop_string, flop)
        hand2array(turn_string, turn)
        hand2array(river_string, river)
        board = flop + turn + river
        print board
        results = calculate_river(hole, board)
        display_output_river(results)
    return 0

# This is what actually runs
if __name__=='__main__':
    #import psyco
    #psyco.full()

    length = len(sys.argv)
    if length == 2:
        main(sys.argv[1], "", "", "")
    elif length == 3:
        main(sys.argv[1], sys.argv[2], "", "")
    elif length == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3], "")
    elif length == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:  
        print "Usage: calc.py <hole_cards> <flop> <turn> <river>"

