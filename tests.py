from main import get_scale_in_key, get_triads, get_progression_with_triads, get_chords, get_tablature, \
    remove_open_position, order_patterns_by_value

import unittest


def get_progression_with_triades(chord_progression, triades):
    pass


class TestChordGenerator(unittest.TestCase):


    def test_get_scale_in_key(self):
        expected = ['Bb', 'C', 'D', 'Eb','F', 'G', 'A']
        major_key = get_scale_in_key("Bb", "MAJOR")
        self.assertEqual(expected, major_key)

        expected = ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'F']
        major_key = get_scale_in_key("F#", "MAJOR")
        self.assertEqual(expected, major_key)

        expected = ['E', 'F#', 'G', 'A', 'B', 'C', 'D']
        minor_key = get_scale_in_key("E", "MINOR")
        self.assertEqual(expected, minor_key)

    def test_get_chords(self):
        current_key_scale = ['G', 'A', 'A#', 'C', 'D', 'D#', 'F']
        progression_formula = [1, 4, 1, 5]
        chord_progression = get_chords(current_key_scale, progression_formula)
        self.assertListEqual(['G', 'C', 'G', 'D'], chord_progression)


    def test_get_triads(self):
        key_scale = ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']
        chord_progression = ['Bb', 'F', 'Eb', 'Bb']
        expected = {'Bb': {'1st': ['D', 'F', 'Bb'],
                           '2nd': ['F', 'Bb', 'D'],
                           'root': ['Bb', 'D', 'F']},
                    'Eb': {'1st': ['G', 'Bb', 'Eb'],
                           '2nd': ['Bb', 'Eb', 'G'],
                           'root': ['Eb', 'G', 'Bb']},
                    'F': {'1st': ['A', 'C', 'F'], '2nd': ['C', 'F', 'A'], 'root': ['F', 'A', 'C']}}
        self.assertEqual(get_triads(chord_progression, key_scale), expected)

    def test_get_progression_with_triads(self):
        chord_progression = ['Bb', 'F', 'Eb', 'Bb']
        triads = {'Bb': {'1st': ['D', 'F', 'Bb'],
                         '2nd': ['F', 'Bb', 'D'],
                         'root': ['Bb', 'D', 'F']},
                  'Eb': {'1st': ['G', 'Bb', 'Eb'],
                         '2nd': ['Bb', 'Eb', 'G'],
                         'root': ['Eb', 'G', 'Bb']},
                  'F': {'1st': ['A', 'C', 'F'], '2nd': ['C', 'F', 'A'], 'root': ['F', 'A', 'C']}}
        expected_triade_progression =  {
            'PATTERN_1': [['Bb', 'D', 'F'], ['A', 'C', 'F'], ['Bb', 'Eb', 'G'], ['Bb', 'D', 'F']],
            'PATTERN_2': [['D', 'F', 'Bb'], ['C', 'F', 'A'], ['Eb', 'G', 'Bb'], ['D', 'F', 'Bb']],
            'PATTERN_3': [['F', 'Bb', 'D'], ['F', 'A', 'C'], ['G', 'Bb', 'Eb'], ['F', 'Bb', 'D']]
        }

        self.assertDictEqual(get_progression_with_triads(chord_progression, triads, "MAJOR"), expected_triade_progression)

        # test minor
        chord_progression = ['E', 'A', 'E', 'B']
        triads = {'A': {'1st': ['C', 'E', 'A'], '2nd': ['E', 'A', 'C'], 'root': ['A', 'C', 'E']},
                  'B': {'1st': ['D', 'F#', 'B'], '2nd': ['F#', 'B', 'D'], 'root': ['B', 'D', 'F#']},
                  'E': {'1st': ['G', 'B', 'E'], '2nd': ['B', 'E', 'G'], 'root': ['E', 'G', 'B']}}

        expected_triade_progression = {'PATTERN_1': [['G', 'B', 'E'], ['A', 'C', 'E'], ['G', 'B', 'E'], ['F#', 'B', 'D']],
                                       'PATTERN_2': [['E', 'G', 'B'], ['E', 'A', 'C'], ['E', 'G', 'B'], ['D', 'F#', 'B']],
                                       'PATTERN_3': [['B', 'E', 'G'], ['C', 'E', 'A'], ['B', 'E', 'G'], ['B', 'D', 'F#']]}

        self.assertDictEqual(get_progression_with_triads(chord_progression, triads, "MINOR"),
                             expected_triade_progression)

    def test_get_tablature(self):
        progression_with_triads = {'PATTERN_1': [['A#', 'D', 'G'], ['C', 'D#', 'G'], ['A#', 'D', 'G'], ['A', 'D', 'F']],
                                   'PATTERN_2': [['G', 'A#', 'D'], ['G', 'C', 'D#'], ['G', 'A#', 'D'], ['F', 'A', 'D']],
                                   'PATTERN_3': [['D', 'G', 'A#'], ['D#', 'G', 'C'], ['D', 'G', 'A#'], ['D', 'F', 'A']]}
        expected_tablature = {'A': {'PATTERN_1': [(1, 0, 0), (3, 1, 0), (1, 0, 0), (0, 0, 10)],
                                    'PATTERN_2': [(10, 8, 7), (10, 10, 8), (10, 8, 7), (8, 7, 7)],
                                    'PATTERN_3': [(5, 5, 3), (6, 5, 5), (5, 5, 3), (5, 3, 2)]},
                              'D': {'PATTERN_1': [(8, 7, 8), (10, 8, 8), (8, 7, 8), (7, 7, 6)],
                                    'PATTERN_2': [(5, 3, 3), (5, 5, 4), (5, 3, 3), (3, 2, 3)],
                                    'PATTERN_3': [(0, 0, 11), (1, 0, 1), (0, 0, 11), (0, 10, 10)]},
                              'E': {'PATTERN_1': [(6, 5, 5), (8, 6, 5), (6, 5, 5), (5, 5, 3)],
                                    'PATTERN_2': [(3, 1, 0), (3, 3, 1), (3, 1, 0), (1, 0, 0)],
                                    'PATTERN_3': [(10, 10, 8), (11, 10, 10), (10, 10, 8), (10, 8, 7)]},
                              'G': {'PATTERN_1': [(3, 3, 3), (5, 4, 3), (3, 3, 3), (2, 3, 1)],
                                    'PATTERN_2': [(0, 11, 10), (0, 1, 11), (0, 11, 10), (10, 10, 10)],
                                    'PATTERN_3': [(7, 8, 6), (8, 8, 8), (7, 8, 6), (7, 6, 5)]}}
        self.assertDictEqual(expected_tablature, get_tablature(progression_with_triads))

    def test_remove_open_position(self):
        test_tablature = {
            'D': {'PATTERN_1': [(8, 7, 8), (10, 8, 8), (8, 7, 8), (7, 7, 6)],
                  'PATTERN_2': [(5, 3, 3), (5, 5, 4), (5, 3, 3), (3, 2, 3)],
                  'PATTERN_3': [(0, 0, 11), (1, 0, 1), (0, 0, 11), (0, 10, 10)]
                  }
        }

        expected_transformed_tablature = {
            'D': {'PATTERN_1': [(8, 7, 8), (10, 8, 8), (8, 7, 8), (7, 7, 6)],
                  'PATTERN_2': [(5, 3, 3), (5, 5, 4), (5, 3, 3), (3, 2, 3)],
                  'PATTERN_3': [(12, 12, 11), (13, 12, 13), (12, 12, 11), (12, 10, 10)]}
        }
        self.assertDictEqual(expected_transformed_tablature, remove_open_position(test_tablature))

    def test_order_patterns_by_value(self):
        test_tablature = {
            'D': {'PATTERN_1': [(8, 7, 8), (10, 8, 8), (8, 7, 8), (7, 7, 6)],
                  'PATTERN_2': [(12, 12, 11), (13, 12, 13), (12, 12, 11), (12, 10, 10)],
                  'PATTERN_3': [(5, 3, 3), (5, 5, 4), (5, 3, 3), (3, 2, 3)]
                  }
        }
        expected_tablature = {
            'D': {'PATTERN_1': [(5, 3, 3), (5, 5, 4), (5, 3, 3), (3, 2, 3)],
                  'PATTERN_2': [(8, 7, 8), (10, 8, 8), (8, 7, 8), (7, 7, 6)],
                  'PATTERN_3': [(12, 12, 11), (13, 12, 13), (12, 12, 11), (12, 10, 10)]}
        }
        self.assertDictEqual(expected_tablature, order_patterns_by_value(test_tablature))
