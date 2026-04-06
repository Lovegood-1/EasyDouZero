from __future__ import annotations

from abc import ABC
from collections import Counter
from typing import Iterable, Optional, Sequence

from base_element.ActionType import CMoveType


MIN_SEQUENCE_LENGTH = 2


def normalize_cards(cards: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(cards))



def is_continuous_seq(cards: Sequence[int]) -> bool:
    if len(cards) < MIN_SEQUENCE_LENGTH:
        return False

    for index in range(len(cards) - 1):
        if cards[index + 1] - cards[index] != 1:
            return False
    return True



def count_values(cards: Sequence[int]) -> Counter:
    return Counter(cards)



def ranks_with_count(cards: Sequence[int], count: int) -> list[int]:
    return sorted(rank for rank, amount in count_values(cards).items() if amount == count)


class Move(ABC):
    move_type = CMoveType.TYPE_15_WRONG

    def __init__(
        self,
        cards: Iterable[int],
        *,
        rank: Optional[int] = None,
        sequence_length: Optional[int] = None,
    ) -> None:
        self._cards = normalize_cards(cards)
        self._rank = rank
        self._sequence_length = sequence_length

    @property
    def cards(self) -> tuple[int, ...]:
        return self._cards

    @property
    def rank(self) -> Optional[int]:
        return self._rank

    @property
    def sequence_length(self) -> Optional[int]:
        return self._sequence_length

    @property
    def is_valid(self) -> bool:
        return self.move_type != CMoveType.TYPE_15_WRONG

    @property
    def is_pass(self) -> bool:
        return self.move_type == CMoveType.TYPE_0_PASS

    @property
    def is_bomb(self) -> bool:
        return self.move_type == CMoveType.TYPE_4_BOMB

    @property
    def is_king_bomb(self) -> bool:
        return self.move_type == CMoveType.TYPE_5_KING_BOMB

    def to_list(self) -> list[int]:
        return list(self.cards)

    def can_beat(self, rival_move: "Move") -> bool:
        if not isinstance(rival_move, Move):
            return False

        if not self.is_valid or not rival_move.is_valid:
            return False

        if self.is_pass:
            return False

        if rival_move.is_pass:
            return True

        if self.is_king_bomb:
            return not rival_move.is_king_bomb

        if rival_move.is_king_bomb:
            return False

        if self.is_bomb:
            if rival_move.is_bomb:
                return self._compare_rank(rival_move)
            return True

        if rival_move.is_bomb:
            return False

        if self.move_type != rival_move.move_type:
            return False

        if not self._matches_shape(rival_move):
            return False

        return self._compare_rank(rival_move)

    def beats(self, rival_move: "Move") -> bool:
        return self.can_beat(rival_move)

    def _matches_shape(self, rival_move: "Move") -> bool:
        return self.sequence_length == rival_move.sequence_length

    def _compare_rank(self, rival_move: "Move") -> bool:
        if self.rank is None or rival_move.rank is None:
            return False
        return self.rank > rival_move.rank

    @classmethod
    def filter_beatable(cls, candidate_moves: Iterable["Move"], rival_move: "Move") -> list["Move"]:
        return [move for move in candidate_moves if move.can_beat(rival_move)]

    def select_beating_moves(self, candidate_moves: Iterable["Move"]) -> list["Move"]:
        return self.filter_beatable(candidate_moves, self)

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(cards={list(self.cards)}, "
            f"move_type={self.move_type.name}, rank={self.rank}, "
            f"sequence_length={self.sequence_length})"
        )


class WrongMove(Move):
    move_type = CMoveType.TYPE_15_WRONG


class PassMove(Move):
    move_type = CMoveType.TYPE_0_PASS

    def __init__(self) -> None:
        super().__init__((), rank=None, sequence_length=None)


class SingleMove(Move):
    move_type = CMoveType.TYPE_1_SINGLE

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        super().__init__(normalized, rank=normalized[0] if rank is None else rank, sequence_length=None)


class PairMove(Move):
    move_type = CMoveType.TYPE_2_PAIR

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        super().__init__(normalized, rank=normalized[0] if rank is None else rank, sequence_length=None)


class TripleMove(Move):
    move_type = CMoveType.TYPE_3_TRIPLE

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        super().__init__(normalized, rank=normalized[0] if rank is None else rank, sequence_length=None)


class BombMove(Move):
    move_type = CMoveType.TYPE_4_BOMB

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        super().__init__(normalized, rank=normalized[0] if rank is None else rank, sequence_length=None)


class KingBombMove(Move):
    move_type = CMoveType.TYPE_5_KING_BOMB

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        super().__init__(normalize_cards(cards), rank=30 if rank is None else rank, sequence_length=None)


class TripleWithSingleMove(Move):
    move_type = CMoveType.TYPE_6_3_1

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        triple_rank = rank if rank is not None else ranks_with_count(normalized, 3)[0]
        super().__init__(normalized, rank=triple_rank, sequence_length=None)


class TripleWithPairMove(Move):
    move_type = CMoveType.TYPE_7_3_2

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        triple_rank = rank if rank is not None else ranks_with_count(normalized, 3)[0]
        super().__init__(normalized, rank=triple_rank, sequence_length=None)


class SerialSingleMove(Move):
    move_type = CMoveType.TYPE_8_SERIAL_SINGLE

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None, sequence_length: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        super().__init__(
            normalized,
            rank=normalized[0] if rank is None else rank,
            sequence_length=len(normalized) if sequence_length is None else sequence_length,
        )


class SerialPairMove(Move):
    move_type = CMoveType.TYPE_9_SERIAL_PAIR

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None, sequence_length: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        unique_cards = sorted(set(normalized))
        super().__init__(
            normalized,
            rank=unique_cards[0] if rank is None else rank,
            sequence_length=len(unique_cards) if sequence_length is None else sequence_length,
        )


class SerialTripleMove(Move):
    move_type = CMoveType.TYPE_10_SERIAL_TRIPLE

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None, sequence_length: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        triple_ranks = ranks_with_count(normalized, 3)
        super().__init__(
            normalized,
            rank=triple_ranks[0] if rank is None else rank,
            sequence_length=len(triple_ranks) if sequence_length is None else sequence_length,
        )


class SerialTripleWithSingleMove(Move):
    move_type = CMoveType.TYPE_11_SERIAL_3_1

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None, sequence_length: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        triple_ranks = ranks_with_count(normalized, 3)
        super().__init__(
            normalized,
            rank=triple_ranks[0] if rank is None and triple_ranks else rank,
            sequence_length=len(triple_ranks) if sequence_length is None else sequence_length,
        )


class SerialTripleWithPairMove(Move):
    move_type = CMoveType.TYPE_12_SERIAL_3_2

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None, sequence_length: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        triple_ranks = ranks_with_count(normalized, 3)
        super().__init__(
            normalized,
            rank=triple_ranks[0] if rank is None and triple_ranks else rank,
            sequence_length=len(triple_ranks) if sequence_length is None else sequence_length,
        )


class FourWithTwoSinglesMove(Move):
    move_type = CMoveType.TYPE_13_4_2

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        four_rank = rank if rank is not None else ranks_with_count(normalized, 4)[0]
        super().__init__(normalized, rank=four_rank, sequence_length=None)


class FourWithTwoPairsMove(Move):
    move_type = CMoveType.TYPE_14_4_22

    def __init__(self, cards: Iterable[int], rank: Optional[int] = None) -> None:
        normalized = normalize_cards(cards)
        four_ranks = ranks_with_count(normalized, 4)
        super().__init__(normalized, rank=max(four_ranks) if rank is None else rank, sequence_length=None)
