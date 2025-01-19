from copy import copy
from random import shuffle
from statics import NOTES_SHARP

# Define the tuning of the strings along with their starting pitches
TUNING = {
    "E": 2,  # E2
    "A": 2,  # A2
    "D": 3,  # D3
    "G": 3,  # G3
    "B": 3,  # B3
    "e": 4   # E4
}

def get_string_notes(string, starting_pitch):
    """
    Generate notes for a string including their pitches.

    :param string: The note name of the string (e.g., "E").
    :param starting_pitch: The starting pitch number for the string.
    :return: A list of notes with their corresponding pitches.
    """
    list_sharp = copy(NOTES_SHARP)
    start_index_sharp = list_sharp.index(string.upper())
    list_sharp = list_sharp[start_index_sharp:] + list_sharp[:start_index_sharp]

    notes_with_pitch = []
    pitch = starting_pitch

    for i, note in enumerate(list_sharp * 2):  # Repeat the notes to cover 24 frets
        if i > 0 and note == "C":
            pitch += 1  # Increment pitch at each "C"
        notes_with_pitch.append(f"{note}{pitch}")

    return notes_with_pitch[:24]  # Return the first 24 notes (0-23 frets)

class Challenge:
    def __init__(self, current_string="E"):
        self.fretboard = self.build_fret_board()
        self.current_string = current_string
        self.current_position = "before_12"
        self.current_note_to_find = None

    def start(self):
        still_to_be_discovered_notes_before_12 = copy(self.fretboard[self.current_string]["before_12"])
        still_to_be_discovered_notes_after_12 = copy(self.fretboard[self.current_string]["after_12"])
        both_list = list(zip(still_to_be_discovered_notes_before_12,
                             still_to_be_discovered_notes_after_12))
        shuffle(both_list)
        still_to_be_discovered_notes_before_12, still_to_be_discovered_notes_after_12 = zip(*both_list)
        self.still_to_be_discovered_notes = dict()
        self.still_to_be_discovered_notes["before_12"] = list(still_to_be_discovered_notes_before_12)
        self.still_to_be_discovered_notes["after_12"] = list(still_to_be_discovered_notes_after_12)
        # # test
        # self.still_to_be_discovered_notes = {'after_12': ['G3', 'F#3'],
        #                                      'before_12': ['G2', 'F#2']}

        self.current_note_to_find = self.still_to_be_discovered_notes["before_12"].pop(0)
        print(f"Current note to find: {self.current_note_to_find}")

    def build_fret_board(self):
        """
        Build the fretboard dictionary with notes and their pitches.
        """
        fretboard = {}
        for string, starting_pitch in TUNING.items():
            fretboard[string] = {
                "before_12": get_string_notes(string, starting_pitch)[:12],
                "after_12": get_string_notes(string, starting_pitch)[12:24],
            }
        return fretboard

    def validate_note(self, detected_note):
        if detected_note == self.current_note_to_find:
            print(f"note found: {detected_note}")
            self.next_note()
            return True
        return False

    def next_note(self):
        # print(f"won: {challenge.is_won()}")
        if self.current_position == "before_12":
            self.current_position = "after_12"
        else:
            self.current_position = "before_12"
        if len(self.still_to_be_discovered_notes[self.current_position]) > 0:
            self.current_note_to_find = self.still_to_be_discovered_notes[self.current_position].pop(0)
        else:
            self.current_note_to_find = None
        print(f"Current note to find: {self.current_note_to_find}")
        return self.current_note_to_find

    def is_won(self):
        if self.current_note_to_find is None:
            return len(self.still_to_be_discovered_notes["before_12"]) == 0 and len(self.still_to_be_discovered_notes["after_12"]) == 0
        return False

# challenge = Challenge()
#
# challenge.validate_note("E4")
# challenge.validate_note("G2")
# challenge.validate_note("G3")
# challenge.validate_note("F#2")
# challenge.validate_note("F#3")

