from src.base_element.MoveType import CMoveType, MIN_SINGLE_CARDS, MIN_PAIRS, MIN_TRIPLES, select
import collections
import itertools


class CGenerate(object):
    """
    This is for generating the possible combinations
    """
    def __init__(self, cards_list):
        self.cards_list = cards_list
        self.cards_dict = collections.defaultdict(int)

        for i in self.cards_list:
            self.cards_dict[i] += 1

        self.cached_single_card_moves = self.gen_type_1_single()
        self.cached_pair_moves = self.gen_type_2_pair()
        self.cached_triple_moves = self.gen_type_3_triple()

    def _gen_serial_moves(self, cards, min_serial, repeat=1, repeat_num=0):
        if repeat_num < min_serial:  # at least repeat_num is min_serial
            repeat_num = 0

        single_cards = sorted(list(set(cards)))
        seq_records = list()
        moves = list()

        start = i = 0
        longest = 1
        while i < len(single_cards):
            if i + 1 < len(single_cards) and single_cards[i + 1] - single_cards[i] == 1:
                longest += 1
                i += 1
            else:
                seq_records.append((start, longest))
                i += 1
                start = i
                longest = 1

        for seq in seq_records:
            if seq[1] < min_serial:
                continue
            start, longest = seq[0], seq[1]
            longest_list = single_cards[start: start + longest]

            if repeat_num == 0:  # No limitation on how many sequences
                steps = min_serial
                while steps <= longest:
                    index = 0
                    while steps + index <= longest:
                        target_moves = sorted(longest_list[index: index + steps] * repeat)
                        moves.append(target_moves)
                        index += 1
                    steps += 1

            else:  # repeat_num > 0
                if longest < repeat_num:
                    continue
                index = 0
                while index + repeat_num <= longest:
                    target_moves = sorted(longest_list[index: index + repeat_num] * repeat)
                    moves.append(target_moves)
                    index += 1

        return moves

    def gen_type_1_single(self):
        single_card_moves = []
        for i in set(self.cards_list):
            single_card_moves.append([i])
        return single_card_moves

    def gen_type_2_pair(self):
        pair_moves = []
        for k, v in self.cards_dict.items():
            if v >= 2:
                pair_moves.append([k, k])
        return pair_moves

    def gen_type_3_triple(self):
        triple_cards_moves = []
        for k, v in self.cards_dict.items():
            if v >= 3:
                triple_cards_moves.append([k, k, k])
        return triple_cards_moves

    def gen_type_4_bomb(self):
        bomb_moves = []
        for k, v in self.cards_dict.items():
            if v == 4:
                bomb_moves.append([k, k, k, k])
        return bomb_moves

    def gen_type_5_king_bomb(self):
        final_bomb_moves = []
        if 20 in self.cards_list and 30 in self.cards_list:
            final_bomb_moves.append([20, 30])
        return final_bomb_moves

    def gen_type_6_3_1(self):
        result = []
        for t in self.cached_single_card_moves:
            for i in self.cached_triple_moves:
                if t[0] != i[0]:
                    result.append(t+i)
        return result

    def gen_type_7_3_2(self):
        result = list()
        for t in self.cached_pair_moves:
            for i in self.cached_triple_moves:
                if t[0] != i[0]:
                    result.append(t+i)
        return result

    def gen_type_8_serial_single(self, repeat_num=0):
        return self._gen_serial_moves(self.cards_list, MIN_SINGLE_CARDS, repeat=1, repeat_num=repeat_num)

    def gen_type_9_serial_pair(self, repeat_num=0):
        single_pairs = list()
        for k, v in self.cards_dict.items():
            if v >= 2:
                single_pairs.append(k)

        return self._gen_serial_moves(single_pairs, MIN_PAIRS, repeat=2, repeat_num=repeat_num)

    def gen_type_10_serial_triple(self, repeat_num=0):
        single_triples = list()
        for k, v in self.cards_dict.items():
            if v >= 3:
                single_triples.append(k)

        return self._gen_serial_moves(single_triples, MIN_TRIPLES, repeat=3, repeat_num=repeat_num)

    def gen_type_11_serial_3_1(self, repeat_num=0):
        serial_3_moves = self.gen_type_10_serial_triple(repeat_num=repeat_num)
        serial_3_1_moves = list()

        for s3 in serial_3_moves:  # s3 is like [3,3,3,4,4,4]
            s3_set = set(s3)
            new_cards = [i for i in self.cards_list if i not in s3_set]

            # Get any s3_len items from cards
            subcards = select(new_cards, len(s3_set))

            for i in subcards:
                serial_3_1_moves.append(s3 + i)

        return list(k for k, _ in itertools.groupby(serial_3_1_moves))

    def gen_type_12_serial_3_2(self, repeat_num=0):
        serial_3_moves = self.gen_type_10_serial_triple(repeat_num=repeat_num)
        serial_3_2_moves = list()
        pair_set = sorted([k for k, v in self.cards_dict.items() if v >= 2])

        for s3 in serial_3_moves:
            s3_set = set(s3)
            pair_candidates = [i for i in pair_set if i not in s3_set]

            # Get any s3_len items from cards
            subcards = select(pair_candidates, len(s3_set))
            for i in subcards:
                serial_3_2_moves.append(sorted(s3 + i * 2))

        return serial_3_2_moves

    def gen_type_13_4_2(self):
        four_cards = list()
        for k, v in self.cards_dict.items():
            if v == 4:
                four_cards.append(k)

        result = list()
        for fc in four_cards:
            cards_list = [k for k in self.cards_list if k != fc]
            subcards = select(cards_list, 2)
            for i in subcards:
                result.append([fc]*4 + i)
        return list(k for k, _ in itertools.groupby(result))

    def gen_type_14_4_22(self):
        four_cards = list()
        for k, v in self.cards_dict.items():
            if v == 4:
                four_cards.append(k)

        result = list()
        for fc in four_cards:
            cards_list = [k for k, v in self.cards_dict.items() if k != fc and v>=2]
            subcards = select(cards_list, 2)
            for i in subcards:
                result.append([fc] * 4 + [i[0], i[0], i[1], i[1]])
        return result

    # generate all possible moves from given cards
    def gen_moves(self):
        moves = []
        moves.extend(self.gen_type_1_single())
        moves.extend(self.gen_type_2_pair())
        moves.extend(self.gen_type_3_triple())
        moves.extend(self.gen_type_4_bomb())
        moves.extend(self.gen_type_5_king_bomb())
        moves.extend(self.gen_type_6_3_1())
        moves.extend(self.gen_type_7_3_2())
        moves.extend(self.gen_type_8_serial_single())
        moves.extend(self.gen_type_9_serial_pair())
        moves.extend(self.gen_type_10_serial_triple())
        moves.extend(self.gen_type_11_serial_3_1())
        moves.extend(self.gen_type_12_serial_3_2())
        moves.extend(self.gen_type_13_4_2())
        moves.extend(self.gen_type_14_4_22())
        return moves


def gen_moves_by_hand_cards_and_trival(hand_cards, rival_cards):
    generate = CGenerate(cards_list=hand_cards)
    rival_move = rival_cards

    rival_move_type = get_move_type(rival_cards)['type']
    rival_move_len = get_move_type(rival_cards).get('len', 1)
    moves = list()

    if rival_move_type == CMoveType.TYPE_0_PASS:
        moves = generate.gen_moves()

    elif rival_move_type == CMoveType.TYPE_1_SINGLE:
        all_moves = generate.gen_type_1_single()
        moves = filter_type_1_single(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_2_PAIR:
        all_moves = generate.gen_type_2_pair()
        moves = filter_type_2_pair(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_3_TRIPLE:
        all_moves = generate.gen_type_3_triple()
        moves = filter_type_3_triple(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_4_BOMB:
        all_moves = generate.gen_type_4_bomb() + generate.gen_type_5_king_bomb()
        moves = filter_type_4_bomb(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_5_KING_BOMB:
        moves = []

    elif rival_move_type == CMoveType.TYPE_6_3_1:
        all_moves = generate.gen_type_6_3_1()
        moves = filter_type_6_3_1(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_7_3_2:
        all_moves = generate.gen_type_7_3_2()
        moves = filter_type_7_3_2(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_8_SERIAL_SINGLE:
        all_moves = generate.gen_type_8_serial_single(repeat_num=rival_move_len)
        moves = filter_type_8_serial_single(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_9_SERIAL_PAIR:
        all_moves = generate.gen_type_9_serial_pair(repeat_num=rival_move_len)
        moves = filter_type_9_serial_pair(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_10_SERIAL_TRIPLE:
        all_moves = generate.gen_type_10_serial_triple(repeat_num=rival_move_len)
        moves = filter_type_10_serial_triple(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_11_SERIAL_3_1:
        all_moves = generate.gen_type_11_serial_3_1(repeat_num=rival_move_len)
        moves = filter_type_11_serial_3_1(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_12_SERIAL_3_2:
        all_moves = generate.gen_type_12_serial_3_2(repeat_num=rival_move_len)
        moves = filter_type_12_serial_3_2(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_13_4_2:
        all_moves = generate.gen_type_13_4_2()
        moves = filter_type_13_4_2(all_moves, rival_move)

    elif rival_move_type == CMoveType.TYPE_14_4_22:
        all_moves = generate.gen_type_14_4_22()
        moves = filter_type_14_4_22(all_moves, rival_move)

    if rival_move_type not in [CMoveType.TYPE_0_PASS,
                                CMoveType.TYPE_4_BOMB, CMoveType.TYPE_5_KING_BOMB]:
        moves = moves + generate.gen_type_4_bomb() + generate.gen_type_5_king_bomb()

    if len(rival_move) != 0:  # rival_move is not 'pass'
        moves = moves + [[]]

    for m in moves:
        m.sort()

    return moves

# check if move is a continuous sequence
def is_continuous_seq(move):
    i = 0
    while i < len(move) - 1:
        if move[i+1] - move[i] != 1:
            return False
        i += 1
    return True

# return the type of the move
def get_move_type(move):
    move_size = len(move)
    move_dict = collections.Counter(move)

    if move_size == 0:
        return {'type': CMoveType.TYPE_0_PASS}

    if move_size == 1:
        return {'type': CMoveType.TYPE_1_SINGLE, 'rank': move[0]}

    if move_size == 2:
        if move[0] == move[1]:
            return {'type': CMoveType.TYPE_2_PAIR, 'rank': move[0]}
        elif move == [20, 30]:  # Kings
            return {'type': CMoveType.TYPE_5_KING_BOMB}
        else:
            return {'type': CMoveType.TYPE_15_WRONG}

    if move_size == 3:
        if len(move_dict) == 1:
            return {'type': CMoveType.TYPE_3_TRIPLE, 'rank': move[0]}
        else:
            return {'type': CMoveType.TYPE_15_WRONG}

    if move_size == 4:
        if len(move_dict) == 1:
            return {'type': CMoveType.TYPE_4_BOMB,  'rank': move[0]}
        elif len(move_dict) == 2:
            if move[0] == move[1] == move[2] or move[1] == move[2] == move[3]:
                return {'type': CMoveType.TYPE_6_3_1, 'rank': move[1]}
            else:
                return {'type': CMoveType.TYPE_15_WRONG}
        else:
            return {'type': CMoveType.TYPE_15_WRONG}

    if is_continuous_seq(move):
        return {'type': CMoveType.TYPE_8_SERIAL_SINGLE, 'rank': move[0], 'len': len(move)}

    if move_size == 5:
        if len(move_dict) == 2:
            return {'type': CMoveType.TYPE_7_3_2, 'rank': move[2]}
        else:
            return {'type': CMoveType.TYPE_15_WRONG}

    count_dict = collections.defaultdict(int)
    for c, n in move_dict.items():
        count_dict[n] += 1

    if move_size == 6:
        if (len(move_dict) == 2 or len(move_dict) == 3) and count_dict.get(4) == 1 and \
                (count_dict.get(2) == 1 or count_dict.get(1) == 2):
            return {'type': CMoveType.TYPE_13_4_2, 'rank': move[2]}

    if move_size == 8 and (((len(move_dict) == 3 or len(move_dict) == 2) and
            (count_dict.get(4) == 1 and count_dict.get(2) == 2)) or count_dict.get(4) == 2):
        return {'type': CMoveType.TYPE_14_4_22, 'rank': max([c for c, n in move_dict.items() if n == 4])}

    mdkeys = sorted(move_dict.keys())
    if len(move_dict) == count_dict.get(2) and is_continuous_seq(mdkeys):
        return {'type': CMoveType.TYPE_9_SERIAL_PAIR, 'rank': mdkeys[0], 'len': len(mdkeys)}

    if len(move_dict) == count_dict.get(3) and is_continuous_seq(mdkeys):
        return {'type': CMoveType.TYPE_10_SERIAL_TRIPLE, 'rank': mdkeys[0], 'len': len(mdkeys)}

    # Check Type 11 (serial 3+1) and Type 12 (serial 3+2)
    if count_dict.get(3, 0) >= MIN_TRIPLES:
        serial_3 = list()
        single = list()
        pair = list()

        for k, v in move_dict.items():
            if v == 3:
                serial_3.append(k)
            elif v == 1:
                single.append(k)
            elif v == 2:
                pair.append(k)
            else:  # no other possibilities
                return {'type': CMoveType.TYPE_15_WRONG}

        serial_3.sort()
        if is_continuous_seq(serial_3):
            if len(serial_3) == len(single)+len(pair)*2:
                return {'type': CMoveType.TYPE_11_SERIAL_3_1, 'rank': serial_3[0], 'len': len(serial_3)}
            if len(serial_3) == len(pair) and len(move_dict) == len(serial_3) * 2:
                return {'type': CMoveType.TYPE_12_SERIAL_3_2, 'rank': serial_3[0], 'len': len(serial_3)}

        if len(serial_3) == 4:
            if is_continuous_seq(serial_3[1:]):
                return {'type': CMoveType.TYPE_11_SERIAL_3_1, 'rank': serial_3[1], 'len': len(serial_3) - 1}
            if is_continuous_seq(serial_3[:-1]):
                return {'type': CMoveType.TYPE_11_SERIAL_3_1, 'rank': serial_3[0], 'len': len(serial_3) - 1}

    return {'type': CMoveType.TYPE_15_WRONG}



def common_handle(moves, rival_move):
    new_moves = list()
    for move in moves:
        if move[0] > rival_move[0]:
            new_moves.append(move)
    return new_moves

def filter_type_1_single(moves, rival_move):
    return common_handle(moves, rival_move)


def filter_type_2_pair(moves, rival_move):
    return common_handle(moves, rival_move)


def filter_type_3_triple(moves, rival_move):
    return common_handle(moves, rival_move)


def filter_type_4_bomb(moves, rival_move):
    return common_handle(moves, rival_move)

# No need to filter for type_5_king_bomb

def filter_type_6_3_1(moves, rival_move):
    rival_move.sort()
    rival_rank = rival_move[1]
    new_moves = list()
    for move in moves:
        move.sort()
        my_rank = move[1]
        if my_rank > rival_rank:
            new_moves.append(move)
    return new_moves

def filter_type_7_3_2(moves, rival_move):
    rival_move.sort()
    rival_rank = rival_move[2]
    new_moves = list()
    for move in moves:
        move.sort()
        my_rank = move[2]
        if my_rank > rival_rank:
            new_moves.append(move)
    return new_moves

def filter_type_8_serial_single(moves, rival_move):
    return common_handle(moves, rival_move)

def filter_type_9_serial_pair(moves, rival_move):
    return common_handle(moves, rival_move)

def filter_type_10_serial_triple(moves, rival_move):
    return common_handle(moves, rival_move)

def filter_type_11_serial_3_1(moves, rival_move):
    rival = collections.Counter(rival_move)
    rival_rank = max([k for k, v in rival.items() if v == 3])
    new_moves = list()
    for move in moves:
        mymove = collections.Counter(move)
        my_rank = max([k for k, v in mymove.items() if v == 3])
        if my_rank > rival_rank:
            new_moves.append(move)
    return new_moves

def filter_type_12_serial_3_2(moves, rival_move):
    rival = collections.Counter(rival_move)
    rival_rank = max([k for k, v in rival.items() if v == 3])
    new_moves = list()
    for move in moves:
        mymove = collections.Counter(move)
        my_rank = max([k for k, v in mymove.items() if v == 3])
        if my_rank > rival_rank:
            new_moves.append(move)
    return new_moves

def filter_type_13_4_2(moves, rival_move):
    rival_move.sort()
    rival_rank = rival_move[2]
    new_moves = list()
    for move in moves:
        move.sort()
        my_rank = move[2]
        if my_rank > rival_rank:
            new_moves.append(move)
    return new_moves

def filter_type_14_4_22(moves, rival_move):
    rival = collections.Counter(rival_move)
    rival_rank = my_rank = 0
    for k, v in rival.items():
        if v == 4:
            rival_rank = k
    new_moves = list()
    for move in moves:
        mymove = collections.Counter(move)
        for k, v in mymove.items():
            if v == 4:
                my_rank = k
        if my_rank > rival_rank:
            new_moves.append(move)
    return new_moves
