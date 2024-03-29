import pygame
import random
import sys
import os
from queue import PriorityQueue
import math
import heapq

current_dir = os.path.dirname(__file__)
os.chdir(current_dir)

# inicializar pygame
pygame.init()
pygame.font.init()
fonte = pygame.font.Font("arial.ttf", 36)

# tela
largura_tela = 800
altura_tela = 600
tamanho_celula = 40
tela = pygame.display.set_mode((largura_tela, altura_tela))

global nivel
nivel = 1
global pontuacao
pontuacao = 0
tempo_de_inicio = pygame.time.get_ticks()
pontos_brancos = []
frutas = []

mapa = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

pacman_tamanho = 20
fantasma_tamanho = 20

# cores
preto = (0, 0, 0)
azul = (0, 0, 255)
branco = (255, 255, 255)
vermelho = (255, 0, 0)

# sprites
pacman = pygame.image.load("pacman.png")
pacman = pygame.transform.scale(pacman, (tamanho_celula, tamanho_celula))
blinky_sprite = pygame.image.load("blinky.png")
blinky_sprite = pygame.transform.scale(blinky_sprite, (tamanho_celula, tamanho_celula))
clyde_sprite = pygame.image.load("clyde.png")
clyde_sprite = pygame.transform.scale(clyde_sprite, (tamanho_celula, tamanho_celula))
inky_sprite = pygame.image.load("inky.png")
inky_sprite = pygame.transform.scale(inky_sprite, (tamanho_celula, tamanho_celula))
pinky_sprite = pygame.image.load("pinky.png")
pinky_sprite = pygame.transform.scale(pinky_sprite, (tamanho_celula, tamanho_celula))
chao = pygame.image.load('chao.png')
chao = pygame.transform.scale(chao, (tamanho_celula, tamanho_celula))
parede = pygame.image.load('parede.png')
parede = pygame.transform.scale(parede, (tamanho_celula, tamanho_celula))

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direcao = 0
        self.velocidade = 2

    # teclas de controle
    def atualizar(self):
        # 0 parado,  1 esquerda, 2 direita, 3 cima, 4 baixo
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.direcao = 1
        elif teclas[pygame.K_RIGHT]:
            self.direcao = 2
        elif teclas[pygame.K_UP]:
            self.direcao = 3
        elif teclas[pygame.K_DOWN]:
            self.direcao = 4

        # manter ele se movendo depois de apertar 1 tecla
        if self.direcao == 0:
            self.x - self.velocidade
            self.y - self.velocidade
        if self.direcao == 1:
            novo_x = self.x - self.velocidade
            if not colisao_parede(novo_x, self.y):
                self.x = novo_x
        elif self.direcao == 2:
            novo_x = self.x + self.velocidade
            if not colisao_parede(novo_x + tamanho_celula - 1, self.y):
                self.x = novo_x
        elif self.direcao == 3:
            novo_y = self.y - self.velocidade
            if not colisao_parede(self.x, novo_y):
                self.y = novo_y
        elif self.direcao == 4:
            novo_y = self.y + self.velocidade
            if not colisao_parede(self.x, novo_y + tamanho_celula - 1):
                self.y = novo_y

    def desenhar(self, tela):
        tela.blit(pacman, (self.x, self.y))

class Blinky:   
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 2
        self.direcao = 0
        self.tempo_parado = 0

    def atualizar(self):
        # algoritmo A*
        caminho = encontrar_caminho((self.x, self.y), (pacman_sprite.x, pacman_sprite.y), mapa)
        if caminho:
            proximo_destino = caminho
            dx = proximo_destino[0] - self.x
            dy = proximo_destino[1] - self.y
            if dx > 0:
                self.direcao = 2  # direita
            elif dx < 0:
                self.direcao = 1  # esquerda
            elif dy > 0:
                self.direcao = 4  # baixo
            elif dy < 0:
                self.direcao = 3  # cima
            else:
                # caminho não encontrado
                self.velocidade = 0

        if self.direcao == 1:  # esquerda
            novo_x = self.x - self.velocidade
            if not colisao_parede(novo_x, self.y):
                self.x = novo_x

        elif self.direcao == 2:  # direita
            novo_x = self.x + self.velocidade
            if not colisao_parede(novo_x + tamanho_celula - 1, self.y):
                self.x = novo_x

        elif self.direcao == 3:  # cima
            novo_y = self.y - self.velocidade
            if not colisao_parede(self.x, novo_y):
                self.y = novo_y

        elif self.direcao == 4:  # baixo
            novo_y = self.y + self.velocidade
            if not colisao_parede(self.x, novo_y + tamanho_celula - 1):
                self.y = novo_y
                    
    def colidir_com_fruta_vermelha(self):
        self.velocidade = 0
        self.tempo_parado = pygame.time.get_ticks()

    def voltar_a_se_mover(self):
        self.velocidade = 2   

    def desenhar(self, tela):
        tela.blit(blinky_sprite, (self.x, self.y))

class Pinky:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 1
        self.direcao = random.choice([1, 2, 3, 4]) #  1 esquerda, 2 direita, 3 cima, 4 baixo
        self.tempo_parado = 0

    def atualizar(self):
        novo_x, novo_y = self.x, self.y

        if self.direcao == 1:  # esquerda
            novo_x = self.x - self.velocidade
            if not colisao_parede(novo_x, self.y):
                self.x = novo_x
            else:
                self.direcao = random.choice([2, 3, 4])

        elif self.direcao == 2:  # direita
            novo_x = self.x + self.velocidade
            if not colisao_parede(novo_x + tamanho_celula - 1, self.y):
                self.x = novo_x
            else:
                self.direcao = random.choice([1, 3, 4])

        elif self.direcao == 3:  # cima
            novo_y = self.y - self.velocidade
            if not colisao_parede(self.x, novo_y):
                self.y = novo_y
            else:
                self.direcao = random.choice([1, 2, 4])

        elif self.direcao == 4:  # baixo
            novo_y = self.y + self.velocidade
            if not colisao_parede(self.x, novo_y + tamanho_celula - 1):
                self.y = novo_y
            else:
                self.direcao = random.choice([1, 2, 3])

    def colidir_com_fruta_vermelha(self):
        self.velocidade = 0
        self.tempo_parado = pygame.time.get_ticks()

    def voltar_a_se_mover(self):
        self.velocidade = 1   

    def desenhar(self, tela):
        tela.blit(pinky_sprite, (self.x, self.y))

class Inky:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 1
        self.direcao = 0 #  0 parado, 1 esquerda, 2 direita, 3 cima, 4 baixo
        self.tempo_parado = 0

    def atualizar(self):
        proxima_direcao = self.busca_gulosa((pacman_sprite.x, pacman_sprite.y))
        
        # atualizar dreção
        if proxima_direcao:
            self.direcao = proxima_direcao

        novo_x, novo_y = self.x, self.y

        if self.direcao == 0: # parado
            self.velocidade = 0

        if self.direcao == 1:  # esquerda
            self.velocidade = 1
            novo_x = self.x - self.velocidade
            if not colisao_parede(novo_x, self.y):
                self.x = novo_x

        elif self.direcao == 2:  # direita
            self.velocidade = 1
            novo_x = self.x + self.velocidade
            if not colisao_parede(novo_x + tamanho_celula - 1, self.y):
                self.x = novo_x

        elif self.direcao == 3:  # cima
            self.velocidade = 1
            novo_y = self.y - self.velocidade
            if not colisao_parede(self.x, novo_y):
                self.y = novo_y

        elif self.direcao == 4:  # baixo
            self.velocidade = 1
            novo_y = self.y + self.velocidade
            if not colisao_parede(self.x, novo_y + tamanho_celula - 1):
                self.y = novo_y

    def busca_gulosa(self, objetivo):
        # heuristica
        def distancia_euclidiana(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        acoes_possiveis = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    novo_x = self.x + dx * self.velocidade
                    novo_y = self.y + dy * self.velocidade

                    if not colisao_parede(novo_x, novo_y):
                        acoes_possiveis.append((novo_x, novo_y))

        # calcula a heurística para cada ação possível
        heuristicas = [distancia_euclidiana(acao, objetivo) for acao in acoes_possiveis]

        # escolhe a ação com a menor heurística
        if heuristicas:
            melhor_acao_index = heuristicas.index(min(heuristicas))
            melhor_acao = acoes_possiveis[melhor_acao_index]
            
            # calcula a direção
            dx = melhor_acao[0] - self.x
            dy = melhor_acao[1] - self.y
            
            if dx == 0:
                if dy < 0:
                    return 3  # cima
                else:
                    return 4  # baixo
            elif dx < 0:
                return 1  # esquerda
            else:
                return 2  # direita

        # fica parado se nao tiver nada para fazer
        return 0

    def colidir_com_fruta_vermelha(self):
        self.velocidade = 0
        self.tempo_parado = pygame.time.get_ticks()

    def voltar_a_se_mover(self):
        self.velocidade = 1

    def desenhar(self, tela):
        tela.blit(inky_sprite, (self.x, self.y))

class Clyde:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 1
        self.direcao = 0  # 0 parado, 1 esquerda, 2 direita, 3 cima, 4 baixo
        self.tempo_parado = 0

    def atualizar(self):
        proxima_direcao = self.busca_gulosa(mapa, (self.x, self.y), (pacman_sprite.x, pacman_sprite.y))

        # Atualize a direção se for possível
        if proxima_direcao:
            self.direcao = proxima_direcao

        # Calcule as posições de destino na grade
        novo_x, novo_y = self.x, self.y

        if self.direcao == 0:  # Parado
            self.velocidade = 0

        if self.direcao == 1:  # Esquerda
            novo_x = self.x - self.velocidade
            if not colisao_parede(novo_x, self.y):
                self.x = novo_x

        elif self.direcao == 2:  # Direita
            novo_x = self.x + self.velocidade
            if not colisao_parede(novo_x, self.y):
                self.x = novo_x

        elif self.direcao == 3:  # Cima
            novo_y = self.y - self.velocidade
            if not colisao_parede(novo_x, self.y):
                self.y = novo_y

        elif self.direcao == 4:  # Baixo
            novo_y = self.y + self.velocidade
            if not colisao_parede(novo_x, self.y):
                self.y = novo_y

    def busca_gulosa(self, mapa, inicio, objetivo):
        # Função para calcular a distância de Manhattan entre dois pontos
        def distancia_manhattan(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return abs(x1 - x2) + abs(y1 - y2)

        # Obtém todas as ações possíveis (movimentos) a partir da posição atual
        acoes_possiveis = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    novo_x = self.x + dx * self.velocidade
                    novo_y = self.y + dy * self.velocidade

                    if not colisao_parede(novo_x, novo_y):
                        acoes_possiveis.append((novo_x, novo_y))

        # Calcula a heurística (distância de Manhattan) para cada ação possível
        heuristicas = [distancia_manhattan(acao, objetivo) for acao in acoes_possiveis]

        # Escolhe a ação com a menor heurística (menor distância de Manhattan)
        if heuristicas:
            melhor_acao_index = heuristicas.index(min(heuristicas))
            melhor_acao = acoes_possiveis[melhor_acao_index]

            # Calcula a direção com base na ação escolhida
            dx = melhor_acao[0] - self.x
            dy = melhor_acao[1] - self.y

            if dx == 0:
                if dy < 0:
                    return 3  # Cima
                else:
                    return 4  # Baixo
            elif dx < 0:
                return 1  # Esquerda
            else:
                return 2  # Direita

        # Se não houver ações possíveis, retorna 0 (parado)
        return 0

    def colidir_com_fruta_vermelha(self):
        self.velocidade = 0
        self.tempo_parado = pygame.time.get_ticks()

    def voltar_a_se_mover(self):
        self.velocidade = 1

    def desenhar(self, tela):
        tela.blit(clyde_sprite, (self.x, self.y))

def encontrar_caminho(inicio, objetivo, mapa):
    # cima, baixo, esquerda, direita
    movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # distância de Manhattan
    def heuristica(ponto, objetivo):
        return abs(ponto[0] - objetivo[0]) + abs(ponto[1] - objetivo[1])

    fila_aberta = [(0, inicio)]
    custos = {inicio: 0}

    while fila_aberta:
        custo_atual, posicao_atual = heapq.heappop(fila_aberta)

        if posicao_atual == objetivo:
            # reconstrir o caminho
            caminho = []
            while posicao_atual in custos:
                caminho.insert(0, posicao_atual)
                posicao_atual = custos[posicao_atual]
            return caminho

        for dx, dy in movimentos:
            nova_posicao = (posicao_atual[0] + dx, posicao_atual[1] + dy)

            if nova_posicao[0] < 0 or nova_posicao[0] >= len(mapa) or \
               nova_posicao[1] < 0 or nova_posicao[1] >= len(mapa[0]) or \
               mapa[nova_posicao[0]][nova_posicao[1]] == 1:
                continue

            novo_custo = custo_atual + 1

            if nova_posicao not in custos or novo_custo < custos[nova_posicao]:
                custos[nova_posicao] = novo_custo
                prioridade = novo_custo + heuristica(nova_posicao, objetivo)
                heapq.heappush(fila_aberta, (prioridade, nova_posicao))

    # se nenhum caminho foi encontrado, retorna vazio
    return []

# instâncias
pacman_sprite = Pacman(int(largura_tela // 2 + tamanho_celula), int(altura_tela // 2 - tamanho_celula / 2))
pinky = Pinky(11 * tamanho_celula, 1 * tamanho_celula)
inky = Inky(10 * tamanho_celula, 1 * tamanho_celula)
clyde = Clyde(9 * tamanho_celula, 1 * tamanho_celula)
blinky = Blinky(8 * tamanho_celula, 1 * tamanho_celula)
fantasmas = [pinky, inky, clyde, blinky]

# desenha o mapa
def desenhar_mapa():
    global mapa

    for linha in range(len(mapa)):
        for coluna in range(len(mapa[0])):
            if mapa[linha][coluna] == 0:
                ponto = pygame.Rect(coluna * tamanho_celula + tamanho_celula // 4, linha * tamanho_celula + tamanho_celula // 4, tamanho_celula // 2, tamanho_celula // 2)
                if ponto in pontos_brancos:
                    pygame.draw.circle(tela, preto, (coluna * tamanho_celula + tamanho_celula // 2, linha * tamanho_celula + tamanho_celula // 2), tamanho_celula // 8)
                else:
                    pygame.draw.circle(tela, branco, (coluna * tamanho_celula + tamanho_celula // 2, linha * tamanho_celula + tamanho_celula // 2), tamanho_celula // 8)
            elif mapa[linha][coluna] == 1:
                tela.blit(parede, (coluna * tamanho_celula, linha * tamanho_celula))
            elif mapa[linha][coluna] == 2:
                pygame.draw.circle(tela, vermelho, (coluna * tamanho_celula + tamanho_celula // 2, linha * tamanho_celula + tamanho_celula // 2), tamanho_celula // 4)

# verifica colisões
def colisao_parede(x, y):
    i = x // tamanho_celula
    j = y // tamanho_celula

    if x < 0 or x >= largura_tela or y < 0 or y >= altura_tela:
        return True

    return mapa[j][i] == 1

# verifica colisões entre 2 retangulos
def colisao_retangulo(retangulo1, retangulo2):
    return retangulo1.colliderect(retangulo2)

# tela de derrota
def tela_derrota():
    derrota = True
    while derrota:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Esc sai do jogo
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_RETURN:  # Enter preinicia o jogo
                    reiniciar_jogo(pacman_sprite, fantasmas)

        tela.fill(preto)
        texto_derrota = fonte.render("Você Perdeu!", True, (255, 0, 0))
        texto_retangulo = texto_derrota.get_rect()
        texto_retangulo.center = (largura_tela // 2, altura_tela // 2 - (2 * tamanho_celula))
        texto_instrucoes = fonte.render("Pressione Enter para reiniciar ou Esc para sair.", True, (255, 255, 255))
        texto_retangulo2 = texto_instrucoes.get_rect()
        texto_retangulo2.center = (largura_tela // 2, altura_tela // 2)
        tela.blit(texto_derrota, texto_retangulo.topleft)
        tela.blit(texto_instrucoes, texto_retangulo2.topleft)
        pygame.display.flip()

# tela de vitoria
def tela_vitoria():
    vitoria = True
    global nivel
    while vitoria:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Esc sai do jogo
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_RETURN:  # Enter reinicia o jogo
                    nivel += 1
                    proximo_nivel()
                    reiniciar_jogo(pacman_sprite, fantasmas)

        tela.fill(preto)
        texto_vitoria = fonte.render("Você Venceu!", True, (0, 255, 0))
        texto_retangulo = texto_vitoria.get_rect()
        texto_retangulo.center = (largura_tela // 2, altura_tela // 2 - (2 * tamanho_celula))

        texto_instrucoes = fonte.render("Pressione Enter para jogar novamente ou Esc para sair.", True, (255, 255, 255))
        texto_retangulo2 = texto_instrucoes.get_rect()
        texto_retangulo2.center = (largura_tela // 2, altura_tela // 2)

        texto_pontuacao = fonte.render("Pontuacao: " + str(pontuacao), True, (0, 0 , 255))
        texto_retangulo3 = texto_pontuacao.get_rect()
        texto_retangulo3.center = (largura_tela // 2, altura_tela // 2 + 100)

        tela.blit(texto_vitoria, texto_retangulo.topleft)
        tela.blit(texto_instrucoes, texto_retangulo2.topleft)
        tela.blit(texto_pontuacao, texto_retangulo3.topleft)

        pygame.display.flip()

# recomeça o jogo
def reiniciar_jogo(pacman_sprite, fantasmas):
    global pontuacao
    pontuacao = 0
    global tempo_de_inicio
    tempo_de_inicio = 0

    # limpa o mapa
    pontos_brancos.clear()
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[0])):
            if mapa[linha][coluna] == -1:
                mapa[linha][coluna] = 0

    # reinicie as posições dos personagens
    pacman_sprite.x = int(largura_tela // 2 + tamanho_celula)
    pacman_sprite.y = int(altura_tela // 2 - tamanho_celula / 2)
    pinky.x = 11 * tamanho_celula
    pinky.y = 1 * tamanho_celula
    pinky.velocidade = 1
    inky.x = 10 * tamanho_celula
    inky.y = 1 * tamanho_celula
    inky.velocidade = 1
    clyde.x = 9 * tamanho_celula
    clyde.y = 1 * tamanho_celula
    clyde.velocidade = 1
    blinky.x = 8 * tamanho_celula
    blinky.y = 1 * tamanho_celula
    blinky.velocidade = 1.5

    # garantir que os fantasmas nao fiquem parados
    for fantasma in fantasmas:
        fantasma.velocidade = 1

    # frutas
    for fruta in frutas:
        mapa[fruta.y // tamanho_celula][fruta.x // tamanho_celula] = 2

    # reinicia a pontuação
    pontos_brancos.clear()
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[0])):
            if mapa[linha][coluna] == 0:
                pontos_brancos.append(pygame.Rect(coluna * tamanho_celula, linha * tamanho_celula, tamanho_celula, tamanho_celula))

    # continua o jogo
    jogo(pacman_sprite, fantasmas)

# delimita a condição de vitória, 0 pontos brancos no mapa
def contar_pontos_brancos_no_mapa():
    contador = 0
    for linha in mapa:
        contador += linha.count(0)
    return contador

# exibe a pontuação
def exibir_pontuacao(pontuacao):
    texto_pontos = fonte.render("Pontuação: " + pontuacao, True, (255, 255, 255))
    tela.blit(texto_pontos, (0, 0))

# exibe o tempo de jogo
def exibir_tempo_de_jogo(tempo_de_inicio):
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido = (tempo_atual - tempo_de_inicio) // 1000  # converte milissegundos em segundos
    minutos = tempo_decorrido // 60
    segundos = tempo_decorrido % 60

    tempo_formatado = "{:02d}:{:02d}".format(minutos, segundos)

    texto_tempo = fonte.render("Tempo: " + tempo_formatado, True, branco)
    tela.blit(texto_tempo, (580, 0))

# troca o mapa e recomeça o jogo
def proximo_nivel():
    global mapa

    if nivel == 2:
        mapa = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    if nivel == 3:
        mapa = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    reiniciar_jogo(pacman_sprite, fantasmas)

# "main"
def jogo(pacman_sprite, fantasmas):
    global mapa
    global pontuacao
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # limpa a tela
        tela.fill(preto)

        # desenha o mapa
        desenhar_mapa()

        for fantasma in fantasmas:
            fantasma.atualizar()
            fantasma.desenhar(tela)
            if fantasma.velocidade == 0:
                tempo_atual = pygame.time.get_ticks()
                tempo_decorrido = tempo_atual - fantasma.tempo_parado

                # 7 segundos
                if tempo_decorrido >= 7000:
                    fantasma.voltar_a_se_mover()

        pacman_sprite.atualizar()
        pacman_sprite.desenhar(tela)

        # retangulos
        pacman_rect = pygame.Rect(pacman_sprite.x, pacman_sprite.y, tamanho_celula, tamanho_celula)
        blinky_rect = pygame.Rect(blinky.x, blinky.y, tamanho_celula, tamanho_celula)
        clyde_rect = pygame.Rect(clyde.x, clyde.y, tamanho_celula, tamanho_celula)
        inky_rect = pygame.Rect(inky.x, inky.y, tamanho_celula, tamanho_celula)
        pinky_rect = pygame.Rect(pinky.x, pinky.y, tamanho_celula, tamanho_celula)

        # verifica colisões dos retangulos
        if (colisao_retangulo(pacman_rect, blinky_rect) or
            colisao_retangulo(pacman_rect, clyde_rect) or
            colisao_retangulo(pacman_rect, inky_rect) or
            colisao_retangulo(pacman_rect, pinky_rect)):
            tela_derrota()

        # pontos
        for linha in range(len(mapa)):
            for coluna in range(len(mapa[0])):
                if mapa[linha][coluna] == 0:
                    ponto = pygame.Rect(coluna * tamanho_celula + tamanho_celula // 4, linha * tamanho_celula + tamanho_celula // 4, tamanho_celula // 2, tamanho_celula // 2)
                    if ponto.colliderect(pacman_rect):
                        pontuacao += 10
                        mapa[linha][coluna] = -1  # marca o ponto como coletado

        if contar_pontos_brancos_no_mapa() == 0:
            tela_vitoria()

        # frutas vermelhas
        for linha in range(len(mapa)):
            for coluna in range(len(mapa[0])):
                if mapa[linha][coluna] == 2:
                    fruta = pygame.Rect(coluna * tamanho_celula + tamanho_celula // 4, linha * tamanho_celula + tamanho_celula // 4, tamanho_celula // 2, tamanho_celula // 2)
                    if fruta.colliderect(pacman_rect):
                        pontuacao += 50
                        for fantasma in fantasmas:
                            fantasma.colidir_com_fruta_vermelha()
                        frutas.append(fruta)
                        mapa[linha][coluna] = -1  # marca o ponto como coletado

        exibir_pontuacao(str(pontuacao))
        exibir_tempo_de_jogo(tempo_de_inicio)

        pygame.display.flip()

# jogar
jogo(pacman_sprite, fantasmas)