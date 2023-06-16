import pygame
from pygame.locals import *

# Andre Luiz Vieira Mostaro - 22006533
# Gabriel Gomes Bobrov Lopes - 21953131
# Gustavo Mateus de Sousa de Santana - 21954293
# Higor da Silva Rocha - 22002910

pygame.init()

# define o tamanho da tela do jogo e texto do cabeçalho
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Programação de Jogos // Grupo 5 - BREAKOUT')

# define a fonte aplicada
font = pygame.font.SysFont('Constantia', 30)

# define cor do background
bg = (255, 255, 255)

# define as cores dos grupos de blocos
ceub_roxo_escuro = (67, 5, 78)
ceub_roxo = (102, 44, 146)
ceub_lilas = (191, 0, 135)

# define cor da barra e sua borda
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)

# define a cor do texto printado na tela
text_col = (78, 81, 139)

# define as variaveis aplicadas ao jogo

cols = 6 # aumento a qtdade de colunas por linhas de blocos
rows = 6 # aumento a qtdade de linhas de blocos
clock = pygame.time.Clock() # atualizacao de tela

fps = 60 # quanto maior fps, maior velocidade
live_ball = False
game_over = 0

# funcao para exibir texto na tela do jogo
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# define a classe da parede de tijolos
class wall():
	def __init__(self):
		self.width = screen_width // cols # define o comp de cada bloco dividindo o tamanho da tela pela qtdade de colunas de blocos
		self.height = 50

	# funcao de criacao do bloco de tijolos e forma a parede
	def create_wall(self):
		self.blocks = []
		block_individual = []
		for row in range(rows):
			block_row = []
			# faz iteracao por cada coluna na linha
			for col in range(cols):
				# gera as posições x e y para cada bloco e cria um retângulo
				block_x = col * self.width
				block_y = row * self.height
				rect = pygame.Rect(block_x, block_y, self.width, self.height)
				# atribuir força de bloqueio com base na linha
				if row < 2:
					strength = 3
				elif row < 4:
					strength = 2
				elif row < 6:
					strength = 1
					# cria uma lista para armazenar os dados de retângulo e forca
				block_individual = [rect, strength]
				# adiciona o bloco individual na linha
				block_row.append(block_individual)
			# adiciona a linha na lista de blocos
			self.blocks.append(block_row)

	# funcao de desenho da parede com as cores setadas
	def draw_wall(self):
		for row in self.blocks:
			for block in row:
				if block[1] == 3:
					block_col = ceub_roxo_escuro
				elif block[1] == 2:
					block_col = ceub_roxo
				elif block[1] == 1:
					block_col = ceub_lilas
				pygame.draw.rect(screen, block_col, block[0])
				pygame.draw.rect(screen, bg, (block[0]), 2)

#define a classe da barra
class paddle():
	def __init__(self):
		self.reset()

	# funcao de movimento da barra
	def move(self):
		self.direction = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.rect.left > 0:
			self.rect.x -= self.speed
			self.direction = -1
		if key[pygame.K_RIGHT] and self.rect.right < screen_width:
			self.rect.x += self.speed
			self.direction = 1

	# funcao de desenho da barra
	def draw(self):
		pygame.draw.rect(screen, paddle_col, self.rect)
		pygame.draw.rect(screen, paddle_outline, self.rect, 3)

	# funcao de reset da barra
	def reset(self):
		self.height = 20
		self.width = int(screen_width / cols)
		self.x = int((screen_width / 2) - (self.width / 2))
		self.y = screen_height - (self.height * 2)
		self.speed = 10
		self.rect = Rect(self.x, self.y, self.width, self.height)
		self.direction = 0

# define a classe da bolinha
class game_ball():
	def __init__(self, x, y):
		self.reset(x, y)

	# funcao de movimento da bolinha
	def move(self):
		# define o limiar de colisao
		collision_thresh = 5
		# inicia supondo que a parede esta toda destruida
		wall_destroyed = 1
		row_count = 0
		for row in wall.blocks:
			item_count = 0
			for item in row:
				# checa colisao
				if self.rect.colliderect(item[0]):
					# colisao de cima
					if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
						self.speed_y *= -1
					# colisao por baixo
					if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
						self.speed_y *= -1
					# colisao pela esquerda
					if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
						self.speed_x *= -1
					# colisao pela direita
					if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
						self.speed_x *= -1
					# reduz a vida dos blocos (causa dano)
					if wall.blocks[row_count][item_count][1] > 1:
						wall.blocks[row_count][item_count][1] -= 1
					else:
						wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

				# verifica se o bloco ainda existe qdo a parede nao esta toda destruida
				if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
					wall_destroyed = 0

				item_count += 1

			row_count += 1
		# percorre todos os blocos e verifica se a parede foi destruída
		if wall_destroyed == 1:
			self.game_over = 1

		# verifica se ha colisao com paredes da tela
		if self.rect.left < 0 or self.rect.right > screen_width:
			self.speed_x *= -1

		# verifica se ha colisao com as partes de cima e baixo da tela
		if self.rect.top < 0:
			self.speed_y *= -1
		if self.rect.bottom > screen_height:
			self.game_over = -1

		# colisao com a barra
		if self.rect.colliderect(player_paddle):
			# verifica colisa por cima (unica possivel)
			if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
				self.speed_y *= -1
				self.speed_x += player_paddle.direction
				if self.speed_x > self.speed_max:
					self.speed_x = self.speed_max
				elif self.speed_x < 0 and self.speed_x < -self.speed_max:
					self.speed_x = -self.speed_max
			else:
				self.speed_x *= -1

		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		return self.game_over

	# funcao de desenho da bolinha
	def draw(self):
		pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
		pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)

	# funcao de reset da bolinha
	def reset(self, x, y):
		self.ball_rad = 10
		self.x = x - self.ball_rad
		self.y = y
		self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
		self.speed_x = 4
		self.speed_y = -4
		self.speed_max = 5
		self.game_over = 0

# comando para criar o muro
wall = wall()
wall.create_wall()

# comando para criar a barra do jogador
player_paddle = paddle()

# comando para criar a bolinha
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

# roda o jogo
run = True
while run:
	clock.tick(fps)
	screen.fill(bg)

	wall.draw_wall()
	player_paddle.draw()
	ball.draw()

	if live_ball:
		player_paddle.move()
		game_over = ball.move()
		if game_over != 0:
			live_ball = False

	# define as mensagens exibidas na tela ao jogador
	if not live_ball:
		if game_over == 0:
			draw_text('Clique com mouse na tela para iniciar um novo jogo', font, text_col, 100, screen_height // 2 + 100)
		elif game_over == 1:
			draw_text('Parabéns, você venceu!', font, text_col, 240, screen_height // 2 + 50)
			draw_text('Clique novamente para iniciar novo jogo', font, text_col, 100, screen_height // 2 + 100)
		elif game_over == -1:
			draw_text('Se deu mal eim pai!', font, text_col, 240, screen_height // 2 + 50)
			draw_text('Clique novamente para iniciar novo jogo', font, text_col, 100, screen_height // 2 + 100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
			live_ball = True
			ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
			player_paddle.reset()
			wall.create_wall()

	# atualiza display durante o jogo
	pygame.display.update()

# fecha o jogo
pygame.quit()
