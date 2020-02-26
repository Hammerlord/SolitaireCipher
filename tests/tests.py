import unittest
from random import randrange

from src.solitaire import *


class SolitaireCipherTests(unittest.TestCase):

    def test_deck_contains_correct_cards(self):
        cards = generate_cards()
        card_map = {}
        for card in cards:
            self.assertNotIn(card, card_map)
            card_map[card] = True

    def test_move_big_joker(self):
        #             |-| -> |
        items = [1, 2, 5, 3, 4]
        result = move_joker(5, items)
        self.assertListEqual(result, [1, 2, 3, 4, 5])

    def test_big_joker_wraparound_skips_first_index(self):
        #           | <- |-|
        items = [1, 2, 3, 5, 4]
        result = move_joker(5, items)
        self.assertListEqual(result, [1, 5, 2, 3, 4])

    def test_big_joker_last_to_third_index(self):
        #              | <- |-|
        items = [1, 2, 3, 4, 5]
        result = move_joker(5, items)
        self.assertListEqual(result, [1, 2, 5, 3, 4])

    def test_move_small_joker(self):
        #                |-|->|
        items = [1, 2, 3, 4, 5]
        result = move_joker(4, items)
        self.assertListEqual(result, [1, 2, 3, 5, 4])

    def test_small_joker_wraparound_skips_first_index(self):
        #           |   <-  |-|
        items = [1, 2, 3, 5, 4]
        result = move_joker(4, items)
        self.assertListEqual(result, [1, 4, 2, 3, 5])

    def test_triple_cut_indices_noninclusive(self):
        #        |1|   |---- 2 ----|    |- 3 -|   Expect 1 and 3 to be swapped, 2 remains same
        items = ['a', 'b', 'c', 'd', 'e', 'f']
        cut_indices = (items.index('b'), items.index('d'))
        result = triple_cut(cut_indices, items)
        self.assertListEqual(['e', 'f', 'b', 'c', 'd', 'a'], result)

    def test_triple_cut_indices_consecutive(self):
        #        |- 1 -|     |- 2 -|   |- 3 -|   Expect 1 and 3 to be swapped, 2 remains same
        items = ['a', 'b', 'c', 'd', 'e', 'f']
        cut_indices = (items.index('c'), items.index('d'))
        result = triple_cut(cut_indices, items)
        self.assertListEqual(['e', 'f', 'c', 'd', 'a', 'b'], result)

    def test_triple_cut_handles_unsorted_indices(self):
        items = ['a', 'b', 'c', 'd', 'e', 'f']
        cut_indices = (items.index('d'), items.index('b'))  # d > b
        result = triple_cut(cut_indices, items)
        self.assertListEqual(['e', 'f', 'b', 'c', 'd', 'a'], result)

    def test_triple_cut_start_end_indices(self):
        items = ['a', 'b', 'c', 'd', 'e', 'f']
        cut_indices = (items.index('a'), items.index('f'))
        result = triple_cut(cut_indices, items)
        self.assertListEqual(items, result)

    def test_is_joker(self):
        # The two highest values of a deck are the jokers.
        items = [1, 2, 3, 4, 5]
        self.assertFalse(is_joker(3, items))
        self.assertTrue(is_joker(4, items))
        self.assertTrue(is_joker(5, items))

    def test_count_cut_moves_cards_above_last(self):
        #        |- 1 -|    |2|    1 moves just before 2
        items = [1, 2, 4, 5, 3]  # Not a joker at the last value.
        self.assertListEqual(count_cut(items), [5, 1, 2, 4, 3])

    def test_count_cut_joker(self):
        items = [1, 2, 3, 4, 5]
        self.assertListEqual(count_cut(items), [1, 2, 3, 4, 5])
        items = [1, 2, 3, 5, 4]
        self.assertListEqual(count_cut(items), [1, 2, 3, 5, 4])

    def test_num_to_letter_wraparound(self):
        result = [number_to_letter(num) for num in [1, 5, 26, 41, 52]]
        self.assertListEqual(result, ['B', 'F', 'A', 'P', 'A'])

    def test_get_keystream_value(self):
        items = [1, 2, 3, 4, 5]
        result = get_keystream_value(items)
        self.assertEqual(result, 2)

    def test_get_keystream_value_big_joker(self):
        items = [5, 2, 3, 4, 1]
        result = get_keystream_value(items)
        self.assertEqual(result, 1)

    def test_get_keystream_value_small_joker(self):
        items = [4, 5, 2, 3, 1]
        result = get_keystream_value(items)
        self.assertEqual(result, 1)

    def test_encrypt_decrypt_same_message(self):
        input_key = generate_cards()
        message = "IFYOUCANREADTHISGOODFORYOU"
        encrypted = encrypt(input_key, message)
        decrypted = decrypt(input_key, encrypted)
        self.assertEqual(message, decrypted)

    def test_encrypt_handles_nonalphabetical_smallcase(self):
        input_key = generate_cards()
        message = "If you can read this, good for you"
        encrypted = encrypt(input_key, message)
        decrypted = decrypt(input_key, encrypted)
        self.assertEqual("IFYOUCANREADTHISGOODFORYOU", decrypted)

    def test_encrypt_decrypt_random_sequences(self):
        input_key = generate_cards()
        num_letters = len(LETTERS)
        for i in range(100):
            sequence = ''.join([number_to_letter(randrange(num_letters)) for j in range(15)])
            encrypted = encrypt(input_key, sequence)
            decrypted = decrypt(input_key, encrypted)
            self.assertEqual(sequence, decrypted)
