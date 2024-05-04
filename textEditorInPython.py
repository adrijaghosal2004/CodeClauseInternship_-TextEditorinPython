import tkinter as tk
from tkinter import filedialog
import re
import keyword
from nltk.corpus import words

root = tk.Tk()
root.title("Text Editor")

def new_file():
    text_area.delete('1.0', tk.END)
    update()

def open_file():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, file.read())
        current_file = file_path

def save_file():
    if current_file:
        with open(current_file, 'w') as file:
            text = text_area.get('1.0', tk.END)
            file.write(text)
    else:
        save_as_file()

def save_as_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            text = text_area.get('1.0', tk.END)
            file.write(text)

def update(event=None):
    word_count()
    highlight()

def word_count():
    text = text_area.get('1.0', tk.END)
    words = re.findall(r'\w+', text)
    current_font = word_count_label.cget("font")
    word_count_label.config(text=f"Word Count: {len(words)}",font=(current_font,11))

words = set(words.words())
    
def highlight():
    text = text_area.get('1.0', tk.END).strip()
    if not text:
        return
    text_area.tag_configure("keyword", foreground="blue")
    text_area.tag_remove("keyword", "1.0", tk.END)
    for pattern in keyword.kwlist:
        start = "1.0"
        while True:
            start = text_area.search(r'\b' + pattern + r'\b', start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = f"{start}+{len(pattern)}c"
            text_area.tag_add("keyword", start, end)
            start = end
    
    text_area.tag_remove("spell_error", "1.0", tk.END)
    for word in re.findall(r'\b\w+\b', text):
        if word.lower() not in words:
            start = "1.0"
            while True:
                start = text_area.search(r'\m' + re.escape(word) + r'\M', start, stopindex=tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(word)}c"
                text_area.tag_add("spell_error", start, end)
                text_area.tag_configure("spell_error", underline=True, underlinefg="red")
                start = end

def change_text_size():
    selected_size = tk.simpledialog.askinteger("Text Size", "Choose a Text Size",
                                               parent=root, minvalue=6, maxvalue=200)
    if selected_size:
        text_area.configure(font=("Arial", selected_size))

menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Text Size", command=change_text_size)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menu_bar)

text_area = tk.Text(root,bg="light yellow")
text_area.pack(expand=True, fill='both')
text_area.bind('<KeyRelease>',update)

word_count_label = tk.Label(root, text="Word Count: 0")
word_count_label.pack()

current_file = None

root.mainloop()
