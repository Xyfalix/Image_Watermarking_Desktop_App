from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox

import PIL
from PIL import Image, ImageTk, ImageGrab

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Arial"
chosen_color = 'black'
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Watermark App")
window.config(bg='#3E3B36', width=1500, height=800)

canvas = Canvas(width=1000, height=800, bg='#36393e', highlightbackground='#36393e')
canvas.grid(column=0, row=0, rowspan=7)
resized_sample_image = None
# # Open image file
# sample_image = Image.open("sample_pic.jpg")
#
# # resize image to fit canvas
# resized_image = sample_image.resize((canvas.winfo_reqwidth(), canvas.winfo_reqheight()))
#
# # create PhotoImage object from resized image
# resized_sample_image = ImageTk.PhotoImage(resized_image)
#
# # create image on canvas
# canvas.create_image(0, 0, image=resized_sample_image, anchor="nw", tag='picture')
canvas.create_text(500, 400, text='Sample Text', fill=chosen_color, font=('Arial', 20), tag='text')

# ---------------------------- Text Input Widget ------------------------------- #
# Add text item update functionality to the text entry widget
def update_text(event=None):
    canvas.itemconfig('text', text=text_entry.get())

text_input_frame = Frame(window)
text_input_frame.grid(column=0, row=7, pady=20, sticky="w")

text_input_label = Label(text_input_frame, text="Text: ", font=(FONT_NAME, 12), fg='white', bg='#3E3B36')
text_input_label.grid(column=0, row=0, sticky="w")

# entries
text_entry = Entry(text_input_frame, width=159)
text_entry.insert(0, 'Sample Text')  # Add default text
text_entry.grid(column=1, row=0, sticky='ew')
text_entry.bind('<KeyRelease>', update_text)

# ---------------------------- Font Color Widget ------------------------------- #
def choose_color():
    global chosen_color
    color = colorchooser.askcolor(title="Choose Color")
    if color:
        chosen_color = color[1]  # set the chosen color to the hex value
        print("Chosen color:", chosen_color)
        canvas.itemconfig('text', fill=color[1])


color_frame = Frame(window, bg='#3E3B36')
color_frame.grid(column=1, row=0, padx=10, pady=10, sticky="s")

color_button = Button(color_frame, text="Select Color", font=(FONT_NAME, 12),
                      command=choose_color, bg="#36393e", fg="white",)
color_button.grid(column=0, row=0, pady=10)

# ---------------------------- Font Type Widget ------------------------------- #
def change_font(event):
    # Retrieve the selected font from the OptionMenu widget
    selected_font_name = selected_font.get()
    print(selected_font_name)

    # get current font size
    try:
        font_size = canvas.itemcget('text', 'font').split()[-1]
        print(font_size)

    except IndexError:
        font_size = canvas.itemcget('text', 'font')
        print(font_size)

    else:
        # Update the font of the text widget
        canvas.itemconfig('text', font=(selected_font_name, font_size))

# Define a function to handle mouse scrolling on the font_optionmenu widget
def scroll_options(event):
    # Get the current index of the selected option
    current_index = all_fonts.index(selected_font.get())

    # Determine the direction of the scroll and update the selected option
    if event.delta > 0 and current_index > 0:
        selected_font.set(all_fonts[current_index - 1])
    elif event.delta < 0 and current_index < len(all_fonts) - 1:
        selected_font.set(all_fonts[current_index + 1])


font_type_frame = Frame(window, bg='#3E3B36')
font_type_frame.grid(column=1, row=1, padx=10, pady=10, sticky="s")

# define 3 columns in the font type frame
for col in range(3):
    font_type_frame.columnconfigure(col, weight=1)

font_type_label = Label(font_type_frame, text="Font Type:", font=(FONT_NAME, 12), fg='white', bg='#3E3B36')
font_type_label.grid(column=0, row=0, sticky="w")

selected_font = StringVar(font_type_frame)
selected_font.set("Select Font")

all_fonts = font.families()

# Create a dropdown menu with a built-in scroll wheel option
font_type_combobox = ttk.Combobox(font_type_frame, textvariable=selected_font, state='readonly')
font_type_combobox['values'] = all_fonts
font_type_combobox.current(0)
font_type_combobox.bind("<<ComboboxSelected>>", change_font)
font_type_combobox.grid(column=1, row=0, padx=(10, 0), pady=10)

# ---------------------------- Font Size Widget ------------------------------- #
# Define a function to handle changes in the font size combobox
def change_size(event):
    # Retrieve the selected font size from the combobox
    selected_font_size = int(size_combobox.get())

    # Get current font
    current_font = canvas.itemcget('text', 'font').split()[0]
    print(current_font)

    # Update the font of the text widget
    canvas.itemconfig('text', font=(current_font, selected_font_size))


font_size_frame = Frame(window, bg='#3E3B36')
font_size_frame.grid(column=1, row=2, padx=10, pady=10, sticky="s")

# Define 2 columns in the size frame
for col in range(2):
    font_size_frame.columnconfigure(col, weight=1)

font_size_label = Label(font_size_frame, text="Font Size", font=(FONT_NAME, 12), fg='white', bg='#3E3B36')
font_size_label.grid(column=0, row=0, sticky="w")

# Create a list of font sizes to be displayed in the combobox
all_sizes = [str(i) for i in range(6, 101, 1)]

# Create the size combobox and add it to the size frame
selected_size = StringVar(font_size_frame)
selected_size.set(all_sizes[0])
size_combobox = ttk.Combobox(font_size_frame, values=all_sizes, textvariable=selected_size)
size_combobox.current(14)
size_combobox.config(width=5)
size_combobox.grid(column=1, row=0, padx=(10, 0), pady=10)

# Bind the ComboboxSelected event to the size combobox
size_combobox.bind("<<ComboboxSelected>>", change_size)

# ---------------------------- Opacity Widget ------------------------------- #
# opacity_frame = Frame(window, bg='#3E3B36')
# opacity_frame.grid(column=1, row=3, padx=10, pady=10, sticky="n")
#
# opacity_label = Label(opacity_frame, text="Opacity", font=(FONT_NAME, 12), fg='white', bg='#3E3B36')
# opacity_label.grid(column=0, row=0, sticky="w")
#
# # Define 2 columns for the opacity frame
# for col in range(2):
#     opacity_frame.columnconfigure(col, weight=1)

# Define a function to update the text item's opacity
# def update_opacity(val):
#     alpha = round(int(val)/100*255)  # Convert the slider value to an integer between 0 and 255
#     # get current color from text
#     current_color = canvas.itemcget('text', 'fill')
#     rgb_color = window.winfo_rgb(current_color)
#     # Convert the RGB values to the range 0-255
#     red = rgb_color[0] // 256
#     print(red)
#     green = rgb_color[1] // 256
#     print(green)
#     blue = rgb_color[2] // 256
#     print(blue)
#
#     # Add an alpha value to create an RGBA color
#     rgba_color = (red, green, blue, alpha)
#     print(rgba_color)
#
#     # Convert the RGBA color to a hexadecimal string format that tkinter can recognize
#     hex_color = '#{0:02x}{1:02x}{2:02x}{3:02x}'.format(*rgba_color)
#     print(hex_color)
#
#     canvas.itemconfig('text', fill=rgba_color)
#
#
# # Create a slider widget for adjusting opacity
# opacity_slider = Scale(opacity_frame, from_=0, to=100, orient=HORIZONTAL, length=200, command=update_opacity)
# opacity_slider.set(100)  # Set the initial opacity to 100% (1.0)
# opacity_slider.grid(column=1, row=0, padx=10, pady=10)

# ---------------------------- Text Move Widget ------------------------------- #
# text move widget
# function to move text up by 10 pixels

def move_text_up(event=None):
    canvas.move('text', 0, -10)

# function to move text down by 10 pixels
def move_text_down(event=None):
    canvas.move('text', 0, 10)

# function to move text left by 10 pixels
def move_text_left(event=None):
    canvas.move('text', -10, 0)

# function to move text right by 10 pixels
def move_text_right(event=None):
    canvas.move('text', 10, 0)


text_move_frame = Frame(window, bg='#3E3B36')
text_move_frame.grid(column=1, row=4, padx=10, pady=10, sticky="s")

# Define 3 columns for the text_move frame
for col in range(3):
    text_move_frame.columnconfigure(col, weight=1)

# Define 3 rows for the text_move frame
for row in range(4):
    text_move_frame.rowconfigure(row, weight=1)

movement_label = Label(text_move_frame, text="Text Movement", font=(FONT_NAME, 12), fg='white', bg='#3E3B36')
movement_label.grid(column=0, row=0, columnspan=3)

# up button
up_button = Button(text_move_frame, text="▲", font=(FONT_NAME, 12), command=move_text_up, bg="#36393e", fg="white", width=7)
up_button.grid(column=1, row=1, pady=10)

# down button
down_button = Button(text_move_frame, text="▼", font=(FONT_NAME, 12), command=move_text_down, bg="#36393e", fg="white", width=7)
down_button.grid(column=1, row=3, pady=10)

# left button
left_button = Button(text_move_frame, text="◀", font=(FONT_NAME, 12), command=move_text_left, bg="#36393e", fg="white", width=7)
left_button.grid(column=0, row=2, pady=10)

# right button
right_button = Button(text_move_frame, text="▶", font=(FONT_NAME, 12), command=move_text_right, bg="#36393e", fg="white", width=7)
right_button.grid(column=2, row=2, pady=10)

# ---------------------------- Rotation Widget ------------------------------- #

# function to rotate text 5 degrees clockwise
def rotate_anticlockwise(event=None):
    # get current angle of text
    current_angle = float(canvas.itemcget('text', 'angle'))
    new_angle = current_angle + 5
    # carry out the rotation clockwise
    canvas.itemconfig('text', angle=new_angle)

# function to rotate text 5 degrees anticlockwise
def rotate_clockwise(event=None):
    # get current angle of text
    current_angle = float(canvas.itemcget('text', 'angle'))
    new_angle = current_angle - 5
    canvas.itemconfig('text', angle=new_angle)


rotation_frame = Frame(window, bg='#3E3B36')
rotation_frame.grid(column=1, row=5, padx=10, pady=10, sticky="s")

# Define 2 columns for the rotation frame
for col in range(2):
    rotation_frame.columnconfigure(col, weight=1)

# Define 2 rows for the rotation frame
for row in range(2):
    rotation_frame.rowconfigure(row, weight=1)

rotation_label = Label(rotation_frame, text="Rotation", font=(FONT_NAME, 12), fg='white', bg='#3E3B36')
rotation_label.grid(column=0, row=0, columnspan=2)

# rotate anticlockwise button
anticlockwise_button = Button(rotation_frame, text="↺", font=(FONT_NAME, 15), command=rotate_anticlockwise, bg="#36393e", fg="white", width=7)
anticlockwise_button.grid(column=0, row=1, padx=10, pady=10)

# rotate clockwise button
clockwise_button = Button(rotation_frame, text="↻", font=(FONT_NAME, 15), command=rotate_clockwise, bg="#36393e", fg="white", width=7)
clockwise_button.grid(column=1, row=1, padx=10, pady=10)


# ---------------------------- Load Save Widget ------------------------------- #
def load_file():
    global resized_sample_image
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("jpg files", "*.jpg"), ("png files", "*.png"),
                                                     ("All files", "*.*")))
    if filename:
        # Open image file
        try:
            image = Image.open(filename)

        except PIL.UnidentifiedImageError:
            messagebox.showerror(title="Incorrect File Format",
                                 message=f"The file you tried to open is not 'png' or 'jpeg' format!")

        else:
            # resize image to fit canvas
            resized_image = image.resize((canvas.winfo_reqwidth(), canvas.winfo_reqheight()))

            # create PhotoImage object from resized image
            resized_sample_image = ImageTk.PhotoImage(resized_image)

            # create image on canvas
            loaded_pic = canvas.create_image(0, 0, image=resized_sample_image, anchor="nw", tag='picture')
            canvas.tag_lower(loaded_pic)


def save_file():
    filename = filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(("PNG files", "*.png"),),
                                            defaultextension=".png")
    print(filename)
    if filename:
        x = window.winfo_rootx() + canvas.winfo_x()
        y = window.winfo_rooty() + canvas.winfo_y()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        print(x, y, width, height)

        image = ImageGrab.grab(bbox=[x, y, x + width, y + height])
        image.save(fp=filename)


load_save_frame = Frame(window, bg='#3E3B36')
load_save_frame.grid(column=1, row=6, padx=10, pady=10, sticky="s")

# Define 2 columns for the rotation frame
for col in range(2):
    load_save_frame.columnconfigure(col, weight=1)

# Define 2 rows for the rotation frame
for row in range(2):
    load_save_frame.rowconfigure(row, weight=1)

load_label = Label(load_save_frame, text="Load File", font=(FONT_NAME, 12), fg='white', bg='#3E3B36')
load_label.grid(column=0, row=0)

save_label = Label(load_save_frame, text="Save File", font=(FONT_NAME, 12), fg='white', bg='#3E3B36')
save_label.grid(column=1, row=0)

load_button = Button(load_save_frame, text="📂", font=(FONT_NAME, 15), command=load_file, bg="#36393e", fg="white", width=7)
load_button.grid(column=0, row=1, padx=10, pady=10)

save_button = Button(load_save_frame, text="💾", font=(FONT_NAME, 15), command=save_file, bg="#36393e", fg="white", width=7)
save_button.grid(column=1, row=1, padx=10, pady=10)

# Make frames wider
window.columnconfigure(1, minsize=300)

window.mainloop()

# Decide what functionalities the Image Watermarking Desktop App should have
# TODO 1: Select the location to upload the image from
# TODO 2: Show the option to add text(add logo functionality later) or select from a template
# TODO 3: Provide the following property modifiers for the logo/text.
#  Text, font type, color, font size, Tile, Tile Spacing, Opacity, Rotation
# TODO 4: Add in the file save settings. Resize image optional
