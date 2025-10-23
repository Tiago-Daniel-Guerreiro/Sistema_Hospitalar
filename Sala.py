from enum import Enum
import os
from Pessoas import Funcionario, Paciente
from Cargos import Cargo

class StatusAtendimento(Enum):
    ESPERA = "Em Espera"
    ATENDIMENTO = "Em Atendimento"
    ATENDIDO = "Atendido"

class StatusSala(Enum):
    DISPONIVEL = "Disponível"
    OCUPADO = "Ocupado"

class Sala:
    def __init__(self, id_sala:int, nome:str):
        self.id_sala = id_sala
        self.nome = nome
"""
class Pessoa:
    def __init__(self, nome:str, id_pessoa:int):
        self.nome = nome
        self.id_pessoa = id_pessoa

class Paciente(Pessoa):
    def __init__(self, nome:str, id_pessoa:int):
        super().__init__(nome, id_pessoa)
        self.senha = None
        self.status = StatusAtendimento.ESPERA

    def atribuir_senha(self, senha):
        self.senha = senha
        print(f"Paciente {self.nome}, a sua senha é {self.senha}.")

class Funcionario(Pessoa):
    def __init__(self, nome:str, id_pessoa:int, especialidade):
        super().__init__(nome, id_pessoa)
        self.especialidade = especialidade
"""
class SalaAtendimento(Sala):
    def __init__(self, id_sala, nome):
        super().__init__(id_sala, nome)
        self.funcionarios = []
        self.paciente_atual = None
        self.status = StatusSala.DISPONIVEL

    def adicionar_funcionario(self, funcionario:Funcionario):
        self.funcionarios.append(funcionario)

    def chamar_paciente(self, paciente:Paciente):
        if self.status == StatusSala.DISPONIVEL:
            self.paciente_atual = paciente
            self.status = StatusSala.OCUPADO
            paciente.status = StatusAtendimento.ATENDIMENTO
            print(f"Senha {paciente.senha} chamada para a sala {self.nome}.")
            return True
        print(f"A sala {self.nome} está ocupada.")
        return False

    def finalizar_atendimento(self):
        if self.paciente_atual:
            self.paciente_atual.status = StatusAtendimento.ATENDIDO
            print(f"Atendimento do paciente {self.paciente_atual.nome} (senha {self.paciente_atual.senha}) finalizado na sala {self.nome}.")
            self.paciente_atual = None
            self.status = StatusSala.DISPONIVEL
        
class SalaEspera(Sala):
    def __init__(self, id_sala, nome, prefixo_senha="A"):
        super().__init__(id_sala, nome)
        self.salas_atendimento_associadas = []
        self.fila_espera = []
        self.contador_senhas = 0
        self.prefixo_senha = prefixo_senha

    def adicionar_sala_atendimento(self, sala_atendimento:SalaAtendimento):
        self.salas_atendimento_associadas.append(sala_atendimento)

    def pegar_senha(self, paciente:Paciente):
        self.contador_senhas += 1
        senha = f"{self.prefixo_senha}{self.contador_senhas:03d}"
        paciente.atribuir_senha(senha)
        self.fila_espera.append(paciente)

    def chamar_proximo(self):
        if not self.fila_espera:
            print(f"Não há pacientes na fila de espera de {self.nome}.")
            return

        for sala in self.salas_atendimento_associadas:
            if sala.status == StatusSala.DISPONIVEL:
                paciente_a_chamar = self.fila_espera.pop(0)
                sala.chamar_paciente(paciente_a_chamar)
                return
        
        print("Todas as salas de atendimento estão ocupadas. Por favor, aguarde.")

    def mostrar_painel(self):
        print(f"\nPainel da Sala de Espera: {self.nome}")
        for sala in self.salas_atendimento_associadas:
            if sala.paciente_atual:
                senha_atual = sala.paciente_atual.senha 

            print(f"Sala: {sala.nome}, Status: {sala.status.value}, Senha em Atendimento: {senha_atual}")

        for c in self.fila_espera[:3]:
            proximas_senhas = c.senha

        print(f",Próximos na fila: {proximas_senhas}")

    def mostrar_painel(self):
        print(f"\nPainel da Sala de Espera: {self.nome}")
        for sala in self.salas_atendimento_associadas:
            senha_atual = None
            if sala.paciente_atual:
                senha_atual = sala.paciente_atual.senha 
            texto = f"Sala: {sala.nome}, Status: {sala.status.value}"
            if(senha_atual):
                texto += f", Senha em Atendimento: {senha_atual}"
            print(texto)
        for c in self.fila_espera[:3]:
            print(f"Próximos na fila: {c.senha}")

class SalaEspecial(Sala):
    def __init__(self, id_sala, nome, especialidade:Cargo):
        super().__init__(id_sala, nome)
        self.funcionarios = []
        self.especialidade = especialidade

    def adicionar_funcionario(self, funcionario:Funcionario):
        if funcionario.especialidade == self.especialidade:
            self.funcionarios.append(funcionario) 
        else:
            print(f"Funcionário {funcionario.nome} não possui a especialidade necessária para esta sala.")
        

    def realizar_procedimento_especial(self, paciente:Paciente):
        print(f"{self.nome} - Codigo por colocar")

class Recepcao:
    def __init__(self):
        self.areas = {} # Ex: {"Cardiologia": SalaEspera(...)}

    def adicionar_area(self, nome_area, sala_espera):
        self.areas[nome_area] = sala_espera

    def menu_principal(self):
        paciente_id_counter = 1
        while True:
            print("Bem-vindo à Recepção!")
            print("Por favor, escolha a área para a qual deseja atendimento:")
            
            opcoes_areas = list(self.areas.keys())
            for i, area in enumerate(opcoes_areas):
                print(f"{i + 1}. {area}")
            print("0. Sair")

            try:
                escolha = int(input("Escolha uma opção: "))
                if escolha == 0:
                    print("Obrigado, volte sempre.")
                    break
                if 1 <= escolha <= len(opcoes_areas):
                    area_escolhida = opcoes_areas[escolha - 1]
                    sala_espera_selecionada = self.areas[area_escolhida]
                    
                    nome_paciente = input("Por favor, insira o seu nome: ")
                    #novo_paciente = Paciente(nome_paciente, f"C{paciente_id_counter}")
                    paciente_id_counter += 1

                    #self.menu_sala_espera(sala_espera_selecionada, novo_paciente)
                else:
                    input("Opção inválida. Pressione Enter para continuar...")
            except ValueError:
                input("Entrada inválida. Pressione Enter para continuar...")

    def menu_sala_espera(self, sala_espera, paciente):
        sala_espera.pegar_senha(paciente)
        while True:
            sala_espera.mostrar_painel()
            print("\nOpções:")
            print("1. Chamar próximo paciente (simulação do sistema)")
            print("2. Finalizar atendimento na sala (simulação do sistema)")
            print("3. Voltar para a recepção")
            
            escolha = input("Escolha uma opção: ")
            match escolha:
                case "1":
                    sala_espera.chamar_proximo()
                    input("Pressione Enter para continuar...")
                case "2":
                    # Simulação para finalizar atendimento em uma sala ocupada
                    for sala in sala_espera.salas_atendimento_associadas:
                        if sala.status == StatusSala.OCUPADO:
                            sala_para_finalizar = sala
                        else:
                            sala_para_finalizar = None

                    if sala_para_finalizar != None:
                        sala_para_finalizar.finalizar_atendimento()
                    else:
                        print("Nenhuma sala em atendimento para finalizar.")

                    input("Pressione Enter para continuar...")
                case "3":
                    break
                case _:
                    input("Opção inválida. Pressione Enter para continuar...")
def teste():
    atendimento_cardio1 = SalaAtendimento(101, "Cardio 1")
    atendimento_cardio2 = SalaAtendimento(102, "Cardio 2")
    atendimento_orto1 = SalaAtendimento(201, "Orto 1")

    espera_cardiologia = SalaEspera(10, "Espera Cardiologia", prefixo_senha="C")
    espera_cardiologia.adicionar_sala_atendimento(atendimento_cardio1)
    espera_cardiologia.adicionar_sala_atendimento(atendimento_cardio2)

    espera_ortopedia = SalaEspera(20, "Espera Ortopedia", prefixo_senha="O")
    espera_ortopedia.adicionar_sala_atendimento(atendimento_orto1)

    recepcao_principal = Recepcao()
    recepcao_principal.adicionar_area("Cardiologia", espera_cardiologia)
    recepcao_principal.adicionar_area("Ortopedia", espera_ortopedia)

    recepcao_principal.menu_principal()
    
if __name__ == "__main__":
    teste()
