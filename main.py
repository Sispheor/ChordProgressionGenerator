import re
from copy import copy

from tabulate import tabulate

# Variables
KEY = "C"
# PROGRESSION = ["I", "V", "IV", "I"] # major
# PROGRESSION = ["i", "iv", "i", "v"] # minor
# PROGRESSION = ["VIIdim", "I","VIIdim", "vi"] # dim
# PROGRESSION = ["IIIaug", "i"] # aug
PROGRESSION = ["I", "Isus4", "I", "Isus2"] # sus
DEFAULT_PATTERN = {
    "PATTERN_1": ["Root", "Root", "Root", "Root"],
    "PATTERN_2": ["1st", "1st", "1st", "1st"],
    "PATTERN_3": ["2nd", "2nd", "2nd", "2nd"],
}

# Statics
NOTES_FLAT = ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
NOTES_SHARP = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
TUNING = ["E", "A", "D", "G", "B", "E"]
ROMAN_REGEX = r"(XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I|xv|xiv|xiii|xii|xi|x|ix|viii|vii|vi|v|iv|iii|ii|i)(dim|aug|sus4|sus2)?"

CHORD_FORMULAS = {
    "MAJOR": {
        "formula": [1, 3, 5]
    },
    "MINOR": {
        "formula": [1, "b3", 5]
    },
    "DIM": {
        "formula": [1, "b3", "b5"]
    },
    "AUG": {
        "formula": [1, 3, "#5"]
    },
    "SUS2": {
        "formula": [1, 2, 5]
    },
    "SUS4": {
        "formula": [1, 4, 5]
    },
}

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
    },
    "SUS2": {
        "patterns": {
            "PATTERN_1": ["Root", "Root", "Root", "Root"],
            "PATTERN_2": ["1st", "1st", "1st", "1st"],
            "PATTERN_3": ["2nd", "2nd", "2nd", "2nd"],
        }
    },
    "SUS4": {
        "patterns": {
            "PATTERN_1": ["Root", "Root", "Root", "Root"],
            "PATTERN_2": ["1st", "1st", "1st", "1st"],
            "PATTERN_3": ["2nd", "2nd", "2nd", "2nd"],
        }
    }
}

class ChordProgression(object):

    def __init__(self, progression_list_as_roman_number, key):
        self.progression_list_as_roman_number = progression_list_as_roman_number
        self.key = key
        self.base_scale = "MAJOR"
        if "m" in self.key:
            self.key = self.key.replace("m", "")
            self.base_scale = "MINOR"
        self.chords = list()
        self.key_scale = get_scale_in_key(self.key, self.base_scale)

    def generate_chords(self):
        for chord_roman_number in self.progression_list_as_roman_number:
            new_chord = Chord(self, chord_roman_number)
            self.chords.append(new_chord)

    def pretty_print(self):
        print(f"Progression: {self.progression_list_as_roman_number}")
        list_chord_name = [chord.root_note for chord in self.chords]
        print(f"Chords: {list_chord_name}\n")
        for chord in self.chords:
            print(f"Triad inversions of chord '{chord.root_note}' {chord.quality}")
            chord.pretty_print_triads()
            print("\n")


class Chord(object):

    def __init__(self, progression, roman_number):
        self.progression = progression
        match = re.search(ROMAN_REGEX, roman_number)
        root_note_roman = match.group(1)
        root_note_integer = _roman_to_int(root_note_roman)
        self.root_note = self.progression.key_scale[root_note_integer - 1]

        self.quality = "MAJOR"
        if root_note_roman.islower():
            self.quality = "MINOR"
        if match.group(2) is not None:
            self.quality = match.group(2).upper()

        self.chord_scale = get_scale_in_key(self.root_note) # always based on major scale
        self.triads = self.get_triads()

    def __str__(self):
        return self.root_note

    def get_triads(self):
        triads = dict()
        triads[self.root_note] = dict()
        chord_formula = CHORD_FORMULAS[self.quality]["formula"]
        root = list()
        for degree in chord_formula:
            if isinstance(degree, int):
                root.append(self.chord_scale[degree - 1])
            else:
                # we have a string
                number_letter_regex = r"(.)(\d)"
                match = re.search(number_letter_regex, degree)
                letter = match.group(1)
                position = match.group(2)
                base_note = self.chord_scale[int(position) -1]
                new_note = get_flat_or_sharp_note(base_note, letter)
                root.append(new_note)

        first_inversion = root[1:] + [root[0]]
        second_inversion = first_inversion[1:] + [first_inversion[0]]
        triads[self.root_note]["root"] = root
        triads[self.root_note]["1st"] = first_inversion
        triads[self.root_note]["2nd"] = second_inversion

        return triads

    def pretty_print_triads(self):
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


def _roman_to_int(s):
    s = s.upper()
    sum = 0
    prevValue = 0
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    for c in s:
        currentValue = value[c]
        sum += (currentValue - 2 * prevValue) if (currentValue > prevValue) else currentValue
        prevValue = currentValue
    return sum

def get_scale_in_key(key, base_scale="MAJOR"):
    list_to_use = NOTES_SHARP
    if "b" in key:
        list_to_use = NOTES_FLAT
    scale_formula = copy(SCALE_FORMULAS[base_scale]["formula"])
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

def get_flat_or_sharp_note(base_note, letter):
    list_to_use = NOTES_SHARP
    if "b" in base_note:
        list_to_use = NOTES_FLAT
    index = list_to_use.index(base_note)
    if letter == "b":  # return previous note (flat)
        return list_to_use[(index - 1) % len(list_to_use)]
    if letter == "#": # return the next note (sharp)
        return list_to_use[(index + 1) % len(list_to_use)]

def get_progression_with_triads(chord_progression):
    progression_with_triads = {}
    main_pattern = SCALE_FORMULAS[chord_progression.chords[0].quality]["patterns"]  # the pattern to use correspond to the first note of the progression
    for chord in chord_progression.progression_list_as_roman_number:
        if "sus" in chord:
            main_pattern = DEFAULT_PATTERN
            break

    for pattern_name, pattern in main_pattern.items():
        progression_with_triads[pattern_name] = list()
        for chord, inversion in zip(chord_progression.chords, pattern):
            progression_with_triads[pattern_name].append(chord.triads[chord.root_note][inversion.lower()])
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
    def format_pattern_line(string, patterns, idx):
        return (
            f"{string:<2} | "
            f"{patterns['PATTERN_1'][0][idx]:<2} - {patterns['PATTERN_1'][1][idx]:<2} - {patterns['PATTERN_1'][2][idx]:<2} - {patterns['PATTERN_1'][3][idx]:<2}    "
            f"{patterns['PATTERN_2'][0][idx]:<2} - {patterns['PATTERN_2'][1][idx]:<2} - {patterns['PATTERN_2'][2][idx]:<2} - {patterns['PATTERN_2'][3][idx]:<2}    "
            f"{patterns['PATTERN_3'][0][idx]:<2} - {patterns['PATTERN_3'][1][idx]:<2} - {patterns['PATTERN_3'][2][idx]:<2} - {patterns['PATTERN_3'][3][idx]:<2}"
        )

    def format_short_pattern_line(string, patterns, idx):
        return (
            f"{string:<2} | "
            f"{patterns['PATTERN_1'][0][idx]:<2} - {patterns['PATTERN_1'][1][idx]:<2}    "
            f"{patterns['PATTERN_2'][0][idx]:<2} - {patterns['PATTERN_2'][1][idx]:<2}    "
            f"{patterns['PATTERN_3'][0][idx]:<2} - {patterns['PATTERN_3'][1][idx]:<2}"
        )

    empty_string = "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

    for string, patterns in tablature.items():
        print("\n")
        print(f"ROOT STRING: {string}")
        root_string = string
        second_string = get_next_string(root_string)
        third_string = get_next_string(second_string)

        # Print strings above the third string
        for guitar_string in reversed(TUNING):
            if guitar_string == third_string:
                break
            print(f"{guitar_string}  | {empty_string}")

        # Print patterns
        if len(patterns['PATTERN_1']) > 2:
            print(format_pattern_line(third_string, patterns, 2))
            print(format_pattern_line(second_string, patterns, 1))
            print(format_pattern_line(root_string, patterns, 0))
        else:
            print(format_short_pattern_line(third_string, patterns, 2))
            print(format_short_pattern_line(second_string, patterns, 1))
            print(format_short_pattern_line(root_string, patterns, 0))

        # Print strings below the root string
        strings_before_root = []
        for guitar_string in TUNING:
            if guitar_string == root_string:
                break
            strings_before_root.append(f"{guitar_string}  | {empty_string}")

        for line in reversed(strings_before_root):
            print(line)


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
    chord_progression = ChordProgression(PROGRESSION, KEY)
    chord_progression.generate_chords()
    chord_progression.pretty_print()

    # Get all triade progression possibilities
    print("Patterns:\n")
    progression_with_triads = get_progression_with_triads(chord_progression)
    for pattern_name, progression in progression_with_triads.items():
        print(f"{pattern_name}: {progression}")

    tablature = get_tablature(progression_with_triads)
    tablature = remove_open_position(tablature)
    tablature = order_patterns_by_value(tablature)
    pretty_print_tablature(tablature)

