def get_english_score(input_bytes):
    # From http://norvig.com/mayzner.html
    char_scores = {
        'E': 1249, 'T': 928, 'A': 804, 'O': 764, 'I': 757, 'N': 723, 'S': 651, 'R': 628, 'H': 505, 'L': 407,
        'D': 382, 'C': 334, 'U': 273, 'M': 251, 'F': 240, 'P': 214, 'G': 187, 'W': 168, 'Y': 166, 'B': 148,
        'V': 105, 'K': 54, 'X': 23, 'J': 16, 'Q': 12, 'Z': 9}

    return sum([char_scores.get(chr(byte), 0) for byte in input_bytes.upper()])
