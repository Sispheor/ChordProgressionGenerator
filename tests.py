from main import get_major_scale_in_key, get_major_triades, get_progression_with_triades

import unittest

class TestChordGenerator(unittest.TestCase):


    def test_get_major_scale_in_key(self):
        expected = ['Bb', 'C', 'D', 'Eb','F', 'G', 'A']
        major_key = get_major_scale_in_key("Bb")
        self.assertEqual(expected, major_key)

        expected = ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'F']
        major_key = get_major_scale_in_key("F#")
        self.assertEqual(expected, major_key)


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
        self.assertEqual(get_major_triades(chord_progression, major_scale), expected)

    def test_get_progression_with_triades(self):
        chord_progression = ['Bb', 'F', 'Eb', 'Bb']
        triades = {'Bb': {'1st': ['D', 'F', 'Bb'],
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

        self.assertDictEqual(get_progression_with_triades(chord_progression, triades), expected_triade_progression)