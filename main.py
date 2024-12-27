from copy import copy
from pprint import pprint

from tabulate import tabulate

# Variables
KEY = "Bb"
PROGRESSION = [1,5,4,1]

# Statics
NOTES_FLAT = ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
NOTES_SHARP = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
MAJOR_SCALE_FORMULA = [2,2,1,2,2,2,1]
MAJOR_TRIADE = {
    "root": [1, 3, 5],
    "1st": [3, 5, 1],
    "2nd": [5, 1, 3],
}
PATTERN_1 = ["Root", "1st", "2nd", "Root"]
PATTERN_2 = ["1st", "2nd", "Root", "1st"]
PATTERN_3 = ["2nd", "Root", "1st", "2nd"]
PATTERNS = {
    "PATTERN_1": PATTERN_1,
    "PATTERN_2": PATTERN_2,
    "PATTERN_3": PATTERN_3,
}

TUNING = ["E", "A", "D", "G", "B", "E"]


def get_major_scale_in_key(key):
    list_to_use = NOTES_SHARP
    if "b" in key:
        list_to_use = NOTES_FLAT

    # Find the starting index of the key in the notes list
    start_index = list_to_use.index(key)
    # Initialize the major scale with the root note
    major_scale = [key]
    # Generate the scale by applying the formula
    current_index = start_index
    for step in MAJOR_SCALE_FORMULA:
        current_index = (current_index + step) % len(list_to_use)  # Wrap around the list if necessary
        if list_to_use[current_index] not in major_scale:
            major_scale.append(list_to_use[current_index])
    return major_scale


def get_chords(current_key_major_scale, progression_formula):
    return [current_key_major_scale[degree - 1] for degree in progression_formula]

def get_major_triades(chord_progression, major_scale):
    triades = {}
    for note in chord_progression:
        root_index = major_scale.index(note)
        triades[note] = {
            inversion: [
                major_scale[(root_index + degree - 1) % len(major_scale)]
                for degree in formula
            ]
            for inversion, formula in MAJOR_TRIADE.items()
        }

    return triades

def get_progression_with_triades(chord_progression, triades):
    progression_with_triades = {}
    for pattern_name, pattern in PATTERNS.items():
        progression_with_triades[pattern_name] = [
            triades[chord][inversion.lower()] for chord, inversion in zip(chord_progression, pattern)
        ]
    return progression_with_triades


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


def get_tablature(progression_with_triades):
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
        for pattern_name, progression in progression_with_triades.items():
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
    # headers = ["Position", "Order", "Notes"]
    for key, notes in triades.items():
        line_root = ["root"] + notes["root"]
        line_1st = ["1st"] + notes["1st"]
        line_2nd = ["2nd"] + notes["2nd"]
        table = list()
        table.append(line_root)
        table.append(line_1st)
        table.append(line_2nd)
        print(tabulate(table, tablefmt="github"))
        print("\n")


def move_chord_plus_12(pattern):
    def add_12(note):
        return note + 12

    new_pattern = list()
    for chord in pattern:
        note_1 = chord[0]
        note_2 = chord[1]
        note_3 = chord[2]
        if note_1 < 8:
            note_1 = add_12(note_1)
        if note_2 < 8:
            note_2= add_12(note_2)
        if note_3 < 8:
            note_3= add_12(note_3)
        new_chord = (note_1, note_2, note_3)
        new_pattern.append(new_chord)
    return new_pattern

def remove_open_position(tablature):
    for string, patterns in tablature.items():
        for pattern_name, pattern in patterns.items():
            for chord in pattern:
                if 0 in chord: # if we find one zero, move the whole pattern to 12 position
                    tablature[string][pattern_name] = move_chord_plus_12(pattern)
                    break
    return tablature


if __name__ == '__main__':
    major_scale = get_major_scale_in_key(KEY)
    print(f"\n'{KEY}' major scale: {major_scale}")
    # Get chord list for major scale
    chord_progression = get_chords(major_scale, PROGRESSION)
    print(f"{PROGRESSION} chord progression in key of {KEY}: {chord_progression}\n")

    # Get triades for each chord of the progression
    triades = get_major_triades(chord_progression, major_scale)
    print("Triade in each note:\n")
    pretty_print_triade(triades)

    # Get all triade progression possibilities
    print("Patterns:\n")
    progression_with_triades = get_progression_with_triades(chord_progression, triades)
    for pattern_name, progression in progression_with_triades.items():
        print(f"{pattern_name}: {progression}")

    tablature = get_tablature(progression_with_triades)
    tablature = remove_open_position(tablature)

    pretty_print_tablature(tablature)




# TODO
# order pattern (12 a the end)
