import calendar
from datetime import datetime, timedelta, date
from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, List
from Horario import (
    Horario_Semanal, Horario, IntervaloTempo, HoraMinuto, 
    Horario_Mensal, FuncionarioHorario, Dias_Semana,
    formatar_timedelta
)

Inicio_Turno_noturno = timedelta(hours=22)
Fim_Turno_noturno = timedelta(hours=7)
max_pausas = 24

class RegraDePagamento(ABC):
    @abstractmethod
    def calcular(self, funcionario, contexto: dict) -> float:
        pass

class RegraSalarioBase(RegraDePagamento):
    def calcular(self, funcionario, contexto: dict) -> float:
        return funcionario.salario_base

class RegraBonusFixo(RegraDePagamento):
    def __init__(self, valor_bonus: float):
        self._valor_bonus = valor_bonus
        
    def calcular(self, funcionario, contexto: dict) -> float:
        return self._valor_bonus

class RegraBonusPorAtendimento(RegraDePagamento):
    def __init__(self, valor_por_paciente: float):
        self._valor_por_paciente = valor_por_paciente
    
    def calcular(self, funcionario, contexto: dict) -> float:
        if not isinstance(funcionario, (Medico, EnfermeiroChefe)):
            return 0.0
        
        ano = None
        mes = None

        if 'mes' in contexto:
            mes = contexto['mes'] 

        if 'ano' in contexto:
            ano = contexto['ano']
        
        if mes is not None and ano is not None: # Filtra atendimentos do mês/ano específico
            atendimentos_filtrados = []
 
            for atendimento in funcionario.atendimentos_realizados:
                if atendimento['data'].month == mes and atendimento['data'].year == ano:
                    atendimentos_filtrados.append(atendimento)    

            return len(atendimentos_filtrados) * self._valor_por_paciente
        
        return len(funcionario.atendimentos_realizados) * self._valor_por_paciente

class RegraPagamentoPorHora(RegraDePagamento):
    def __init__(self, valor_por_hora: float):
        self._valor_por_hora = valor_por_hora
    
    def calcular(self, funcionario, contexto: dict) -> float:
        if isinstance(funcionario, (Administrativo, EnfermeiroChefe)): # Se o funcionario for das classes que têm horas_registradas
            return funcionario.horas_registradas * self._valor_por_hora
        return 0.0
    
class RegraBonusPercentual(RegraDePagamento):
    def __init__(self, percentual: float):
        self._percentual = percentual
    def calcular(self, funcionario, contexto: dict) -> float:
        return funcionario.salario_base * (self._percentual / 100)

class Cargo:
    class Administrativo(Enum):
        Coordenador = "Coordenador"
        Gestor = "Gestor"
        Diretor = "Diretor"

    class Apoio(Enum):
        Rececionista = "Rececionista"
        Auxiliar = "Auxiliar de Serviços Gerais"
        PessoalGeral = "Pessoal Geral"

    class Saude(Enum):
        Fisioterapeuta = "Fisioterapeuta"
        Nutricionista = "Nutricionista"
        Enfermeiro = "Enfermeiro"
        Farmaceutico = "Farmacêutico"

        class Medico(Enum):
            Geral = "Médico Geral"
            Cardiologia = "Cardiologista"
            CirurgiaGeral = "Cirurgião Geral"
            MedicinaInterna = "Médico de Medicina Interna"
            Psiquiatria = "Psiquiatra"

class StatusAtendimento(Enum):
    SEM_SALA = "Sem Sala Definida"
    ESPERA = "Em Espera"
    ATENDIMENTO = "Em Atendimento"
    ATENDIDO = "Atendido"

class StatusSala(Enum):
    DISPONIVEL = "Disponível"
    OCUPADO = "Ocupado"

class Pessoa(ABC):
    def __init__(self, nome:str, idade:int):
        self._nome = nome
        self._idade = idade

    @abstractmethod
    def __str__(self):
        pass

    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome:str):
        if self._nome == None or self._nome == "":
            return
        self._nome = novo_nome
    
    @property
    def idade(self) -> int:
        return self._idade
    
    @idade.setter
    def idade(self,nova_idade:int):
        if nova_idade > 0 and nova_idade < 100:
            self._idade = nova_idade
    
class Paciente(Pessoa):
    def __init__(self, nome: str, idade: int, numero_utente: int):
        Pessoa.__init__(self, nome, idade)
        self._numero_utente = numero_utente
        self.status = StatusAtendimento.SEM_SALA
        self.area_atendimento = None
        self.sala_atendimento = None
        self.senha = None

    def __str__(self):        
        relatorio = f"\nPaciente: {self.nome}"
        relatorio += f"\nNº Utente: {self.numero_utente}"
        relatorio += f"\nIdade: {self.idade} anos"
        relatorio += f"\nStatus: {self.status.value}\n"
        Paciente_historicos.Pacientes[self.numero_utente] = self

        atendimentos_paciente = Paciente_historicos.obter_historicos_paciente(self.numero_utente)

        relatorio += f"\nAtendimentos: {len(atendimentos_paciente)}"
        
        for atendimento in atendimentos_paciente:
            # Encontra qual funcionário fez o atendimento
            for id in atendimento.keys():
                relatorio += f"\n#{id} - {atendimento[id]}"
                relatorio += f"({atendimento['data']} às {atendimento['hora']})"
                break

        relatorio += "Funcionarios que atenderam o paciente:\n"

        for funcionario in Paciente_historicos.obter_funcionarios_paciente(self.numero_utente):
            relatorio += f"\n - {funcionario}"

        relatorio += "\n"
        return relatorio
    
    def atribuir_senha(self, senha: str, area_nome: str):
        self.senha = senha
        self.area_atendimento = area_nome

    @property
    def numero_utente(self) -> str:
        return f"{self._numero_utente:09d}"

        # Versão antiga
        #while len(valor) < 9: # se o numero for 1332
        #    valor = "0" + valor # fica 000001332

    @numero_utente.setter
    def numero_utente(self, novo_valor:int):
        # O Numero deve estar entre 0 e 999999999, o limite vem do facto do numero de utente ter 9 caracteres
        if novo_valor >= 0 and novo_valor <= 999999999: 
            self._numero_utente = novo_valor 

    @property
    def historico_medico_Ids(self) -> str:
        resultado = ""

        if len(self.__historico_medico_Ids) > 0:
            for id_historico in self.__historico_medico_Ids:
                resultado += "\t" + self.obter_historico_medico_id(id_historico) + "\n"

        return resultado

    def obter_historico_medico_id(self,id_historico:int) -> str:
        if id_historico in Paciente_historicos.obter_historicos_paciente(self.numero_utente):
            return str(id_historico) + " - " + self.__historico_medico(id_historico)
        
        return "O id não corresponde a nenhum historico médico"
    
class Funcionario(Pessoa):
    def __init__(self, nome: str, idade: int, salario: float, numero_funcionario: int, cargo: Cargo, horario_semanal: Horario_Semanal):
        Pessoa.__init__(self, nome, idade)
        self._numero_funcionario = numero_funcionario
        self._salario_base = max(0, salario) # O Salario não pode ser negativo
        self._cargo = cargo
        
        self.horario_semanal = horario_semanal
        self.horario_funcionario = FuncionarioHorario(self.horario_semanal)
        self.atendimentos_realizados = []
        self.regras_pagamento = [RegraSalarioBase()]

    def __str__(self):
        atendimentos = self.obter_atendimentos()
        pagamento = self.calcular_pagamento()
        
        relatorio = f"\nFuncionário: {self.nome}"
        relatorio += f"\nNº Funcionário: {self.numero_funcionario}"
        relatorio += f"\nIdade: {self.idade} anos"
        relatorio += f"\nCargo: {self._cargo.name if hasattr(self._cargo, 'name') else self._cargo.value}"
        relatorio += f"\nSalário Base: {self._salario_base:.2f}€"
        relatorio += f"\nSalário Total: {pagamento['total_a_pagar']:.2f}€"
        relatorio += f"\nAtendimentos Realizados: {len(atendimentos)}"
        
        if atendimentos:
            relatorio += "\nÚltimos atendimentos:"
            for atendimento in atendimentos[-3:]:
                relatorio += f"\n  - {atendimento['paciente'].nome}: {atendimento['descricao']} "
                relatorio += f"({atendimento['data']} às {atendimento['hora']})"
        
        return relatorio
    
    @property
    def numero_funcionario(self) -> int:
        return self._numero_funcionario

    @property
    def salario(self) -> float:
        return self._salario_base

    @property
    def cargo(self) -> Cargo:
        return self._cargo
    
    @property
    def salario_base(self) -> float:
        return self._salario_base

    def adicionar_regra_pagamento(self, regra: RegraDePagamento):
        if regra not in self.regras_pagamento:
            self.regras_pagamento.append(regra)

    def registrar_ponto(self, data: date, inicio_real_str: str, fim_real_str: str, pausas_reais: list = None):
        self.horario_funcionario.registrar_ponto(data, inicio_real_str, fim_real_str, pausas_reais)
    
    def definir_horario_especifico(self, data: date, horario: Horario):
        self.horario_funcionario.definir_horario_especifico(data, horario)
    
    def calcular_diferenca_diaria(self, data: date) -> dict:
        return self.horario_funcionario.calcular_diferencas(data)
    
    def obter_resumo_horas_mes(self, mes: int = None, ano: int = None) -> dict:
        if mes is None:
            mes = datetime.now().month
        if ano is None:
            ano = datetime.now().year
        
        resumo = self.horario_funcionario.obter_resumo_mensal(mes, ano)
        
        # Contar atendimentos do mês
        num_atendimentos = 0
        for atendimento in self.atendimentos_realizados:
            if atendimento['data'].month == mes and atendimento['data'].year == ano:
                num_atendimentos += 1
        
        return {
            "funcionario": self.nome,
            "mes": mes,
            "ano": ano,
            "cargo": self._cargo.name,
            "dias_trabalhados": resumo["dias_com_registro"],
            "horas_previstas": resumo["previstos"]["trabalhado"],
            "horas_reais": resumo["reais"]["trabalhado"],
            "horas_diurnas": resumo["reais"]["diurno"],
            "horas_noturnas": resumo["reais"]["noturno"],
            "diferenca": resumo["diferenca"],
            "atendimentos": num_atendimentos
        }
        
    def listar_registros_ponto_mes(self, mes: int = None, ano: int = None) -> List[Dict]:
        if mes is None:
            mes = datetime.now().month
        if ano is None:
            ano = datetime.now().year
        
        registros = []
        num_dias = calendar.monthrange(ano, mes)[1]
        data_inicial = date(ano, mes, 1)
        
        for i in range(num_dias):
            data_atual = data_inicial + timedelta(days=i)
            diferencas = self.calcular_diferenca_diaria(data_atual)
            
            if diferencas:  # Se houver registro para este dia
                registros.append({
                    "data": diferencas['data'],
                    "dia_semana": Dias_Semana.data_para_enum(data_atual).name,
                    "trabalhado_previsto": str(diferencas['tempo_trabalhado_previsto']),
                    "trabalhado_real": str(diferencas['tempo_trabalhado_real']),
                    "atraso": str(diferencas['atraso']),
                    "extra_falta": formatar_timedelta(diferencas['tempo_extra'])
                })
        
        return registros

    def registrar_atendimento(self, paciente: 'Paciente', descricao: str, data: date = None):
        if data is None:
            data = datetime.now().date()
        
        self.atendimentos_realizados.append({
            "paciente": paciente,
            "descricao": descricao,
            "data": data,
            "hora": datetime.now().strftime("%H:%M:%S")
        })

    def obter_atendimentos(self) -> List[Dict]:
        return self.atendimentos_realizados

    def calcular_pagamento(self, mes: int = None, ano: int = None, contexto: dict = None) -> Dict:
        if mes is None:
            mes = datetime.now().month
        if ano is None:
            ano = datetime.now().year
        
        if contexto is None:
            contexto = {}
        
        contexto['mes'] = mes
        contexto['ano'] = ano

        resumo = self.horario_funcionario.obter_resumo_mensal(mes, ano)
        
        # Timedelta para horas, o // faz o mesmo do que / mas o resultado é um inteiro
        horas_reais_float = resumo["reais"]["trabalhado"].total_seconds() // 3600
        horas_previstas_float = resumo["previstos"]["trabalhado"].total_seconds() // 3600
        diferenca_horas = horas_reais_float - horas_previstas_float
        
        # Conta os atendimentos realizados no mês
        num_atendimentos = 0
        for atendimento in self.atendimentos_realizados:
            if atendimento['data'].month == mes and atendimento['data'].year == ano:
                num_atendimentos += 1

        # Calcula o pagamento total usando as regras de pagamento
        total_a_pagar = 0.0
        for regra in self.regras_pagamento:
            total_a_pagar += regra.calcular(self, contexto)
        
        return {
            "funcionario": self.nome,
            "cargo": self._cargo.name,
            "mes": mes,
            "ano": ano,
            "salario_base": self._salario_base,
            "horas_previstas": horas_previstas_float,
            "horas_reais": horas_reais_float,
            "horas_diurnas": resumo["reais"]["diurno"],
            "horas_noturnas": resumo["reais"]["noturno"],
            "diferenca_horas": diferenca_horas,
            "total_atendimentos": num_atendimentos,
            "total_a_pagar": total_a_pagar
        }
    
class Medico(Funcionario):
    def __init__(self, nome: str, idade: int, salario: float, numero_funcionario: int, especialidade: Cargo, horario_semanal: Horario_Semanal):
        Funcionario.__init__(self, nome, idade, salario, numero_funcionario, especialidade, horario_semanal)
        self._especialidade = especialidade
        
        # Adiciona a regra de bônus por atendimento
        self.adicionar_regra_pagamento(RegraBonusPorAtendimento(valor_por_paciente=50.0))

    def __str__(self):
        atendimentos = self.obter_atendimentos()
        pagamento = self.calcular_pagamento()
        
        relatorio = f"\nDr./Dra. {self.nome}"
        relatorio += f"\nNº Funcionário: {self.numero_funcionario}"
        relatorio += f"\nIdade: {self.idade} anos"
        relatorio += f"\nEspecialidade: {self._especialidade.value}"
        relatorio += f"\nSalário Base: {self._salario_base:.2f}€"
        relatorio += f"\nBônus por Atendimento: 50.00€ por paciente"
        relatorio += f"\nTotal de Atendimentos: {len(atendimentos)}"
        relatorio += f"\nSalário Total (mês atual): {pagamento['total_a_pagar']:.2f}€"
        
        if atendimentos:
            relatorio += "\nÚltimos atendimentos:"
            for atendimento in atendimentos[-5:]:
                relatorio += f"\n  - {atendimento['paciente'].nome}: {atendimento['descricao']} "
                relatorio += f"({atendimento['data']} às {atendimento['hora']})"
        
        return relatorio
    
    @property
    def especialidade(self) -> Cargo:
        return self._especialidade

class Enfermeiro(Funcionario):
    def __init__(self, nome: str, idade: int, salario: float, numero_funcionario: int, horario_semanal: Horario_Semanal):
        # Usa chamada direta para evitar problemas com herança múltipla (EnfermeiroChefe)
        Funcionario.__init__(self, nome, idade, salario, numero_funcionario, Cargo.Saude.Enfermeiro, horario_semanal)
        
        self._turno = "dia"  # Inicializa com o valor padrão
        # Determinar turno com base no horário semanal
        if horario_semanal:
            totais = horario_semanal.calcular_totais_semanais()
            if totais["noturno"] > totais["diurno"]:
                self._turno = "noite"
        
        # Adiciona regra de bônus noturno se aplicável
        if self._turno == "noite":
            self.adicionar_regra_pagamento(RegraBonusFixo(300.0))

    def __str__(self):
        atendimentos = self.obter_atendimentos()
        pagamento = self.calcular_pagamento()
        
        relatorio = f"\nEnfermeiro(a) {self.nome}"
        relatorio += f"\nNº Funcionário: {self.numero_funcionario}"
        relatorio += f"\nIdade: {self.idade} anos"
        relatorio += f"\nTurno: {self._turno.capitalize()}"
        relatorio += f"\nSalário Base: {self._salario_base:.2f}€"
        
        if self._turno == "noite":
            relatorio += f"\nBônus Noturno: 300.00€"
        
        relatorio += f"\nTotal de Atendimentos: {len(atendimentos)}"
        relatorio += f"\nSalário Total (mês atual): {pagamento['total_a_pagar']:.2f}€"
        
        if atendimentos:
            relatorio += "\nÚltimos atendimentos:"
            for atendimento in atendimentos[-3:]:
                relatorio += f"\n  - {atendimento['paciente'].nome}: {atendimento['descricao']} "
                relatorio += f"({atendimento['data']} às {atendimento['hora']})"
        
        return relatorio

    @property
    def turno(self) -> str:
        return self._turno

class Administrativo(Funcionario):
    def __init__(self, nome: str, idade: int, salario: float, numero_funcionario: int, setor: str, horas_registradas: float, horario_semanal: Horario_Semanal):
        # Usa chamada direta para evitar problemas com herança múltipla (EnfermeiroChefe)
        Funcionario.__init__(self, nome, idade, salario, numero_funcionario, Cargo.Administrativo.Coordenador, horario_semanal)
        self.setor = setor
        self.horas_registradas = horas_registradas
        
        # Adiciona regra de pagamento por hora
        self.adicionar_regra_pagamento(RegraPagamentoPorHora(valor_por_hora=10.0))
    
    def __str__(self):
        atendimentos = self.obter_atendimentos()
        pagamento = self.calcular_pagamento()
        
        relatorio = f"\nAdministrativo: {self.nome}"
        relatorio += f"\nNº Funcionário: {self.numero_funcionario}"
        relatorio += f"\nIdade: {self.idade} anos"
        relatorio += f"\nSetor: {self.setor}"
        relatorio += f"\nCargo: {self._cargo.value}"
        relatorio += f"\nSalário Base: {self._salario_base:.2f}€"
        relatorio += f"\nPagamento por Hora: 10.00€/h"
        relatorio += f"\nHoras Registradas: {self.horas_registradas:.2f}h"
        relatorio += f"\nSalário Total (mês atual): {pagamento['total_a_pagar']:.2f}€"
        relatorio += f"\nAtendimentos Realizados: {len(atendimentos)}"
        
        if atendimentos:
            relatorio += "\nÚltimos atendimentos:"
            for atendimento in atendimentos[-3:]:
                relatorio += f"\n  - {atendimento['paciente'].nome}: {atendimento['descricao']} "
                relatorio += f"({atendimento['data']} às {atendimento['hora']})"
        
        return relatorio

class EnfermeiroChefe(Enfermeiro, Administrativo):
    def __init__(self, nome: str, idade: int, salario: float, numero_funcionario: int, setor: str, bonus_percentual_chefia: float, horario_semanal: Horario_Semanal):
        # Inicializa primeiro como Enfermeiro (que já configura Funcionario e o turno)
        Enfermeiro.__init__(self, nome, idade, salario, numero_funcionario, horario_semanal)
        
        # Adiciona atributos específicos do Administrativo
        self.setor = setor
        self.horas_registradas = 0.0
        
        # Adiciona regras de pagamento específicas do EnfermeiroChefe
        # (o bônus noturno já foi adicionado pelo Enfermeiro se aplicável)
        self.adicionar_regra_pagamento(RegraBonusPorAtendimento(valor_por_paciente=50.0))
        self.adicionar_regra_pagamento(RegraBonusPercentual(bonus_percentual_chefia))
        self.adicionar_regra_pagamento(RegraPagamentoPorHora(valor_por_hora=10.0))

    def __str__(self):
        atendimentos = self.obter_atendimentos()
        pagamento = self.calcular_pagamento()
        
        relatorio = f"\nEnfermeiro(a) Chefe: {self.nome}"
        relatorio += f"\nNº Funcionário: {self.numero_funcionario}"
        relatorio += f"\nIdade: {self.idade} anos"
        relatorio += f"\nTurno: {self._turno.capitalize()}"
        relatorio += f"\nSetor: {self.setor}"
        relatorio += f"\nSalário Base: {self._salario_base:.2f}€"
        
        if self._turno == "noite":
            relatorio += f"\nBônus Noturno: 300.00€"
        
        relatorio += f"\nBônus por Atendimento: 50.00€ por paciente"
        relatorio += f"\nBônus de Chefia: Percentual sobre salário base"
        relatorio += f"\nPagamento por Hora: 10.00€/h"
        relatorio += f"\nHoras Registradas: {self.horas_registradas:.2f}h"
        relatorio += f"\nTotal de Atendimentos: {len(atendimentos)}"
        relatorio += f"\nSalário Total (mês atual): {pagamento['total_a_pagar']:.2f}€"
        
        if atendimentos:
            relatorio += "\nÚltimos atendimentos:"
            for atendimento in atendimentos[-3:]:
                relatorio += f"\n  - {atendimento['paciente'].nome}: {atendimento['descricao']} "
                relatorio += f"({atendimento['data']} às {atendimento['hora']})"
        
        return relatorio
    
class Sala(ABC):
    def __init__(self, id_sala: int, nome: str, capacidade: int):
        self.id_sala = id_sala
        self.nome = nome
        self.capacidade = capacidade
    
    @abstractmethod
    def detalhar_sala(self):
        pass

class SalaAtendimento(Sala):
    def __init__(self, id_sala: int, nome: str, capacidade: int = 1):
        Sala.__init__(self, id_sala, nome, capacidade)
        self.funcionarios: List[Funcionario] = []
        self.paciente_atual = None
        self.funcionario_atual = None
        self.status = StatusSala.DISPONIVEL
        self.atendimentos_realizados = []
    
    def detalhar_sala(self):
        detalhes = f"\nSala de Atendimento:"
        detalhes += f"\nID: {self.id_sala}"
        detalhes += f"\nNome: {self.nome}"
        detalhes += f"\nCapacidade: {self.capacidade} pessoa(s)"
        detalhes += f"\nStatus: {self.status.value}"
        detalhes += f"\nFuncionários vinculados: {len(self.funcionarios)}"
        
        if self.paciente_atual:
            detalhes += f"\nPaciente atual: {self.paciente_atual.nome} ({self.paciente_atual.senha})"

        if self.funcionario_atual:
            detalhes += f"\nFuncionário atual: {self.funcionario_atual.nome}"
        
        detalhes += f"\nAtendimentos realizados: {len(self.atendimentos_realizados)}"
        return detalhes

    def adicionar_funcionario(self, funcionario: Funcionario):
        if funcionario not in self.funcionarios:
            self.funcionarios.append(funcionario)

    def chamar_paciente(self, paciente: Paciente, funcionario: Funcionario) -> bool:
        if self.status == StatusSala.DISPONIVEL:
            self.paciente_atual = paciente
            self.funcionario_atual = funcionario
            self.status = StatusSala.OCUPADO
            paciente.status = StatusAtendimento.ATENDIMENTO
            paciente.sala_atendimento = self.nome
            print(f"Paciente {paciente.nome} ({paciente.senha}) chamado para {self.nome}")
        return False

    def finalizar_atendimento(self, descricao: str = "Atendimento realizado"):
        if self.paciente_atual and self.funcionario_atual:
            # Registra o atendimento no funcionário
            self.funcionario_atual.registrar_atendimento(
                self.paciente_atual,
                descricao
            )
            
            # Registra o histórico da sala
            self.atendimentos_realizados.append({
                "paciente": self.paciente_atual,
                "funcionario": self.funcionario_atual,
                "descricao": descricao,
                "data_hora": datetime.now()
            })
            
            paciente_finalizado = self.paciente_atual
            self.paciente_atual.status = StatusAtendimento.ATENDIDO
            self.paciente_atual.sala_atendimento = None
            self.paciente_atual = None
            self.status = StatusSala.DISPONIVEL
            print(f"Paciente {paciente_finalizado.nome} teve seu atendimento finalizado")
            return True
        return False

class SalaEspera(Sala):
    def __init__(self, id_sala: int, nome: str, capacidade: int = 50, prefixo_senha: str = "A"):
        Sala.__init__(self, id_sala, nome, capacidade)
        self.salas_atendimento: List[SalaAtendimento] = []
        self.fila_espera: List[Paciente] = []
        self.contador_senhas = 0
        self.prefixo_senha = prefixo_senha
    
    def detalhar_sala(self):
        detalhes = f"\nSala de Espera:"
        detalhes += f"\nID: {self.id_sala}"
        detalhes += f"\nNome: {self.nome}"
        detalhes += f"\nCapacidade: {self.capacidade} pessoa(s)"
        detalhes += f"\nPrefixo de senha: {self.prefixo_senha}"
        detalhes += f"\nPacientes em espera: {len(self.fila_espera)}"
        detalhes += f"\nSalas de atendimento vinculadas: {len(self.salas_atendimento)}"
        detalhes += f"\nSenhas emitidas: {self.contador_senhas}"
        return detalhes

    def adicionar_sala_atendimento(self, sala_atendimento: SalaAtendimento):
        self.salas_atendimento.append(sala_atendimento)

    def pegar_senha(self, paciente: Paciente):
        self.contador_senhas += 1
        senha = f"{self.prefixo_senha}{self.contador_senhas:03d}"
        paciente.atribuir_senha(senha, self.nome)
        paciente.status = StatusAtendimento.ESPERA
        self.fila_espera.append(paciente)
        print(f"Paciente {paciente.nome} pegou senha: {senha} (Área: {self.nome})")

    def chamar_proximo(self, funcionario: Funcionario) -> bool:
        if not self.fila_espera:
            print("Não há pacientes na fila de espera.")
            return False

        for sala in self.salas_atendimento:
            if sala.status == StatusSala.DISPONIVEL:
                paciente_a_chamar = self.fila_espera.pop(0) # Remove o paciente da fila e guarda-o em uma variável
                
                if funcionario not in sala.funcionarios:
                    sala.adicionar_funcionario(funcionario)
                
                sala.chamar_paciente(paciente_a_chamar, funcionario)
                return True

        print("Todas as salas de atendimento estão ocupadas.")
        return False

    def mostrar_painel(self):
        print(f"\nPainel: {self.nome}: ")
        
        for sala in self.salas_atendimento:
            senha_atual = ""
            funcionario_atual = ""

            if sala.paciente_atual:
                senha_atual = sala.paciente_atual.senha

            if sala.funcionario_atual:
                funcionario_atual = sala.funcionario_atual.nome 

            status = sala.status.value
            print(f"{sala.nome} / Status: {status} / Atendendo: {senha_atual} ({funcionario_atual})")

        print(f"\nFila de espera ({len(self.fila_espera)} pacientes):")
        if self.fila_espera:
            i = 1
            for paciente in self.fila_espera[:5]: # Mostra apenas os primeiros 5 pacientes na fila
                print(f"{i} - {paciente.senha} - {paciente.nome}")
                i += 1
        else:
            print("(Vazia)")

class SalaCirurgia(Sala):
    def __init__(self, id_sala: int, nome: str, capacidade: int = 10):
        Sala.__init__(self, id_sala, nome, capacidade)
        self.equipamentos: List[str] = []
    
    def adicionar_equipamento(self, equipamento: str):
        if equipamento in self.equipamentos:
            print(f"Equipamento '{equipamento}' já existe na {self.nome}")
        else:
            self.equipamentos.append(equipamento)
            print(f"Equipamento '{equipamento}' adicionado à {self.nome}")
    
    def detalhar_sala(self):
        detalhes = f"\nSala de Cirurgia"
        detalhes += f"\nID: {self.id_sala}"
        detalhes += f"\nNome: {self.nome}"
        detalhes += f"\nCapacidade: {self.capacidade} pessoa(s)"
        detalhes += f"\nEquipamentos ({len(self.equipamentos)}):"
        
        if self.equipamentos:
            i = 1
            for equipamento in self.equipamentos:
                detalhes += f"\n  {i}. {equipamento}"
                i += 1
        else:
            detalhes += "\n  (Nenhum equipamento cadastrado)"

        return detalhes

class SistemaHospital:
    def __init__(self):
        self.pacientes: Dict[str, Paciente] = {}
        self.funcionarios: Dict[int, Funcionario] = {}
        self.salas_espera: Dict[str, SalaEspera] = {}
        self.salas_cirurgia: Dict[str, SalaCirurgia] = {}
        self.historico_atendimentos: List[Dict] = []
        self._proximo_numero_utente = 1

    def registrar_paciente(self, nome_ou_paciente, idade: int = None) -> Paciente:
        if isinstance(nome_ou_paciente, Paciente):
            paciente = nome_ou_paciente
        elif isinstance(nome_ou_paciente, str) and idade is not None:
            numero_utente = self._proximo_numero_utente
            self._proximo_numero_utente += 1
            paciente = Paciente(nome_ou_paciente, idade, numero_utente)
        else:
            return None
        
        self.pacientes[paciente.numero_utente] = paciente
        return paciente

    def registrar_funcionario(self, funcionario: Funcionario):
        if not isinstance(funcionario, Funcionario): # "is" não não funciona com subclasses
            return
                
        self.funcionarios[funcionario.numero_funcionario] = funcionario

    def obter_funcionario(self, numero_funcionario: int):
        if numero_funcionario not in self.funcionarios:
            return None
        return self.funcionarios[numero_funcionario]
        
    def obter_paciente(self, numero_utente: int):
        utente_str = f"{numero_utente:09d}"
        if utente_str not in self.pacientes:
            return None

        return self.pacientes[utente_str]
    
    def criar_area_especializada(self, nome_area: str, num_salas: int = 2, prefixo_senha: str = "A", capacidade_espera: int = 50, capacidade_atendimento: int = 1) -> SalaEspera:
        sala_espera = SalaEspera(len(self.salas_espera), nome_area, capacidade_espera, prefixo_senha)
        
        for i in range(num_salas): # Cada Área de atendimento tem a sua casa decimal como 100 ou 200, e cada sala é um aumento de 1
            sala = SalaAtendimento(len(self.salas_espera) * 100 + i, f"{nome_area} - Sala {i+1}", capacidade_atendimento)
            sala_espera.adicionar_sala_atendimento(sala)
        
        self.salas_espera[nome_area] = sala_espera
        return sala_espera

    def criar_sala_cirurgia(self, nome: str, capacidade: int = 10) -> SalaCirurgia:
        capacidade = max(1, capacidade)  # Capacidade mínima = 1
        id_sala = len(self.salas_cirurgia) + 1
        sala = SalaCirurgia(id_sala, nome, capacidade)
        self.salas_cirurgia[nome] = sala
        return sala

class Paciente_historicos:    
    Pacientes = {}
    Funcionarios = {}
    Historico_Medico = {}
    
    @staticmethod
    def adicionar_funcionario(funcionario):
        num_funcionario = funcionario.numero_funcionario

        if num_funcionario in Paciente_historicos.Historico_Medico:
            return False

        Paciente_historicos.Funcionarios[num_funcionario] = funcionario
        Paciente_historicos.Historico_Medico[num_funcionario] = {}
        return True
       
    @staticmethod
    def adicionar_paciente(paciente):
        if isinstance(paciente, Paciente):
            Paciente_historicos.Pacientes[paciente.numero_utente] = paciente
            return True
        return False
    
    @staticmethod
    def adicionar_historico(numero_funcionario: int, numero_utente: str, id_historico: int, descricao: str) -> bool:
        if numero_funcionario not in Paciente_historicos.Funcionarios:
            return False
        if numero_utente not in Paciente_historicos.Pacientes:
            return False
        
        if numero_funcionario not in Paciente_historicos.Historico_Medico:
            Paciente_historicos.Historico_Medico[numero_funcionario] = {}
        
        if numero_utente not in Paciente_historicos.Historico_Medico[numero_funcionario]:
            Paciente_historicos.Historico_Medico[numero_funcionario][numero_utente] = {}
        
        if id_historico in Paciente_historicos.Historico_Medico[numero_funcionario][numero_utente]:
            return False
        
        Paciente_historicos.Historico_Medico[numero_funcionario][numero_utente][id_historico] = descricao
        return True
    
    @staticmethod
    def obter_historico(id_historico: int):
        for numero_funcionario in Paciente_historicos.Historico_Medico.values():
            if id_historico in numero_funcionario:
                return numero_funcionario[id_historico]
        return None
    
    @staticmethod
    def obter_historicos_paciente(numero_utente: str) -> Dict[int, str]:
        historicos = {}
        
        for numero_funcionario in Paciente_historicos.Historico_Medico:
            pacientes_dict = Paciente_historicos.Historico_Medico[numero_funcionario]
            if numero_utente in pacientes_dict:
                historicos.update(pacientes_dict[numero_utente])

        return historicos

    @staticmethod
    def obter_funcionarios_paciente(numero_utente: str) -> List[int]:
        funcionarios = []
        for numero_funcionario in Paciente_historicos.Historico_Medico:
            pacientes_dict = Paciente_historicos.Historico_Medico[numero_funcionario]
            if numero_utente in pacientes_dict:
                funcionarios.append(numero_funcionario)
                
        return funcionarios
    
    @staticmethod
    def obter_pacientes_funcionario(numero_funcionario: int) -> List[str]:
        if numero_funcionario in Paciente_historicos.Historico_Medico:
            return list(Paciente_historicos.Historico_Medico[numero_funcionario].keys())
        return []
    
    @staticmethod
    def obter_historicos_funcionario_paciente(numero_funcionario: int, numero_utente: str) -> Dict[int, str]:
        if numero_funcionario in Paciente_historicos.Historico_Medico:
            if numero_utente in Paciente_historicos.Historico_Medico[numero_funcionario]:
                return Paciente_historicos.Historico_Medico[numero_funcionario][numero_utente]
        return {}
    
    @staticmethod
    def listar_todos_historicos() -> str:
        resultado = "Historico Médico Completo:\n"

        if not Paciente_historicos.Historico_Medico:
            resultado += "Nenhum histórico registrado.\n"
            return resultado
        
        for numero_funcionario in Paciente_historicos.Historico_Medico:
            pacientes_dict = Paciente_historicos.Historico_Medico[numero_funcionario]
            if numero_funcionario in Paciente_historicos.Funcionarios:
                funcionario_info = Paciente_historicos.Funcionarios[numero_funcionario]
                resultado += f"\nMédico/Funcionário: {funcionario_info.nome} (#{numero_funcionario})\n"
                
                for numero_paciente in pacientes_dict:
                    historicos_dict = pacientes_dict[numero_paciente]
                    if numero_paciente in Paciente_historicos.Pacientes:
                        paciente_info = Paciente_historicos.Pacientes[numero_paciente]
                        resultado += f"Paciente: {paciente_info.nome} (#{numero_paciente})\n"
                        
                        for id_historico in historicos_dict:
                            descricao = historicos_dict[id_historico]
                            resultado += f"Id {id_historico}: {descricao}\n"
        
        resultado += f"\n"
        return resultado
    
    @staticmethod
    def limpar():
        Paciente_historicos.Pacientes.clear()
        Paciente_historicos.Funcionarios.clear()
        Paciente_historicos.Historico_Medico.clear()

