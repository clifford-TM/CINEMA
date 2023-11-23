import os
import numpy as np

# Carregar a matriz do arquivo
def carregar_matriz(nome_arquivo):
    try:
        matriz = np.loadtxt(nome_arquivo, dtype=int)
        return matriz
    except FileNotFoundError:
        return None

# Metodo para testar alteração do estado da matriz
def simular_venda(matriz, linha, coluna):
    if matriz[linha - 1, coluna - 1] == 0:
        matriz[linha - 1, coluna - 1] = 1
        return True  # A venda foi realizada com sucesso
    else:
        return False  # A cadeira já está vendida


# Salvar o arquivo como uma nova matriz
def salvar_matriz(nome_arquivo, matriz):
    # Obtém o caminho absoluto do diretório atual
    diretorio_atual = os.path.dirname(__file__)
    # Define o caminho completo para o arquivo "matriz.txt"
    caminho_matriz = os.path.join(diretorio_atual, nome_arquivo)
    np.savetxt(caminho_matriz, matriz, fmt="%d")


# Caso o gerente queira adicionar um novo filme, a matriz será criada dessa forma
def criar_matriz(nome_arquivo):  
    matriz = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    
    # Salve a matriz em um arquivo de texto
    np.savetxt(nome_arquivo, matriz, fmt="%d", delimiter=" ")


def teste():
    # Carregar a matriz do arquivo
    matriz = carregar_matriz("infos/matriz.txt")

    if matriz is not None:
        # Simular a venda da cadeira na linha 2, coluna 3 (por exemplo)
        linha_venda = int(input("Selecione a fileira da poltrona: "))
        coluna_venda = int(input("Selecione a coluna da poltrona: "))

        if simular_venda(matriz, linha_venda, coluna_venda):
            print(f"Cadeira ({linha_venda}, {coluna_venda}) vendida com sucesso.")
            salvar_matriz("matriz.txt", matriz)
        else:
            print(f"A cadeira ({linha_venda}, {coluna_venda}) já está vendida.")

    else:
        print("Erro ao carregar a matriz do arquivo.")

