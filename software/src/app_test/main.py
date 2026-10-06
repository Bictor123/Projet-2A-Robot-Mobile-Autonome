'''
Inspiration tuto:
https://www.google.com/search?q=cr%C3%A9er+application+mobile+android+sur+python+tutoriel&ie=UTF-8#fpstate=ive&vld=cid:5c392bd7-654b-497d-aa8a-eae86387a61f_d97b3f3d,vid:ykCUSLV0pdo,st:0
'''


import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import random

kivy.require('2.0.0')


class GameView(BoxLayout):
    def __init__(self):
        super(GameView, self).__init__()
        self.randomValue= random.randint(0,1000)

    def check_number(self):
        if int(self.answer_input.text)== self.randomValue:
            self.result_label.text= "Bravo!"
            self.result_label.color= "#00EF0B"
            self.randomValue= random.randint(0,1000)
        elif int(self.answer_input.text) > self.randomValue : 
            self.result_label.text= "Less mon petit "
            self.result_label.color= "#FFFF00"
        elif int(self.answer_input.text) < self.randomValue : 
            self.result_label.text= "More mon grand "
            self.result_label.color= "#EF3E00"

class TahProjet(App):
    def build (self):
        return GameView()

tahProjet=TahProjet()
tahProjet.run()
