from abc import ABC, abstractmethod
from Cargos import Cargo
from HorarioV2 import FuncionarioHorario
import Sala 

#Pacientes_Historico = {}
#numero funciorio: numero Pacientes
#[id_hisorico] = descricao
"""

class Paciente_historicos:
    Pacientes = {}
    Funcionarios = {}
    Historico_Medico = {}
    
    def Definir():
        Paciente_historicos.Pacientes = {"Ola": "Teste"}
        Paciente_historicos.Testes = "Ola"    
    def Teste():
        print(str(Paciente_historicos.Testes))
        
Paciente_historicos.Definir()
print (Paciente_historicos.Pacientes)
Paciente_historicos.Teste()
"""

class Pessoa(ABC):
    def __init__(self, nome:str, idade:int):
        self._nome = nome
        self._idade = idade

    @abstractmethod
    def mostrar_informacoes(self):
        pass

    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome:str):
        if self._nome != None or self._nome != "":
            self._nome = novo_nome
    
    @property
    def idade(self) -> int:
        return self._idade
    
    @idade.setter
    def idade(self,nova_idade:int):
        if nova_idade > 0 and nova_idade < 100:
            self._idade = nova_idade
    
class Paciente(Pessoa):
    def __init__(self,nome:str,idade:int,numero_utente:int):
        super().__init__(self,nome,idade)
        self._numero_utente = numero_utente
    
    def __str__(self):
        return f"O paciente {self.nome} de {self.idade} anos e tem {len(Paciente_historicos.Paciente_historicos())} consultas no historico."

    @property
    def numero_utente(self) -> str:
        return f"{self.numero_utente:09d}"
    
        # Versão antiga
        #while len(valor) < 9: # se o numero for 1332
        #    valor = "0" + valor # fica 000001332

    @numero_utente.setter
    def numero_utente(self, novo_valor:int):
        # O Numero deve estar entre 0 e 999999999, o limite vem do facto do numero de utente ter 9 caracteres
        if novo_valor >= 0 and novo_valor <= 999999999: 
            self._numero_utente = novo_valor 

    @property
    def __historico_medico_Ids(self) -> str:
        if len(self.__historico_medico_Ids) < 0:
            return ""
        
        resultado = []

        for id in self.__historico_medico_Ids:
            resultado.append("\t" + self.obter_historico_medico_id(id))

        return "\n".join(resultado)

    @__historico_medico_Ids.setter
    def historico_medico(self,novo_historico:dict):
        self.__historico_medico = novo_historico

    def obter_historico_medico_id(self,id:int) -> str:
        if(id in self.__historico_medico.key()):
            return id + " - " + self.__historico_medico(id)
        else:
            return "O id não corresponde a nenhum historico médico"
        
    def mostrar_historico_medico_id(self, id:int):
        print(self.obter_historico_medico_id(id))
    
    def adicionar_registro(self, id:int, descricao:str):
        self.historico_medico = id,descricao

    def mostrar_historico(self):
        print("Historico médico - ", self.nome)
        print(self.historico_medico())

    def mostrar_informacoes(self):
        print(str(self))

class Funcionario(Pessoa):
    def __init__(self, nome:str, idade:int, salario:float, numero_funcionario:int):
        super().__init__(nome, idade)
        self._cargo = Cargo.Geral
        self._numero_funcionario = numero_funcionario
        self.__salario = salario
        
    def __str__(self):
        return f"O funcionario {self.nome} de {self.idade} anos recebe {self.salario} e tem o cargo {self.cargo}."
    @property

    def numero_funcionario(self):
        return self._numero_funcionario
    
    @numero_funcionario.setter
    def numero_funcionario(self,novo_numero):
        self.numero_funcionario = novo_numero

    @property
    def salario(self):
        return str(self.__salario) + "$"
    
    @salario.setter
    def salario(self, novo_valor:int):
        if novo_valor > 0:
            self.salario = novo_valor

    @property
    def cargo(self):
        return self._cargo.name
    
    @cargo.setter
    def cargo(self, novo_cargo):
        if novo_cargo is Cargo:
            self._cargo = novo_cargo
    @property
    def numero_funcionario(self):
        return self._numero_funcionario
    
    @numero_funcionario.setter
    def numero_funcionario(self,novo_numero):
        self.numero_funcionario = novo_numero

    def aplicar_aumento_salarial(self,percentagem:int):
        if percentagem > 0:
            self.salario += self.salario * (percentagem/100)

    def mostrar_informacoes(self):
        print(str(self))

class Membro_Hospitalar(Funcionario):
    def __init__(self, nome:str, idade:int, salario_base:float, numero_funcionario:int, horario:FuncionarioHorario):
        super().__init__(nome, idade, salario_base, numero_funcionario)
        self.cargo = Cargo.Saude.Medico.Geral
        self._horario = horario

    @property
    def horario(self):
        return self._horario

    @horario.setter
    def horario(self, novo_horario:FuncionarioHorario):
        self._horario = novo_horario

    def Obter_Tempo_De_Trabalho(self):
        return "Tempo de trabalho: POR FAZER"
        #return self.horario.horario_mensal.obter_detalhes_Mensais()
    
    def mostrar_informacoes(self):
        return f"O {self.cargo} {self.nome}, tem {self.idade},"

class Medico(Membro_Hospitalar):
    def __init__(self, nome, idade, salario_base,horario):
        super().__init__(nome,idade,salario_base,horario)
        self.cargo = Cargo.Saude

class Paciente_historicos:
    def __init__(self):
        
        self.Pacientes = {}
        self.Funcionarios = {}
        self.Historico_Medico = {}

    def Adicionar_Medico(self,funcionario:Funcionario):
        self.Funcionarios.update({funcionario.numero_funcionario:funcionario})

    def Adicionar_Paciente(self,paciente:Paciente):
        self.Pacientes.update({paciente.numero_utente:paciente})

    def Adicionar_Pacientes_Historico(self,numero_paciente,numero_funcionario, id_historico, descricao):
        if not numero_paciente in self.Pacientes.keys():
            return
        if not numero_funcionario in self.Funcionarios.keys():
            return
        
        # {numF: {numP: {idH:disc}}}

        if id_historico in self.Historico_Medico[numero_funcionario][numero_paciente].keys():
            return
        
        self.Historico_Medico.update({numero_funcionario:{numero_paciente:{id_historico:descricao}}})
        
        #dictPaciente = Pacientes_Historico[numero_funcionario]
        #dictPaciente[numero_paciente].update({id_hisorico:descricao})
    
    def Obter_historico(self,id_historico):
        for num_funcionario in self.Funcionarios:
            for num_paciente in self.Obter_Num_Pacientes_Do_Funcionario():
                for id_historico_paciente_atual in self.Obter_Ids_Historico_Com_Num_Paciente_e_Funcionario(num_funcionario,num_paciente):
                    if id_historico == id_historico_paciente_atual:
                        return self.Historico_Medico[num_funcionario][num_paciente][id_historico]
                    
    def Obter_Ids_Historicos_Medicos_De_Paciente(self,numero_paciente):
        ids_historico_paciente = []

        for num_funcionario in self.Funcionarios:
            num_pacientes_do_funcionario = self.Obter_Num_Pacientes_Do_Funcionario()
            for num_Paciente_atual in num_pacientes_do_funcionario:
                if numero_paciente == num_Paciente_atual:
                    ids_historico_paciente.append(self.Obter_Ids_Historico_Com_Num_Paciente_e_Funcionario(num_funcionario,numero_paciente))
        return ids_historico_paciente

    def Obter_Num_Funcionario_atenderam_Paciente(self,numero_paciente):
        num_funcionarios = []
        pacientes_por_Funcionario = []
        
        for num_funcionario in self.Funcionarios:
            pacientes_por_Funcionario.append(self.Obter_Num_Pacientes_Do_Funcionario())

        for num_paciente in pacientes_por_Funcionario:
            if numero_paciente == num_paciente:
                num_funcionarios.append(num_funcionario)

        return num_funcionarios
    
    def Obter_Num_Pacientes_Do_Funcionario(self,numero_funcionario):
        return self.Historico_Medico[numero_funcionario].keys()
    
    def Obter_Ids_Historico_Com_Num_Paciente_e_Funcionario(self,num_funcionario,num_paciente):
        return self.Historico_Medico[num_funcionario:num_paciente].keys()
    
# Cada paciente que um medico atendeu
# Cada funcionario que atendeu um paciente especifico
# procurar pelo id_historico










"""

Classe Medico:
       • __init__(self, nome, idade, salario_base, especialidade): inicializa médico com especialidade e
       salário base.
       • @property especialidade: retorna a especialidade do médico.
       • @especialidade.setter: define a especialidade, desde que não seja vazia.
       • adicionar_paciente(self, paciente): adiciona paciente à lista de atendidos.
       • listar_pacientes(self): mostra todos os pacientes do médico.
       • calcular_pagamento(self): retorna salário base + valor fixo por paciente atendido.
       • exibir_informacoes(self): exibe nome, especialidade e número de pacientes.

Classe Enfermeiro:
       • __init__(self, nome, idade, salario_base, turno): inicializa enfermeiro com turno (dia/noite).
       • @property turno: retorna o turno atual.
       • @turno.setter: define o turno apenas se for "dia" ou "noite".
       • adicionar_paciente(self, paciente): adiciona paciente sob cuidado.
       • listar_pacientes(self): exibe pacientes sob responsabilidade.
       • calcular_pagamento(self): retorna salário base + adicional conforme o turno.
       • exibir_informacoes(self): exibe nome, turno e total de pacientes.

Classe Administrativo:
       • __init__(self, nome, idade, salario_base, setor): inicializa funcionário administrativo com setor e
       salário base.
       • @property setor: retorna o setor de atuação.
       • @setor.setter: define o setor apenas se for válido.
       • registrar_horas(self, horas): acumula horas trabalhadas.
       • calcular_pagamento(self): retorna salário base + valor por hora registrada.
       • exibir_informacoes(self): mostra nome, setor e total de horas trabalhadas.

Classe EnfermeiroChefe:
       • __init__(self, nome, idade, salario_base, turno, setor, bonus_chefia): inicializa o híbrido com
       dados de enfermeiro e administrativo.
       • @property bonus_chefia: retorna o bônus adicional.
       • @bonus_chefia.setter: define o bônus apenas se for positivo.
       • calcular_pagamento(self): combina o pagamento de enfermeiro e administrativo + bônus de
       chefia.
       • exibir_informacoes(self): mostra nome, turno, setor e pacientes sob cuidado.

       


Classe Medico:
       • __init__(self, nome, idade, salario_base, especialidade): inicializa médico com especialidade e
       salário base.
       • @property especialidade: retorna a especialidade do médico.
       • @especialidade.setter: define a especialidade, desde que não seja vazia.
       • adicionar_paciente(self, paciente): adiciona paciente à lista de atendidos.
       • listar_pacientes(self): mostra todos os pacientes do médico.
       • calcular_pagamento(self): retorna salário base + valor fixo por paciente atendido.
       • exibir_informacoes(self): exibe nome, especialidade e número de pacientes.

Classe Enfermeiro:
       • __init__(self, nome, idade, salario_base, turno): inicializa enfermeiro com turno (dia/noite).
       • @property turno: retorna o turno atual.
       • @turno.setter: define o turno apenas se for "dia" ou "noite".
       • adicionar_paciente(self, paciente): adiciona paciente sob cuidado.
       • listar_pacientes(self): exibe pacientes sob responsabilidade.
       • calcular_pagamento(self): retorna salário base + adicional conforme o turno.
       • exibir_informacoes(self): exibe nome, turno e total de pacientes.
"""