
letras = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 
    'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 
    'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 
    'W': 22, 'X': 23, 'Y': 24, 'Z': 25
}

frequencia_letras = {
    "E": 12.02, "T": 9.10, "A": 8.12, "O": 7.68, "I": 7.31,
    "N": 6.95, "S": 6.28, "R": 6.02, "H": 5.92, "D": 4.32, 
    "L": 3.98, "U": 2.88, "C": 2.71, "M": 2.61, "F": 2.30,
    "Y": 2.11, "W": 2.09, "G": 2.03, "P": 1.82, "B": 1.49,
    "V": 1.11, "K": 0.69, "X": 0.17, "Q": 0.11, "J": 0.10,
    "Z": 0.07
}

def ShiftCipher(plaintext, key):
    cipher_text = ''
    print(f'\nCodificando {plaintext} por Shift Cipher...\n')

    for letter in plaintext:
        if letter.upper() in letras:
            a = letras[letter.upper()]
            c = (a + key) % 26

            cipher_letter = [letra for letra, num in letras.items() if num == c][0]
            cipher_text += cipher_letter
        else:
            cipher_text += letter
    print(f'Texto codificado: {cipher_text}\n')
    return cipher_text

def calculate_frequency(text):
    frequencies = {}
    total = 0
    for letter in text.upper():
        if letter in letras:
            frequencies[letter] = frequencies.get(letter, 0) + 1
            total += 1

    for letter in frequencies:
        frequencies[letter] = (frequencies[letter] / total) * 100

    return frequencies

def frequency_difference(freq1, freq2):
    diff = sum(
        abs(freq1.get(letter, 0) - freq2.get(letter, 0))
        for letter in freq2
    )
    return diff

def BruteForce(ciphertext, frequencies):
    print('Decodificando por ataque de força bruta...\n')

    best_decrypted_text = ''
    best_key = None
    min_diff = float('inf')

    print('Resultados por ataque de força bruta:')
    for key in range(26):
        decrypted_text = ''

        for cipher_letter in ciphertext:
            if cipher_letter.upper() in letras:
                a = letras[cipher_letter.upper()]
                c = (a - key) % 26

                decrypted_letter = [letra for letra, num in letras.items() if num == c][0]
                decrypted_text += decrypted_letter
            else:
                decrypted_text += cipher_letter

        decrypted_freq = calculate_frequency(decrypted_text)
        diff = frequency_difference(decrypted_freq, frequencies)

        print(f"\nChave: {key}")
        print("Texto decifrado:")
        print(decrypted_text)
        print("Diferença de frequência:", round(diff))

        if diff < min_diff:
            min_diff = diff
            best_decrypted_text = decrypted_text
            best_key = key

    print('\nMelhor chave de acordo com a frequência:', best_key)
    print('Texto decifrado mais próximo encontrado:')
    print(best_decrypted_text)

# ========> Inserir a string e a chave. Retorna a codificação
ciphertext = ShiftCipher("learningtocodeisanessentialskillintodaysdigitalworldwheretechnologyevolvesrapidly", 43)

# ========> Inserir o texto codificado. Retorna a decodificação por força bruta (todas as chaves possíveis) e a de acordo com a frequência
BruteForce(ciphertext, frequencia_letras)
