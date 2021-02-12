C1 = ''
with open('rus_text.txt') as file:
    C1 = file.read()

C2 = ''
with open('eng_text.txt') as file:
    C2 = file.read()
print(C2)

rus = {
    'о': 0.09,
    'е': 0.072,
    'а': 0.062,
    'и': 0.062,
    'н': 0.053,
    'т': 0.053,
    'с': 0.045,
    'р': 0.04,
    'в': 0.038,
    'л': 0.035,
    'к': 0.028,
    'м': 0.026,
    'д': 0.025,
    'п': 0.023,
    'у': 0.021,
    'я': 0.018,
    'з': 0.016,
    'ы': 0.016,
    'б': 0.014,
    'ь': 0.014,
    'ъ': 0.013,
    'г': 0.013,
    'ч': 0.012,
    'й': 0.01,
    'х': 0.009,
    'ж': 0.007,
    'ш': 0.006,
    'ю': 0.006,
    'ц': 0.004,
    'щ': 0.003,
    'э': 0.003,
    'ф': 0.002
}


C1_chars = {}

count = 0
#for char in C1:
#    if char.isalpha():
#        count += 1
#        if char not in C1_chars:
#            C1_chars[char] = 0
#        else:
#            C1_chars[char] += 1
for a in rus:
    print(a, rus[a])
