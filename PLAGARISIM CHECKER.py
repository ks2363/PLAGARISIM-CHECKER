import difflib
import requests
import bs4
import tkinter
from tkinter import messagebox

class plagiarism_checker:
    def root_quit(self):
        self.root.destroy()
    
    def quit_plagiarised_window(self):
        self.plagiarised_window.destroy()

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Plagiarism Checker')
        self.root.geometry('600x620')

        def_x = 50
        def_y = 25

        lbl_root_title = tkinter.Label(self.root, text='Plagiarism Checker')
        lbl_root_title.config(font=('TkDefaultFont, 24'))
        lbl_root_title.place(x=def_x, y=def_y)

        lbl_for_checking = tkinter.Label(self.root, text='Entry text to check', font='TkDefaultFont, 10')
        lbl_for_checking.place(x=def_x, y=def_y + 90)
        self.ent_for_checking = tkinter.Text(self.root, height=16, width=62)
        self.ent_for_checking.place(x=def_x, y=def_y + 120)

        lbl_website_for_checking = tkinter.Label(self.root, text='Enter website to compare')
        lbl_website_for_checking.place(x=def_x, y=def_y + 410)
        self.ent_website_for_checking = tkinter.Entry(self.root, width=90)
        self.ent_website_for_checking.place(x=def_x, y=def_y + 440, height=30)

        self.btn_calc_plagiarisedness = tkinter.Button(self.root, text='Calculate', command=self.calc_plagiarisedness,
                                                       borderwidth=10, height=2, width=16)
        self.btn_calc_plagiarisedness.place(x=def_x + 180, y=def_y + 510)

        self.btn_exit_win = tkinter.Button(self.root, text='Quit', command=self.root_quit,
                                           height=2, width=9, borderwidth=5)
        self.btn_exit_win.place(x=def_x + 430, y=def_y + 510)

        # Provide the full path to the icon file
        icon_path = r'C:\Users\LENOVO\Downloads\plagiar_icon.ico'
        self.root.iconbitmap(icon_path)

        self.root.mainloop()

    def calc_plagiarisedness(self):
        try:
            user_text_entry = self.ent_for_checking.get('1.0', tkinter.END)
            website_url = self.ent_website_for_checking.get()
            
            # Check if the URL is valid
            if not website_url.startswith('http'):
                raise requests.exceptions.RequestException('Invalid URL')

            website_response = requests.get(website_url)
            website_response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

            website_for_compare = website_response.text
            soup = bs4.BeautifulSoup(website_for_compare, 'lxml')
            soup_text = soup.findAll(text=True)

            visible_text = ''
            for each_char in soup_text:
                visible_text = visible_text + each_char
            web_text_for_compare = visible_text

            compare_sequences = difflib.SequenceMatcher(None, user_text_entry, web_text_for_compare)
            amount_plagiarised = compare_sequences.ratio()
            amount_plagiarised_percentage = round(amount_plagiarised * 100, 2)

            self.ent_for_checking.delete('1.0', tkinter.END)
            self.ent_website_for_checking.delete('0', tkinter.END)

            self.plagiarised_window = tkinter.Toplevel()
            self.plagiarised_window.geometry('256x170')

            btn_exit_plagiarised_window = tkinter.Button(self.plagiarised_window, text='Quit', borderwidth=5,
                                                         command=self.quit_plagiarised_window, height=1, width=8)
            btn_exit_plagiarised_window.place(x=93, y=120)

            if amount_plagiarised_percentage > 50:
                plagiarism_info_text = f'{amount_plagiarised_percentage}% Plagiarised'
                lbl_plagiarism_info = tkinter.Label(self.plagiarised_window, text=plagiarism_info_text, fg='red')
                lbl_plagiarism_info.config(font=('TkDefaultFont', 16))
                lbl_plagiarism_info.place(x=32, y=39)
            else:
                plagiarism_info_text = f'Not Plagiarised-\n{amount_plagiarised_percentage}% plagiarised'
                lbl_plagiarism_info = tkinter.Label(self.plagiarised_window, text=plagiarism_info_text, fg='green')
                lbl_plagiarism_info.config(font=('TkDefaultFont', 16))
                lbl_plagiarism_info.place(x=49, y=28)

        except requests.exceptions.RequestException as e:
            messagebox.showerror('User Error', str(e))

plagiarism_checker()
