import tkinter as tk
import constants


class Ciphers:
    alphabets = constants.alphabets
    other = constants.other
    rus_alph = constants.rus_alph
    rus_alph_upper = constants.rus_alph_upper
    eng_alph = constants.eng_alph
    eng_alph_upper = constants.eng_alph_upper

    def __init__(self, text=None, key=None, lang=None, row=None, col=None):
        self.ciphers_dict = {
            'caesar': {'encrypt': self.caesar_encrypt, 'decrypt': self.caesar_decrypt, 'alph': self.caesar_alph},
            'atbash': {'encrypt': self.atbash_encrypt, 'decrypt': self.atbash_decrypt, 'alph': self.atbash_alph},
            'route_permutation': {'encrypt': self.route_perm_encrypt, 'text': self.route_perm_encrypt_text}}
        self.ciphers_alph = {
        }
        self.text = text
        self.key = key
        self.lang = lang
        self.row = row
        self.col = col
        self.alph_upper = self.alphabets[lang]['upper'] if lang else None
        self.alph_lower = self.alphabets[lang]['lower'] if lang else None

    def caesar_alph(self):
        key = str(self.key) if isinstance(self.key, int) else self.key
        if not key.isdigit():
            return 'key != digit'
        key = int(key)
        alph = self.alph_upper
        encrypted_alph = alph[key:] + alph[:key]
        return encrypted_alph

    def caesar_decrypt(self):
        ...

    def caesar_encrypt(self) -> str:
        key = str(self.key) if isinstance(self.key, int) else self.key
        if not key.isdigit():
            return 'key != digit'
        encrypted_result = ''
        key = int(key)
        lang_alph_lower = Ciphers.alphabets[self.lang]['lower']
        lang_alph_upper = Ciphers.alphabets[self.lang]['upper']
        if self.text:
            for letter in self.text:
                if letter in lang_alph_lower:
                    index = lang_alph_lower.index(letter)
                    encrypted_result += lang_alph_lower[(index + key) % len(lang_alph_lower)]
                elif letter in lang_alph_upper:
                    index = lang_alph_upper.index(letter)
                    encrypted_result += lang_alph_upper[(index + key) % len(lang_alph_upper)]
                elif letter in Ciphers.other:
                    encrypted_result += letter
                else:
                    print('unexpected letter', letter)
        return encrypted_result

    def atbash_encrypt(self) -> str:
        encrypted_result = ''
        lang_alph_lower = Ciphers.alphabets[self.lang]['lower']
        lang_alph_upper = Ciphers.alphabets[self.lang]['upper']
        if self.text:
            for letter in self.text:
                if letter in lang_alph_lower:
                    index = lang_alph_lower.index(letter)
                    encrypted_result += lang_alph_lower[-1 - index]
                elif letter in lang_alph_upper:
                    index = lang_alph_upper.index(letter)
                    encrypted_result += lang_alph_upper[-1 - index]
                elif letter in Ciphers.other:
                    encrypted_result += letter
                else:
                    print('unexpected letter', letter)
        return encrypted_result

    def atbash_alph(self):
        key = 32 if self.lang == 'rus' else 25
        alph = self.alph_upper
        return alph[key:] + alph[:key]

    def atbash_decrypt(self):
        ...

    def route_perm_encrypt(self):
        row = int(self.row)
        col = int(self.col)
        text = self.text
        text += ' ' * (row * col - len(text) + 1)

        min_2 = min(row, col) // 2
        n = 0
        data = [[''] * col for _ in range(row)]

        for i in range(min_2):
            for j in range(i, col - i, 1):
                data[i][j] = text[n]
                n += 1
            for j in range(i + 1, row - i, 1):
                data[j][~i] = text[n]
                n += 1
            for j in range(col - i - 2, i - 1, -1):
                data[~i][j] = text[n]
                n += 1
            for j in range(row - i - 2, i, -1):
                data[j][i] = text[n]
                n += 1

        if n != row * col:
            for j in range(min_2, col - min_2, 1):
                data[min_2][j] = text[n]
                n += 1
            for j in range(min_2 + 1, row - min_2, 1):
                data[j][~min_2] = text[n]
                n += 1
        self.data = data
        return data

    def route_perm_encrypt_text(self):
        data = self.data
        res = ''
        for i in range(len(data)):
            if i % 2 == 0:
                res += ''.join(data[i][::-1])
            else:
                res += ''.join(data[i])
        return res


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.frames = {}

        self.caesar_frame = CaesarFrame()
        self.caesar_frame.grid(row=1, column=1, sticky="nsew")
        self.frames['caesar_frame'] = self.caesar_frame

        self.atbash_frame = AtbashFrame()
        self.atbash_frame.grid(row=1, column=1, sticky="nsew")
        self.frames['atbash_frame'] = self.atbash_frame

        self.main_frame = MainFrame()
        self.main_frame.grid(row=1, column=1, sticky="nsew")
        self.frames['main_frame'] = self.main_frame

        self.route_perm_frame = RoutePermutationFrame()
        self.route_perm_frame.grid(row=1, column=1, sticky="nsew")
        self.frames['route_perm_frame'] = self.route_perm_frame

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f'{self.width}x{self.height}')
        self.title('ciphers')

        self.mainmenu = tk.Menu(master=self)
        self.config(menu=self.mainmenu)

        self.cipher_menu_var = tk.StringVar()
        self.cipher_menu = tk.Menu(master=self.mainmenu, tearoff=0)
        self.cipher_menu.add_radiobutton(label='caesar',
                                         command=lambda: self.show_frame(self.caesar_frame), value='caesar',
                                         variable=self.cipher_menu_var)
        self.cipher_menu.add_radiobutton(label='atbash',
                                         command=lambda: self.show_frame(self.atbash_frame), value='atbash',
                                         variable=self.cipher_menu_var)
        self.cipher_menu.add_radiobutton(label='route permutation',
                                         command=lambda: self.show_frame(self.route_perm_frame), value='route_perm',
                                         variable=self.cipher_menu_var)
        self.mainmenu.add_cascade(label='ciphers', menu=self.cipher_menu)

        self.language_menu_var = tk.StringVar(value='eng')
        self.language_menu = tk.Menu(master=self.mainmenu, tearoff=0)
        self.language_menu.add_radiobutton(label='russian', command=lambda: self.set_app_language('rus'), value='rus',
                                           variable=self.language_menu_var)
        self.language_menu.add_radiobutton(label='english', command=lambda: self.set_app_language('eng'), value='eng',
                                           variable=self.language_menu_var)
        self.mainmenu.add_cascade(label='language', menu=self.language_menu)
        self.show_frame(self.main_frame)

    @staticmethod
    def show_frame(frame):
        frame.tkraise()

    def set_app_language(self, lang: str):
        self.mainmenu.entryconfigure(1, label=constants.menus['ciphers'][lang])
        self.mainmenu.entryconfigure(2, label=constants.menus['language'][lang])
        self.cipher_menu.entryconfigure(0, label=constants.menus['caesar'][lang])
        self.cipher_menu.entryconfigure(1, label=constants.menus['atbash'][lang])
        self.cipher_menu.entryconfigure(2, label=constants.menus['route_permutation'][lang])
        self.language_menu.entryconfigure(0, label=constants.menus['russian'][lang])
        self.language_menu.entryconfigure(1, label=constants.menus['english'][lang])
        self.title(constants.title[lang])

        for frame in self.frames.values():
            frame.encrypted_text_label_var.set(constants.labels['encrypted_text_label'][lang])
            frame.encrypted_text_var.set(frame.encrypted_text_var.get() if (frame.entry_cleared['key_entry_var'] and
                                                                            frame.entry_cleared['text_entry_var']) else
                                         constants.labels['encrypted_text'][lang])
            frame.rus_button['text'] = constants.buttons['rus'][lang]
            frame.eng_button['text'] = constants.buttons['eng'][lang]
            frame.key_entry_var.set(frame.key_entry_var.get() if frame.entry_cleared[
                'key_entry_var'] else constants.entrys['key_entry'][lang])
            frame.text_entry_var.set(frame.text_entry_var.get() if frame.entry_cleared[
                'text_entry_var'] else constants.entrys['text_entry'][lang])
            frame.encrypted_alph_var.set(frame.encrypted_alph_var.get() if frame.entry_cleared[
                'key_entry_var'] else constants.labels['encrypted_alph'][lang])


class FrameConstructor(tk.Frame):
    def __init__(self, cipher=None):
        super().__init__()
        self.cipher = cipher
        self.encrypted_text_var = tk.StringVar(value=constants.labels['encrypted_text']['eng'])
        self.encrypted_text = tk.Entry(master=self, textvariable=self.encrypted_text_var, state='readonly', width=100)
        self.encrypted_text_label_var = tk.StringVar(value=constants.labels['encrypted_text_label']['eng'])
        self.encrypted_text_label = tk.Label(master=self, textvariable=self.encrypted_text_label_var)
        self.lang_var = tk.StringVar(value='eng')
        self.rus_button = tk.Radiobutton(self, text="rus",
                                         indicatoron=False, value="rus", width=15,
                                         command=lambda: self.lang_button_command(self.cipher), variable=self.lang_var)

        self.eng_button = tk.Radiobutton(self, text="eng",
                                         indicatoron=False, value="eng", width=15,
                                         command=lambda: self.lang_button_command(self.cipher), variable=self.lang_var)
        self.lang_buttons = {'eng': self.eng_button, 'rus': self.rus_button}
        self.key_entry_var = tk.StringVar(value='key')
        self.key_entry = tk.Entry(master=self, textvariable=self.key_entry_var)
        self.key_entry.var = self.key_entry_var
        self.key_entry.var_name = 'key_entry_var'
        self.key_entry.bind('<1>',
                            lambda event, entry=self.key_entry: self.clear_entry_background(entry))
        self.text_entry_var = tk.StringVar(value='text')
        self.text_entry = tk.Entry(master=self, textvariable=self.text_entry_var)
        self.text_entry.var = self.text_entry_var
        self.text_entry.var_name = 'text_entry_var'
        self.text_entry.bind('<1>',
                             lambda event, entry=self.text_entry: self.clear_entry_background(
                                 entry))
        self.trace_funcs = {'text_entry_var': self.text_entry_var_trace,
                            'key_entry_var': self.key_entry_var_trace,
                            'route_permutation_row_var': self.route_permutation_trace,
                            'route_permutation_col_var': self.route_permutation_trace,
                            'route_permutation_text_var': self.route_permutation_trace}
        self.entry_cleared = {'text_entry_var': False,
                              'key_entry_var': False}
        self.encrypted_alph_var = tk.StringVar(
            value=constants.labels['encrypted_alph']['eng'])
        self.encrypted_alph = tk.Entry(master=self, textvariable=self.encrypted_alph_var, state='readonly', width=100)
        self.atbash_alph_var = tk.StringVar(value=constants.labels['atbash_alph']['eng'])
        self.atbash_alph = tk.Entry(master=self, state='readonly', width=100, textvariable=self.atbash_alph_var)
        self.route_permutation_row_var = tk.StringVar(value='row')
        self.route_permutation_row = tk.Entry(master=self, textvariable=self.route_permutation_row_var)
        self.route_permutation_row.var = self.route_permutation_row_var
        self.route_permutation_row.var_name = 'route_permutation_row_var'
        self.route_permutation_row.bind('<1>',
                                        lambda e, entry=self.route_permutation_row: self.clear_entry_background(
                                            entry))
        self.route_permutation_col_var = tk.StringVar(value='col')
        self.route_permutation_col = tk.Entry(master=self, textvariable=self.route_permutation_col_var)
        self.route_permutation_col.var = self.route_permutation_col_var
        self.route_permutation_col.var_name = 'route_permutation_col_var'
        self.route_permutation_col.bind('<1>',
                                        lambda e, entry=self.route_permutation_col: self.clear_entry_background(
                                            entry))
        self.route_permutation_text_var = tk.StringVar(value='text')
        self.route_permutation_text = tk.Entry(master=self, width=100, textvariable=self.route_permutation_text_var)
        self.route_permutation_text.var = self.route_permutation_text_var
        self.route_permutation_text.var_name = 'route_permutation_text_var'
        self.route_permutation_text.bind('<1>',
                                         lambda e, entry=self.route_permutation_text: self.clear_entry_background(
                                             entry))
        self.route_permutation_list = {}
        self.last_row = -1
        self.last_col = -1
        self.route_permutation_result_var = tk.StringVar()
        self.route_permutation_result = tk.Entry(master=self, state='readonly', width=100,
                                                 textvariable=self.route_permutation_result_var)

    def set_route_permutation_result(self):
        self.route_permutation_result.grid(row=3, column=0, columnspan=10)

    def set_route_permutation_text(self):
        self.route_permutation_text.grid(row=1, column=0, columnspan=40)

    def set_route_permutation_row(self):
        self.route_permutation_row.grid(row=0, column=0)

    def set_route_permutation_col(self):
        self.route_permutation_col.grid(row=0, column=1)

    def set_encrypted_alph(self):
        self.encrypted_alph.grid(row=1, column=1)

    def set_encrypted_text(self):
        self.encrypted_text.grid(row=0, column=1)

    def set_encrypted_text_label(self):
        self.encrypted_text_label.grid(row=0, column=0)

    def set_lang_buttons(self):
        self.rus_button.grid(row=3, column=0)
        self.eng_button.grid(row=4, column=0)

    def set_atbash_alph(self):
        self.atbash_alph.grid(row=1, column=1)

    def set_key_entry(self):
        self.key_entry.grid(row=2, column=0)
        self.encrypted_alph_var.set(constants.labels['encrypted_alph']['eng'])

    def set_text_entry(self):
        self.text_entry.grid(row=1, column=0)

    def lang_button_command(self, cipher_name):

        text = self.text_entry_var.get()
        lang = self.lang_var.get()
        key = self.key_entry_var.get()

        lang_alph_lower = Ciphers.alphabets[lang]['lower']
        lang_alph_upper = Ciphers.alphabets[lang]['upper']
        max_key_entry_value = len(lang_alph_lower) - 1
        text_last_letter = text[-1] if text else ''

        cipher = Ciphers(text, key, lang)
        cipher_alph = cipher.ciphers_dict[cipher_name]['alph']

        self.encrypted_alph_var.set(cipher_alph())
        self.atbash_alph_var.set(constants.labels['atbash_alph'][lang])

        if text_last_letter not in lang_alph_lower + lang_alph_upper:
            self.encrypted_text_var.set(
                '' if self.entry_cleared['text_entry_var'] else constants.labels['encrypted_text'][lang])
            self.text_entry_var.set(
                '' if self.entry_cleared['text_entry_var'] else constants.entrys['text_entry'][lang])
        if key.isdigit() and int(key) > max_key_entry_value:
            self.key_entry_var.set(max_key_entry_value)

    def text_entry_var_trace(self, cipher_name):

        text = self.text_entry_var.get()
        key = self.key_entry_var.get()
        lang = self.lang_var.get()

        cipher = Ciphers(text, key, lang)
        cipher_func = cipher.ciphers_dict[cipher_name]['encrypt']

        text_last_letter = text[-1] if text else ''
        all_text_except_last_letter = text[:-1]
        lang_alph_lower = Ciphers.alphabets[lang]['lower']
        lang_alph_upper = Ciphers.alphabets[lang]['upper']
        lang_button = self.rus_button if lang == 'rus' else self.eng_button

        if text:
            if text_last_letter not in lang_alph_lower + lang_alph_upper and text_last_letter not in Ciphers.other:
                self.text_entry_var.set(all_text_except_last_letter)
                self.flash(lang_button, 100)
            else:
                self.encrypted_text_var.set(cipher_func())

    def route_permutation_trace(self, cipher_name):
        text = self.route_permutation_text_var.get()
        row = self.route_permutation_row_var.get()
        if not row.isdigit():
            return
        row = int(row)
        col = self.route_permutation_col_var.get()
        if not col.isdigit():
            return
        col = int(col)
        if row < self.last_row or col < self.last_col:
            text = text[:row * col]
            self.route_permutation_text_var.set(text)
            for i in self.route_permutation_list:
                self.route_permutation_list[i].destroy()
            self.route_permutation_list = {}
        self.last_row = row
        self.last_col = col
        if len(text) > row * col:
            self.route_permutation_text_var.set(text[:-1])
            return
        cipher = Ciphers(text=text, col=col, row=row)
        cipher_func = cipher.ciphers_dict[cipher_name]['encrypt']
        cipher_text = cipher.ciphers_dict[cipher_name]['text']
        data = cipher_func()
        for i in range(len(data)):
            for j in range(len(data[i])):
                label_name = f'{i}_{j}'
                if label_name in self.route_permutation_list:
                    self.route_permutation_list[label_name]['text'] = data[i][j]
                else:
                    exec(f'l{label_name} = tk.Label(master=self,text=data[i][j])')
                    exec(f'l{label_name}.grid(row={4 + i},column={3 + j})')
                    self.route_permutation_list[label_name] = eval(f'l{label_name}')
        self.route_permutation_result_var.set(cipher_text())

    #  лагает при спаме
    def flash(self, obj, delay):
        self.after(delay, obj.flash())

    def key_entry_var_trace(self, cipher_name):

        text = self.text_entry_var.get()
        key = self.key_entry_var.get()
        lang = self.lang_var.get()

        lang_alph_lower = Ciphers.alphabets[lang]['lower']
        lang_button = self.lang_buttons[lang]
        max_key_entry_value = len(lang_alph_lower) - 1
        all_text_except_last_letter = key[:-1]

        if key.isdigit():
            if int(key) > max_key_entry_value:
                key = max_key_entry_value
                self.key_entry_var.set(key)
                self.flash(lang_button, 100)
            cipher = Ciphers(text, key, lang)
            cipher_func = cipher.ciphers_dict[cipher_name]['encrypt']
            cipher_alph = cipher.ciphers_dict[cipher_name]['alph']

            self.encrypted_text_var.set(cipher_func())
            self.encrypted_alph_var.set(cipher_alph())
        else:
            self.key_entry_var.set(all_text_except_last_letter)

    def clear_entry_background(self, entry):
        entry_var = entry.var
        entry_var_name = entry.var_name
        entry_var.set('')
        entry.unbind('<1>')
        trace_func = self.trace_funcs[entry_var_name]
        entry_var.trace_add('write', lambda name, index, mode: trace_func(self.cipher))
        self.entry_cleared[entry_var_name] = True


class CaesarFrame(FrameConstructor):
    def __init__(self):
        super().__init__(cipher='caesar')
        self.set_encrypted_alph()
        self.set_encrypted_text()
        self.set_encrypted_text_label()
        self.set_key_entry()
        self.set_text_entry()
        self.set_lang_buttons()


class AtbashFrame(FrameConstructor):
    def __init__(self):
        super().__init__(cipher='atbash')
        self.set_atbash_alph()
        self.set_encrypted_text()
        self.set_encrypted_text_label()
        self.set_text_entry()
        self.set_lang_buttons()


class MainFrame(FrameConstructor):
    def __init__(self):
        super().__init__()


class CaesarWordFrame(FrameConstructor):
    def __init__(self):
        super().__init__(cipher='caesar_word')
        self.set_encrypted_alph()
        self.set_encrypted_text()
        self.set_encrypted_text_label()
        self.set_key_entry()
        self.set_text_entry()
        self.set_lang_buttons()


class RoutePermutationFrame(FrameConstructor):
    def __init__(self):
        super().__init__(cipher='route_permutation')
        self.set_route_permutation_row()
        self.set_route_permutation_col()
        self.set_route_permutation_text()
        self.set_route_permutation_result()


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
