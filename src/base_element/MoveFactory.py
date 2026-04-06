from __future__ import annotations

import collections
from dataclasses import dataclass
from typing import Iterable, Optional

from base_element.ActionType import CMoveType
from base_element.Move import (
    BombMove,
    FourWithTwoPairsMove,
    FourWithTwoSinglesMove,
    KingBombMove,
    Move,
    PassMove,
    PairMove,
    SerialPairMove,
    SerialSingleMove,
    SerialTripleMove,
    SerialTripleWithPairMove,
    SerialTripleWithSingleMove,
    SingleMove,
    TripleMove,
    TripleWithPairMove,
    TripleWithSingleMove,
    WrongMove,
    is_continuous_seq,
    normalize_cards,
)
from utils import MIN_TRIPLES


@dataclass(frozen=True)
class MoveMetadata:
    move_type: CMoveType
    rank: Optional[int] = None
    sequence_length: Optional[int] = None


class MoveFactory:
    _MOVE_TYPES = {
        CMoveType.TYPE_0_PASS: PassMove,
        CMoveType.TYPE_1_SINGLE: SingleMove,
        CMoveType.TYPE_2_PAIR: PairMove,
        CMoveType.TYPE_3_TRIPLE: TripleMove,
        CMoveType.TYPE_4_BOMB: BombMove,
        CMoveType.TYPE_5_KING_BOMB: KingBombMove,
        CMoveType.TYPE_6_3_1: TripleWithSingleMove,
        CMoveType.TYPE_7_3_2: TripleWithPairMove,
        CMoveType.TYPE_8_SERIAL_SINGLE: SerialSingleMove,
        CMoveType.TYPE_9_SERIAL_PAIR: SerialPairMove,
        CMoveType.TYPE_10_SERIAL_TRIPLE: SerialTripleMove,
        CMoveType.TYPE_11_SERIAL_3_1: SerialTripleWithSingleMove,
        CMoveType.TYPE_12_SERIAL_3_2: SerialTripleWithPairMove,
        CMoveType.TYPE_13_4_2: FourWithTwoSinglesMove,
        CMoveType.TYPE_14_4_22: FourWithTwoPairsMove,
        CMoveType.TYPE_15_WRONG: WrongMove,
    }

    @classmethod
    def create_move(cls, cards: Iterable[int]) -> Move:
        normalized = normalize_cards(cards)
        metadata = cls.detect(normalized)
        move_class = cls._MOVE_TYPES[metadata.move_type]

        if move_class is PassMove:
            return PassMove()
        if move_class is WrongMove:
            return WrongMove(normalized)

        kwargs = {}
        if metadata.rank is not None:
            kwargs["rank"] = metadata.rank
        if metadata.sequence_length is not None:
            kwargs["sequence_length"] = metadata.sequence_length
        return move_class(normalized, **kwargs)

    @classmethod
    def detect(cls, cards: Iterable[int]) -> MoveMetadata:
        move = list(normalize_cards(cards))
        move_size = len(move)
        move_dict = collections.Counter(move)

        if move_size == 0:
            return MoveMetadata(CMoveType.TYPE_0_PASS)

        if move_size == 1:
            return MoveMetadata(CMoveType.TYPE_1_SINGLE, rank=move[0])

        if move_size == 2:
            if move[0] == move[1]:
                return MoveMetadata(CMoveType.TYPE_2_PAIR, rank=move[0])
            if move == [20, 30]:
                return MoveMetadata(CMoveType.TYPE_5_KING_BOMB, rank=30)
            return MoveMetadata(CMoveType.TYPE_15_WRONG)

        if move_size == 3:
            if len(move_dict) == 1:
                return MoveMetadata(CMoveType.TYPE_3_TRIPLE, rank=move[0])
            return MoveMetadata(CMoveType.TYPE_15_WRONG)

        if move_size == 4:
            if len(move_dict) == 1:
                return MoveMetadata(CMoveType.TYPE_4_BOMB, rank=move[0])
            if len(move_dict) == 2:
                if move[0] == move[1] == move[2] or move[1] == move[2] == move[3]:
                    return MoveMetadata(CMoveType.TYPE_6_3_1, rank=move[1])
            return MoveMetadata(CMoveType.TYPE_15_WRONG)

        if is_continuous_seq(move):
            return MoveMetadata(
                CMoveType.TYPE_8_SERIAL_SINGLE,
                rank=move[0],
                sequence_length=len(move),
            )

        if move_size == 5:
            if len(move_dict) == 2:
                triple_rank = max(rank for rank, count in move_dict.items() if count == 3)
                return MoveMetadata(CMoveType.TYPE_7_3_2, rank=triple_rank)
            return MoveMetadata(CMoveType.TYPE_15_WRONG)

        count_dict = collections.defaultdict(int)
        for _, count in move_dict.items():
            count_dict[count] += 1

        if move_size == 6:
            if (len(move_dict) in (2, 3) and count_dict.get(4) == 1 and
                    (count_dict.get(2) == 1 or count_dict.get(1) == 2)):
                return MoveMetadata(CMoveType.TYPE_13_4_2, rank=move[2])

        if move_size == 8 and (((len(move_dict) in (2, 3)) and
                (count_dict.get(4) == 1 and count_dict.get(2) == 2)) or count_dict.get(4) == 2):
            bomb_rank = max(rank for rank, count in move_dict.items() if count == 4)
            return MoveMetadata(CMoveType.TYPE_14_4_22, rank=bomb_rank)

        move_keys = sorted(move_dict.keys())
        if len(move_dict) == count_dict.get(2) and is_continuous_seq(move_keys):
            return MoveMetadata(
                CMoveType.TYPE_9_SERIAL_PAIR,
                rank=move_keys[0],
                sequence_length=len(move_keys),
            )

        if len(move_dict) == count_dict.get(3) and is_continuous_seq(move_keys):
            return MoveMetadata(
                CMoveType.TYPE_10_SERIAL_TRIPLE,
                rank=move_keys[0],
                sequence_length=len(move_keys),
            )

        if count_dict.get(3, 0) >= MIN_TRIPLES:
            serial_triples = []
            single_cards = []
            pair_cards = []

            for rank, count in move_dict.items():
                if count == 3:
                    serial_triples.append(rank)
                elif count == 1:
                    single_cards.append(rank)
                elif count == 2:
                    pair_cards.append(rank)
                else:
                    return MoveMetadata(CMoveType.TYPE_15_WRONG)

            serial_triples.sort()
            if is_continuous_seq(serial_triples):
                if len(serial_triples) == len(single_cards) + len(pair_cards) * 2:
                    return MoveMetadata(
                        CMoveType.TYPE_11_SERIAL_3_1,
                        rank=serial_triples[0],
                        sequence_length=len(serial_triples),
                    )
                if len(serial_triples) == len(pair_cards) and len(move_dict) == len(serial_triples) * 2:
                    return MoveMetadata(
                        CMoveType.TYPE_12_SERIAL_3_2,
                        rank=serial_triples[0],
                        sequence_length=len(serial_triples),
                    )

            if len(serial_triples) == 4:
                if is_continuous_seq(serial_triples[1:]):
                    return MoveMetadata(
                        CMoveType.TYPE_11_SERIAL_3_1,
                        rank=serial_triples[1],
                        sequence_length=len(serial_triples) - 1,
                    )
                if is_continuous_seq(serial_triples[:-1]):
                    return MoveMetadata(
                        CMoveType.TYPE_11_SERIAL_3_1,
                        rank=serial_triples[0],
                        sequence_length=len(serial_triples) - 1,
                    )

        return MoveMetadata(CMoveType.TYPE_15_WRONG)
