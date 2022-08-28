from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
CURR_WORD = {}

# -------------------- READING DATA -------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

words = data.to_dict(orient="records")


# -------------------- NEXT WORD -------------------- #
def next_word():
    global CURR_WORD, FLIP_TIMER
    root.after_cancel(FLIP_TIMER)
    CURR_WORD = random.choice(words)
    canvas.itemconfigure(curr_side, image=img_front)
    canvas.itemconfigure(language_text, text="French", fill="black")
    canvas.itemconfigure(word_text, text=CURR_WORD["French"], fill="black")
    FLIP_TIMER = root.after(3000, func=flip_card)


# -------------------- FLIP CARD -------------------- #
def flip_card():
    canvas.itemconfigure(curr_side, image=img_back)
    canvas.itemconfigure(language_text, text="English", fill="white")
    canvas.itemconfigure(word_text, text=CURR_WORD["English"], fill="white")


# -------------------- RIGHT BUTTON -------------------- #
def right_btn():
    words.remove(CURR_WORD)
    next_word()


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
button_right = Button(image=image_right, highlightthickness=0, borderwidth=0, command=right_btn)
button_right.grid(row=1, column=1)

image_wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=image_wrong, highlightthickness=0, borderwidth=0, command=next_word)
button_wrong.grid(row=1, column=0)

# First Word
FLIP_TIMER = root.after(3000, func=flip_card)
next_word()


root.mainloop()

# -------------------- REMOVE KNOWN WORDS FOR NEXT RUNS -------------------- #
words_to_learn = pandas.DataFrame(words)
words_to_learn.to_csv("data/words_to_learn.csv", index=False)
