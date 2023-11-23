import sys
import os

"""Essas linhas são necessárias no código para dar um append do diretório de venda.py
ao nosso arquivo, já que a importação from convencional não consegue localizar pastas em
níveis superiores."""


# Obtendo o diretório atual e o adicionando ao caminho de pesquisa do python
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
sys.path.append(diretorio_atual)

# Importações
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from infos.carregar_filmes import filmes
from infos.carregar_salas_e_horarios import carregar_salas_e_horarios
from escolha_cadeira import escolha_cadeira


# Tela do modulo
class telaAtendente(Toplevel):
    def __init__(self, original):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("720x512")
        self.title("Venda de Ingressos")

        # Titulo
        Label(self, text = "Venda de Ingressos", font = ("Arial", 35)).pack(pady = 5)

        # Rotulo de seleção de filme
        Label(self, text = "Selecionar Filme", font = ("Arial", 10)).pack(pady = 5)
        self.comboFilmes = Combobox(self, width=60) # Combobox para filmes
        self.comboFilmes.pack(pady=5)

        # Rotulo de seleção de sala
        Label(self, text = "Selecionar Sala", font = ("Arial", 10)).pack(pady = 5)
        self.comboSalas = Combobox(self, width=30)  # ComboBox para salas
        self.comboSalas.pack(pady=5)

        # Rotulo de seleção de horario
        Label(self, text = "Selecionar Horário", font = ("Arial", 10)).pack(pady = 5)
        self.comboHorarios = Combobox(self, width=30)  # ComboBox para horários
        self.comboHorarios.pack(pady=5)
    

        # Botão para chamar a função selecionar_filme
        self.btnSelecionarFilme = Button(self, text='Selecionar Filme', width=35, command=self.selecionar_filme)
        self.btnSelecionarFilme.pack(pady=15)

        # Botão para Limpar
        self.btnLimpar = Button(self, text='Limpar', width=35, command=self.limpar)
        self.btnLimpar.pack(pady=10)

        # Botao de sair
        self.btnSair = Button(self, text = 'Sair', width = 25, command = self.deslogar)
        self.btnSair.pack(pady = 10)

        # Carregar salas e horarios
        salas, horarios = carregar_salas_e_horarios()

        # Atribuir cada lista aos values das comboboxes
        self.comboFilmes['values'] = filmes 
        self.comboSalas['values'] = salas
        self.comboHorarios['values'] = horarios

        
        """Utilizamos lambda para receber os argumentos event(da combobox) e combobox(variavel
        definida entre as 3 acima) para chamarmos o metodo on_combobox_select se em alguma das combobox
        ocorrer um evento, o dever dele é verificar qual combobox foi acionada e mandar o valor para a função
        combobox_select"""

        # O metodo bind é responsável por dizer o evento vinculado a lambda, no caso "ComboboxSelected"
        # Neste caso o evento vinculado a lambda foi "<<ComboboxSelected>>"
        # Lambda também diz qual foi a combobox selecionada antes de chamar on_combobox_selected
        self.comboFilmes.bind("<<ComboboxSelected>>", lambda event, combobox=self.comboFilmes: self.on_combobox_select(event, combobox))
        self.comboSalas.bind("<<ComboboxSelected>>", lambda event, combobox=self.comboSalas: self.on_combobox_select(event, combobox))
        self.comboHorarios.bind("<<ComboboxSelected>>", lambda event, combobox=self.comboHorarios: self.on_combobox_select(event, combobox))



    # Metodo para quando uma combobox for selecioanda
    def on_combobox_select(self, event, combobox):
        # Obtendo os valores selecionados nas Comboboxes
        filme_selecionado = self.comboFilmes.get()
        sala_selecionada = self.comboSalas.get()
        horario_selecionado = self.comboHorarios.get()

        caminho_arquivo = "infos/Filmes/filmes.txt"

         
        with open(caminho_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()

        # Inicialize listas para valores das outras Comboboxes
        filmes_disponiveis = []
        salas_disponiveis = []
        horarios_disponiveis = []

        # Analise as linhas do arquivo
        for linha in linhas:
            # Método split divide a linha por uma quebra usando ";" como referência
            partes = linha.split('; ')
            
            if len(partes) >= 3:
                # De acordo com o formato são geradas 3 partes
                nome_filme = partes[0].split(': ')[1]
                sala = partes[1].split(': ')[1]
                horario = partes[2].split(': ')[1]
            

            """O algoritimo de filtro fará com que caso não haja um valor selecionado em qualquer
            combobox, todos as linhas com valores serão considerados disponíveis, caso seja selecionado
            algum valor em uma combobox, só estarão disponiveis as linhas onde aqueles valores forem encontrados"""

            # Caso não haja um filme selecionado o meotodo dará append em todas as salas e horarios
            if combobox == self.comboFilmes:
                if (not filme_selecionado or filme_selecionado == nome_filme) and \
                (not sala_selecionada or sala_selecionada == sala) and \
                (not horario_selecionado or horario_selecionado == horario):
                    # Todas as salas e horarios disponiveis ou aquelas que contém o filme
                    salas_disponiveis.append(sala)
                    horarios_disponiveis.append(horario)

            # Caso não haja uma sala selecionada o meotodo dará append em todos os filmes e horarios
            if combobox == self.comboSalas:
                if (not filme_selecionado or filme_selecionado == nome_filme) and \
                (not sala_selecionada or sala_selecionada == sala) and \
                (not horario_selecionado or horario_selecionado == horario):
                    # Todos os filmes e horarios disponiveis ou aqueles estarão na sala
                    filmes_disponiveis.append(nome_filme)
                    horarios_disponiveis.append(horario)

            # Caso não haja um horario selecionado o meotodo dará append em todos os filmes e salas
            if combobox == self.comboHorarios:
                if (not filme_selecionado or filme_selecionado == nome_filme) and \
                (not sala_selecionada or sala_selecionada == sala) and \
                (not horario_selecionado or horario_selecionado == horario):
                    # Todos os filmes e salas disponiveis ou aqueles estarão no horário
                    filmes_disponiveis.append(nome_filme)
                    salas_disponiveis.append(sala)

        # Atualize os valores das outras Comboboxes com as listas criadas
        if combobox == self.comboFilmes:
            self.comboSalas['values'] = list(set(salas_disponiveis))
            self.comboHorarios['values'] = list(set(horarios_disponiveis))

        if combobox == self.comboSalas:
            self.comboFilmes['values'] = list(set(filmes_disponiveis))
            self.comboHorarios['values'] = list(set(horarios_disponiveis))

        if combobox == self.comboHorarios:
            self.comboFilmes['values'] = list(set(filmes_disponiveis))
            self.comboSalas['values'] = list(set(salas_disponiveis))

    # Para reverter os filtros utilize a função limpar
    def limpar(self):
        # Limpar as seleções das comboboxes
        self.comboFilmes.set("")
        self.comboSalas.set("")
        self.comboHorarios.set("")
        
        # Carregar salas e horarios novamente
        salas, horarios = carregar_salas_e_horarios()

        # Reatribuir os valores para as comboboxes
        self.comboFilmes['values'] = filmes
        self.comboSalas['values'] = salas
        self.comboHorarios['values'] = horarios


    # Esse metodo vai criar o token da sessão para carregar a matriz
    def selecionar_filme(self):
        filme_selecionado = self.comboFilmes.get()
        sala_selecionada = self.comboSalas.get()
        horario_selecionado = self.comboHorarios.get()

        if filme_selecionado and sala_selecionada and horario_selecionado:
            # Como o formato txt não aceita ":" fazemos o tratamento de dados
            horario_token = horario_selecionado.replace(":","-")
            token = f"Filme- {filme_selecionado}; Sala- {sala_selecionada}; Horario- {horario_token.strip()}.txt"
            escolha_cadeira(self, token, filme_selecionado, sala_selecionada, horario_selecionado)          
        else:
            messagebox.showinfo("Erro", "Preencha todos os campos")
      
    # Voltar para a tela de login
    def deslogar(self):
        self.destroy()
        self.original_frame.mostrar()










        