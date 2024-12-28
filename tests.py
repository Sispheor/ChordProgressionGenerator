from main import get_scale_in_key, get_triads, get_progression_with_triads

import unittest


def get_progression_with_triades(chord_progression, triades):
    pass


class TestChordGenerator(unittest.TestCase):


    def test_get_major_scale_in_key(self):
        expected = ['Bb', 'C', 'D', 'Eb','F', 'G', 'A']
        major_key = get_scale_in_key("Bb")
        self.assertEqual(expected, major_key)

        expected = ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'F']
        major_key = get_scale_in_key("F#")
        self.assertEqual(expected, major_key)

        expected = ['E', 'F#', 'G', 'A', 'B', 'C', 'D']
        minor_key = get_scale_in_key("E", scale_type="MINOR")
        self.assertEqual(expected, minor_key)


    def test_get_major_triades(self):
        major_scale = ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']
        chord_progression = ['Bb', 'F', 'Eb', 'Bb']
        expected = {'Bb': {'1st': ['D', 'F', 'Bb'],
                           '2nd': ['F', 'Bb', 'D'],
                           'root': ['Bb', 'D', 'F']},
                    'Eb': {'1st': ['G', 'Bb', 'Eb'],
                           '2nd': ['Bb', 'Eb', 'G'],
                           'root': ['Eb', 'G', 'Bb']},
                    'F': {'1st': ['A', 'C', 'F'], '2nd': ['C', 'F', 'A'], 'root': ['F', 'A', 'C']}}
        self.assertEqual(get_triads(chord_progression, major_scale), expected)

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