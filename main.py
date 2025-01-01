import re
from copy import copy
from pprint import pprint

from tabulate import tabulate

# Variables
KEY = "Am"
# SCALE_MODE = "DIMINISHED"
# PROGRESSION = ["I", "V", "IV", "I"] # major
# PROGRESSION = [1,4,1,5] # minor
# PROGRESSION = ["i", "iv", "i", "v"] # minor
# PROGRESSION = ["VIIdim", "I","VIIdim", "vi"] # dim
PROGRESSION = ["IIIaug", "i"] # aug

# Statics
NOTES_FLAT = ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
NOTES_SHARP = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
TUNING = ["E", "A", "D", "G", "B", "E"]

SCALE_FORMULAS = {
    "MAJOR": {
        "formula": [2,2,1,2,2,2,1],
        "patterns": {
            "PATTERN_1": ["Root", "1st", "2nd", "Root"],
            "PATTERN_2": ["1st", "2nd", "Root", "1st"],
            "PATTERN_3": ["2nd", "Root", "1st", "2nd"]
        }
    },
    "MINOR": {
        "formula": [2,1,2,2,1,2,2],
        "patterns": {
            "PATTERN_1": ["1st", "Root", "1st", "2nd"],
            "PATTERN_2": ["Root", "2nd", "Root", "1st"],
            "PATTERN_3": ["2nd", "1st", "2nd", "Root"],
        }
    },
    "DIM": {
        "formula": [2,1,2,1,2,1,2,1],
        "patterns": {
            "PATTERN_1": ["Root", "Root", "Root", "Root"],
            "PATTERN_2": ["1st", "1st", "1st", "1st"],
            "PATTERN_3": ["2nd", "2nd", "2nd", "2nd"],
        }
    },
    "AUG": {
        "formula": [3,1,3,1,3,1],
        "patterns": {
            "PATTERN_1": ["2nd", "Root"],
            "PATTERN_2": ["1st", "2nd"],
            "PATTERN_3": ["Root", "1st"],
        }
    }
}

TRIADE_INVERSIONS = {
    "root": [1, 3, 5],
    "1st": [3, 5, 1],
    "2nd": [5, 1, 3],
}

ROMAN_REGEX = r"(XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I|xv|xiv|xiii|xii|xi|x|ix|viii|vii|vi|v|iv|iii|ii|i)(dim|aug)?"


class Chord(object):

    def __init__(self, roman_number):
        match = re.search(ROMAN_REGEX, roman_number)
        chord_key_roman = match.group(1)
        chord_key_integer = self._roman_to_int(chord_key_roman)

        self.quality = "MAJOR"
        if chord_key_roman.islower():
            self.quality = "MINOR"
        if match.group(2) is not None:
            self.quality = match.group(2).upper()
        base_scale = "MAJOR"
        key = KEY
        if "m" in KEY:
            key = key.replace("m", "")
            base_scale = "MINOR"
        chord_scale = self.get_scale_in_key(key, base_scale)
        self.name = chord_scale[chord_key_integer - 1]
        self.key_scale = self.get_scale_in_key(self.name, self.quality)
        self.triads = self.get_triads()

    def __str__(self):
        return self.name

    def _roman_to_int(self, s):
        s = s.upper()
        sum = 0
        prevValue = 0
        value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

        for c in s:
            currentValue = value[c]
            sum += (currentValue - 2 * prevValue) if (currentValue > prevValue) else currentValue
            prevValue = currentValue
        return sum

    def get_triads(self):
        triads = dict()
        index = 0
        root_index = self.key_scale.index(self.name)
        triads[self.name] = {
            inversion: [
                self.key_scale[(root_index + degree - 1) % len(self.key_scale)]
                for degree in formula
            ]
            for inversion, formula in TRIADE_INVERSIONS.items()
        }
        index += 1
        return triads

    def get_scale_in_key(self, key, scale_type):
        list_to_use = NOTES_SHARP
        if "b" in key:
            list_to_use = NOTES_FLAT

        scale_formula = copy(SCALE_FORMULAS[scale_type]["formula"])
        # Find the starting index of the key in the notes list
        start_index = list_to_use.index(key)
        # Initialize the scale with the root note
        current_scale = [key]
        # Generate the scale by applying the formula
        current_index = start_index
        for step in scale_formula:
            current_index = (current_index + step) % len(list_to_use)  # Wrap around the list if necessary
            if list_to_use[current_index] not in current_scale:
                current_scale.append(list_to_use[current_index])
        return current_scale

    def pretty_print_triade(self):
        headers = ["Position", "Note1", "Note2", "Note3"]
        for key, notes in self.triads.items():
            line_root = ["root"] + notes["root"]
            line_1st = ["1st"] + notes["1st"]
            line_2nd = ["2nd"] + notes["2nd"]
            table = list()
            table.append(line_root)
            table.append(line_1st)
            table.append(line_2nd)
            print(tabulate(table, headers, tablefmt="github"))

def get_chords(progression):
    chords = list()
    for chord_roman_number in progression:
        new_chord = Chord(chord_roman_number)
        chords.append(new_chord)
    return chords

def get_progression_with_triads(chord_progression):
    progression_with_triads = {}
    main_pattern = SCALE_FORMULAS[chord_progression[0].quality]["patterns"] # the pattern to use correspond to the first note of the progression
    for pattern_name, pattern in main_pattern.items():
        progression_with_triads[pattern_name] = list()
        for chord, inversion in zip(chord_progression, pattern):
            progression_with_triads[pattern_name].append(chord.triads[chord.name][inversion.lower()])
    return progression_with_triads

def get_string_notes(string):
    list_sharp = copy(NOTES_SHARP)
    list_flat = copy(NOTES_FLAT)
    start_index_sharp = list_sharp.index(string)
    list_sharp = list_sharp[start_index_sharp:] + list_sharp[:start_index_sharp]
    start_index_flat = list_flat.index(string)
    list_flat = list_flat[start_index_flat:] + list_flat[:start_index_flat]
    string_notes = {
        "#": list_sharp,
        "b": list_flat
    }
    return string_notes

def get_note_index_on_string(string, note):
    current_string_notes = get_string_notes(string)
    if note in current_string_notes["#"]:
        return current_string_notes["#"].index(note)
    else:
        return current_string_notes["b"].index(note)

def get_next_string(base_string):
    index_previous_string = TUNING.index(base_string)
    return TUNING[index_previous_string+1]

def get_tablature(progression_with_triads):
    tablature = {}
    number_string = 0
    for string in TUNING:
        tablature[string] = {
            "PATTERN_1": [],
            "PATTERN_2": [],
            "PATTERN_3": []
        }
        number_string = number_string + 1
        if number_string > 3:
            break # no more than 4 string for triade

    for string, patterns in tablature.items():
        # print(f"String: {string}")
        for pattern_name, progression in progression_with_triads.items():
            # print(pattern_name)
            root_string = string
            second_string = get_next_string(root_string)
            third_string = get_next_string(second_string)
            for triade in progression:
                first_note = get_note_index_on_string(root_string, triade[0])
                second_note = get_note_index_on_string(second_string, triade[1])
                third_note = get_note_index_on_string(third_string, triade[2])
                tablature[string][pattern_name].append((first_note, second_note, third_note))
    return tablature

def pretty_print_tablature(tablature):
    empty_string = "- - - - - - - - -    - - - - - - - - -   - - - - - - - - -"
    for string, patterns in tablature.items():
        print("\n")
        print(f"ROOT STRING: {string}")
        root_string = string
        second_string = get_next_string(root_string)
        third_string = get_next_string(second_string)

        string_after_third = list()
        for guitar_string in reversed(TUNING):
            if guitar_string == third_string:
                break
            print(f"{guitar_string}  | {empty_string}")

        # print(f"{third_string:<2} | {patterns['PATTERN_1'][0][2]:<2} - {patterns['PATTERN_1'][1][2]:<2} - {patterns['PATTERN_1'][2][2]:<2} - {patterns['PATTERN_1'][3][2]:<2}", end='')
        # print(f"    {patterns['PATTERN_2'][0][2]:<2} - {patterns['PATTERN_2'][1][2]:<2} - {patterns['PATTERN_2'][2][2]:<2} - {patterns['PATTERN_2'][3][2]:<2}", end='')
        # print(f"    {patterns['PATTERN_3'][0][2]:<2} - {patterns['PATTERN_3'][1][2]:<2} - {patterns['PATTERN_3'][2][2]:<2} - {patterns['PATTERN_3'][3][2]:<2}", flush=True)
        #
        # print(f"{second_string:<2} | {patterns['PATTERN_1'][0][1]:<2} - {patterns['PATTERN_1'][1][1]:<2} - {patterns['PATTERN_1'][2][1]:<2} - {patterns['PATTERN_1'][3][1]:<2}", end='')
        # print(f"    {patterns['PATTERN_2'][0][1]:<2} - {patterns['PATTERN_2'][1][1]:<2} - {patterns['PATTERN_2'][2][1]:<2} - {patterns['PATTERN_2'][3][1]:<2}", end='')
        # print(f"    {patterns['PATTERN_3'][0][1]:<2} - {patterns['PATTERN_3'][1][1]:<2} - {patterns['PATTERN_3'][2][1]:<2} - {patterns['PATTERN_3'][3][1]:<2}", flush=True)
        #
        # print(f"{root_string:<2} | {patterns['PATTERN_1'][0][0]:<2} - {patterns['PATTERN_1'][1][0]:<2} - {patterns['PATTERN_1'][2][0]:<2} - {patterns['PATTERN_1'][3][0]:<2}", end='')
        # print(f"    {patterns['PATTERN_2'][0][0]:<2} - {patterns['PATTERN_2'][1][0]:<2} - {patterns['PATTERN_2'][2][0]:<2} - {patterns['PATTERN_2'][3][0]:<2}", end='')
        # print(f"    {patterns['PATTERN_3'][0][0]:<2} - {patterns['PATTERN_3'][1][0]:<2} - {patterns['PATTERN_3'][2][0]:<2} - {patterns['PATTERN_3'][3][0]:<2}", flush=True)

        print(f"{third_string:<2} | {patterns['PATTERN_1'][0][2]:<2} - {patterns['PATTERN_1'][1][2]:<2}", end='')
        print(f"    {patterns['PATTERN_2'][0][2]:<2} - {patterns['PATTERN_2'][1][2]:<2} ", end='')
        print(f"    {patterns['PATTERN_3'][0][2]:<2} - {patterns['PATTERN_3'][1][2]:<2} ", flush=True)

        print(f"{second_string:<2} | {patterns['PATTERN_1'][0][1]:<2} - {patterns['PATTERN_1'][1][1]:<2}", end='')
        print(f"    {patterns['PATTERN_2'][0][1]:<2} - {patterns['PATTERN_2'][1][1]:<2}", end='')
        print(f"    {patterns['PATTERN_3'][0][1]:<2} - {patterns['PATTERN_3'][1][1]:<2}", flush=True)

        print(f"{root_string:<2} | {patterns['PATTERN_1'][0][0]:<2} - {patterns['PATTERN_1'][1][0]:<2}", end='')
        print(f"    {patterns['PATTERN_2'][0][0]:<2} - {patterns['PATTERN_2'][1][0]:<2}", end='')
        print(f"    {patterns['PATTERN_3'][0][0]:<2} - {patterns['PATTERN_3'][1][0]:<2}", flush=True)

        string_before_root = list()
        for i in range(len(TUNING)):
            if TUNING[i] == root_string:
                break
            guitar_string = f"{TUNING[i]}  | {empty_string}"
            string_before_root.append(guitar_string)
        for i in reversed(string_before_root):
            print(i)

def move_chord_plus_12(pattern):
    return [
        tuple(note + 12 if note < 7 else note for note in chord)
        for chord in pattern
    ]

def remove_open_position(tablature):
    for string, patterns in tablature.items():
        for pattern_name, pattern in patterns.items():
            for chord in pattern:
                if 0 in chord and (10 in chord or 11 in chord): # if we find one zero, move the whole pattern to 12 position
                    tablature[string][pattern_name] = move_chord_plus_12(pattern)
                    break
    return tablature


def order_patterns_by_value(tablature):
    for string, patterns in tablature.items():
        # Extract and sort the contents of the patterns
        sorted_contents = sorted(patterns.values(), key=lambda pattern: sum(sum(chord) for chord in pattern))
        # Reassign the sorted contents to the original keys
        reordered_patterns = {key: content for key, content in zip(patterns.keys(), sorted_contents)}
        tablature[string] = reordered_patterns
    return tablature


if __name__ == '__main__':
    chord_progression = get_chords(PROGRESSION)
    print(f"Progression: {PROGRESSION}. Chords in key of {KEY}: " + ' '.join(str(x) for x in chord_progression))

    # Get triads for each chord of the progression
    # triads = get_triads(chord_progression)
    print("Triad in each note:\n")
    for chord in chord_progression:
        print(f"Triad of chord: {chord.name} {chord.quality}")
        chord.pretty_print_triade()
        print("\n")

    # Get all triade progression possibilities
    print("Patterns:\n")
    progression_with_triads = get_progression_with_triads(chord_progression)
    for pattern_name, progression in progression_with_triads.items():
        print(f"{pattern_name}: {progression}")

    tablature = get_tablature(progression_with_triads)
    tablature = remove_open_position(tablature)
    tablature = order_patterns_by_value(tablature)
    pretty_print_tablature(tablature)

