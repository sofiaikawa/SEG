from pandas import DataFrame
import itertools
from collections import Counter
import math

bigram_frequency = {
    "th": 0.03882543, "he": 0.03681391, "in": 0.02283899, "er": 0.02178042, "an": 0.02140460,
    "re": 0.01749394, "nd": 0.01571977, "on": 0.01418244, "en": 0.01383239, "at": 0.01335523,
    "ou": 0.01285484, "ed": 0.01275779, "ha": 0.01274742, "to": 0.01169655, "or": 0.01151094,
    "it": 0.01134891, "is": 0.01109877, "hi": 0.01092302, "es": 0.01092301, "ng": 0.01053385
}
trigram_frequency = {
    "the": 0.03508232, "and": 0.01593878, "ing": 0.01147042, "her": 0.00822444, "hat": 0.00650715,
    "his": 0.00596748, "tha": 0.00593593, "ere": 0.00560594, "for": 0.00555372, "ent": 0.00530771,
    "ion": 0.00506454, "ter": 0.00461099, "was": 0.00460487, "you": 0.00437213, "ith": 0.00431250,
    "ver": 0.00430732, "all": 0.00422758, "wit": 0.00397290, "thi": 0.00394796, "tio": 0.00378058
}
quadrigram_frequency = {
    "that": 0.00761242, "ther": 0.00604501, "with": 0.00573866, "tion": 0.00551919, "here": 0.00374549,
    "ould": 0.00369920, "ight": 0.00309440, "have": 0.00290544, "hich": 0.00284292, "whic": 0.00283826,
    "this": 0.00276333, "thin": 0.00270413, "they": 0.00262421, "atio": 0.00262386, "ever": 0.00260695,
    "from": 0.00258580, "ough": 0.00253447, "were": 0.00231089, "hing": 0.00229944, "ment": 0.00223347
}

def encrypt_transposition(plaintext, key):
    # Determina o número de colunas e linhas
    num_cols = len(key)
    grid = [''] * num_cols
    
    for i, char in enumerate(plaintext):
        col = i % num_cols
        grid[col] += char

    # Ordena as colunas de acordo com a chave
    sorted_key = sorted([(char, i) for i, char in enumerate(key)])
    cipher_text = ''.join(grid[i] for _, i in sorted_key)

    return cipher_text


def calcular_similaridade(texto, bigram_frequency, trigram_frequency, quadrigram_frequency):
    # Separar o texto em bigramas, trigramas e quadrigramas
    bigramas = [texto[i:i+2] for i in range(len(texto) - 1)]
    trigramas = [texto[i:i+3] for i in range(len(texto) - 2)]
    quadrigramas = [texto[i:i+4] for i in range(len(texto) - 3)]

    # Contar as ocorrências de cada n-grama
    contagem_bigramas = Counter(bigramas)
    contagem_trigramas = Counter(trigramas)
    contagem_quadrigramas = Counter(quadrigramas)

    total_bigramas = sum(contagem_bigramas.values())
    total_trigramas = sum(contagem_trigramas.values())
    total_quadrigramas = sum(contagem_quadrigramas.values())

    pontuacao = 0

    # Pesos para bigramas, trigramas e quadrigramas
    peso_bigramas = 0.5
    peso_trigramas = 1.0
    peso_quadrigramas = 1.5

    # Calcula a pontuação para os bigramas
    for bigrama, freq_esperada in bigram_frequency.items():
        freq_observada = contagem_bigramas.get(bigrama, 0) / total_bigramas if total_bigramas > 0 else 0
        pontuacao += peso_bigramas * abs(freq_esperada - freq_observada)

    # Calcula a pontuação para os trigramas
    for trigrama, freq_esperada in trigram_frequency.items():
        freq_observada = contagem_trigramas.get(trigrama, 0) / total_trigramas if total_trigramas > 0 else 0
        pontuacao += peso_trigramas * abs(freq_esperada - freq_observada)

    # Calcula a pontuação para os quadrigramas
    for quadrigrama, freq_esperada in quadrigram_frequency.items():
        freq_observada = contagem_quadrigramas.get(quadrigrama, 0) / total_quadrigramas if total_quadrigramas > 0 else 0
        pontuacao += peso_quadrigramas * abs(freq_esperada - freq_observada)

    # Normalização pelo número total de n-gramas
    pontuacao /= (peso_bigramas + peso_trigramas + peso_quadrigramas)

    return pontuacao

def decrypt(ciphertext):
    best_score = float('inf')
    best_decryption = None

    # Calcula o valor inicial de colunas mais próximo da raiz quadrada do comprimento do texto
    approx_sqrt = int(math.sqrt(len(ciphertext)))

    # Limita o range de colunas para valores próximos da raiz quadrada
    for num_cols in range(approx_sqrt, approx_sqrt + 3):
        if len(ciphertext) % num_cols != 0:
            continue

        num_rows = len(ciphertext) // num_cols
        matriz = [ciphertext[i * num_cols : (i + 1) * num_cols] for i in range(num_rows)]

        print(f'***Matriz analisada: {matriz}***\n')        
        for permutacao in itertools.permutations(range(num_rows)):  
            decrypted_txt = ''

            for i in range(num_cols):
                for row in permutacao:   
                    decrypted_txt += matriz[row][i]
            print(f'Texto resultante da permutação: {decrypted_txt}')
            # Calcula a pontuação de similaridade de linguagem
            score = calcular_similaridade(decrypted_txt, bigram_frequency, trigram_frequency, quadrigram_frequency)
            print(f'Pontuação da frequência: {score}\n')
            if score < best_score:
                best_score = score
                best_decryption = decrypted_txt

    return best_decryption

# Exemplo de uso:
msg = "meetmeatnextmidnight"
key = "FANCY"
ciphertext = encrypt_transposition(msg, key)
print(f"\nTexto Cifrado: {ciphertext}\n")

decrypt(ciphertext)