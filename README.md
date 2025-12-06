# Micromouse no MMS – Trabalho de Fundamentos da Programação EE2

### Autores
- Arthur de Souza  
- Arthur Filipe  
- Eduardo Emanuel  
- Fábio Henrique  
- Gabriel de Oliveira  

---

## Descrição do projeto
Este projeto implementa um **robô explorador de labirinto 16x16** utilizando Python. O objetivo é mapear o labirinto, detectar paredes com sensores, calcular caminhos usando **floodfill**, achar o melhor caminho até o centro e alcançá-lo no menor tempo.

O projeto foi desenvolvido por alunos da Escola Politécnica de Pernambuco como parte da disciplina **Fundamentos da Programação** e foi feito para rodar no Micromouse Simulator do Mackorone, disponível em: https://github.com/mackorone/mms

---

## Como funciona

O robô explora o labirinto utilizando três técnicas principais de navegação e decisão: **Wall Follower**, **BFS** e **Floodfill**. A seguir, descrevemos o funcionamento de cada etapa do fluxo:

---

### 1. Exploração do labirinto (RUN 1)  

- O robô inicia na posição `(0,0)` olhando para cima.  
- Inicialmente, explora o labirinto usando o algoritmo Wall Follower:
  - Mantém contato constante com a parede à esquerda.  
  - Anda sempre seguindo a parede e virando quando necessário.  
  - Fácil de implementar, mas não garante o caminho mais curto.  

- Caso o robô fique sem novidades por mais de 20 passos, muda para **Floodfill**:
  - Floodfill utiliza uma variação do BFS (Busca em largura) para calcular a menor distância de cada célula até as células não visitadas.  
  - Cada célula recebe um valor de distância e o robô escolhe sempre o vizinho com menor distância para continuar explorando.  
  - Garante que todas as células não visitadas sejam alcançadas de forma eficiente.

- Durante a exploração, o robô:
  - Detecta paredes com sensores e atualiza o mapa interno `maze`.  
  - Marca cada célula visitada visualmente com verde.

### 2. Retorno ao início  

- Após explorar todo o labirinto, o robô retorna à posição inicial `(0,0)` utilizando **Floodfill**:
  - Calcula o caminho mais curto de cada célula até o início.  
  - Sempre escolhe o vizinho com menor distância para avançar.  
  - O caminho percorrido é marcado com azul.  

---

### 3. Execução do caminho ótimo (RUN 2)  

- O robô calcula o caminho mais curto até o centro `(7,7),(7,8),(8,7),(8,8)` usando **Floodfill**:
  - Como cada célula tem o valor de distância até o centro, o robô escolhe o vizinho que aproxima mais do objetivo.  
  - Garante movimentos seguros, evitando paredes detectadas anteriormente.  
  - O caminho é marcado com vermelho.  

---

## Estrutura do código

### Bibliotecas importadas
- `API`: fornece funções do robô (movimento e sensores).  
- `sys`: usado para logging no terminal.  
- `numpy`: manipulação de matrizes e distâncias.  
- `deque`: fila dupla para BFS/floodfill.

### Principais variáveis
- `maze[x][y][d]`: mapa do labirinto, indicando presença de paredes (`True/False`).  
- `visited[x][y]`: marca células visitadas.  
- `dist[x][y]`: distância até os objetivos, usada no floodfill.  
- `DX` e `DY`: vetores de movimento para cada direção (cima, direita, baixo, esquerda).

### Funções principais

| Função | Descrição |
|--------|-----------|
| `marcar_paredes(x,y,d)` | Atualiza o mapa do labirinto com as paredes detectadas|
| `floodfill_dist(objetivos)` | Calcula a distância mínima de cada célula até os objetivos usando busca em largura.|
| `girar_para(d, nd)` | Gira o robô para a direção desejada usando o mínimo de giros. |
| `passo_seguro_frente(x,y,d)` | Move o robô para frente se não houver parede; atualiza o mapa em caso de parede. |
| `escolher_movimento_flood(x,y,d)` | Seleciona a próxima direção com menor distância ao objetivo. |
| `existe_celula_nao_visitada()` | Verifica se ainda existem células não exploradas. |
| `executar_run1()` | Explora o labirinto, alternando entre Wall Follower e Floodfill, quando o WF não é capaz de achar novas posições. |
| `retornar_ao_inicio(x,y,d)` | Retorna o robô à posição inicial `(0,0)` usando floodfill. |
| `executar_run2(start_dir)` | Executa a run 2, fazendo o melhor caminho até o centro. |
| `main()` | Roda o código completo: RUN1 → Retorno → RUN2. |

---

## Como executar

1. Baixe como .zip
2. Coloque no MMS o filepath do codigomicromouse.py
   Ex: "C:\Users\John-Doe\Downloads\trabalho-de-fundamentos\codigomicromouse.py
