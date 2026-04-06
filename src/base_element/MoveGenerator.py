from __future__ import annotations

import collections
import itertools
from typing import Iterable

from base_element.Move import Move
from base_element.MoveFactory import MoveFactory
from utils import MIN_PAIRS, MIN_SINGLE_CARDS, MIN_TRIPLES, select


class MoveGenerator:
    def __init__(self, cards_list: Iterable[int]):
        self.cards_list = sorted(cards_list)
        self.cards_dict = collections.defaultdict(int)

        for card in self.cards_list:
            self.cards_dict[card] += 1

        self._single_card_groups = self._gen_type_1_single_cards()
        self._pair_groups = self._gen_type_2_pair_cards()
        self._triple_groups = self._gen_type_3_triple_cards()
        self._bomb_groups = self._gen_type_4_bomb_cards()
        self._king_bomb_groups = self._gen_type_5_king_bomb_cards()

    def _create_moves(self, raw_moves: Iterable[Iterable[int]]) -> list[Move]:
        moves = []
        seen = set()
        for cards in raw_moves:
            move = MoveFactory.create_move(cards)
            identity = (move.move_type, move.cards)
            if not move.is_valid or identity in seen:
                continue
            seen.add(identity)
            moves.append(move)
        return moves

    def _gen_serial_moves(self, cards, min_serial, repeat=1, repeat_num=0):
        if repeat_num < min_serial:
            repeat_num = 0

        single_cards = sorted(list(set(cards)))
        seq_records = []
        moves = []

        start = index = 0
        longest = 1
        while index < len(single_cards):
            if index + 1 < len(single_cards) and single_cards[index + 1] - single_cards[index] == 1:
                longest += 1
                index += 1
            else:
                seq_records.append((start, longest))
                index += 1
                start = index
                longest = 1

        for start, longest in seq_records:
            if longest < min_serial:
                continue
            longest_list = single_cards[start:start + longest]

            if repeat_num == 0:
                steps = min_serial
                while steps <= longest:
                    index = 0
                    while steps + index <= longest:
                        target_moves = sorted(longest_list[index:index + steps] * repeat)
                        moves.append(target_moves)
                        index += 1
                    steps += 1
            else:
                if longest < repeat_num:
                    continue
                index = 0
                while index + repeat_num <= longest:
                    target_moves = sorted(longest_list[index:index + repeat_num] * repeat)
                    moves.append(target_moves)
                    index += 1

        return moves

    def _gen_type_1_single_cards(self):
        return [[card] for card in sorted(set(self.cards_list))]

    def gen_type_1_single(self) -> list[Move]:
        return self._create_moves(self._single_card_groups)

    def _gen_type_2_pair_cards(self):
        return [[rank, rank] for rank, amount in self.cards_dict.items() if amount >= 2]

    def gen_type_2_pair(self) -> list[Move]:
        return self._create_moves(self._pair_groups)

    def _gen_type_3_triple_cards(self):
        return [[rank, rank, rank] for rank, amount in self.cards_dict.items() if amount >= 3]

    def gen_type_3_triple(self) -> list[Move]:
        return self._create_moves(self._triple_groups)

    def _gen_type_4_bomb_cards(self):
        return [[rank, rank, rank, rank] for rank, amount in self.cards_dict.items() if amount == 4]

    def gen_type_4_bomb(self) -> list[Move]:
        return self._create_moves(self._bomb_groups)

    def _gen_type_5_king_bomb_cards(self):
        if 20 in self.cards_list and 30 in self.cards_list:
            return [[20, 30]]
        return []

    def gen_type_5_king_bomb(self) -> list[Move]:
        return self._create_moves(self._king_bomb_groups)

    def gen_type_6_3_1(self) -> list[Move]:
        result = []
        for single in self._single_card_groups:
            for triple in self._triple_groups:
                if single[0] != triple[0]:
                    result.append(single + triple)
        return self._create_moves(result)

    def gen_type_7_3_2(self) -> list[Move]:
        result = []
        for pair in self._pair_groups:
            for triple in self._triple_groups:
                if pair[0] != triple[0]:
                    result.append(pair + triple)
        return self._create_moves(result)

    def gen_type_8_serial_single(self, repeat_num=0) -> list[Move]:
        return self._create_moves(
            self._gen_serial_moves(self.cards_list, MIN_SINGLE_CARDS, repeat=1, repeat_num=repeat_num)
        )

    def gen_type_9_serial_pair(self, repeat_num=0) -> list[Move]:
        single_pairs = [rank for rank, amount in self.cards_dict.items() if amount >= 2]
        return self._create_moves(
            self._gen_serial_moves(single_pairs, MIN_PAIRS, repeat=2, repeat_num=repeat_num)
        )

    def gen_type_10_serial_triple(self, repeat_num=0) -> list[Move]:
        single_triples = [rank for rank, amount in self.cards_dict.items() if amount >= 3]
        return self._create_moves(
            self._gen_serial_moves(single_triples, MIN_TRIPLES, repeat=3, repeat_num=repeat_num)
        )

    def gen_type_11_serial_3_1(self, repeat_num=0) -> list[Move]:
        serial_3_moves = self.gen_type_10_serial_triple(repeat_num=repeat_num)
        serial_3_1_moves = []

        for serial_move in serial_3_moves:
            serial_set = set(serial_move.cards)
            new_cards = [card for card in self.cards_list if card not in serial_set]
            subcards = select(new_cards, len(serial_set))

            for cards in subcards:
                serial_3_1_moves.append(serial_move.to_list() + cards)

        return self._create_moves(k for k, _ in itertools.groupby(sorted(serial_3_1_moves)))

    def gen_type_12_serial_3_2(self, repeat_num=0) -> list[Move]:
        serial_3_moves = self.gen_type_10_serial_triple(repeat_num=repeat_num)
        serial_3_2_moves = []
        pair_set = sorted([rank for rank, amount in self.cards_dict.items() if amount >= 2])

        for serial_move in serial_3_moves:
            serial_set = set(serial_move.cards)
            pair_candidates = [rank for rank in pair_set if rank not in serial_set]
            subcards = select(pair_candidates, len(serial_set))
            for cards in subcards:
                serial_3_2_moves.append(sorted(serial_move.to_list() + cards * 2))

        return self._create_moves(serial_3_2_moves)

    def gen_type_13_4_2(self) -> list[Move]:
        four_cards = [rank for rank, amount in self.cards_dict.items() if amount == 4]
        result = []

        for rank in four_cards:
            cards_list = [card for card in self.cards_list if card != rank]
            subcards = select(cards_list, 2)
            for cards in subcards:
                result.append([rank] * 4 + cards)

        return self._create_moves(k for k, _ in itertools.groupby(sorted(result)))

    def gen_type_14_4_22(self) -> list[Move]:
        four_cards = [rank for rank, amount in self.cards_dict.items() if amount == 4]
        result = []

        for rank in four_cards:
            cards_list = [card for card, amount in self.cards_dict.items() if card != rank and amount >= 2]
            subcards = select(cards_list, 2)
            for cards in subcards:
                result.append([rank] * 4 + [cards[0], cards[0], cards[1], cards[1]])

        return self._create_moves(result)

    def generate_all_moves(self) -> list[Move]:
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

    def gen_moves(self) -> list[Move]:
        return self.generate_all_moves()
