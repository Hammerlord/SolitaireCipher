import random
from typing import Callable, List
import functools

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
LETTER_TO_NUM_MAP = {}
for i, letter in enumerate(LETTERS):
    LETTER_TO_NUM_MAP[letter] = i


def encrypt(key: list, msg: str) -> str:
    """
    :param key: The ordering of the cards to encrypt by.
    :param msg: The plaintext message to encrypt.
    :return: The encrypted message.
    """
    return transform(key, msg, lambda n, k: n + k)


def decrypt(key: list, msg: str) -> str:
    """
    :param key: The same initial ordering of cards used to encrypt.
    :param msg: The ciphertext to decrypt.
    :return: The decrypted message.
    """
    return transform(key, msg, lambda n, k: n - k)


def transform(cards: List[int], msg: str, combine: Callable) -> str:
    """
    Encrypts or decrypts the message, depending on the `combine` parametre.
    :param cards: The ordering of the cards, or "key."
    :param msg: The message to encrypt or decrypt.
    :param combine: Function to combine (add/subtract) a letter number value with a keystream-generated value.
    :return: The encrypted/decrypted result.
    """
    input = format_input(msg)
    cards = list(cards)
    run_keystream_sequence = compose(count_cut,
                                     triple_cut_by_jokers,
                                     move_joker_b,
                                     move_joker_a)
    output = []
    while len(output) < len(input):
        cards = run_keystream_sequence(cards)
        ks_val = get_keystream_value(cards)
        if is_joker(ks_val, cards):
            continue
        current_letter = input[len(output)]
        value = combine(LETTER_TO_NUM_MAP[current_letter], ks_val)
        output.append(number_to_letter(value))

    return ''.join(output)


def generate_cards(suits=4) -> List[int]:
    """
    :param suits: Typically, Solitaire crypto uses either 2 or 4 suits.
    :return: A randomized deck of cards based on the number of suits.
    """
    jokers = 2
    deck_size = suits * 13 + jokers
    cards = list(range(1, deck_size + 1))
    random.shuffle(cards)
    return cards


def triple_cut_by_jokers(cards: List[int]) -> list:
    joker_a = len(cards) - 1
    joker_b = len(cards)
    return triple_cut((cards.index(joker_a), cards.index(joker_b)), cards)


def move_joker_a(cards: List[int]) -> list:
    return move_joker(len(cards) - 1, cards)


def move_joker_b(cards: List[int]) -> list:
    return move_joker(len(cards), cards)


def get_keystream_value(cards: List[int]) -> int:
    """
    Given a deck of cards:
    1) Check the top card. If it isn't a joker, count that many places down the deck and
    return the value of the card at the resultant location.
    2) If the first card is a joker, return the value of the last card in the deck.
    """
    index = cards[0] if not is_joker(cards[0], cards) else len(cards) - 1
    return cards[index]


def is_joker(value: int, cards: List[int]) -> bool:
    """
    :param value: The card to check.
    :param cards: The deck of cards, whose size is used to check for jokers.
    :return: True if value is a joker. Jokers are always the highest 2 values in a deck.
    """
    return value > len(cards) - 2


def move_joker(joker: int, cards: List[int]) -> List[int]:
    """
    Moves a joker down the deck based on special rules:
    The smaller joker moves 1 card down, while the larger joker moves 2 cards down.
    :return: New deck with the moved joker.
    """

    def wraparound(n: int) -> int:
        if n >= len(cards):
            # The wraparound value cannot be 0; it must always skip the first index
            return n % len(cards) + 1
        return n

    cards = list(cards)
    jump = 2 if joker is len(cards) else 1
    index = cards.index(joker)
    cards.insert(wraparound(index + jump), cards.pop(index))
    return cards


def triple_cut(cut_indices: tuple, cards: list) -> List[int]:
    """
    Given two indices, perform a "triple cut," swapping cards above the top index with cards below the bottom index
    (retaining their respective order).
    :return: New deck that has been cut.
    """
    lower, higher = sorted(cut_indices)
    return cards[higher + 1:] + cards[lower:higher + 1] + cards[:lower]


def count_cut(cards: List[int]) -> List[int]:
    """
    Perform a "count cut": Look at the value of the last card in the deck. Take that number of cards off
    the top of the deck and move them just above the bottom card (retaining their order).
    :return: New deck that has been cut.
    """
    last = len(cards) - 1
    value = cards[last]
    if is_joker(value, cards):
        return list(cards)
    return cards[value:last] + cards[:value] + [cards[last]]


def number_to_letter(n: int) -> str:
    """
    Given a number, get its associated letter value.
    """
    return LETTERS[n % len(LETTERS)]


def format_input(msg: str) -> List[str]:
    """
    Formats a string into the accepted format for encryption/decryption. Non-alphabetical characters are ignored.
    """
    return [char for char in msg.upper() if char in LETTER_TO_NUM_MAP]


def compose(*functions):
    """
    Composes n functions together.
    Taken from: https://mathieularose.com/function-composition-in-python/
    """
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)
