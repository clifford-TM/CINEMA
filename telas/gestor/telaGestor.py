import sys
import os

"""Essas linhas são necessárias no código para dar um append do diretório de venda.py
ao nosso arquivo, já que a importação from convencional não consegue localizar pastas em
níveis superiores."""


# Obtendo o diretório do arquivo atual e adicionando ao caminho de pesquisa do python
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(diretorio_atual)

# Importações
from tkinter import *
from telaGerenciamentoFilmes import telaGerenciamentoFilmes
from telaGerenciamentoFuncionarios import telaGerenciamentoFuncionarios

# Tela do modulo
class telaGestor(Toplevel):
    def __init__(self, original):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("720x512")
        self.title("Gerenciamento do Cinema")

        Label(self, text = "Gerenciamento do Cinema", font = ("Georgia", 35)).pack(pady = 30)
        
        # Botão para acessar a tela de filmes
        self.btnFilmes = Button(self, text = 'Cadastrar Filmes', font = ("Georgia", 10), width = 30, command = self.abrirCadastroFilmes)
        self.btnFilmes.pack(pady = 10)

         # Botão para acessar a tela de filmes
        self.btnFilmes = Button(self, text = 'Excluir Filmes', font = ("Georgia", 10), width = 30, command = self.abrirExcluirFilmes)
        self.btnFilmes.pack(pady = 10)
        
        # Botão para cadastrar funcionários
        self.btnFuncionarios = Button(self, text = 'Cadastrar Funcionários',  font = ("Georgia", 10), width = 30, command = self.abrirCadastroFuncionarios)
        self.btnFuncionarios.pack(pady = 10)

        # Botão para excluir funcionários
        self.btnFuncionarios = Button(self, text = 'Excluir Funcionários',  font = ("Georgia", 10), width = 30, command = self.abrirExcluirFuncionarios)
        self.btnFuncionarios.pack(pady = 10)
        
        # Botão para sair
        self.btnSair = Button(self, text = 'Sair', font = ("Georgia", 10), width = 25, command = self.deslogar)
        self.btnSair.pack(pady = 50)

    # Cada botão chama uma das funções com o parametro "command"
    def abrirCadastroFilmes(self):
        # Fechar a tela atual
        self.destroy()
        # Ir para a tela de gerenciamento de filmes
        telaGerenciamentoFilmes(self.original_frame, "cadastrar")

    def abrirExcluirFilmes(self):
        # Fechar a tela atual
        self.destroy()
        # Ir para a tela de gerenciamento de filmes
        telaGerenciamentoFilmes(self.original_frame, "excluir")

    def abrirCadastroFuncionarios(self):
        # Fechar a tela atual
        self.destroy()
        # Ir para a tela de gerenciamento de filmes
        telaGerenciamentoFuncionarios(self.original_frame, "cadastrar")

    def abrirExcluirFuncionarios(self):
        # Fechar a tela atual
        self.destroy()
        # Ir para a tela de gerenciamento de filmes
        telaGerenciamentoFuncionarios(self.original_frame, "excluir")

    def deslogar(self):
        # Fechar a tela atual
        self.destroy()
        self.original_frame.mostrar()  


