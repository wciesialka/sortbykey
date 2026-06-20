from enum import Enum


class WheelOfFifths(Enum):
    Abm = ('Ab', 'minor', '1A')
    BM = ('B', 'major', '1B')
    Ebm = ('Eb', 'minor', '2A')
    FM = ('Gb', 'major', '2B')
    Bbm = ('Bb', 'minor', '3A')
    CM = ('C', 'major', '3B')
    Fm = ('F', 'minor', '4A')
    AbM = ('Ab', 'major', '4B')
    Cm = ('C', 'minor', '5A')
    EbM = ('Eb', 'major', '5B')
    Gm = ('G', 'minor', '6A')
    BbM = ('Bb', 'major', '6B')
    Dm = ('D', 'minor', '7A')
    FM_ = ('F', 'major', '7B')
    Am = ('A', 'minor', '8A')
    CM_ = ('C', 'major', '8B')
    Em = ('E', 'minor', '9A')
    GM = ('G', 'major', '9B')
    Bm = ('B', 'minor', '10A')
    DM = ('D', 'major', '10B')
    Fm_ = ('Gb', 'minor', '11A')
    AM = ('A', 'major', '11B')
    Cm_ = ('C', 'minor', '12A')
    EM = ('E', 'major', '12B')

    @staticmethod
    def normalize_note(note: str) -> str:
        """Convert sharp notation to flat notation."""
        sharp_to_flat = {
            'F#': 'Gb',
            'C#': 'Db',
            'G#': 'Ab',
            'D#': 'Eb',
            'A#': 'Bb',
        }
        return sharp_to_flat.get(note.upper(), note)

    @staticmethod
    def camelot_notation(root_note, scale):
        root_note = WheelOfFifths.normalize_note(root_note)
        for key in WheelOfFifths:
            if key.value[0] == root_note and key.value[1] == scale.lower():
                return key.value[2]
        return None
    
    @staticmethod
    def wheel_notation(camelot):
        for key in WheelOfFifths:
            if key.value[2] == camelot.upper():
                return (key.value[0], key.value[1])
    
    @staticmethod
    def is_camelot_notation(variable: str):        
        for key in WheelOfFifths:
            if variable == key.value[2]:
                return True
        return variable == "o"
