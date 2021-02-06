from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog, font, ttk, colorchooser
import json
import re
import os

# Reading data from settings.json
with open('settings.json','r') as file:
    data = json.load(file)

# Making variables used in Toolbar
current_font_family = data['font family']
current_font_size = data['font size']
bold_state = 'normal'
italic_state = 'roman'
underline_state = 'normal'
font_color = (None, 'black')
bg_color = (None, 'white')
file_path = None
file_modified = None
show_statusbar = None
show_toolbar = None
word_wrap_var = False

# Making functions of Text Editor
# Extra Functions
def write_in_json(data_name,data_value):
    data[data_name] = data_value
    with open('settings.json','w') as file:
        json.dump(data,file)

def file_modify(event=None):
    global file_modified
    file_modified = None

def close(event=None):
    global file_path
    if file_modified:
        root.destroy()

    else:
        user_choice = askyesnocancel('Text Editor', 'Do want save changes?')
        if user_choice == True:
            save_file()

        elif user_choice == False:
            root.destroy()

        else:
            pass
# Functions used in File Menu

def new_file(event=None):
    global file_path
    global file_modified
    if file_modified:
        text_area.delete(1.0, END)

    else:
        user_choice = askyesnocancel('Text Editor', 'Do want save changes?')
        if user_choice == True:
            save_file()
            text_area.delete(1.0, END)
            root.title('Untitled - Text Editor')

        elif user_choice == False:
            text_area.delete(1.0, END)
            root.title('Untitled - Text Editor')

        else:
            pass
        file_modified = False


def open_file(event=None):
    global file_path
    global file_modified
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(
    ), title='Open', filetypes=(('Text Files', '*.txt'), ('All Files', '*.*')))
    if file_path == "":
        pass

    else:
        try:
            with open(file_path, 'r') as f:
                text_area.delete(1.0, END)
                text_area.insert(1.0, f.read())

        except:
            showinfo('Text Editor', 'This file type is not supported')
        root.title(os.path.basename(f"{file_path} - Text Editor"))
    file_modified = False


def save_file(event=None):
    global file_path
    global file_modified
    if file_path:
        text_content = text_area.get(1.0, END)
        with open(file_path, 'w') as file:
            file.write(text_content)

    else:
        text_content = text_area.get(1.0, END)
        file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(
        ), initialfile='Untitled', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
    root.title(os.path.basename(f"{file_path} - Text Editor"))
    file_modified = False


def save_as_file(event=None):
    global file_modified
    text_content = text_area.get(1.0, END)
    file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(
    ), initialfile='Untitled', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text_content)
    root.title(os.path.basename(f"{file_path} - Text Editor"))
    file_modified = False


# Function used in Veiw Menu
def veiw_toolbar(event=None):
    global show_toolbar
    if show_toolbar:
        toolbar.pack_forget()
        show_toolbar = False

    else:
        text_area.pack_forget()
        statusbar.pack_forget()
        toolbar.pack(side=TOP, fill=X)
        statusbar.pack(side=BOTTOM, fill=X)
        text_area.pack(fill=BOTH, expand=True)
        show_toolbar = True


def veiw_statusbar(event=None):
    global show_statusbar
    if show_statusbar:
        statusbar.pack_forget()
        show_statusbar = False

    else:
        text_area.pack_forget()
        statusbar.pack(side=BOTTOM, fill=X)
        text_area.pack(fill=BOTH, expand=True)
        show_statusbar = True

def word_wrap(event=None):
    global word_wrap_var
    if word_wrap_var:
        text_area.configure(wrap="none")
        text_area.pack_forget()
        x_scroll_bar.pack(side=BOTTOM,fill=X)
        text_area.pack(fill=BOTH, expand=True)
        word_wrap_var = False

    else:
        x_scroll_bar.pack_forget()
        text_area.configure(wrap="word")
        word_wrap_var = True
        

# Function used in Edit Menu
def find_replace(event=None):
    match_condition = False
    def find(event=None):
        if find_entry.get():
            match_condition = False
            text_area.tag_remove('sel', 1.0, END)
            text_content = text_area.get(1.0, END)
            word = find_entry.get()
            matches = re.finditer(word, text_content)
            for match in matches:
                line = text_area.get(1.0, 'end-1c').count('\n')+1
                text_area.focus()
                word_start = f"{line}.{match.span()[0]}"
                word_end = f"{line}.{match.span()[1]}"
                text_area.tag_add('sel', word_start, word_end)
                match_condition = True
        if not match_condition:
            showinfo('Text Editor', f'Cannot find "{find_entry.get()}"')

    def replace(event=None):
        if find_entry.get() and replace_entry.get():
            find_word = find_entry.get()
            replace_word = replace_entry.get()
            text_content = text_area.get(1.0, END)
            new_text_content = text_content.replace(find_word, replace_word)
            text_area.delete(1.0, END)
            text_area.insert(1.0, new_text_content)

    find_dailog = Toplevel()
    find_dailog.geometry('330x130')
    find_dailog.title('Find/Replace')
    find_dailog.attributes('-topmost', 'true')
    find_frame = LabelFrame(find_dailog, text='Find/Replace', pady=10, padx=5)
    find_frame.pack(pady=5)

    find_label = Label(find_frame, text='Find: ')
    replace_label = Label(find_frame, text='Replace: ')

    find_entry = Entry(find_frame, width=22)
    replace_entry = Entry(find_frame, width=22)

    findnext_button = ttk.Button(find_frame, text='Find Next', command=find)
    replace_button = ttk.Button(find_frame, text='Replace', command=replace)

    find_label.grid()
    replace_label.grid()

    find_entry.grid(row=0, column=1)
    replace_entry.grid(row=1, column=1)

    findnext_button.grid(row=0, column=2, padx=5, pady=2)
    replace_button.grid(row=1, column=2, padx=5, pady=2)

# Function used in Toolbar
# Font formating functions
def change_font(event=None):
    global current_font_family
    current_font_family = font_var.get()
    text_area.configure(font=(current_font_family, current_font_size))
    write_in_json('font family',current_font_family)

def change_size(event=None):
    global current_font_size
    current_font_size = font_size_var.get()
    text_area.configure(font=(current_font_family, current_font_size))
    write_in_json('font size',current_font_size)


def change_bold(event=None):
    global bold_state
    global italic_state
    global underline_state
    text_property = font.Font(font=text_area['font'])
    if text_property.actual()['weight'] == 'normal':
        bold_state = 'bold'
        text_area.configure(
            font=(current_font_family, current_font_size, italic_state, underline_state, bold_state))
    elif text_property.actual()['weight'] == 'bold':
        bold_state = 'normal'
        text_area.configure(
            font=(current_font_family, current_font_size, italic_state, underline_state, bold_state))


def change_italic(event=None):
    global italic_state
    global bold_state
    global underline_state
    text_property = font.Font(font=text_area['font'])
    if text_property.actual()['slant'] == 'roman':
        italic_state = 'italic'
        text_area.configure(
            font=(current_font_family, current_font_size, italic_state, underline_state, bold_state))

    elif text_property.actual()['slant'] == 'italic':
        italic_state = 'roman'
        text_area.configure(
            font=(current_font_family, current_font_size, italic_state, underline_state, bold_state))


def change_underline(event=None):
    global italic_state
    global bold_state
    global underline_state
    text_property = font.Font(font=text_area['font'])
    if text_property.actual()['underline'] == 0:
        underline_state = 'underline'
        text_area.configure(
            font=(current_font_family, current_font_size, italic_state, underline_state, bold_state))

    elif text_property.actual()['underline'] == 1:
        underline_state = 'normal'
        text_area.configure(
            font=(current_font_family, current_font_size, italic_state, underline_state, bold_state))


def change_font_color(event=None):
    global font_color
    font_color = colorchooser.askcolor()
    text_area.configure(fg=font_color[1], bg=bg_color[1])


def change_bg_color(event=None):
    global bg_color
    bg_color = colorchooser.askcolor()
    text_area.configure(fg=font_color[1], bg=bg_color[1])

# Text aligning functions
def align_left(event=None):
    text_content = text_area.get(1.0, END)
    text_area.tag_config('left', justify=LEFT)
    text_area.delete(1.0, END)
    text_area.insert(INSERT, text_content, 'left')


def align_right(event=None):
    text_content = text_area.get(1.0, END)
    text_area.tag_config('right', justify=RIGHT)
    text_area.delete(1.0, END)
    text_area.insert(INSERT, text_content, 'right')


def align_center(event=None):
    text_content = text_area.get(1.0, END)
    text_area.tag_config('center', justify=CENTER)
    text_area.delete(1.0, END)
    text_area.insert(INSERT, text_content, 'center')


def increase_text(event=None):
    global current_font_size
    if current_font_size - 5 <= 1:
        current_font_size = 1
    else:
        current_font_size = current_font_size - 5
    text_area['font'] = (current_font_family, current_font_size,
                         italic_state, underline_state, bold_state)

    font_size_var.set(current_font_size)


def decrease_text(event=None):
    global current_font_size
    current_font_size = current_font_size + 5
    text_area['font'] = (current_font_family, current_font_size,
                         italic_state, underline_state, bold_state)
    font_size_var.set(current_font_size)

# Function used in Help Menu
def about():
    showinfo('Text Editor', 'This is a Text Editor By Shreyansh Raj')

# Function used in StatusBar
def give_status(event=None):
    if text_area.edit_modified():
        text_content = text_area.get(1.0, 'end-1c').split('\n')
        line = text_area.get(1.0, 'end-1c').count('\n')+1
        column = len(text_content[line-1])+1
        words = len(text_area.get(1.0, 'end-1c').split())
        statusbar.configure(
            text=f'Line: {line}, Column: {column},Words: {words}')
    text_area.edit_modified(False)


# GUI interface
root = Tk()
root.title('Untitled - Text Editor')
root.wm_iconbitmap('icon.ico')
root.state('zoomed')
root.minsize(680,500)

# Making Boolean Variables for toolbar/statusbar
show_toolbar = BooleanVar()
show_toolbar.set(True)
show_statusbar = BooleanVar()
show_statusbar.set(True)

file_modified = BooleanVar()
file_modified.set(False)

# Making PhotoImages of images
# images used in File Menu
new_icon = PhotoImage(file='images/new.png')
open_icon = PhotoImage(file='images/open.png')
save_icon = PhotoImage(file='images/save.png')
save_as_icon = PhotoImage(file='images/save_as.png')
exit_icon = PhotoImage(file='images/exit.png')

# images used in Edit Menu
cut_icon = PhotoImage(file='images/cut.png')
copy_icon = PhotoImage(file='images/copy.png')
paste_icon = PhotoImage(file='images/paste.png')
undo_icon = PhotoImage(file='images/undo.png')
redo_icon = PhotoImage(file='images/redo.png')
clear_all_icon = PhotoImage(file='images/clear_all.png')
find_icon = PhotoImage(file='images/find.png')

# images used Toolbar
bold_icon = PhotoImage(file='images/bold.png')
italic_icon = PhotoImage(file='images/italic.png')
underline_icon = PhotoImage(file='images/underline.png')
font_color_icon = PhotoImage(file='images/font_color.png')
bg_color_icon = PhotoImage(file='images/color.png')
align_left_icon = PhotoImage(file='images/align_left.png')
align_center_icon = PhotoImage(file='images/align_center.png')
align_right_icon = PhotoImage(file='images/align_right.png')
increase_text_icon = PhotoImage(file='images/increase_text.png')
decrease_text_icon = PhotoImage(file='images/decrease_text.png')

# Icon used in Help Menu
help_icon = PhotoImage(file='images/help.png')

# images used in View Menu
toolbar_icon = PhotoImage(file='images/tool_bar.png')
statusbar_icon = PhotoImage(file='images/status_bar.png')
word_wrap_icon = PhotoImage(file='images/word_wrap.png')

# Starting making menus
main_menu = Menu(root)
# Making File Menu
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='New', image=new_icon,
                      compound=LEFT, accelerator='Ctrl+N', command=new_file)
file_menu.add_command(label='Open...', image=open_icon,
                      compound=LEFT, accelerator='Ctrl+O', command=open_file)
file_menu.add_command(label='Save', image=save_icon,
                      compound=LEFT, accelerator='Ctrl+S', command=save_file)
file_menu.add_command(label='Save As...', image=save_as_icon,
                      compound=LEFT, accelerator='Ctrl+Alt+S')
file_menu.add_separator()
file_menu.add_command(label='Exit', image=exit_icon,
                      compound=LEFT, accelerator='Esc', command=close)

# Making Edit Menu
edit_menu = Menu(root, tearoff=0)
edit_menu.add_command(label='Cut', image=cut_icon,
                      compound=LEFT, accelerator='Ctrl+X', command=lambda: text_area.event_generate('<<Cut>>'))
edit_menu.add_command(label='Copy', image=copy_icon,
                      compound=LEFT, accelerator='Ctrl+C', command=lambda: text_area.event_generate('<<Copy>>'))
edit_menu.add_command(label='Paste', image=paste_icon,
                      compound=LEFT, accelerator='Ctrl+V', command=lambda: text_area.event_generate('<<Paste>>'))
edit_menu.add_separator()
edit_menu.add_command(label='Undo', image=undo_icon,
                      compound=LEFT, accelerator='Ctrl+Z', command=lambda: text_area.event_generate('<<Undo>>'))
edit_menu.add_command(label='Redo', image=redo_icon,
                      compound=LEFT, accelerator='Ctrl+Y', command=lambda: text_area.event_generate('<<Redo>>'))
edit_menu.add_separator()
edit_menu.add_command(label='Clear All', image=clear_all_icon,
                      compound=LEFT, command=lambda: text_area.delete(1.0, END))
edit_menu.add_separator()
edit_menu.add_command(label='Find/Replce', image=find_icon,
                      compound=LEFT, accelerator='Ctrl+F', command=find_replace)

# Making View Menu
view_menu = Menu(root, tearoff=0)
view_menu.add_checkbutton(label='Tool Bar', image=toolbar_icon,
                          compound=LEFT, variable=show_toolbar, command=veiw_toolbar)
view_menu.add_checkbutton(label='Status Bar', image=statusbar_icon,
                          compound=LEFT, variable=show_statusbar, command=veiw_statusbar)
view_menu.add_checkbutton(label='Word Wrap', image=word_wrap_icon,
                          compound=LEFT, variable=word_wrap_var,
                          command=word_wrap)

# Making Help Menu
help_menu = Menu(root, tearoff=0)
help_menu.add_command(label='About Text Editor', image=help_icon,
                      compound=LEFT, accelerator='F1', command=about)

# Configuring all menu
main_menu.add_cascade(label='File', menu=file_menu)
main_menu.add_cascade(label='Edit', menu=edit_menu)
main_menu.add_cascade(label='View', menu=view_menu)
main_menu.add_cascade(label='Help', menu=help_menu)
root.config(menu=main_menu)


# Making toolbar
toolbar = Label(root)
toolbar.pack(side=TOP, fill=X)

# Making statusbar
statusbar = Label(root, text='Line: 1, Column: 1,Words: 0',
                  font=('Century Gothic', 10), relief=SUNKEN)
statusbar.pack(side=BOTTOM, fill=X)

# Making text Area
# Adding scroll bar
y_scroll_bar = Scrollbar(root)
x_scroll_bar = Scrollbar(root,orient=HORIZONTAL)
text_area = Text(root, font=(current_font_family, current_font_size),wrap="none", undo=True, relief=SUNKEN, borderwidth=10, padx=10, pady=10)
y_scroll_bar.pack(side=RIGHT,fill=Y)
x_scroll_bar.pack(side=BOTTOM,fill=X)
text_area.pack(fill=BOTH, expand=True)
text_area.focus_set()
text_area.bind('<<Modified>>', give_status, add='+')
y_scroll_bar.config(command=text_area.yview)
x_scroll_bar.config(command=text_area.xview)
text_area.config(yscrollcommand=y_scroll_bar.set)
text_area.config(xscrollcommand=x_scroll_bar.set)

# Making Comboox of font styles
font_tuple = sorted(font.families())
font_var = StringVar()
font_var.set(data['font family'])
font_combobox = ttk.Combobox(
    toolbar, value=font_tuple, textvariable=font_var, state='readonly')
font_combobox.bind("<<ComboboxSelected>>", change_font)
font_combobox.grid(row=0, column=0, padx=5)

# Making Combobox of font size
font_size_tuple = tuple(range(8, 73, 2))
font_size_var = StringVar()
font_size_var.set(data['font size'])
font_size_combobox = ttk.Combobox(
    toolbar, width=8, value=font_size_tuple, textvariable=font_size_var)
font_size_combobox.bind("<<ComboboxSelected>>", change_size)
font_size_combobox.bind("<Return>", change_size)
font_size_combobox.grid(row=0, column=1, padx=5)

# Making Bold Button
bold_button = ttk.Button(toolbar, text='1', image=bold_icon)
bold_button.bind('<Button-1>', change_bold)
bold_button.grid(row=0, column=2, padx=5)

# Making italic Button
italic_button = ttk.Button(toolbar, text='2', image=italic_icon)
italic_button.bind('<Button-1>', change_italic)
italic_button.grid(row=0, column=3, padx=5)

# Making underline Button
underline_button = ttk.Button(toolbar, text='3', image=underline_icon)
underline_button.bind('<Button-1>', change_underline)
underline_button.grid(row=0, column=4, padx=5)

# Making change font color Button
font_color_button = ttk.Button(toolbar, image=font_color_icon)
font_color_button.bind('<Button-1>', change_font_color)
font_color_button.grid(row=0, column=5, padx=5)

# Making change bg color Button
bg_color_button = ttk.Button(toolbar, image=bg_color_icon)
bg_color_button.bind('<Button-1>', change_bg_color)
bg_color_button.grid(row=0, column=6, padx=5)

# Making Align Left Button
align_left_button = ttk.Button(toolbar, image=align_left_icon)
align_left_button.bind('<Button-1>', align_left)
align_left_button.grid(row=0, column=7, padx=5)

# Making Align Center Button
align_center_button = ttk.Button(toolbar, image=align_center_icon)
align_center_button.bind('<Button-1>', align_center)
align_center_button.grid(row=0, column=8, padx=5)

# Making Align Right Button
align_right_button = ttk.Button(toolbar, image=align_right_icon)
align_right_button.bind('<Button-1>', align_right)
align_right_button.grid(row=0, column=9, padx=5)

# Making text incease/decrease Button
increase_text_button = ttk.Button(toolbar, image=increase_text_icon)
increase_text_button.bind('<Button-1>', increase_text)
increase_text_button.grid(row=0, column=10, padx=5)

decrease_text_button = ttk.Button(toolbar, image=decrease_text_icon)
decrease_text_button.bind('<Button-1>', decrease_text)
decrease_text_button.grid(row=0, column=11, padx=5)

# binding with file menu option
root.bind('<Control-n>', new_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-s>', save_file)
root.bind('<Control-Alt-s>', save_as_file)
root.bind('<Escape>', close)

# binding with edit menu option
root.bind('<Control-f>', find_replace)

text_area.bind('<<Modified>>', file_modify, add='+')
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()