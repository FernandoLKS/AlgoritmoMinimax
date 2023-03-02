import numpy as np

class Estado:
    def __init__ (self, E, P, V):
        self.Est = E       #Estado que o Tabuleiro esta
        self.Player = P    #Player que esta na jogada
        self.minimax = 0   #Valor minimax
        self.Visitado = V  #Mostra se um determinado estado ja foi visitado
    
class Nodo:
    def __init__(self, E, P, V):
        self.EstTabuleiro = Estado(E, P, V)
        self.Filhos = []
    
def criaArvore():
    A = Nodo(np.zeros((3,3)), 1, 1)
    Arvore(A)
    return A
	
def Arvore(Raiz):
    Filhos = EstadosVazios(Raiz.EstTabuleiro.Est)
    j = 0
    Max = -1
    Min = 1
    for i in Filhos:
        if(Raiz.EstTabuleiro.Player == 1):
            Novo = Nodo(Raiz.EstTabuleiro.Est.copy(), 2, 0)
            Novo.EstTabuleiro.Est[i[0]][i[1]] = 1          							     
        elif(Raiz.EstTabuleiro.Player == 2):
            Novo = Nodo(Raiz.EstTabuleiro.Est.copy(), 1, 0)
            Novo.EstTabuleiro.Est[i[0]][i[1]] = 2
        MM = EstadoObjetivo(Novo.EstTabuleiro.Est)
        if(MM != 2):
            Novo.EstTabuleiro.minimax = MM            
        else:
            Arvore(Novo)							
        Raiz.Filhos.append(Novo)         
        if(Raiz.EstTabuleiro.Player == 1):            
            if(Raiz.Filhos[j].EstTabuleiro.minimax >= Max):
                Max = Raiz.Filhos[j].EstTabuleiro.minimax 
                Raiz.EstTabuleiro.minimax = Max           
        elif(Raiz.EstTabuleiro.Player == 2):            
            if(Raiz.Filhos[j].EstTabuleiro.minimax <= Min):
                Min = Raiz.Filhos[j].EstTabuleiro.minimax 
                Raiz.EstTabuleiro.minimax = Min  
        j += 1
    
def Minimax(Raiz, EstadoAtual):   
    j = 0
    EstObj = EstadoObjetivo(Raiz.EstTabuleiro.Est)
    if(EstObj == 2):		
        for i in EstadosVazios(Raiz.EstTabuleiro.Est):
            if(Raiz.Filhos[j].EstTabuleiro.Visitado == 1):            
                return Minimax(Raiz.Filhos[j], EstadoAtual)
            j += 1
        Max = -1
        Min = 1
        j = 0     
        for i in EstadosVazios(Raiz.EstTabuleiro.Est):
            if(Raiz.EstTabuleiro.Player == 1):            
                if(Raiz.Filhos[j].EstTabuleiro.minimax >= Max):
                    pos = j
                    Max = Raiz.Filhos[j].EstTabuleiro.minimax 
                    Raiz.EstTabuleiro.minimax = Max           
            elif(Raiz.EstTabuleiro.Player == 2):            
                if(Raiz.Filhos[j].EstTabuleiro.minimax <= Min):
                    pos = j
                    Min = Raiz.Filhos[j].EstTabuleiro.minimax 
                    Raiz.EstTabuleiro.minimax = Min 
            j += 1
	    
        Raiz.Filhos[pos].EstTabuleiro.Visitado = 1

        for x in range(3):
            for y in range(3):
                if(Raiz.Filhos[pos].EstTabuleiro.Est[x][y] != Raiz.EstTabuleiro.Est[x][y]):
                    return x, y
		
def JogHumano(Raiz, PosJogX, PosJogY):
    j=0
    for i in EstadosVazios(Raiz.EstTabuleiro.Est):
        if(Raiz.Filhos[j].EstTabuleiro.Visitado == 1): 
            return JogHumano(Raiz.Filhos[j], PosJogX, PosJogY)
        j += 1
    j = 0
    for i in EstadosVazios(Raiz.EstTabuleiro.Est):
        for x in range(3):
            for y in range(3):
                if(Raiz.Filhos[j].EstTabuleiro.Est[PosJogX][PosJogY] != 0):
                    Raiz.Filhos[j].EstTabuleiro.Visitado = 1
        j += 1            
            
#1 - Vitoria X; 0 - Empate; -1 - Vitoria O; 2 - Nao acabou o jogo 
def EstadoObjetivo(Estado):
    # diagonal principal
    if(Estado[0][0] == Estado[1][1] and Estado[1][1] == Estado[2][2] and Estado[0][0] != 0):
        if(Estado[0][0] == 1): return 1
        return -1
    # diagonal secundaria
    if(Estado[0][2] == Estado[1][1] and Estado[1][1] == Estado[2][0] and Estado[0][2] != 0):
        if(Estado[0][2] == 1): return 1
        return -1
    # linhas 
    for i in range(3):
        if(Estado[i][0] == Estado[i][1] and Estado[i][1] == Estado[i][2] and Estado[i][0] != 0):            
            if(Estado[i][0] == 1): return 1
            return -1  
    # coluna    
    for i in range(3):
        if(Estado[0][i] == Estado[1][i] and Estado[1][i] == Estado[2][i] and Estado[0][i] != 0):            
            if(Estado[0][i] == 1): return 1
            return -1
    # Nao acabou ainda
    for i in range(3):
        for j in range(3):
            if(Estado[i][j] == 0):
                return 2
    #empate
    return 0
       
def EstadosVazios(Estado):    
    Pos = []
    for i in range(3):
        for j in range(3):
            if(Estado[i][j] == 0):
                Pos.append([i,j])
    return Pos
