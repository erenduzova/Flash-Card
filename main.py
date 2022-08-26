from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
CURR_WORD = {}

# -------------------- READING DATA -------------------- #
data = pandas.read_csv("data/french_words.csv")
words_to_learn = data.to_dict(orient="records")


# -------------------- NEW WORD -------------------- #
def next_word():
    global CURR_WORD, FLIP_TIMER
    root.after_cancel(FLIP_TIMER)
    CURR_WORD = random.choice(words_to_learn)
    canvas.itemconfigure(curr_side, image=img_front)
    canvas.itemconfigure(language_text, text="French", fill="black")
    canvas.itemconfigure(word_text, text=CURR_WORD["French"], fill="black")
    FLIP_TIMER = root.after(3000, func=flip_card)


# -------------------- FLIP CARD -------------------- #
def flip_card():
    canvas.itemconfigure(curr_side, image=img_back)
    canvas.itemconfigure(language_text, text="English", fill="white")
    canvas.itemconfigure(word_text, text=CURR_WORD["English"], fill="white")


# -------------------- UI SETUP -------------------- #
root = Tk()
root.title("Flash Card")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(root, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Card images
img_back = PhotoImage(file="images/card_back.png")
img_front = PhotoImage(file="images/card_front.png")
curr_side = canvas.create_image(400, 263, image=img_front)

# Canvas Text
language_text = canvas.create_text(400, 150, font=("Ariel", 40, "italic"), text="Language")
word_text = canvas.create_text(400, 263, font=("Ariel", 60, "bold"), text="Word")

# Right and Wrong Buttons
image_right = PhotoImage(file="images/right.png")
button_right = Button(image=image_right, highlightthickness=0, borderwidth=0, command=next_word)
button_right.grid(row=1, column=1)

image_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=image_wrong, highlightthickness=0, borderwidth=0, command=next_word)
button_wrong.grid(row=1, column=0)

# First Word
next_word()
FLIP_TIMER = root.after(3000, func=flip_card)

root.mainloop()
