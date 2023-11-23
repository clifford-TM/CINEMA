# Importacoes
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from infos import venda
from telaTicket import TelaTicketsVendidos

# Tela do modulo
class escolha_cadeira(Toplevel):
    def __init__(self, original, token, filme, sala, horario):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("720x512")
        self.title("Escolha as cadeiras")
        self.token = token
        self.filme = filme
        self.sala = sala
        self.horario = horario 

        # Titulo
        Label(self, text="Escolha as cadeiras", font=("Arial", 35)).pack(pady=20)

        # Carregando a matriz do filme escolhido a partir do token
        caminho_arquivo = f"infos/Filmes/Poltronas/{self.token}"
        self.poltronas = venda.carregar_matriz(caminho_arquivo)

        # Lista para armazenar as cadeiras selecionadas e os tipos de ingresso
        self.poltronas_selecionadas = {}

        # Frame para conter os botões e ComboBox
        frame_cadeiras = Frame(self)
        frame_cadeiras.pack()

        # Defina os textos dos botões para as poltronas disponíveis (0) e ocupadas (1)
        texto_disponivel = "Verde"
        texto_ocupado = "Vermelho"
        self.letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

        for i in range(len(self.poltronas)):
            for j in range(len(self.poltronas[i])):
                # Determine o texto do botão com base no valor na matriz
                if self.poltronas[i][j] == 0:
                    texto = texto_disponivel
                else:
                    texto = texto_ocupado

                # Crie um botão para cada poltrona
                self.botao = Button(frame_cadeiras, text=f"{self.letras[j]}{i+1}", width=4)
                if texto == texto_disponivel:
                    # Lambda chamará anonimamente a função de selecionar com os parametros corretos
                    # texto_cadeira está na função lambda para estanciar self
                    self.botao.config(command=lambda linha=(i+1), coluna=(j+1), texto_cadeira=self.botao["text"]: self.selecionar_cadeira(linha, coluna))
                    self.botao.config(bg="green")
                else:
                    self.botao.config(bg="red")
                    self.botao.config(state="disabled")
                self.botao.grid(row=i, column=j, padx=8, pady=8)

        # Cor para indicar que a cadeira está na lista, mas não vendida
        self.cor_selecionada = "yellow"

         # ComboBox para escolher o tipo de ingresso
        Label(self, text="Tipo de Ingresso:").pack(pady=10)
        self.combobox_ingresso = Combobox(self, values=["Meia", "Inteira", "Não Pagante"])
        self.combobox_ingresso.pack(pady=5)

        # Botão para concluir a compra
        btn_concluir_compra = Button(self, text="Concluir Compra", command=self.concluir_venda)
        btn_concluir_compra.pack(pady=10)

        # Botao para exibir o relatorio de vendas
        btn_mostrar_relatorio = Button(self, text="Relatório de Vendas", command=self.relatorio_vendas)
        btn_mostrar_relatorio.pack(pady=10)

    # Metodo para selecionar uma cadeira
    def selecionar_cadeira(self, linha, coluna):
        # Verificando se a cadeira já está na lista
        if (linha, coluna) in self.poltronas_selecionadas:
            self.poltronas_selecionadas.pop((linha, coluna)) # Remover a cadeira da lista
            self.mudar_cor_botao(linha, coluna, "green") # Mudar a cor de volta para verde
        else:
            # Adicionar a cadeira à lista de cadeiras selecionadas com tipo de ingresso escolhido
            tipo_ingresso = self.combobox_ingresso.get()
            if tipo_ingresso:  # Verifica se o tipo de ingresso foi escolhido
                self.poltronas_selecionadas[(linha, coluna)] = tipo_ingresso
                self.mudar_cor_botao(linha, coluna, "yellow") # Mudar a cor para indicar que está na lista

    # Metodo para alterar a cor dos botões
    def mudar_cor_botao(self, linha, coluna, cor):
        # winfo_children verifica os widgets presentes na classe TopLevel(self)
        for widget in self.winfo_children():
            # isinstance vai procurar a presença do widget "Frame"
            if isinstance(widget, Frame):
                for botao in widget.winfo_children():
                    texto_botao = botao["text"]
                    if f"{self.letras[coluna-1]}{linha}" in texto_botao:
                        botao.config(bg=cor)

    # Metodo para desabilitar o botão caso a cadeira seja vendida
    def desabilitar_botao(self, linha, coluna):
        # winfo_children verifica os widgets presentes na classe TopLevel(self)
        for widget in self.winfo_children():
            # isinstance vai procurar a presença do widget "Frame"
            if isinstance(widget, Frame):
                for botao in widget.winfo_children():
                    texto_botao = botao["text"]
                    if f"{self.letras[coluna-1]}{linha}" in texto_botao:
                        botao.config(state = "disabled")

    # Metodo de conclusão da venda 
    def concluir_venda(self):
        self.compra = len(self.poltronas_selecionadas)
        # Realizar a venda para cada cadeira selecionada
        for cadeira, tipo_ingresso in self.poltronas_selecionadas.items():
            linha, coluna = cadeira
            sucesso = venda.simular_venda(self.poltronas, linha, coluna)
            if sucesso:
                # Salvando a nova matriz
                venda.salvar_matriz(f"Filmes/Poltronas/{self.token}", self.poltronas)
                # Adiciona a venda ao arquivo de relatório
                self.registrar_venda(self.filme, self.sala, self.horario, linha, coluna, tipo_ingresso)
                self.mudar_cor_botao(linha, coluna, "red") # Mudar a cor para vermelho após a venda
                self.desabilitar_botao(linha, coluna) # Desabilita o botão da poltrona após a venda
            else:
                # Boa sorte para descobrir como fazer ela aparecer
                messagebox.showerror("Erro", f"A Cadeira {self.letras[coluna-1]}{linha} já foi vendida")
            if self.compra == 0:
                # Caso a venda seja feita, o programa mostra uma mensagem
                messagebox.showinfo("Sucesso", "Venda realizada com Sucesso")
                # Mostrar o relatório de vendas
                TelaTicketsVendidos(self, self.filme, self.sala, self.horario)
                # Metodo para limpar o dicionário de poltronas selecionadas
                self.poltronas_selecionadas.clear()

    # Metodo para registrar as vendas no relatório
    def registrar_venda(self, filme, sala, horario, linha, coluna, tipo_ingresso):
        # Adiciona a venda ao arquivo de relatório
        with open("infos/relatorio_vendas.txt", "a") as relatorio:
            relatorio.write(f"Filme: {filme} - {horario.strip()}, Sala: {sala}, Cadeira: {self.letras[coluna-1]}{linha} | Tipo de Ingresso: {tipo_ingresso}\n")
            self.compra -= 1

    # Metodo para exibir o relatório de vendas     
    def relatorio_vendas(self):
        TelaTicketsVendidos(self, self.filme, self.sala, self.horario)