import string
import heapq
from noise import noise

INF = 1000000

CharFrequency = [0.0816700000000000,
                0.0149200000000000,
                0.0278200000000000,
                0.0425300000000000,
                0.127020000000000,
                0.0222800000000000,
                0.0201500000000000,
                0.0609400000000000,
                0.0696600000000000,
                0.00153000000000000,
                0.00772000000000000,
                0.0402500000000000,
                0.0240600000000000,
                0.0674900000000000,
                0.0750700000000000,
                0.0192900000000000,
                0.000950000000000000,
                0.0598700000000000,
                0.0632700000000000,
                0.0905600000000000,
                0.0275800000000000,
                0.00978000000000000,
                0.0236000000000000,
                0.00150000000000000,
                0.0194700000000000,
                0.00102000000000000]

def char_symbol_creator():
    char_freq = []
    for i, char in enumerate(string.ascii_lowercase):
        char_freq.append([CharFrequency[i],[char,'']])
    heapq.heapify(char_freq)	
    while len(char_freq)>1:
        left_node = heapq.heappop(char_freq)
        right_node = heapq.heappop(char_freq)
        for item in left_node[1:]:
            item[1] = '0' + item[1]
        for item in right_node[1:]:
            item[1] = '1' + item[1]
        heapq.heappush(char_freq,[left_node[0]+right_node[0]]+left_node[1:]+right_node[1:])	
    char_freq = heapq.heappop(char_freq)[1:]
    char_freq_dict = {}
    for char, symbol in char_freq:
        char_freq_dict[char] = symbol
    return char_freq_dict

def huffman_encoder(plain_text):
    symbol_dict = char_symbol_creator()
    encoding_text = ""
    for char in plain_text:
        encoding_text += symbol_dict[char]
    return encoding_text

def huffman_decoder(cipher_text):
    symbol_dict = char_symbol_creator()
    char_dict = dict([(value, key) for key, value in symbol_dict.items()])
    pointer = 0
    current, plain_text = "", ""
    while pointer < len(cipher_text):
        current += cipher_text[pointer]
        if current in char_dict:
            plain_text += char_dict[current]
            current = ""
        pointer += 1
    return plain_text

def convolutional_enccoder(binary_text):
    current_state = "00"
    encoder_text = ""
    for i in range(len(binary_text)):
        if current_state == "00":
            if binary_text[i] == "0":
                encoder_text += "00"
                current_state = "00"
                continue
            elif binary_text[i] == "1":
                encoder_text += "11"
                current_state = "10"
                continue
        elif current_state == "10":
            if binary_text[i] == "0":
                encoder_text += "11"
                current_state = "01"
                continue
            elif binary_text[i] == "1":
                encoder_text += "00"
                current_state = "11"
                continue
        elif current_state == "01":
            if binary_text[i] == "0":
                encoder_text += "10"
                current_state = "00"
                continue
            elif binary_text[i] == "1":
                encoder_text += "01"
                current_state = "10"
                continue
        elif current_state == "11":
            if binary_text[i] == "0":
                encoder_text += "01"
                current_state = "01"
                continue
            elif binary_text[i] == "1":
                encoder_text += "10"
                current_state = "11"
                continue
    return encoder_text

def hamming(c1, c2):
    dist = 0
    for i in range(len(c1)):
        if c1[i] != c2[i]:
            dist += 1
    return dist

def argmin(iterable):
    return min(enumerate(iterable), key=lambda x: x[1])[0]

def viterbi_decoder(cipher_text):
    dp = [[0, INF, INF, INF]]
    for i in range(0, len(cipher_text), 2):
        row = [-1, -1, -1, -1]
        cur = cipher_text[i:i+2]
        j = i // 2
        row[0] = min(dp[j][0] + hamming("00", cur), dp[j][2] + hamming("10", cur))
        row[1] = min(dp[j][0] + hamming("11", cur), dp[j][2] + hamming("01", cur))
        row[2] = min(dp[j][1] + hamming("11", cur), dp[j][3] + hamming("01", cur))
        row[3] = min(dp[j][1] + hamming("00", cur), dp[j][3] + hamming("10", cur))
        dp.append(row)
    dp.reverse()
    pointer = 0
    index = argmin(dp[pointer])
    text = ""
    while pointer < len(dp)-1:
        if index == 0:
            if dp[pointer+1][0] > dp[pointer+1][2]:
                text += "0"
                index = 2
            else:
                text += "0"
                index = 0
        elif index == 1:
            if dp[pointer+1][0] > dp[pointer+1][2]:
                text += "1"
                index = 2
            else:
                text += "1"
                index = 0
        elif index == 2:
            if dp[pointer+1][1] > dp[pointer+1][3]:
                text += "0"
                index = 3
            else:
                text += "0"
                index = 1
        elif index == 3:
            if dp[pointer+1][1] > dp[pointer+1][3]:
                text += "1"
                index = 3
            else:
                text += "1"
                index = 1
        pointer += 1
    return text[::-1]

text = "amirhosseinahmadi"
print("Plain Text:", text)
huffman_encoded = huffman_encoder(text)
print("Huffman Encoding:", huffman_encoded)
conv_encoded = convolutional_enccoder(huffman_encoded)
print("Convolutional Encoding:", conv_encoded)
conv_encoded = [int(item) for item in conv_encoded]
noised_data = noise(conv_encoded)
noised_data = list(map(str, noised_data))
noised_data = "".join(noised_data)
viterbi_decoded = viterbi_decoder(noised_data)
print("Viterbi Decoding:", viterbi_decoded)
huffman_decoded = huffman_decoder(viterbi_decoded)
print("Huffman Decoding:", huffman_decoded)