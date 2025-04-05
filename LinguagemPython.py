import pygame
import sys
import math
import time
import random

# Inicialização
pygame.init()
pygame.mixer.init()

# Carregar música
arquivo_musica = r"C:\Users\sadra\Downloads\porco-aranha-simpsons.mp3"
pygame.mixer.music.load(arquivo_musica)
pygame.mixer.music.play(-1)

# Configuração da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Aranha vs Insetos")

# Carregar imagem de fundo
imagem_fundo = pygame.image.load(r"C:\Users\sadra\Downloads\85f34ba2b8c8bf5f7ba1103b23bb6578.jpg")
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))

# Variáveis do jogo
def resetar_jogo():
    global x, y, angulo_atual, velocidade, tempo_animacao, vida, tempo_teia
    global baratas, formigas, inicio, pontos, executando, game_over
    
    x, y = largura // 2, altura // 2
    angulo_atual = 0
    velocidade = 5
    tempo_animacao = 0
    vida = 3
    tempo_teia = 0
    pontos = 0
    executando = True
    game_over = False
    inicio = time.time()
    
    # Resetar inimigos
    baratas = []
    for _ in range(5):
        baratas.append({
            'x': random.randint(0, largura),
            'y': random.randint(0, altura),
            'vel': random.uniform(0.5, 1.5),
            'teia': False
        })
    
    formigas = []
    for _ in range(10):
        formigas.append({
            'x': random.randint(0, largura),
            'y': random.randint(0, altura),
            'vel': random.uniform(1.5, 2.5),
            'teia': False
        })

# Resetar o jogo inicialmente
resetar_jogo()

# Fonte
fonte = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 72)

# Loop principal
clock = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and tempo_teia <= 0 and not game_over:
                tempo_teia = 5  # 5 segundos de teia ativa
            if evento.key == pygame.K_r and game_over:
                resetar_jogo()
    
    if not game_over:
        # Movimentação
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and x > 40:
            x -= velocidade
            angulo_atual = 90
        if teclas[pygame.K_RIGHT] and x < largura - 40:
            x += velocidade
            angulo_atual = -90
        if teclas[pygame.K_UP] and y > 40:
            y -= velocidade
            angulo_atual = 0
        if teclas[pygame.K_DOWN] and y < altura - 40:
            y += velocidade
            angulo_atual = 180
        
        # Atualizar animação
        tempo_animacao += 0.05

        # Atualizar teia
        if tempo_teia > 0:
            tempo_teia -= 1/60

        # Movimento dos inimigos
        for barata in baratas[:]:
            vel = barata['vel'] * (0.3 if barata['teia'] else 1.0)
            if barata['x'] < x:
                barata['x'] += vel
            else:
                barata['x'] -= vel
            if barata['y'] < y:
                barata['y'] += vel
            else:
                barata['y'] -= vel
            
            barata['teia'] = tempo_teia > 0 and math.sqrt((x - barata['x'])**2 + (y - barata['y'])**2) < 200

            if math.sqrt((x - barata['x'])**2 + (y - barata['y'])**2) < 30:
                if barata['teia']:
                    baratas.remove(barata)
                    pontos += 10
                    if random.random() > 0.7:
                        baratas.append({
                            'x': random.randint(0, largura),
                            'y': random.randint(0, altura),
                            'vel': random.uniform(0.5, 1.5),
                            'teia': False
                        })
                else:
                    vida -= 1
                    barata['x'] = random.randint(0, largura)
                    barata['y'] = random.randint(0, altura)
                    if vida <= 0:
                        game_over = True

        for formiga in formigas[:]:
            vel = formiga['vel'] * (0.3 if formiga['teia'] else 1.0)
            if formiga['x'] < x:
                formiga['x'] += vel
            else:
                formiga['x'] -= vel
            if formiga['y'] < y:
                formiga['y'] += vel
            else:
                formiga['y'] -= vel
            
            formiga['teia'] = tempo_teia > 0 and math.sqrt((x - formiga['x'])**2 + (y - formiga['y'])**2) < 200

            if math.sqrt((x - formiga['x'])**2 + (y - formiga['y'])**2) < 20:
                if formiga['teia']:
                    formigas.remove(formiga)
                    pontos += 5
                    if random.random() > 0.5:
                        formigas.append({
                            'x': random.randint(0, largura),
                            'y': random.randint(0, altura),
                            'vel': random.uniform(1.5, 2.5),
                            'teia': False
                        })
                else:
                    vida -= 0.5
                    formiga['x'] = random.randint(0, largura)
                    formiga['y'] = random.randint(0, altura)
                    if vida <= 0:
                        game_over = True

    # Desenhar
    tela.blit(imagem_fundo, (0, 0))
    
    if not game_over:
        # Desenhar teia se ativa
        if tempo_teia > 0:
            pygame.draw.circle(tela, (200, 200, 200, 100), (x, y), 200, 1)
        
        # Desenhar baratas
        for barata in baratas:
            cor = (150, 50, 50) if barata['teia'] else (100, 70, 50)
            pygame.draw.circle(tela, cor, (int(barata['x']), int(barata['y'])), 15)
            pygame.draw.line(tela, cor, (int(barata['x']), int(barata['y'])), 
                             (int(barata['x']-10), int(barata['y']-10)), 2)
            pygame.draw.line(tela, cor, (int(barata['x']), int(barata['y'])), 
                             (int(barata['x']+10), int(barata['y']-10)), 2)
        
        # Desenhar formigas
        for formiga in formigas:
            cor = (100, 0, 0) if formiga['teia'] else (70, 30, 30)
            pygame.draw.ellipse(tela, cor, (int(formiga['x']-8), int(formiga['y']-4), 16, 8))
            pygame.draw.circle(tela, cor, (int(formiga['x']-10), int(formiga['y'])), 5)
            pygame.draw.line(tela, cor, (int(formiga['x']-10), int(formiga['y'])), 
                             (int(formiga['x']-15), int(formiga['y']-5)), 1)
            pygame.draw.line(tela, cor, (int(formiga['x']-10), int(formiga['y'])), 
                             (int(formiga['x']-15), int(formiga['y']+5)), 1)
        
        # Desenhar aranha
        tamanho = 40
        ciclo = math.sin(tempo_animacao * 3) * 20
        
        pygame.draw.ellipse(tela, (30, 30, 30), (x-tamanho//2, y-tamanho//3, tamanho, tamanho//1.5))
        pygame.draw.circle(tela, (50, 50, 50), (x, y), tamanho//3)
        
        for i in range(8):
            olho_ang = angulo_atual - 45 + i*15
            olho_x = x + int(math.cos(math.radians(olho_ang)) * tamanho//3)
            olho_y = y + int(math.sin(math.radians(olho_ang)) * tamanho//3)
            pygame.draw.circle(tela, (200, 0, 0), (olho_x, olho_y), 3)
        
        for lado in [-1, 1]:
            for i in range(4):
                animacao = ciclo if (i % 2 == 0) else -ciclo
                ang_base = angulo_atual + lado*(20 + i*15) + animacao
                
                x1 = x + math.cos(math.radians(ang_base)) * tamanho//2
                y1 = y + math.sin(math.radians(ang_base)) * tamanho//2
                x2 = x1 + math.cos(math.radians(ang_base + lado*15)) * tamanho
                y2 = y1 + math.sin(math.radians(ang_base + lado*15)) * tamanho
                
                pygame.draw.line(tela, (40, 40, 40), (x, y), (x1, y1), 4)
                pygame.draw.line(tela, (30, 30, 30), (x1, y1), (x2, y2), 3)
    else:
        # Tela de Game Over
        texto_game_over = fonte_grande.render("GAME OVER", True, (255, 0, 0))
        texto_pontos_final = fonte.render(f"Pontuação Final: {pontos}", True, (255, 255, 255))
        texto_reiniciar = fonte.render("Pressione R para reiniciar", True, (255, 255, 255))
        
        tela.blit(texto_game_over, (largura//2 - texto_game_over.get_width()//2, altura//2 - 100))
        tela.blit(texto_pontos_final, (largura//2 - texto_pontos_final.get_width()//2, altura//2))
        tela.blit(texto_reiniciar, (largura//2 - texto_reiniciar.get_width()//2, altura//2 + 50))

    # Mostrar informações do jogo
    tempo_decorrido = int(time.time() - inicio) if not game_over else 0
    texto_tempo = fonte.render(f"Tempo: {tempo_decorrido}s", True, (255, 255, 255))
    texto_vida = fonte.render(f"Vida: {int(vida)}", True, (255, 50, 50))
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    
    tela.blit(texto_tempo, (10, 10))
    tela.blit(texto_vida, (10, 50))
    tela.blit(texto_pontos, (10, 90))
    
    pygame.display.flip()
    clock.tick(60)