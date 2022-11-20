eng_alph = 'abcdefghijklmnopqrstuvwxyz'
eng_alph_upper = eng_alph.upper()
rus_alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
rus_alph_upper = rus_alph.upper()
other = '`1234567890-=~!@#$%^&*()_+][}{\';":/?\\.>,< '
labels = {'encrypted_text_label': {'rus': 'зашифрованный текст:', 'eng': 'encrypted text:'},
          'encrypted_text': {'rus': 'ожидается ввод текста/ключа', 'eng': 'waiting for text/key'},
          'encrypted_alph': {'rus': 'ожидается ввод ключа', 'eng': 'waiting for key'},
          'atbash_alph': {'rus': 'ЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮ', 'eng': 'ZABCDEFGHIJKLMNOPQRSTUVWXY'}}
entrys = {'text_entry': {'rus': 'текст', 'eng': "text"},
          'key_entry': {'rus': 'ключ', 'eng': 'key'}}
menus = {'ciphers': {'rus': 'шифры', 'eng': 'ciphers'},
         'caesar': {'rus': 'цезарь', 'eng': 'caesar'},
         'atbash': {'rus': 'атбаш', 'eng': 'atbash'},
         'route_permutation':{'rus':'маршрутная сортировка','eng':'route permutation'},
         'language': {'rus': 'язык', 'eng': 'language'},
         'russian': {'rus': 'русский', 'eng': 'russian'},
         'english': {'rus': 'английский', 'eng': 'english'}}
buttons = {'rus': {'rus': 'рус', 'eng': 'rus'},
           'eng': {'rus': 'англ', 'eng': 'eng'}}
title = {'rus': 'шифры', 'eng': 'ciphers'}
alphabets = {
    'rus':
        {
            'lower': rus_alph,
            'upper': rus_alph_upper
        },
    'eng':
        {
            'lower': eng_alph,
            'upper': eng_alph_upper
        }
}
