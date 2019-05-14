import os


def get_english_score(input_bytes):
    # From http://norvig.com/mayzner.html
    char_scores = {
        'E': 1249, 'T': 928, 'A': 804, 'O': 764, 'I': 757, 'N': 723, 'S': 651, 'R': 628, 'H': 505, 'L': 407,
        'D': 382, 'C': 334, 'U': 273, 'M': 251, 'F': 240, 'P': 214, 'G': 187, 'W': 168, 'Y': 166, 'B': 148,
        'V': 105, 'K': 54, 'X': 23, 'J': 16, 'Q': 12, 'Z': 9, ' ': 6, '\'': 4, '.': 4, '!': 3, '$': 1}

    # If the bytes are an invalid utf8 string return a 0.
    try:
        input_bytes.decode('utf8')
    except:
        return 0

    return sum([char_scores.get(chr(byte), -5000) for byte in input_bytes.upper()])


def attempt_decryption(input, line_no):
    input_bytes = bytes.fromhex(input)
    decrypted = []

    for n in range(256):
        raw = bytearray([byte ^ n for byte in input_bytes])
        score = get_english_score(raw)
        decrypted.append({'score': score, 'data': raw,
                          'key': n, 'line': line_no})

    decrypted.sort(key=lambda s: s['score'], reverse=True)
    del decrypted[5:-1]
    return decrypted


master_list = []
line_no = 1
script_dir = os.path.dirname(os.path.realpath(__file__))
input_fd = os.path.join(script_dir, '4.txt')
with open(input_fd, 'r') as f:
    for line in f:
        master_list += (attempt_decryption(line, line_no))
        line_no += 1

master_list.sort(key=lambda s: s['score'], reverse=True)

for i in range(4):
    print(master_list[i])
