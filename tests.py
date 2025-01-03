from main import get_progression_with_triads, get_tablature, \
    remove_open_position, order_patterns_by_value, Chord, get_flat_or_sharp_note, NOTES_SHARP, ChordProgression

import unittest


class TestChordGenerator(unittest.TestCase):

    def _do_test_chord(self, chord, expected_key_scale, expected_name, expected_quality, expected_triads):
        self.assertListEqual(expected_key_scale, chord.chord_scale)
        self.assertEqual(expected_name, chord.root_note)
        self.assertEqual(expected_quality, chord.quality)
        self.assertDictEqual(expected_triads, chord.triads)

    def test_get_flat_note(self):
        self.assertEqual(get_flat_or_sharp_note("G#", "b"), "G")
        self.assertEqual(get_flat_or_sharp_note("A", "b"), "G#")
        self.assertEqual(get_flat_or_sharp_note("A", "#"), "A#")
        self.assertEqual(get_flat_or_sharp_note("G#", "#"), "A")

    def test_chord_model_major(self):
        chord_progression = ChordProgression("I", key="C")
        expected_key_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        expected_name = "C"
        expected_quality = "MAJOR"
        expected_triads = {'C': {'1st': ['E', 'G', 'C'], '2nd': ['G', 'C', 'E'], 'root': ['C', 'E', 'G']}}
        new_chord = Chord(chord_progression, "I")
        self._do_test_chord(new_chord, expected_key_scale, expected_name, expected_quality, expected_triads)

    def test_chord_model_minor(self):
        chord_progression = ChordProgression("i", key="E")
        expected_key_scale = ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']
        expected_name = "E"
        expected_quality = "MINOR"
        expected_triads = {'E': {'1st': ['G', 'B', 'E'], '2nd': ['B', 'E', 'G'], 'root': ['E', 'G', 'B']}}
        new_chord = Chord(chord_progression, "i")
        self._do_test_chord(new_chord, expected_key_scale, expected_name, expected_quality, expected_triads)

    def test_chord_model_diminished(self):
        chord_progression = ChordProgression("VIIdim", key="F")
        expected_key_scale = ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']
        expected_name = "E"
        expected_quality = "DIM"
        expected_triads = {'E': {'1st': ['G', 'A#', 'E'], '2nd': ['A#', 'E', 'G'], 'root': ['E', 'G', 'A#']}}
        new_chord = Chord(chord_progression, "VIIdim")
        self._do_test_chord(new_chord, expected_key_scale, expected_name, expected_quality, expected_triads)

    def test_chord_model_augmented(self):
        chord_progression = ChordProgression("IIIaug", key="Am")
        expected_key_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        expected_name = "C"
        expected_quality = "AUG"
        expected_triads = {'C': {'1st': ['E', 'G#', 'C'], '2nd': ['G#', 'C', 'E'], 'root': ['C', 'E', 'G#']}}
        new_chord = Chord(chord_progression, "IIIaug")
        self._do_test_chord(new_chord, expected_key_scale, expected_name, expected_quality, expected_triads)

    def test_chord_model_sus2(self):
        chord_progression = ChordProgression("Isus2", key="C")
        expected_key_scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        expected_name = "C"
        expected_quality = "SUS2"
        expected_triads = {'C': {'1st': ['D', 'G', 'C'], '2nd': ['G', 'C', 'D'], 'root': ['C', 'D', 'G']}}
        new_chord = Chord(chord_progression, "Isus2")
        self._do_test_chord(new_chord, expected_key_scale, expected_name, expected_quality, expected_triads)

    def test_get_progression_with_triads(self):
        chord_progression = ChordProgression(progression_list_as_roman_number=["I", "V", "IV", "I"], key="C")
        chord_progression.generate_chords()
        expected_triade_progression =  {'PATTERN_1': [['C', 'E', 'G'], ['B', 'D', 'G'], ['C', 'F', 'A'], ['C', 'E', 'G']],
                                        'PATTERN_2': [['E', 'G', 'C'], ['D', 'G', 'B'], ['F', 'A', 'C'], ['E', 'G', 'C']],
                                        'PATTERN_3': [['G', 'C', 'E'], ['G', 'B', 'D'], ['A', 'C', 'F'], ['G', 'C', 'E']]}
        self.assertDictEqual(get_progression_with_triads(chord_progression), expected_triade_progression)

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
