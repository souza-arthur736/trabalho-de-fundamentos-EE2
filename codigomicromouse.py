###Trabalho de Fundamentos da Programação EE2
###Arthur de Souza, Arthur Filipe, Eduardo Emanuel, Fábio Henrique e Gabriel de Oliveira
#Importação de bibliotecas
import API
import sys
import numpy as np
from collections import deque

def log(msg):
    sys.stderr.write(str(msg) + "\n")
    sys.stderr.flush()

# Direções
CIMA = 0
DIREITA = 1
BAIXO = 2
ESQUERDA = 3

DX = [0, 1, 0, -1]
DY = [1, 0, -1, 0]

# Criação da matriz
N = 16

maze = [[[False]*4 for _ in range(N)] for _ in range(N)] #False = sem parede
visited = [[False]*N for _ in range(N)] 
dist = np.zeros((N,N)) #distancia ao objetivo no FF

#vê se a posição x,y está dentro do labirinto para evitar bugs
def dentro(x,y): 
    return 0 <= x < N and 0 <= y < N

def marcar_paredes(x, y, d):
    #Atualiza a matriz marcando as paredes
    front = API.wallFront()
    left  = API.wallLeft()
    right = API.wallRight()

    # Frente
    if front:
        df = d
        maze[x][y][df] = True
        nx, ny = x + DX[df], y + DY[df]
        if dentro(nx,ny):
            maze[nx][ny][(df+2)%4] = True

    #Aqui o % 4 mantém os valores entre 0,1,2 e 3 (as direções possíveis do labirinto)
    # Esquerda
    dl = (d - 1) % 4
    if left:
        maze[x][y][dl] = True
        nx, ny = x + DX[dl], y + DY[dl]
        if dentro(nx,ny):
            maze[nx][ny][(dl+2)%4] = True

    # Direita
    dr = (d + 1) % 4
    if right:
        maze[x][y][dr] = True
        nx, ny = x + DX[dr], y + DY[dr]
        if dentro(nx,ny):
            maze[nx][ny][(dr+2)%4] = True

#implementação do FF
def floodfill_dist(objetivos):
    global dist
    dist = np.full((N,N), 9999, dtype=int)  # Coloca todos os valores da matriz como 9999. Escolhemos um valor grande para evitar bugs
    fila = deque()

    for (ax,ay) in objetivos:
        dist[ax][ay] = 0
        fila.append((ax,ay))

    while fila:
        x,y = fila.popleft()
        for d in range(4):
            if maze[x][y][d]:
                continue
            nx = x + DX[d]
            ny = y + DY[d]
            if dentro(nx,ny) and dist[nx][ny] > dist[x][y] + 1:
                dist[nx][ny] = dist[x][y] + 1
                fila.append((nx,ny))

#d = direção, nd = nova direção
def girar_para(d, nd):
    diff = (nd - d) % 4
    if diff == 1:
        API.turnRight()
    elif diff == 2:
        API.turnRight()
        API.turnRight()
    elif diff == 3:
        API.turnLeft()
    return nd


def passo_seguro_frente(x, y, d):
    if API.wallFront():
        # marca no mapa parede detectada
        maze[x][y][d] = True
        nx,ny = x + DX[d], y + DY[d]
        if dentro(nx,ny):
            maze[nx][ny][(d+2)%4] = True
        return x,y,d,False

    API.moveForward()
    return x + DX[d], y + DY[d], d, True

#escolhe vizinho de menor distância para o FF
def escolher_movimento_flood(x, y, d):
    melhor = None
    melhor_dist = 10**9

    for nd in range(4):
        if maze[x][y][nd]:
            continue
        nx = x + DX[nd]
        ny = y + DY[nd]
        if dentro(nx,ny) and dist[nx][ny] < melhor_dist:
            melhor_dist = dist[nx][ny]
            melhor = nd

    if melhor is None:
        return (d+2)%4 #direção 0 1 2 ou 3
    return melhor


def existe_celula_nao_visitada():
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                return True
    return False

#Finalmente, a primeira rodada de exploração
def executar_run1():
    log("RUN 1 – Explorando o labirinto...")

    x,y = 0,0
    d = CIMA
    visited[x][y] = True

    modo = "WF"  #WF:wall follower. 
    antigos_v = 0
    passos_sem_novidade = 0

    total_passos = 0
    limite_recalculo = 10
    tentativas_recalculo = 0

    while True:
        #Checa paredes e verifica se os passos são novos ou não, marcando todo o labirinto
        marcar_paredes(x,y,d)
        novos = sum(sum(1 for v in row if v) for row in visited)
        if novos == antigos_v:
            passos_sem_novidade += 1
        else:
            passos_sem_novidade = 0
        antigos_v = novos

        if passos_sem_novidade > 20:
            modo = "FF" #escolhe FF quando não consegue achar novas posições com o WF

        if modo == "FF" and existe_celula_nao_visitada():
            alvo = [(i,j) for i in range(N) for j in range(N) if not visited[i][j]]
            floodfill_dist(alvo)
            nd = escolher_movimento_flood(x,y,d)
        else:
            left  = (d - 1) % 4
            right = (d + 1) % 4
            if not API.wallLeft():
                nd = left
            elif not API.wallFront():
                nd = d
            elif not API.wallRight():
                nd = right
            else:
                nd = (d + 2) % 4

        d = girar_para(d, nd)
        marcar_paredes(x,y,d)
        x2,y2,d2,ok = passo_seguro_frente(x,y,d)

        if not ok:
            tentativas_recalculo += 1
            if tentativas_recalculo > limite_recalculo:
                log("Múltiplas divergências – parando RUN 1.")
                break
            floodfill_dist([(7,7),(7,8),(8,7),(8,8)])
            continue

        tentativas_recalculo = 0
        x,y,d = x2,y2,d2
        total_passos += 1

        visited[x][y] = True
        API.setColor(x,y,"G")

        if (x,y) in [(7,7),(7,8),(8,7),(8,8)]:
            log("RUN 1 completa")
            break

        if total_passos > N*N*30:
            log("Timeout na RUN 1 – provavelmente mapeamento completo.")
            break

    return x,y,d


def retornar_ao_inicio(x,y,d):
    log("Voltando ao início")

    floodfill_dist([(0,0)])

    passos = 0
    while (x,y) != (0,0):

        nd = escolher_movimento_flood(x,y,d)
        d = girar_para(d, nd)
        marcar_paredes(x,y,d)

        x2,y2,d2,ok = passo_seguro_frente(x,y,d)
        if not ok:
            floodfill_dist([(0,0)])
            continue

        x,y,d = x2,y2,d2
        passos += 1
        API.setColor(x,y,"B")

        if passos > N*N*6:
            log("Timeout no retorno!")
            break

    log("Retorno concluído.")
    return x,y,d


def executar_run2(start_dir):
    log("RUN 2 – Executando melhor caminho")

    x,y = 0,0
    d = start_dir
    floodfill_dist([(7,7),(7,8),(8,7),(8,8)])

    passos = 0
    limite_recalculo = 10
    tentativas_recalculo = 0

    while True:
        nd = escolher_movimento_flood(x,y,d)
        d = girar_para(d, nd)
        marcar_paredes(x,y,d)

        x2,y2,d2,ok = passo_seguro_frente(x,y,d)
        if not ok: #corrige a rota do robô
            tentativas_recalculo += 1
            if tentativas_recalculo > limite_recalculo:
                log("Múltiplas divergências – parando RUN 2.")
                break
            floodfill_dist([(7,7),(7,8),(8,7),(8,8)])
            continue
        tentativas_recalculo = 0

        x,y,d = x2,y2,d2
        passos += 1
        API.setColor(x,y,"R")

        if (x,y) in [(7,7),(7,8),(8,7),(8,8)]:
            log(f"RUN 2 completa em {passos} passos")
            break

        if passos > N*N*5:
            log("Timeout na RUN 2")
            break


def main():
    cx,cy,cd = executar_run1()
    sx,sy,sd = retornar_ao_inicio(cx,cy,cd)
    executar_run2(sd)
#executa o código
if __name__ == "__main__":
    main()
