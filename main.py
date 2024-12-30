from copy import copy
from pprint import pprint

from tabulate import tabulate

# Variables
KEY = "G"
SCALE_MODE = "MINOR"
PROGRESSION = [1,4,1,5]

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
    }
}

TRIADE_INVERSIONS = {
    "root": [1, 3, 5],
    "1st": [3, 5, 1],
    "2nd": [5, 1, 3],
}


def get_scale_in_key(key, scale_type):
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


def get_chords(current_key_scale, progression_formula):
    return [current_key_scale[degree - 1] for degree in progression_formula]

def get_triads(chord_progression, scale):
    triads = {}
    for note in chord_progression:
        root_index = scale.index(note)
        triads[note] = {
            inversion: [
                scale[(root_index + degree - 1) % len(scale)]
                for degree in formula
            ]
            for inversion, formula in TRIADE_INVERSIONS.items()
        }

    return triads

def get_progression_with_triads(chord_progression, triads, scale_mode):
    progression_with_triads = {}
    for pattern_name, pattern in SCALE_FORMULAS[scale_mode]["patterns"].items():
        progression_with_triads[pattern_name] = [
            triads[chord][inversion.lower()] for chord, inversion in zip(chord_progression, pattern)
        ]
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

        print(f"{third_string:<2} | {patterns['PATTERN_1'][0][2]:<2} - {patterns['PATTERN_1'][1][2]:<2} - {patterns['PATTERN_1'][2][2]:<2} - {patterns['PATTERN_1'][3][2]:<2}", end='')
        print(f"    {patterns['PATTERN_2'][0][2]:<2} - {patterns['PATTERN_2'][1][2]:<2} - {patterns['PATTERN_2'][2][2]:<2} - {patterns['PATTERN_2'][3][2]:<2}", end='')
        print(f"    {patterns['PATTERN_3'][0][2]:<2} - {patterns['PATTERN_3'][1][2]:<2} - {patterns['PATTERN_3'][2][2]:<2} - {patterns['PATTERN_3'][3][2]:<2}", flush=True)

        print(f"{second_string:<2} | {patterns['PATTERN_1'][0][1]:<2} - {patterns['PATTERN_1'][1][1]:<2} - {patterns['PATTERN_1'][2][1]:<2} - {patterns['PATTERN_1'][3][1]:<2}", end='')
        print(f"    {patterns['PATTERN_2'][0][1]:<2} - {patterns['PATTERN_2'][1][1]:<2} - {patterns['PATTERN_2'][2][1]:<2} - {patterns['PATTERN_2'][3][1]:<2}", end='')
        print(f"    {patterns['PATTERN_3'][0][1]:<2} - {patterns['PATTERN_3'][1][1]:<2} - {patterns['PATTERN_3'][2][1]:<2} - {patterns['PATTERN_3'][3][1]:<2}", flush=True)

        print(f"{root_string:<2} | {patterns['PATTERN_1'][0][0]:<2} - {patterns['PATTERN_1'][1][0]:<2} - {patterns['PATTERN_1'][2][0]:<2} - {patterns['PATTERN_1'][3][0]:<2}", end='')
        print(f"    {patterns['PATTERN_2'][0][0]:<2} - {patterns['PATTERN_2'][1][0]:<2} - {patterns['PATTERN_2'][2][0]:<2} - {patterns['PATTERN_2'][3][0]:<2}", end='')
        print(f"    {patterns['PATTERN_3'][0][0]:<2} - {patterns['PATTERN_3'][1][0]:<2} - {patterns['PATTERN_3'][2][0]:<2} - {patterns['PATTERN_3'][3][0]:<2}", flush=True)
        string_before_root = list()
        for i in range(len(TUNING)):
            if TUNING[i] == root_string:
                break
            guitar_string = f"{TUNING[i]}  | {empty_string}"
            string_before_root.append(guitar_string)
        for i in reversed(string_before_root):
            print(i)



def pretty_print_triade(triades):
    headers = ["Position", "Note1", "Note2", "Note3"]
    for key, notes in triades.items():
        line_root = ["root"] + notes["root"]
        line_1st = ["1st"] + notes["1st"]
        line_2nd = ["2nd"] + notes["2nd"]
        table = list()
        table.append(line_root)
        table.append(line_1st)
        table.append(line_2nd)
        print(tabulate(table, headers, tablefmt="github"))
        print("\n")


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

    scale = get_scale_in_key(KEY, SCALE_MODE)
    print(f"\n'{KEY}' {SCALE_MODE} scale: {scale}")
    # Get chord list for major scale
    chord_progression = get_chords(scale, PROGRESSION)
    print(f"{PROGRESSION} chord progression in key of {KEY} {SCALE_MODE}: {chord_progression}\n")

    # Get triads for each chord of the progression
    triads = get_triads(chord_progression, scale)
    print("Triade in each note:\n")
    pretty_print_triade(triads)

    # Get all triade progression possibilities
    print("Patterns:\n")
    progression_with_triads = get_progression_with_triads(chord_progression, triads, SCALE_MODE)
    for pattern_name, progression in progression_with_triads.items():
        print(f"{pattern_name}: {progression}")

    tablature = get_tablature(progression_with_triads)
    tablature = remove_open_position(tablature)
    tablature = order_patterns_by_value(tablature)

    pretty_print_tablature(tablature)

