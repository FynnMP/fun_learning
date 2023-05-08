import tkinter as tk
import random
from tkinter import messagebox
import time

class MemoryTile:
    def __init__(self, parent):
        self.parent = parent
        self.buttons = [[tk.Button(root,
                                   width=8,
                                   height=4,
                                   wraplength=85,
                                   command=lambda row=row, column=column: self.choose_tile(row, column)
                                   ) for column in range(4)] for row in range(4)]
        for row in range(4):
            for column in range(4):
                self.buttons[row][column].grid(row=row, column=column)
        self.first = None
        self.draw_board()

        self.sentences = {
            'A': 'Reflexive Gestaltungspraxis.',
            'B': 'Sie ist in den Kontext eingebettet.',
            'C': 'Sentence C is ready.',
            'D': 'Get ready for sentence D.',
            'E': 'This is sentence E.',
            'F': 'Here comes sentence F.',
            'G': 'Sentence G is ready.',
            'H': 'Get ready for sentence H.',
        }

        self.score = 0  # Score counter
        self.score_label = tk.Label(root, text='Gewinn CHF: 0')  # Score label
        self.score_label.grid(row=5, columnspan=4)  # Place the score label below the game

    def draw_board(self):
        self.answer = list('AABBCCDDEEFFGGHH')
        random.shuffle(self.answer)
        self.answer = [self.answer[:4],
                       self.answer[4:8],
                       self.answer[8:12],
                       self.answer[12:]]
        for row in self.buttons:
            for button in row:
                button.config(text='', state=tk.NORMAL)
        self.start_time = time.monotonic()

    def choose_tile(self, row, column):
        tile = self.answer[row][column]
        self.buttons[row][column].config(text=self.sentences[tile])
        self.buttons[row][column].config(state=tk.DISABLED)
        if not self.first:
            self.first = (row, column)
        else:
            a, b = self.first
            if self.answer[row][column] == self.answer[a][b]:
                self.answer[row][column] = ''
                self.answer[a][b] = ''
                self.score += 100  # Increment the score
                self.score_label.config(text='Gewinn CHF: {}'.format(self.score))  # Update the score label
                if not any(''.join(row) for row in self.answer):
                    duration = time.monotonic() - self.start_time
                    messagebox.showinfo(title='Success!', message='You win! Time: {:.1f}'.format(duration))
                    self.parent.after(5000, self.draw_board)
            else:
                self.parent.after(3000, self.hide_tiles, row, column, a, b)
            self.first = None

    def hide_tiles(self, x1, y1, x2, y2):
        self.buttons[x1][y1].config(text='', state=tk.NORMAL)
        self.buttons[x2][y2].config(text='', state=tk.NORMAL)


root = tk.Tk()
memory_tile = MemoryTile(root)
root.mainloop()
