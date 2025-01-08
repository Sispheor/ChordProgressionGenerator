import re
from copy import copy

from tabulate import tabulate

from utils import roman_to_int, get_flat_or_sharp_note, get_next_string, get_note_index_on_string
from statics import *

# Variables
KEY = "C"
# PROGRESSION = ["I", "V", "IV", "I"] # major
# PROGRESSION = ["i", "iv", "i", "v"] # minor
# PROGRESSION = ["VIIdim", "I","VIIdim", "vi"] # dim
# PROGRESSION = ["IIIaug", "i"] # aug
PROGRESSION = ["I", "Isus4", "I", "Isus2"] # sus
# PROGRESSION = ["I7", "iii", "ii7", "iv7"] # 7th

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
        print(f"Progression:    {self.progression_list_as_roman_number}")
        list_chords = list()
        for chord in self.chords:
            list_chords.append(f"{chord.root_note} {chord.quality}")
        print(f"Chords:         {list_chords}\n")

        for chord in self.chords:
            print(f"Notes of chord '{chord.root_note}' {chord.quality}")
            chord.pretty_print_notes()
            print("\n")
            chord.print_tab()


class Chord(object):

    def __init__(self, progression, roman_number):
        self.progression = progression
        match = re.search(ROMAN_REGEX, roman_number)
        root_note_roman = match.group(1)
        root_note_integer = roman_to_int(root_note_roman)
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

        triads[self.root_note]["root"] = root
        if self.quality != "7":
            first_inversion = root[1:] + [root[0]]
            second_inversion = first_inversion[1:] + [first_inversion[0]]
            triads[self.root_note]["1st"] = first_inversion
            triads[self.root_note]["2nd"] = second_inversion

        return triads

    def pretty_print_notes(self):
        headers = ["Inversion"]
        for key, notes in self.triads.items():
            note_number = 1
            for note in notes["root"]:
                headers.append(f"Note {note_number}")
                note_number += 1
        for key, notes in self.triads.items():
            table = list()
            line_root = ["root"] + notes["root"]
            table.append(line_root)
            if self.quality != "7":
                line_1st = ["1st"] + notes["1st"]
                line_2nd = ["2nd"] + notes["2nd"]
                table.append(line_1st)
                table.append(line_2nd)
            print(tabulate(table, headers, tablefmt="github"))

    @property
    def tablature_note(self):
        max_string_can_be_used = (len(TUNING) - len(self.triads[self.root_note]["root"])) + 1
        tablature = dict()
        for string_index in range(max_string_can_be_used):
            current_string = TUNING[string_index]
            tablature[current_string] = list()
        for root_string, list_note in tablature.items():
            list_chord = list()
            for position_name, notes in self.triads[self.root_note].items():
                current_string = root_string
                list_note = list()
                for note in notes:
                    current_string_note_index =  get_note_index_on_string(current_string, note)
                    list_note.append(current_string_note_index)
                    current_string = get_next_string(current_string)
                list_chord.append(list_note)
            tablature[root_string] = list_chord
        return tablature

    def print_tab(self):
        # Nombre total d'accords
        num_chords = max(len(chords) for chords in self.tablature_note.values())

        # Initialiser une ligne vide pour chaque corde
        lines = {string: [] for string in TUNING}

        # Parcourir chaque accord
        for chord_index in range(num_chords):
            # Créer un accord pour chaque corde
            for string_index, string in enumerate(reversed(TUNING)):  # Parcours des cordes dans l'ordre inversé
                # Trouver la note correspondante dans cet accord
                if string in self.tablature_note and chord_index < len(self.tablature_note[string]):
                    # Obtenir la note sur cette corde pour cet accord
                    note = self.tablature_note[string][chord_index][string_index] if string_index < len(
                        self.tablature_note[string][chord_index]) else "-"
                    lines[string].append(str(note))
                else:
                    # Si aucune donnée, ajouter un "-"
                    lines[string].append("-")
            # Ajouter un espace entre les accords
            for line in lines.values():
                line.append("-")

        # Construire la tablature sous forme de chaîne
        result = []
        for string in reversed(TUNING):  # Afficher dans l'ordre E aigu à E grave
            line = f"{string} | " + " ".join(lines[string])
            result.append(line)

        print("\n".join(result))


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

    # # Get all triad progression possibilities
    # print("Patterns:\n")
    # progression_with_triads = get_progression_with_triads(chord_progression)
    # for pattern_name, progression in progression_with_triads.items():
    #     print(f"{pattern_name}: {progression}")
    #
    # tablature = get_tablature(progression_with_triads)
    # tablature = remove_open_position(tablature)
    # tablature = order_patterns_by_value(tablature)
    # pretty_print_tablature(tablature)

