from copy import copy

from statics import *


def roman_to_int(s):
    s = s.upper()
    sum = 0
    prevValue = 0
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    for c in s:
        currentValue = value[c]
        sum += (currentValue - 2 * prevValue) if (currentValue > prevValue) else currentValue
        prevValue = currentValue
    return sum

def get_flat_or_sharp_note(base_note, letter):
    list_to_use = NOTES_SHARP
    if "b" in base_note:
        list_to_use = NOTES_FLAT
    index = list_to_use.index(base_note)
    if letter == "b":  # return previous note (flat)
        return list_to_use[(index - 1) % len(list_to_use)]
    if letter == "#": # return the next note (sharp)
        return list_to_use[(index + 1) % len(list_to_use)]

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