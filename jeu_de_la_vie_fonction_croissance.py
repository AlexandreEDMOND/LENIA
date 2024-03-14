import pygame
from constants import *
import random
import numpy as np

class Game:

    def __init__(self, width, height, nmbre_case_width, nmbre_case_height):
        self.w = width
        self.h = height
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.nmbr_case_w = nmbre_case_width
        self.nmbr_case_h = nmbre_case_height
        self.long_case_w = int(self.w / self.nmbr_case_w)
        self.long_case_h = int(self.h / self.nmbr_case_h)
        self.board = []
    
    def init_board(self):
        self.board = []
        for _ in range(self.nmbr_case_h):
            line = []
            for _ in range(self.nmbr_case_w):
                line.append(0)
            self.board.append(line)

    def init_random_board(self):
        self.board = []
        for _ in range(self.nmbr_case_h):
            line = []
            for _ in range(self.nmbr_case_w):
                line.append(random.random())
            self.board.append(line)

    def affichage_quadrillage(self):
        
        for dw in range(self.nmbr_case_w):
            pygame.draw.line(self.screen, NOIR, (dw*self.long_case_w, 0), (dw*self.long_case_w, self.h))
        
        for dh in range(self.nmbr_case_h):
            pygame.draw.line(self.screen, NOIR, (0, dh*self.long_case_h), (self.w, dh*self.long_case_h))

    # Fonction gaussienne centrée en 3 prenant les valeurs de -1 à 1
    def fonction_croissance(self, x):
        return 2*np.exp(-((x-0.40)/0.2) ** 2)-1

    def affichage_board(self):
        for dh in range(self.nmbr_case_h):
            for dw in range(self.nmbr_case_w):
                pygame.draw.rect(self.screen, tuple(self.board[dh][dw]* color for color in BLANC), pygame.Rect(dw*self.long_case_w, dh*self.long_case_h, self.long_case_w, self.long_case_h))

    def calcul_score_near(self, h, w, rayon=1):
        score = 0
        for dh in range(h-rayon, h+rayon+1):
            for dw in range(w-rayon, w+rayon+1):
                if dw == w and dh == h:
                    continue
                if dw < 0:
                    dw += self.nmbr_case_w
                if dw >= self.nmbr_case_w:
                    dw -= self.nmbr_case_w
                if dh < 0:
                    dh += self.nmbr_case_h
                if dh >= self.nmbr_case_h:
                    dh -= self.nmbr_case_h
                score += self.board[dh][dw]
        return score

    def calcul_next_board(self):
        new_board = []
        rayon = 1
        for dh in range(self.nmbr_case_h):
            new_line = []
            for dw in range(self.nmbr_case_w):
                score = self.calcul_score_near(dh, dw, rayon)
                taux_croissance = self.fonction_croissance(score/( (2*rayon + 1)**2 - 1) )
                new_value = self.board[dh][dw]*(1+taux_croissance)
                if new_value > 1:
                    new_value = 1
                if new_value < 0:
                    new_value = 0
                new_line.append(new_value)
            new_board.append(new_line)
        return new_board

    def main_loop(self):
        pygame.display.set_caption('LENIA')
        pygame.init()
        
        self.init_board()
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_r:
                            self.init_random_board()
                        if event.key == pygame.K_i:
                            self.init_board()
            
            self.screen.fill(BLANC)

            
            #self.affichage_quadrillage()
            self.affichage_board()
            self.board = self.calcul_next_board()

            pygame.display.flip()