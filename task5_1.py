import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.figure import Figure

englishLetterFreq = {
    'E': 12.70,
    'T': 9.06,
    'A': 8.17,
    'O': 7.51,
    'I': 6.97,
    'N': 6.75,
    'S': 6.33,
    'H': 6.09,
    'R': 5.99,
    'D': 4.25,
    'L': 4.03,
    'C': 2.78,
    'U': 2.76,
    'M': 2.41,
    'W': 2.36,
    'F': 2.23,
    'G': 2.02,
    'Y': 1.97,
    'P': 1.93,
    'B': 1.29,
    'V': 0.98,
    'K': 0.77,
    'J': 0.15,
    'X': 0.15,
    'Q': 0.10,
    'Z': 0.07
}

russianLetterFreq = {
    'О': 11.18,
    'Е': 8.95,
    'А': 7.64,
    'И': 7.09,
    'Н': 6.78,
    'Т': 6.09,
    'С': 4.97,
    'Л': 4.96,
    'В': 4.38,
    'Р': 4.23,
    'К': 3.30,
    'М': 3.17,
    'Д': 3.09,
    'П': 2.47,
    'Ы': 2.36,
    'У': 2.22,
    'Б': 2.01,
    'Я': 1.96,
    'Ь': 1.84,
    'Г': 1.72,
    'З': 1.48,
    'Ч': 1.40,
    'Й': 1.21,
    'Ж': 1.01,
    'Х': 0.95,
    'Ш': 0.72,
    'Ю': 0.47,
    'Ц': 0.39,
    'Э': 0.36,
    'Щ': 0.30,
    'Ф': 0.21,
    'Ъ': 0.02
}


def map_to_reversed_list(d: dict):
    list_d = list(d.items())
    list_d.sort(key=lambda i: i[1], reverse=True)
    return [i[0] for i in list_d]


def count_bigrams(text):
    res = {}
    for i in range(len(text) - 1):
        if text[i].isalpha() and text[i + 1].isalpha():
            bigram = text[i:i + 2]
            if bigram in res:
                res[bigram] += 1
            else:
                res[bigram] = 1

    return map_to_reversed_list(res)


def count_trigrams(text):
    res = {}
    for i in range(len(text) - 2):
        if text[i].isalpha() and text[i + 1].isalpha() and text[i + 2].isalpha():
            trigram = text[i: i + 3]
            if trigram in res:
                res[trigram] += 1
            else:
                res[trigram] = 1
    return map_to_reversed_list(res)


def analyze_text(text: str):
    msg_freqs = {}  # частоты букв во входном сообщении

    count = 0  # количество уникальных букв в исходном тексте
    for char in text:
        if char.isalpha() and char == char.lower():  # обрабатываем только буквы
            count += 1
            if char in msg_freqs:
                msg_freqs[char] += 1
            else:
                msg_freqs[char] = 1

    for char in msg_freqs:  # перевод в проценты
        msg_freqs[char] *= 100 / count

    return msg_freqs, count_bigrams(text), count_trigrams(text)

def create_table_en(englishLetterFreq, m_freqs):
    arr1 = map_to_reversed_list(englishLetterFreq)
    arr2 = map_to_reversed_list(m_freqs)

    map = {}  # массив соответствий и его формирование
    for i in range(len(arr2)):
        map[arr2[i]] = arr1[i]

    map['c'] = 't'
    map['w'] = 'h'
    map['v'] = 'e'
    map['q'] = 'a'
    map['l'] = 'u'
    map['m'] = 'n'
    map['j'] = 'w'
    map['x'] = 'i'
    map['z'] = 's'
    map['t'] = 'r'
    map['g'] = 'c'
    map['f'] = 'd'
    map['b'] = 'p'
    map['p'] = 'f'
    map['e'] = 'm'
    map['i'] = 'x'
    map['y'] = 'o'
    map['s'] = 'g'
    map['r'] = 'y'
    map['d'] = 'c'
    map['a'] = 'q'

    map['h'] = 'b'
    map['n'] = 'v'
    map['o'] = 'l'

    return map


def create_table(letter_freq: dict, msg_freqs: dict):
    arr1 = map_to_reversed_list(letter_freq)
    arr2 = map_to_reversed_list(msg_freqs)

    map = {}  # массив соответствий и его формирование
    for i in range(len(arr2)):
        map[arr2[i]] = arr1[i]

    map['х'] = 'ч'
    map['л'] = 'т'
    map['ъ'] = 'н'
    map['ы'] = 'в'
    map['т'] = 'б'
    map['а'] = 'р'
    map['э'] = 'г'
    map['ц'] = 'м'
    map['о'] = 'ж'
    map['д'] = 'с'
    map['ч'] = 'и'
    map['р'] = 'щ'
    map['ю'] = 'ы'
    map['к'] = 'п'
    map['й'] = 'а'
    map['у'] = 'з'
    map['ж'] = 'ф'
    map['ф'] = 'ь'
    map['м'] = 'ш'
    map['е'] = 'у'
    map['б'] = 'л'
    map['я'] = 'я'
    map['в'] = 'к'
    map['г'] = 'д'
    map['ш'] = 'ц'
    map['ь'] = 'х'
    map['с'] = 'э'
    map['н'] = 'й'
    map['з'] = 'ю'
    map['п'] = 'е'
    map['и'] = 'о'
    return map


def decrypt(text: str, d: dict) -> str:
    decrypted_text = ''  # итоговое сообщение
    for char in text:  # замена
        if char.isalpha():
            if char in d:
                decrypted_text += d[char]
            else:
                decrypted_text += char #'_'
        else:
            decrypted_text += char
    return decrypted_text


def show_result(text, msg_letter_freqs, freqs, table):
    print('Расшифрованный текст: ')
    print(text)

    fig, ax = plt.subplots(1, 2)
    ax1:Axes = ax[0]
    ax1.bar(msg_letter_freqs.keys(), msg_letter_freqs.values(), width=0.5, color='g')
    ax1.set_title('Частота букв в сообщении')


    ax2 = ax[1]
    ax2.bar(freqs.keys(), freqs.values(), width=0.5, color='r')
    ax2.set_title('Частота букв в алфавите')
    # plt.show()

    for i in table:
        print(i + ': ' + table[i])

    plt.close()


if __name__ == '__main__':
    with open('rus_text_v1.txt', encoding='utf8') as file:
        C1 = ''.join(file.readlines()[1:]).lower()

    m_freqs, bigrams, trigrams = analyze_text(C1)
    l = list(m_freqs.items())
    l.sort(key=lambda i: i[1], reverse=True)
    m_freqs = {x[0]: x[1] for x in l}

    print('Самые частые биграммы: ', ', '.join(bigrams[:6]))
    print('Самые частые триграммы: ', ', '.join(trigrams[:11]))
    table = create_table(russianLetterFreq, m_freqs)  # таблица соответствия символов алфавита и шифротекста
    res_rus = decrypt(C1, table)
    show_result(res_rus, m_freqs, russianLetterFreq, table)

    # with open('eng_text.txt') as file:
    #     C2 = file.read().lower()
    #
    # m_freqs, bigrams, trigrams = analyze_text(C2)
    # l = list(m_freqs.items())
    # l.sort(key=lambda i: i[1], reverse=True)
    # m_freqs = {x[0]: x[1] for x in l}
    #
    # print('Самые частые биграммы: ', ', '.join(bigrams[:6]))
    # print('Самые частые триграммы: ', ', '.join(trigrams[:11]))
    # table = create_table_en(englishLetterFreq, m_freqs)  # таблица соответствия символов алфавита и шифротекста
    # res_eng = decrypt(C2, table)
    # show_result(res_eng, m_freqs, englishLetterFreq, table)


# русские самые частые биграммы и триграммы
# СТ, НО, ЕН, ТО, НА, ОВ, НИ, РА, ВО, КО,
# СТО, ЕНО, НОВ, ТОВ, ОВО, ОВА
