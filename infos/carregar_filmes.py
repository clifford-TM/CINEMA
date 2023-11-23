import os

# Obtendo o diretório do módulo atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Caminho absoluto para o arquivo 'filmes.txt'
caminho_filmes = os.path.join(diretorio_atual, 'Filmes', 'filmes.txt')

# Inicialize a lista de filmes
filmes = []

# Método try deve tentar abrir o arquivo com a lista de filmes
try:
    # Uso do with garante o fechamento do arquivo após a leitura
    with open(caminho_filmes, 'r') as arquivo:
        for linha in arquivo:
            if linha.startswith("Filme:"):
                # Extrai o título do filme da linha
                titulo_filme = linha.split(';')[0].split(': ')[1]
                if titulo_filme not in filmes:
                    filmes.append(titulo_filme)
                else:
                    None
# Caso o programa não encontre o arquivo retorna um erro
except FileNotFoundError:
    print("Arquivo 'filmes.txt' não encontrado.")
