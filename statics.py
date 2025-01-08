
# Statics
NOTES_FLAT = ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
NOTES_SHARP = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
TUNING = ["E", "A", "D", "G", "B", "E"]
ROMAN_REGEX = r"(XV|XIV|XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I|xv|xiv|xiii|xii|xi|x|ix|viii|vii|vi|v|iv|iii|ii|i)(dim|aug|sus4|sus2|7)?"
DEFAULT_PATTERN = {
    "PATTERN_1": ["Root", "Root", "Root", "Root"],
    "PATTERN_2": ["1st", "1st", "1st", "1st"],
    "PATTERN_3": ["2nd", "2nd", "2nd", "2nd"],
}
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
    "7": {
        "formula": [1, 3, 5, 7]
    }
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