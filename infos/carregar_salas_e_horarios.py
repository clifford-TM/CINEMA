# Metodo para carregar salas e horarios
def carregar_salas_e_horarios():
    caminho_arquivo = "infos/Filmes/salas_e_horarios.txt"
    
    # Salas e horarios começam como listas vazias
    salas = []
    horarios = []

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if linha.startswith("salas:"):
                # Salas recebe os valores de "salas" de salas_e_horarios.txt
                salas = [int(sala) for sala in linha.split(":")[1].strip().split(",") if sala.strip().isdigit()]
            if linha.startswith("horarios:"):
                # Horarios recebe os valores de "horarios" de salas_e_horarios.txt
                horarios = [horario.strip() for horario in linha.split(": ")[1].strip().split(",")]

    return salas, horarios

carregar_salas_e_horarios()