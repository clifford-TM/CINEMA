# Importacoes
from tkinter import *
from tkinter import Scrollbar, Text

# Tela do modulo
class TelaTicketsVendidos(Toplevel):
    def __init__(self, original, filme, sala, horario):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("600x400")
        self.title("Relatório de Vendas")
        self.filme = filme
        self.sala = sala
        self.horario =  horario

        # Barra de rolagem
        scrollbar = Scrollbar(self)
        scrollbar.pack(side= RIGHT, fill=Y)

        # Widget Text para exibir os tickets vendidos
        # Diferente das Labels eles não serão exibidos como parte do Frame
        self.text_tickets = Text(self, wrap=WORD, yscrollcommand=scrollbar.set)
        self.text_tickets.pack(expand=True, fill='both')

        # Configuração para a barra de rolagem rolar junto com o widget Text
        scrollbar.config(command=self.text_tickets.yview)

        # Carregando os tickets vendidos
        self.carregar_tickets_vendidos()

    # Metodo para carregar os tickets vendidos para cada sessão de filme
    def carregar_tickets_vendidos(self):
        # Limpe o widget Text antes de carregar os novos tickets
        self.text_tickets.delete(1.0, END)

        # Leia as informações do arquivo de relatório e adicione ao widget Text
        with open("infos/relatorio_vendas.txt", "r") as relatorio:
            linhas = relatorio.readlines()
            informacoes_sessao = f"Filme: {self.filme} - {self.horario.strip()}, Sala: {self.sala},"
            for linha in linhas:
                # Verifique se as informações da sessão estão contidas na linha
                if informacoes_sessao in linha:
                    self.text_tickets.insert(END, linha)

