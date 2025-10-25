from datetime import datetime, timedelta, date
import os
from Program import (
    SistemaHospital, Funcionario, Medico, Enfermeiro, Paciente,
    Cargo, StatusSala, StatusAtendimento, SalaEspera, Paciente_historicos,
    Administrativo, EnfermeiroChefe, SalaCirurgia
)
from Horario import (
    Dias_Semana, HoraMinuto, IntervaloTempo, Horario, Horario_Semanal,
    formatar_timedelta, FuncionarioHorario
)

def aguardar_e_limpar():
    input("\nPressione Enter para continuar...")
    os.system('cls')

def criar_horario_padrao(inicio: str = "09:00", fim: str = "18:00", pausa_inicio: str = "12:00", pausa_fim: str = "13:00") -> Horario_Semanal:
    horario_semanal = Horario_Semanal()
    for dia in [Dias_Semana.Segunda, Dias_Semana.Terca, Dias_Semana.Quarta, Dias_Semana.Quinta, Dias_Semana.Sexta]:
        horario = Horario(
            IntervaloTempo.init_com_HoraMinuto(
                HoraMinuto.init_com_str(inicio),
                HoraMinuto.init_com_str(fim)
            ),
            pausas=[
                IntervaloTempo.init_com_HoraMinuto(
                    HoraMinuto.init_com_str(pausa_inicio),
                    HoraMinuto.init_com_str(pausa_fim)
                )
            ]
        )
        horario_semanal.adicionar_horario(dia, horario)
    return horario_semanal

def criar_horario_interativo() -> Horario_Semanal:
    print("\nConfiguração de Horário Semanal:")
    print("  Para cada dia da semana, defina o horário de trabalho.")
    print("  Deixe o horário de início em branco para marcar o dia como FOLGA.\n")
    
    horario_semanal = Horario_Semanal()
    
    for dia in Dias_Semana:
        print(f"\nConfigurar {dia.name}:")
        
        inicio_str = input(f"Hora de início (HH:MM) [vazio = folga]: ").strip()
        
        if not inicio_str:
            print(f"{dia.name} marcado como folga")
            continue
        
        try:
            fim_str = input(f"Hora de fim (HH:MM): ").strip()
            
            if not fim_str:
                print("Erro: Hora de fim é obrigatória!")
                continue
            
            HoraMinuto.init_com_str(inicio_str)
            HoraMinuto.init_com_str(fim_str)
            
            horario = Horario(
                IntervaloTempo.init_com_HoraMinuto(
                    HoraMinuto.init_com_str(inicio_str),
                    HoraMinuto.init_com_str(fim_str)
                )
            )
            
            print(f"\nDeseja adicionar pausas para {dia.name}? (s/n): ")
            adicionar_pausas = input().strip().lower()
            
            if adicionar_pausas == 's':
                contador_pausas = 0
                while contador_pausas < 24:  # Máximo de 24 pausas por dia
                    print(f"\n  Pausa {contador_pausas + 1} (deixe em branco para terminar):")
                    pausa_inicio_str = input(f"Início da pausa (HH:MM): ").strip()
                    
                    if not pausa_inicio_str:
                        break
                    
                    pausa_fim_str = input(f"Fim da pausa (HH:MM): ").strip()
                    
                    if not pausa_fim_str:
                        print("Pausa ignorada (fim não especificado)")
                        break
                
                    pausa = IntervaloTempo.init_com_HoraMinuto(
                        HoraMinuto.init_com_str(pausa_inicio_str),
                        HoraMinuto.init_com_str(pausa_fim_str)
                    )
                    
                    if horario.pausas.adicionar_pausa(pausa):
                        print(f"Pausa {pausa_inicio_str} - {pausa_fim_str} adicionada!")
                        contador_pausas += 1
                    else:
                        print("Erro: Pausa fora do horário de trabalho ou limite excedido")
                        break
            
            horario_semanal.adicionar_horario(dia, horario)
            
            tempo_trabalhado = horario.tempo_trabalhado()
            print(f"\n{dia.name} configurado: {inicio_str} - {fim_str}")
            print(f"Tempo de trabalho: {formatar_timedelta(tempo_trabalhado)}")
            
        except Exception:
            print(f"Erro ao configurar {dia.name}. -")
            print(f"{dia.name} marcado como folga.")

    print("\nResumo do horário semanal:")

    totais = horario_semanal.calcular_totais_semanais()
    dias_trabalho = len(horario_semanal.horarios)
    
    print(f"Dias de trabalho: {dias_trabalho}")
    print(f"Tempo total semanal: {formatar_timedelta(totais['trabalhado'])}")
    print(f"- Tempo diurno: {formatar_timedelta(totais['diurno'])}")
    print(f"- Tempo noturno: {formatar_timedelta(totais['noturno'])}")
    
    return horario_semanal

class InterfaceHospital:

    def __init__(self):
        self.sistema = SistemaHospital()

    def selecionar_funcionario(self, mensagem: str = "Funcionários:"):
        if not self.sistema.funcionarios:
            print("\nNenhum funcionário registado!")
            return None

        print(f"\n{mensagem}")
        
        i = 1
        for funcionario in self.sistema.funcionarios.values():
            print(f"{i} - {funcionario.nome}")
            i += 1

        try:
            escolha = int(input("\nEscolha o funcionário: "))
            
            contador = 1
            for funcionario in self.sistema.funcionarios.values():
                if contador == escolha:
                    return funcionario
                contador += 1
            
            print("Opção inválida!")
        
        except ValueError:
            print("Valor inválido!")
        return None

    def selecionar_paciente(self, mensagem: str = "Pacientes:", filtro=None): 
        if not self.sistema.pacientes:
            print("\nNenhum paciente registado!")
            return None

        pacientes_filtrados = []
        
        if filtro:
            for paciente in self.sistema.pacientes.values():
                if filtro(paciente): # Exemplo de filtro: lambda paciente: paciente.idade > 18
                    pacientes_filtrados.append(paciente)
        else:
            for paciente in self.sistema.pacientes.values():
                pacientes_filtrados.append(paciente)

        if not pacientes_filtrados:
            print("\nNenhum paciente disponível com os critérios especificados!")
            return None

        print(f"\n{mensagem}")
        i = 1
        for paciente in pacientes_filtrados:
            print(f"{i} - {paciente.nome} (Nº {paciente.numero_utente})")
            i += 1

        try:
            escolha = int(input("\nEscolha o paciente: "))
            
            contador = 1
            for paciente in pacientes_filtrados:
                if contador == escolha:
                    return paciente
                
                contador += 1
            
            print("Opção inválida!")

        except ValueError:
            print("Valor inválido!")
        
        return None

    def obter_mes_ano(self):
        mes_input = input("Mês (1-12, vazio=atual): ").strip()
        ano_input = input("Ano (vazio=atual): ").strip()
        
        mes = datetime.now().month
        ano = datetime.now().year
        
        if mes_input:
            mes = int(mes_input)

        if ano_input:
            ano = int(ano_input)

        return mes, ano
































    def selecionar_area(self, mensagem: str = "Áreas de atendimento:"):
        if not self.sistema.salas_espera:
            print("\nNenhuma área de atendimento registada!")
            return None

        print(f"\n{mensagem}")
        
        i = 1
        for nome_area in self.sistema.salas_espera.keys():
            print(f"{i} - {nome_area}")
            i += 1

        try:
            escolha = int(input("\nEscolha a área: "))
            
            contador = 1
            for nome_area in self.sistema.salas_espera.keys():
                if contador == escolha:
                    return self.sistema.salas_espera[nome_area]
                
                contador += 1
            
            print("Opção inválida!")

        except ValueError:
            print("Valor inválido!")

        return None

    def exibir_menu_generico(self, titulo: str, opcoes: dict, sair_texto: str = "Voltar"):
        while True:
            aguardar_e_limpar()
            print(f"\n{titulo}:")
            
            numeros_opcoes = []
            for numero in opcoes.keys():
                numeros_opcoes.append(int(numero))
            
            numeros_opcoes.sort()
            
            for numero in numeros_opcoes:
                numero_str = str(numero)
                descricao = opcoes[numero_str][0]
                print(f"{numero_str} - {descricao}")
            
            print(f"0. {sair_texto}")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "0":
                return
            
            if opcao in opcoes:
                acao = opcoes[opcao][1]
                if acao is not None and callable(acao): # Verifica se não é null, e se é uma função
                    acao() # Executa ação correspondente
            else:
                print("Opção inválida!")

    def inicializar_dados_padrao(self):
        print("\nSistema hospitalar - inicialização:")
        print("Deseja inicializar os dados padrão? (s/n, padrão: n)")
        
        resposta = input("Escolha (s/n): ").strip().lower()

        if resposta == 's':
            print("\nCarregando dados padrão...")
            self.configuracao_padrao()
            print("Dados padrão carregados com sucesso!")
        else:
            print("\nSistema inicializado sem dados definidos.")
        
        self.menu_principal()

    def menu_principal(self):
        opcoes = {
            "1": ("Funcionários", self.menu_funcionarios),
            "2": ("Recepção (Registrar/Encaminhar Pacientes)", self.menu_recepcao),
            "3": ("Áreas de Atendimento", self.menu_areas),
            "4": ("Salas", self.menu_salas),
            "5": ("Salas de Cirurgia", self.menu_salas_cirurgia),
            "6": ("Pacientes", self.menu_pacientes),
            "7": ("Histórico Médico", self.menu_historico_medico),
        }
        self.exibir_menu_generico("Sistema hospitalar - Menu principal", opcoes, sair_texto="Sair")

    def configuracao_padrao(self):
        self.sistema.criar_area_especializada("Cardiologia", 3, "C")
        self.sistema.criar_area_especializada("Cirurgia Geral", 3, "CG")
        self.sistema.criar_area_especializada("Medicina Interna", 3, "MI")
        self.sistema.criar_area_especializada("Psiquiatria", 2, "PS")
        self.sistema.criar_area_especializada("Medicina Geral", 2, "MG")

        horario_base = criar_horario_padrao() # Cria o horário base padrão (09:00 - 18:00, Segunda a Sexta)

        self.sistema.registrar_funcionario(Medico(nome="Doutor João Silva", idade=45, salario=3000, numero_funcionario=1001, especialidade=Cargo.Saude.Medico.Cardiologia, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Medico(nome="Doutora Maria Santos", idade=38, salario=2900, numero_funcionario=1002, especialidade=Cargo.Saude.Medico.CirurgiaGeral, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Medico(nome="Doutor Pedro Costa", idade=50, salario=3100, numero_funcionario=1003, especialidade=Cargo.Saude.Medico.MedicinaInterna, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Medico(nome="Doutora Sofia Ferreira", idade=41, salario=3200, numero_funcionario=1004, especialidade=Cargo.Saude.Medico.Psiquiatria, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Medico(nome="Doutor Rui Lopes", idade=36, salario=2800, numero_funcionario=1005, especialidade=Cargo.Saude.Medico.Geral, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Medico(nome="Doutora Carla Mendes", idade=43, salario=3050, numero_funcionario=1006, especialidade=Cargo.Saude.Medico.Cardiologia, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Medico(nome="Doutor André Almeida", idade=39, salario=2950, numero_funcionario=1007, especialidade=Cargo.Saude.Medico.CirurgiaGeral, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Medico(nome="Doutora Rita Sousa", idade=34, salario=2750, numero_funcionario=1008, especialidade=Cargo.Saude.Medico.MedicinaInterna, horario_semanal=horario_base))

        self.sistema.registrar_funcionario(Enfermeiro(nome="Enfermeiro Ana Oliveira", idade=32, salario=1800, numero_funcionario=2001, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Enfermeiro(nome="Enfermeiro Carlos Dias", idade=35, salario=1900, numero_funcionario=2002, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Enfermeiro(nome="Enfermeiro Paula Rodrigues", idade=29, salario=1750, numero_funcionario=2003, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Enfermeiro(nome="Enfermeiro Miguel Tavares", idade=31, salario=1850, numero_funcionario=2004, horario_semanal=horario_base))

        self.sistema.registrar_funcionario(Enfermeiro(nome="Enfermeiro Beatriz Martins", idade=27, salario=1700, numero_funcionario=2005, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Enfermeiro(nome="Enfermeiro Gonçalo Pires", idade=33, salario=1950, numero_funcionario=2006, horario_semanal=horario_base))

        self.sistema.registrar_funcionario(EnfermeiroChefe(nome="Enfermeiro Chefe Teresa Silva", idade=42, salario=2500, numero_funcionario=2100, setor="UTI", bonus_percentual_chefia=15.0, horario_semanal=horario_base))
        self.sistema.registrar_funcionario(EnfermeiroChefe(nome="Enfermeiro Chefe Manuel Costa", idade=48, salario=2600, numero_funcionario=2101, setor="Urgências", bonus_percentual_chefia=18.0, horario_semanal=horario_base))

        self.sistema.registrar_funcionario(Administrativo(nome="Adminstrador Isabel Cunha",idade=40,salario=1500,numero_funcionario=3001,setor="Recursos Humanos",horas_registradas=40.0,horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Administrativo(nome="Adminstrador Francisco Gomes",idade=37,salario=1600,numero_funcionario=3002,setor="Contabilidade",horas_registradas=40.0,horario_semanal=horario_base))
        self.sistema.registrar_funcionario(Administrativo(nome="Adminstrador Luísa Pereira",idade=35,salario=1550,numero_funcionario=3003,setor="Receção",horas_registradas=35.0,horario_semanal=horario_base))

        sala_cirurgia1 = self.sistema.criar_sala_cirurgia("Centro Cirúrgico 1", 10)
        sala_cirurgia1.adicionar_equipamento("Bisturi Elétrico")
        sala_cirurgia1.adicionar_equipamento("Mesa Cirúrgica")
        sala_cirurgia1.adicionar_equipamento("Monitor de Sinais Vitais")
        sala_cirurgia1.adicionar_equipamento("Desfibrilador")
        sala_cirurgia1.adicionar_equipamento("Anestesia")
        sala_cirurgia1.adicionar_equipamento("Aspirador Cirúrgico")

        sala_cirurgia2 = self.sistema.criar_sala_cirurgia("Centro Cirúrgico 2", 12)
        sala_cirurgia2.adicionar_equipamento("Bisturi Elétrico")
        sala_cirurgia2.adicionar_equipamento("Mesa Cirúrgica")
        sala_cirurgia2.adicionar_equipamento("Monitor de Sinais Vitais")
        sala_cirurgia2.adicionar_equipamento("Desfibrilador")
        sala_cirurgia2.adicionar_equipamento("Raio-X Portátil")
        sala_cirurgia2.adicionar_equipamento("Sistema de Vídeo Cirúrgico")

        sala_cirurgia3 = self.sistema.criar_sala_cirurgia("Centro Cirúrgico 3", 8)
        sala_cirurgia3.adicionar_equipamento("Bisturi Elétrico")
        sala_cirurgia3.adicionar_equipamento("Mesa Cirúrgica")
        sala_cirurgia3.adicionar_equipamento("Monitor de Sinais Vitais")
        sala_cirurgia3.adicionar_equipamento("Desfibrilador")

        self.sistema.registrar_paciente("Manuel Oliveira", 65)
        self.sistema.registrar_paciente("Ana Paula Silva", 42)
        self.sistema.registrar_paciente("José Carlos Santos", 58)
        self.sistema.registrar_paciente("Maria João Costa", 33)
        self.sistema.registrar_paciente("António Ferreira", 71)
        self.sistema.registrar_paciente("Helena Lopes", 28)
        self.sistema.registrar_paciente("Ricardo Mendes", 45)
        self.sistema.registrar_paciente("Inês Almeida", 19)
        self.sistema.registrar_paciente("Fernando Sousa", 53)
        self.sistema.registrar_paciente("Cristina Rodrigues", 61)
        self.sistema.registrar_paciente("Paulo Tavares", 38)
        self.sistema.registrar_paciente("Sandra Martins", 47)
        self.sistema.registrar_paciente("Vasco Pires", 25)
        self.sistema.registrar_paciente("Mariana Cunha", 31)
        self.sistema.registrar_paciente("Jorge Gomes", 69)
        self.sistema.registrar_paciente("Patrícia Pereira", 36)
        self.sistema.registrar_paciente("Tiago Ribeiro", 22)
        self.sistema.registrar_paciente("Mónica Carvalho", 54)
        self.sistema.registrar_paciente("Daniel Nunes", 40)
        self.sistema.registrar_paciente("Vera Correia", 29)

    def menu_funcionarios(self):
        opcoes = {
            "1": ("Listar funcionários", self.listar_funcionarios),
            "2": ("Registar novo funcionário", self.registar_funcionario_customizado),
            "3": ("Ver histórico de atendimentos de um funcionário", self.relatorio_funcionario),
            "4": ("Ver horário e horas de um funcionário", self.ver_horario_funcionario),
            "5": ("Ver pagamento mensal de um funcionário", self.ver_pagamento_funcionario),
            "6": ("Gerir horários de funcionário", self.menu_horarios),
            "7": ("Registar ponto", self.registar_ponto),
        }
        self.exibir_menu_generico("Funcionários", opcoes)

    def menu_salas(self):
        opcoes = {
            "1": ("Listar salas", self.listar_areas),
            "2": ("Criar nova área (com salas)", self.criar_area_customizada),
            "3": ("Ver status das salas", self.listar_status_salas),
        }
        self.exibir_menu_generico("Salas", opcoes)

    def menu_salas_cirurgia(self):
        opcoes = {
            "1": ("Criar sala de cirurgia", self.criar_sala_cirurgia),
            "2": ("Listar salas de cirurgia", self.listar_salas_cirurgia),
            "3": ("Adicionar equipamento a sala", self.adicionar_equipamento_sala),
            "4": ("Ver detalhes de sala", self.ver_detalhes_sala_cirurgia),
        }
        self.exibir_menu_generico("Salas de Cirurgia", opcoes)

    def menu_pacientes(self):
        opcoes = {
            "1": ("Registar novo paciente", self.registar_novo_paciente),
            "2": ("Ver todos os pacientes", self.listar_pacientes_completo),
            "3": ("Ver histórico de um paciente", self.relatorio_paciente),
            "4": ("Estatísticas do hospital", self.estatisticas_hospital),
        }
        self.exibir_menu_generico("Pacientes", opcoes)

    def menu_customizacao_manual(self):
        opcoes = {
            "1": ("Criar nova área especializada", self.criar_area_customizada),
            "2": ("Registar novo funcionário", self.registar_funcionario_customizado),
            "3": ("Ver áreas criadas", self.listar_areas),
            "4": ("Ver funcionários registados", self.listar_funcionarios),
        }
        self.exibir_menu_generico("Customização manual - áreas e funcionários", opcoes)

    def criar_area_customizada(self):
        print("Criar nova área especializada:")
        
        nome = input("Nome da área (ex: Cardiologia): ").strip()
        if not nome:
            print("Nome inválido!")
            return
        
        try:
            num_salas = int(input("Número de salas: ").strip())
            if num_salas < 1:
                print("Número de salas inválido!")
                return
        except ValueError:
            print("Número inválido!")
            return
        
        sigla = input("Sigla da área (ex: C para Cardiologia): ").strip()
        if sigla == "":
            sigla = nome[0].upper()
        
        self.sistema.criar_area_especializada(nome, num_salas, sigla)
        print(f"A área {nome} criada com sucesso!")

    def registar_funcionario_customizado(self):
        print("\nRegistar novo funcionário:")
        
        nome = input("Nome do funcionário: ").strip()
        if not nome:
            print("Nome inválido!")
            return
        
        try:
            idade = int(input("Idade: ").strip())
            salario = float(input("Salário (Base): ").strip())
            num_funcionario = int(input("Número de funcionário: ").strip())
        except ValueError:
            print("Dados inválidos!")
            return
        
        cargos_disponiveis = []
        
        for cargo_admin in Cargo.Administrativo:
            cargos_disponiveis.append(cargo_admin)
        
        for cargo_apoio in Cargo.Apoio:
            cargos_disponiveis.append(cargo_apoio)

        cargos_disponiveis.append(Cargo.Saude.Enfermeiro)
        cargos_disponiveis.append(Cargo.Saude.Farmaceutico)
        cargos_disponiveis.append(Cargo.Saude.Fisioterapeuta)
        cargos_disponiveis.append(Cargo.Saude.Farmaceutico)

        for especialidade in Cargo.Saude.Medico:
            cargos_disponiveis.append(especialidade)

        cargos_disponiveis.append("EnfermeiroChefe") # Especialização manual para Enfermeiro Chefe

        print("\nCargos disponíveis:")

        i = 1
        for cargo in cargos_disponiveis:
            print(f"{i} - {cargo.value}")
            i += 1

        try:
            cargo_input = int(input(f"\nEscolha o cargo (1-{len(cargos_disponiveis)}): ").strip())
            
            if not (1 <= cargo_input <= len(cargos_disponiveis)):
                print("Cargo inválido!")
                return

            cargo = cargos_disponiveis[cargo_input - 1]

        except ValueError:
            print("Valor inválido!")
            return

        print("\nDefinir horário semanal do funcionário:")
        print("Escolha o tipo de horário:")
        print("1. Configurar horário personalizado (dia a dia)")
        print("2. Usar horário padrão (Segunda a Sexta, 09:00-18:00, pausa 12:00-13:00)")

        try:
            tipo_horario = input("\nEscolha (1-2): ").strip()

            if tipo_horario == "1":
                horario_base = criar_horario_interativo()
            elif tipo_horario == "2":
                horario_base = criar_horario_padrao()
                print("\nHorário padrão aplicado (Segunda a Sexta, 09:00-18:00, pausa 12:00-13:00)")
            else:
                print("Opção inválida! Aplicando horário padrão...")
                horario_base = criar_horario_padrao()
        except Exception:
            print("Erro ao criar horário. A definir horário padrão.")
            horario_base = criar_horario_padrao()

        if cargo in Cargo.Saude.Medico:
            funcionario = Medico(nome, idade, salario, num_funcionario, cargo, horario_base)
        elif cargo == Cargo.Saude.Enfermeiro:
            funcionario = Enfermeiro(nome, idade, salario, num_funcionario, horario_base)
        elif cargo == "EnfermeiroChefe":
            setor = input("Setor (ex: UTI, Emergência): ").strip()
            if not setor:
                setor = "Geral"
                
            bonus_percentual = 0.0

            bonus_percentual_str = input("Bónus percentual de chefia (ex: 10 para 10%): ").strip()
            if bonus_percentual_str:
                bonus_percentual = float(bonus_percentual_str)

            funcionario = EnfermeiroChefe(nome, idade, salario, num_funcionario, setor, bonus_percentual, horario_base)
        elif cargo in Cargo.Administrativo:
            setor = input("Setor (ex: Financeiro, RH): ").strip()
            if not setor:
                setor = "Administrativo"
            horas_registradas = float(input("Horas registradas: ").strip() or "0")
            funcionario = Administrativo(nome, idade, salario, num_funcionario, setor, horas_registradas, horario_base)
        else:
            funcionario = Funcionario(nome, idade, salario, num_funcionario, cargo, horario_base)
        
        self.sistema.registrar_funcionario(funcionario)
        print(f"Funcionário {nome} registado com sucesso!")

    def listar_areas(self):
        print("\nÁreas especializadas:")
        
        if not self.sistema.salas_espera:
            print("Nenhuma área criada ainda.")
            return
        
        for area_nome in self.sistema.salas_espera.keys():
            sala_espera = self.sistema.salas_espera[area_nome]
            print(f"\n{area_nome}")
            print(f"Salas: {len(sala_espera.salas_atendimento)}")
            print(f"Pacientes em espera: {len(sala_espera.fila_espera)}")

    def listar_funcionarios(self):
        print("\nFuncionários registados:")
        
        if not self.sistema.funcionarios:
            print("Nenhum funcionário registado ainda.")
            return
        
        i = 1
        for numero_funcionario in self.sistema.funcionarios.keys():
            funcionario = self.sistema.funcionarios[numero_funcionario]
            print(f"\n{i} - {funcionario.nome}")
            print(f"Nº Funcionário: {numero_funcionario}")
            print(f"Cargo: {funcionario.cargo.name}")
            print(f"Salário: {funcionario.salario:.2f}€")
            print(f"Atendimentos realizados: {len(funcionario.atendimentos_realizados)}")
            i += 1

    def listar_pacientes_completo(self):
        self.listar_pacientes()

    def registar_novo_paciente(self):
        print("\nRegistar novo paciente:")
        
        nome = input("Nome do paciente: ").strip()
        if not nome:
            print("Nome inválido!")
            return
        
        try:
            idade = int(input("Idade: "))
            if idade <= 0:
                print("Idade inválida!")
                return
        except ValueError:
            print("Idade inválida!")
            return
        
        paciente = self.sistema.registrar_paciente(nome, idade)
        print(f"\nPaciente registado com sucesso!")
        print(f"Nome: {paciente.nome}")
        print(f"Número de utente: {paciente.numero_utente}")
        print(f"Idade: {paciente.idade}")

    def listar_status_salas(self):
        print("Status das salas:")
        
        if not self.sistema.salas_espera:
            print("Nenhuma área de atendimento criada ainda.")
            return
        
        for area_nome in self.sistema.salas_espera.keys():
            sala_espera = self.sistema.salas_espera[area_nome]
            print(f"\n{area_nome}")
            print(f"Salas de atendimento: {len(sala_espera.salas_atendimento)}")
            print(f"Pacientes em espera: {len(sala_espera.fila_espera)}")

            i_sala = 1
            for sala in sala_espera.salas_atendimento:
                if sala.status == StatusSala.DISPONIVEL: 
                    status = "Disponível" 
                else:
                    status = "Ocupada"

                paciente_info = ""
                if sala.paciente_atual:
                    paciente_info = f" (com {sala.paciente_atual.nome})"

                print(f"- Sala {i_sala}: {status}{paciente_info}")
                i_sala += 1

    def criar_sala_cirurgia(self):
        print("\nCriar nova sala de cirurgia:")

        nome = input("Nome da sala (ex: Centro Cirúrgico 1): ").strip()
        if not nome:
            print("Nome inválido!")
            return

        if nome in self.sistema.salas_cirurgia:
            print(f"Já existe uma sala de cirurgia com o nome {nome}!")
            return

        try:
            capacidade_input = input("Capacidade (número de pessoas, padrão 10): ").strip()
            capacidade = 10
            if capacidade_input:
                capacidade = int(capacidade_input)
                
            if capacidade < 1:
                print("Capacidade inválida!")
                return
            
        except ValueError:
            print("Número inválido!")
            return
        
        sala = self.sistema.criar_sala_cirurgia(nome, capacidade)
        print(f"\nSala de cirurgia {nome} criada com sucesso!")
        print(f"Id: {sala.id_sala}")
        print(f"Capacidade: {sala.capacidade} pessoas")

    def listar_salas_cirurgia(self):
        print("\nSalas de Cirurgia:")
        
        if not self.sistema.salas_cirurgia:
            print("Nenhuma sala de cirurgia criada ainda.")
            return
        
        for nome in self.sistema.salas_cirurgia.keys():
            sala = self.sistema.salas_cirurgia[nome]
            print(f"\n{nome}")
            print(f"Id: {sala.id_sala}")
            print(f"Capacidade: {sala.capacidade} pessoas")
            print(f"Equipamentos: {len(sala.equipamentos)}")

    def adicionar_equipamento_sala(self):
        if not self.sistema.salas_cirurgia:
            print("\nNenhuma sala de cirurgia criada ainda!")
            return

        print("\nSalas de Cirurgia disponíveis:")
        
        i = 1
        for nome_sala in self.sistema.salas_cirurgia.keys():
            print(f"{i} - {nome_sala}")
            i += 1
        
        try:
            escolha = int(input("\nEscolha a sala: "))
            
            contador = 1
            sala_selecionada = None

            for nome_sala in self.sistema.salas_cirurgia.keys():
                if contador == escolha:
                    sala_selecionada = self.sistema.salas_cirurgia[nome_sala]
                    break

                contador += 1
            
            if not sala_selecionada:
                print("Opção inválida!")
                return
            
            equipamento = input("\nNome do equipamento: ").strip()
            if not equipamento:
                print("Nome de equipamento inválido!")
                return
            
            sala_selecionada.adicionar_equipamento(equipamento)
            
        except ValueError:
            print("Valor inválido!")

    def ver_detalhes_sala_cirurgia(self):
        if not self.sistema.salas_cirurgia:
            print("\nNenhuma sala de cirurgia criada ainda!")
            return
        
        print("\nSalas de Cirurgia disponíveis:")
        
        i = 1
        for nome_sala in self.sistema.salas_cirurgia.keys():
            print(f"{i} - {nome_sala}")
            i += 1
        
        try:
            escolha = int(input("\nEscolha a sala: "))
            
            contador = 1
            sala_selecionada = None
            
            for nome_sala in self.sistema.salas_cirurgia.keys():
                if contador == escolha:
                    sala_selecionada = self.sistema.salas_cirurgia[nome_sala]
                    break

                contador += 1
            
            if not sala_selecionada:
                print("Opção inválida!")
                return
            
            detalhes = sala_selecionada.detalhar_sala()
            print(detalhes)
            
        except ValueError:
            print("Valor inválido!")

    def ver_horario_funcionario(self):
        funcionario = self.selecionar_funcionario("Horário de funcionário:")
        if not funcionario:
            return

        try:          
            mes_ano = self.obter_mes_ano()

            mes = mes_ano[0]
            ano = mes_ano[1]

            resumo = funcionario.obter_resumo_horas_mes(mes, ano)

            print(f"\nHorário do Funcionário {funcionario.nome} - {mes}/{ano}:")
            print(f"Dias trabalhados: {resumo['dias_trabalhados']}")
            print(f"Horas previstas: {formatar_timedelta(resumo['horas_previstas'])}")
            print(f"Horas reais: {formatar_timedelta(resumo['horas_reais'])}")
            print(f"Horas diurnas: {formatar_timedelta(resumo['horas_diurnas'])}")
            print(f"Horas noturnas: {formatar_timedelta(resumo['horas_noturnas'])}")
            print(f"Diferença: {formatar_timedelta(resumo['diferenca'])}")
            print(f"Atendimentos: {resumo['atendimentos']}")

        except ValueError:
            print("Valor inválido!")

    def ver_pagamento_funcionario(self):
        funcionario = self.selecionar_funcionario("Pagamento mensal de funcionário:")
        if not funcionario:
            return

        try:
            mes_ano = self.obter_mes_ano()
            mes = mes_ano[0]
            ano = mes_ano[1]

            pagamento = funcionario.calcular_pagamento(mes, ano)
            
            print(f"\nPagamento de {pagamento['funcionario'].upper()} - {pagamento['mes']}/{pagamento['ano']}")
            print(f"Cargo: {pagamento['cargo']}\n")
            print(f"Salário Base: {pagamento['salario_base']:.2f}€")
            print(f"Horas previstas: {pagamento['horas_previstas']:.1f}h")
            print(f"Horas reais: {pagamento['horas_reais']:.1f}h")
            print(f"Horas diurnas: {formatar_timedelta(pagamento['horas_diurnas'])}")
            print(f"Horas noturnas: {formatar_timedelta(pagamento['horas_noturnas'])}")
            print(f"Diferença: {pagamento['diferenca_horas']:+.1f}h")
            print(f"Total Atendimentos: {pagamento['total_atendimentos']}")
            print(f"Total a Pagar {pagamento['total_a_pagar']:.2f}€")

        except ValueError:
            print("Valor inválido!")

    def menu_recepcao(self):
        if not self.sistema.salas_espera:
            print("\nRealize a configuração inicial primeiro!")
            return

        opcoes = {
            "1": ("Registar novo paciente", self.registar_novo_paciente),
            "2": ("Ver pacientes registados", self.listar_pacientes),
            "3": ("Enviar paciente para área de atendimento", self.enviar_paciente_para_atendimento),
        }
        self.exibir_menu_generico("Recepção - gerenciar pacientes", opcoes)

    def registar_novo_paciente(self):
        print("\nRegistar novo paciente:")
        try:
            nome = input("Nome do paciente: ").strip()
            idade = int(input("Idade: "))

            if not nome or idade <= 0:
                print("Dados inválidos!")
                return

            paciente = self.sistema.registrar_paciente(nome, idade)
            print(f"\nPaciente registado com sucesso!")
            print(f"Nº Utente: {paciente.numero_utente}")
            print(f"Nome: {paciente.nome}")
            print(f"Idade: {paciente.idade}")

        except ValueError:
            print("Erro ao processar dados!")

    def listar_pacientes(self):
        print("\nPacientes registados:")
        if not self.sistema.pacientes:
            print("Nenhum paciente registado!")
            return

        print(f"Pacientes registrados({len(self.sistema.pacientes)}):\n")
        for numero_utente in self.sistema.pacientes.keys():
            paciente = self.sistema.pacientes[numero_utente]
            area_info = ""
            sala_info = ""

            if paciente.area_atendimento:
                area_info = f"\tÁrea: {paciente.area_atendimento}"

            if  paciente.sala_atendimento:
                sala_info = f"\tSala: {paciente.sala_atendimento}"

            print(f"{numero_utente:09d} \t{paciente.nome} \tIdade: {paciente.idade} \tStatus: {paciente.status.value}{area_info}{sala_info}")

    def enviar_paciente_para_atendimento(self):
        if not self.sistema.pacientes:
            print("Nenhum paciente registado!")
            return

        if not self.sistema.salas_espera:
            print("Nenhuma área de atendimento disponível!")
            return

        sala_espera = self.selecionar_area("Áreas de atendimento disponíveis:")
        if not sala_espera:
            return

        paciente = self.selecionar_paciente(
            "Pacientes disponiveis (sem salas):",
            filtro=lambda paciente: paciente.status == StatusAtendimento.SEM_SALA
        )

        if not paciente:
            return

        try:
            sala_espera.pegar_senha(paciente)
            

























            area_nome_encontrado = "Desconhecida"
            for nome_area in self.sistema.salas_espera.keys():
                sala = self.sistema.salas_espera[nome_area]
                if sala == sala_espera:
                    area_nome_encontrado = nome_area
                    break
            
            print(f"Paciente {paciente.nome} inserido na fila de {area_nome_encontrado}!")

        except ValueError:
            print("Erro ao processar dados!")

    def menu_areas(self):
        if not self.sistema.salas_espera:
            print("Nenhuma área de atendimento configurada!")
            return

        while True:
            print("\nÁreas de atendimento:")

            i = 1
            for area_nome in self.sistema.salas_espera.keys():
                print(f"{i} - {area_nome}")
                i += 1

            print("0. Voltar")

            try:
                opcao = int(input("Escolha uma área: "))

                if opcao == 0:
                    break

                contador = 1
                area_selecionada = None

                for area_nome in self.sistema.salas_espera.keys():
                    if contador == opcao:
                        area_selecionada = area_nome
                        break

                    contador += 1

                if not area_selecionada:
                    print("Opção inválida!")
                    continue

                self.gerenciar_area(area_selecionada)

            except ValueError:
                print("Valor inválido!")

    def gerenciar_area(self, area_nome: str):
        sala_espera = self.sistema.salas_espera[area_nome]

        def mostrar_painel_e_opcoes():
            sala_espera.mostrar_painel()
            return True
        
        mostrar_painel_e_opcoes()
        
        opcoes = {
            "1": ("Chamar próximo paciente", lambda: self.chamar_proximo_paciente(sala_espera)),
            "2": ("Finalizar atendimento", lambda: self.finalizar_atendimento(sala_espera)),
        }
        self.exibir_menu_generico("Opcoes", opcoes)

    def chamar_proximo_paciente(self, sala_espera: SalaEspera):
        if not self.sistema.funcionarios:
            print("Nenhum funcionário disponível!")
            return

        print("\nFuncionarios disponíveis:")
        i = 1
        for funcionario in self.sistema.funcionarios.values():
            print(f"{i} {funcionario.nome} - {funcionario.cargo.name}")
            i += 1

        try:
            escolha = int(input("Escolha um funcionário: "))

            contador = 1
            funcionario_selecionado = None
            for funcionario in self.sistema.funcionarios.values():
                if contador == escolha:
                    funcionario_selecionado = funcionario
                    break

                contador += 1

            if not funcionario_selecionado:
                print("Opção inválida!")
                return

            sala_espera.chamar_proximo(funcionario_selecionado)

        except ValueError:
            print("Valor inválido!")

    def finalizar_atendimento(self, sala_espera: SalaEspera):
        sala_com_atendimento = None
        
        for sala in sala_espera.salas_atendimento:
            if sala.status == StatusSala.OCUPADO and sala.paciente_atual:
                sala_com_atendimento = sala
                break

        if not sala_com_atendimento:
            print("Nenhuma sala em atendimento!")
            return

        descricao = input("Descrição do atendimento (ou Enter para padrão): ").strip()
        if not descricao:
            descricao = "Atendimento realizado com sucesso"

        sala_com_atendimento.finalizar_atendimento(descricao)

    def menu_relatorios(self):
        opcoes = {
            "1": ("Relatório de Funcionário", self.relatorio_funcionario),
            "2": ("Relatório de Paciente", self.relatorio_paciente),
            "3": ("Estatísticas do Hospital", self.estatisticas_hospital),
        }
        self.exibir_menu_generico("Relatórios", opcoes)

    def relatorio_funcionario(self):
        funcionario = self.selecionar_funcionario("Relatório de funcionário:")
        if not funcionario:
            return

        relatorio = self.sistema.gerar_relatorio_funcionario(funcionario.numero_funcionario)
        print(relatorio)

    def relatorio_paciente(self):
        paciente = self.selecionar_paciente("Relatório de paciente:")
        if not paciente:
            return

        relatorio = self.sistema.gerar_relatorio_paciente(paciente.numero_utente)
        print(relatorio)

    def estatisticas_hospital(self):
        print("\nEstatisticas do hospital:")

        print(f"\nPacientes registados: {len(self.sistema.pacientes)}")
        print(f"Funcionários: {len(self.sistema.funcionarios)}")
        print(f"Áreas de atendimento: {len(self.sistema.salas_espera)}")

        total_atendimentos = 0
        for funcionario in self.sistema.funcionarios.values():
            total_atendimentos += len(funcionario.obter_atendimentos())

        print(f"Total de atendimentos realizados: {total_atendimentos}")

        if self.sistema.pacientes:
            em_espera = 0
            em_atendimento = 0
            atendidos = 0
            sem_sala = 0
            for paciente in self.sistema.pacientes.values():
                if paciente.status == StatusAtendimento.ESPERA:
                    em_espera += 1
                elif paciente.status == StatusAtendimento.ATENDIMENTO:
                    em_atendimento += 1
                elif paciente.status == StatusAtendimento.ATENDIDO:
                    atendidos += 1
                elif paciente.status == StatusAtendimento.SEM_SALA:
                    sem_sala += 1

            print(f"\nStatus dos Pacientes:")
            print(f"Sem sala definida: {sem_sala}")
            print(f"Em espera: {em_espera}")
            print(f"Em atendimento: {em_atendimento}")
            print(f"Atendidos: {atendidos}")

    def menu_historico_medico(self):
        opcoes = {
            "1": ("Adicionar médico/funcionário ao sistema", self.adicionar_funcionario_historico),
            "2": ("Registrar atendimento médico", self.registrar_atendimento_historico),
            "3": ("Ver histórico de um paciente", self.ver_historico_paciente),
            "4": ("Ver pacientes atendidos por funcionário", self.ver_pacientes_funcionario),
            "5": ("Ver todos os históricos registrados", self.listar_todos_historicos),
        }
        self.exibir_menu_generico("Histórico médico", opcoes)

    def adicionar_funcionario_historico(self):
        print("\nAdicionar medico/funcionario ao historico:")

        if not self.sistema.funcionarios:
            print("Nenhum funcionário registrado no sistema!")
            return

        funcionario = self.selecionar_funcionario("Funcionários disponíveis:")
        if not funcionario:
            return

        if Paciente_historicos.adicionar_funcionario(funcionario):
            print(f"Funcionario {funcionario.nome} adicionado ao sistema de historico!")
        else:
            print("Erro ao adicionar funcionário!")

    def registrar_atendimento_historico(self):
        print("\nRegistrar atendimento medico:")

        if not Paciente_historicos.Funcionarios:
            print("Nenhum médico registrado no histórico!")
            return

        if not self.sistema.pacientes:
            print("Nenhum paciente registrado no sistema!")
            return

        print("\nMédicos/Funcionários disponíveis:")
        
        i = 1
        for numero_funcionario in Paciente_historicos.Funcionarios.keys():
            funcionario = Paciente_historicos.Funcionarios[numero_funcionario]
            print(f"{i} - {funcionario.nome} (#{numero_funcionario})")
            i += 1

        try:
            escolha_funcionario = int(input("\nEscolha o médico: "))
            
            contador = 1
            numero_funcionario_selecionado = None
            for numero_funcionario in Paciente_historicos.Funcionarios.keys():
                if contador == escolha_funcionario:
                    numero_funcionario_selecionado = numero_funcionario
                    break
                contador += 1
            
            if not numero_funcionario_selecionado:
                print("Opção inválida!")
                return

            paciente = self.selecionar_paciente()
            if not paciente:
                return

            # Adiciona o Paciente ao histórico se ainda não existe
            if paciente.numero_utente not in Paciente_historicos.Pacientes or Paciente_historicos.Pacientes[paciente.numero_utente] is None:
                Paciente_historicos.adicionar_paciente(paciente)

            id_historico = int(input("\nId do atendimento (número inteiro): "))
            descricao = input("Descrição do atendimento: ").strip()

            if Paciente_historicos.adicionar_historico(numero_funcionario_selecionado, paciente.numero_utente, id_historico, descricao):
                print("Atendimento registrado com sucesso!")
            else:
                print("Erro ao registrar atendimento (Id duplicado ou dados inválidos)!")
        
        except ValueError:
            print("Valor inválido!")
        
    def ver_historico_paciente(self):
        print("\nVer historico de paciente:")

        if not self.sistema.pacientes:
            print("Nenhum paciente registrado!")
            return

        paciente = self.selecionar_paciente()
        if not paciente:
            return

        try:
            historicos = Paciente_historicos.obter_historicos_paciente(paciente.numero_utente)
            
            if not historicos:
                print(f"\nNenhum historico registrado para {paciente.nome}!")
            else:
                print(f"\nHistorico de {paciente.nome} (#{paciente.numero_utente}):")
                
                for id_historico in historicos.keys():
                    descricao = historicos[id_historico]
                    print(f"\nId {id_historico}:")
                    print(f"{descricao}")

        except ValueError:
            print("Valor inválido!")

    def ver_pacientes_funcionario(self):
        print("\nVer pacientes atendidos por funcionario:")

        if not Paciente_historicos.Funcionarios:
            print("Nenhum funcionário no histórico!")
            return

        print("\nFuncionários com histórico:")
        
        i = 1
        for numero_funcionario in Paciente_historicos.Funcionarios.keys():
            funcionario = Paciente_historicos.Funcionarios[numero_funcionario]
            print(f"{i} - {funcionario.nome} (#{numero_funcionario})")
            i += 1

        try:
            escolha = int(input("\nEscolha o funcionário: "))
            
            contador = 1
            numero_funcionario_selecionado = None
            funcionario_selecionado = None
            
            for numero_funcionario in Paciente_historicos.Funcionarios.keys():
                if contador == escolha:
                    numero_funcionario_selecionado = numero_funcionario
                    funcionario_selecionado = Paciente_historicos.Funcionarios[numero_funcionario]
                    break

                contador += 1
            
            if not numero_funcionario_selecionado:
                print("Opção inválida!")
                return
            
            pacientes_numeros = Paciente_historicos.obter_pacientes_funcionario(numero_funcionario_selecionado)
            
            if not pacientes_numeros:
                print(f"\n{funcionario_selecionado.nome} nao atendeu nenhum paciente!")
            else:
                print(f"\nPacientes atendidos por {funcionario_selecionado.nome} (#{numero_funcionario_selecionado}):")
                
                for numero_utente in pacientes_numeros:
                    if numero_utente in Paciente_historicos.Pacientes:
                        paciente = Paciente_historicos.Pacientes[numero_utente]
                        historicos = Paciente_historicos.obter_historicos_funcionario_paciente(numero_funcionario_selecionado, numero_utente)
                        print(f"\n{paciente.nome} (#{numero_utente:09d})")
                        
                        for id_historico in historicos.keys():
                            descricao = historicos[id_historico]
                            print(f"Id {id_historico}: {descricao}")

        except ValueError:
            print("Valor inválido!")

    def listar_todos_historicos(self):
        print(Paciente_historicos.listar_todos_historicos())

    def menu_horarios(self):
        opcoes = {
            "1": ("Visualizar horário semanal de um funcionário", self.ver_horario_semanal),
            "2": ("Visualizar horário mensal de um funcionário", self.ver_horario_mensal_detalhado),
            "3": ("Editar horário semanal de um funcionário", self.editar_horario_semanal),
            "4": ("Definir horário específico para um dia", self.definir_horario_especifico),
            "5": ("Ver registos de ponto de um funcionário", self.ver_registos_ponto),
        }
        self.exibir_menu_generico("Gestão de Horários", opcoes)

    def ver_horario_semanal(self):
        func = self.selecionar_funcionario()
        if not func:
            return

        print(f"\nHorário Semanal de {func.nome}:")
        
        totais = func.horario_semanal.calcular_totais_semanais()
        
        for dia in Dias_Semana:
            if dia in func.horario_semanal.horarios:
                horario = func.horario_semanal.horarios[dia]
                print(f"\n{dia.name}: {HoraMinuto(horario.intervalo.inicio.seconds // 3600, (horario.intervalo.inicio.seconds % 3600) // 60)} - {HoraMinuto(horario.intervalo.fim.seconds // 3600, (horario.intervalo.fim.seconds % 3600) // 60)}")
                
                if horario.pausas.pausas:
                    print(f"Pausas:")
                    for pausa in horario.pausas.pausas:
                        pausa_inicio = HoraMinuto(pausa.inicio.seconds // 3600, (pausa.inicio.seconds % 3600) // 60)
                        pausa_fim = HoraMinuto(pausa.fim.seconds // 3600, (pausa.fim.seconds % 3600) // 60)
                        print(f"- {pausa_inicio} - {pausa_fim}")
                
                print(f"Tempo trabalhado: {formatar_timedelta(horario.tempo_trabalhado())}")
                print(f"Tempo diurno: {formatar_timedelta(horario.calcular_tempo_diurno())}")
                print(f"Tempo noturno: {formatar_timedelta(horario.calcular_tempo_noturno())}")
            else:
                print(f"\n{dia.name}: Folga")
        
        print(f"\n\nTotais Semanais:")
        print(f"Tempo trabalhado: {formatar_timedelta(totais['trabalhado'])}")
        print(f"Tempo diurno: {formatar_timedelta(totais['diurno'])}")
        print(f"Tempo noturno: {formatar_timedelta(totais['noturno'])}\n")

    def ver_horario_mensal_detalhado(self):
        funcionario = self.selecionar_funcionario()
        if not funcionario:
            return

        try:
            mes, ano = self.obter_mes_ano()
            
            horario_mensal = funcionario.horario_funcionario.obter_horario_mensal(mes, ano)
            detalhes_diarios = horario_mensal.obter_detalhes_Diarios()
            
            print(f"\nHorário Mensal de {funcionario.nome} - {mes:02d}/{ano}")
            print(f"Data / Dia / Valor / Saída / Pausas / Trabalhado / Diurno / Noturno")
            
            for detalhe in detalhes_diarios:
                data_str = detalhe['data'].strftime("%d/%m/%Y")
                dia_semana = detalhe['dia_semana']
                
                if detalhe['trabalhado'] == timedelta(0):
                    print(f"{data_str} / {dia_semana} / Folga")
                else:
                    # O símbolo // faz o mesmo do que / mas retorna inteiros
                    Valor = HoraMinuto(detalhe['Valor'].seconds // 3600, (detalhe['Valor'].seconds % 3600) // 60)
                    saida = HoraMinuto(detalhe['saida'].seconds // 3600, (detalhe['saida'].seconds % 3600) // 60)
                    
                    pausas_str = ""
                    if detalhe['pausas']:
                        pausas_list = []
                        for pausa in detalhe['pausas']:
                            p_inicio = HoraMinuto(pausa.inicio.seconds // 3600, (pausa.inicio.seconds % 3600) // 60)
                            p_fim = HoraMinuto(pausa.fim.seconds // 3600, (pausa.fim.seconds % 3600) // 60)
                            pausas_list.append(f"{p_inicio}-{p_fim}")
                        pausas_str = ", ".join(pausas_list)
                    else:
                        pausas_str = "Sem pausas"
                    
                    trabalhado_str = formatar_timedelta(detalhe['trabalhado'])
                    diurno_str = formatar_timedelta(detalhe['diurno'])
                    noturno_str = formatar_timedelta(detalhe['noturno'])

                    print(f"{data_str} / {dia_semana} / {str(Valor)} / {str(saida)} / {pausas_str} / {trabalhado_str} / {diurno_str} / {noturno_str}")

            detalhes_mensais = horario_mensal.obter_detalhes_Mensais()
            print(f"Totais {formatar_timedelta(detalhes_mensais['trabalhado'])} {formatar_timedelta(detalhes_mensais['diurno'])} {formatar_timedelta(detalhes_mensais['noturno'])}\n")

        except (ValueError, IndexError):
            print("Valor inválido!")
        
    def editar_horario_semanal(self):
        funcionario = self.selecionar_funcionario()
        if not funcionario:
            return

        try:
            print("\nDias da semana:")
            i = 0
            for dia in Dias_Semana:
                print(f"{i} - {dia.name}")
                i += 1
            
            dia_escolha = int(input("\nEscolha o dia da semana: "))
            if not (0 <= dia_escolha <= 6):
                print("Opção inválida!")
                return
            
            contador = 0
            dia_semana_selecionado = None
            for dia in Dias_Semana:
                if contador == dia_escolha:
                    dia_semana_selecionado = dia
                    break

                contador += 1
            
            if not dia_semana_selecionado:
                print("Opção inválida!")
                return
            
            print(f"\nConfigurar horário para {dia_semana_selecionado.name}:")
            print("(Deixe em branco para marcar como folga)")
            
            inicio_str = input("Hora de início (HH:MM): ").strip()
            
            if not inicio_str:
                if dia_semana_selecionado in funcionario.horario_semanal.horarios:
                    funcionario.horario_semanal.horarios[dia_semana_selecionado] = Horario(intervalo=IntervaloTempo(timedelta(0),timedelta(0)))
                print(f"{dia_semana_selecionado.name} marcado como folga!")
                return
            
            fim_str = input("Hora de fim (HH:MM): ").strip()

            horario = Horario(
                IntervaloTempo.init_com_HoraMinuto(
                    HoraMinuto.init_com_str(inicio_str),
                    HoraMinuto.init_com_str(fim_str)
                )
            )
            
            print("\nDeseja adicionar pausas? (s/n)")
            if input().strip().lower() == 's':
                while True:
                    print("\nAdicionar pausa (deixe em branco para terminar):")
                    pausa_inicio_str = input("Hora de início da pausa (HH:MM): ").strip()
                    
                    if not pausa_inicio_str:
                        break
                    
                    pausa_fim_str = input("Hora de fim da pausa (HH:MM): ").strip()
                    
                    pausa = IntervaloTempo.init_com_HoraMinuto(
                        HoraMinuto.init_com_str(pausa_inicio_str),
                        HoraMinuto.init_com_str(pausa_fim_str)
                    )
                    
                    if horario.pausas.adicionar_pausa(pausa):
                        print("Pausa adicionada com sucesso!")
                    else:
                        print("Erro ao adicionar pausa (fora do horário de trabalho ou limite excedido)")
            
            funcionario.horario_semanal.adicionar_horario(dia_semana_selecionado, horario)
            funcionario.horario_funcionario = FuncionarioHorario(funcionario.horario_semanal)

            print(f"\nHorário de {dia_semana_selecionado.name} atualizado com sucesso!")

        except (ValueError, IndexError):
            print(f"Valor inválido!")
        
    def definir_horario_especifico(self):
        funcionario = self.selecionar_funcionario()
        if not funcionario:
            return

        try:
            print("\nDefina a data para o horário específico:")
            dia = int(input("Dia: "))
            mes = int(input("Mês: "))
            ano = int(input("Ano: "))
            
            data_especifica = date(ano, mes, dia)
            
            print(f"\nConfigurar horário para {data_especifica.strftime('%d/%m/%Y')}:")
            print("(Deixe em branco para marcar como folga)")
            
            inicio_str = input("Hora de início (HH:MM): ").strip()
            fim_str = input("Hora de fim (HH:MM): ").strip()
            
            horario = Horario(
                IntervaloTempo.init_com_HoraMinuto(
                    HoraMinuto.init_com_str(inicio_str),
                    HoraMinuto.init_com_str(fim_str)
                )
            )
            
            print("\nDeseja adicionar pausas? (s/n)")
            if input().strip().lower() == 's':
                while True:
                    print("\nAdicionar pausa (deixe em branco para terminar):")

                    pausa_inicio_str = input("Hora de início da pausa (HH:MM): ").strip()                    
                    pausa_fim_str = input("Hora de fim da pausa (HH:MM): ").strip()
                    
                    pausa = IntervaloTempo.init_com_HoraMinuto(
                        HoraMinuto.init_com_str(pausa_inicio_str),
                        HoraMinuto.init_com_str(pausa_fim_str)
                    )
                    
                    if horario.pausas.adicionar_pausa(pausa):
                        print("Pausa adicionada com sucesso!")
                    else:
                        print("Erro ao adicionar pausa")
        
            funcionario.definir_horario_especifico(data_especifica, horario)
            print(f"\nHorário específico para {data_especifica.strftime('%d/%m/%Y')} definido com sucesso!")

        except (ValueError, IndexError):
            print(f"Valor inválido!")
        
    def registar_ponto(self):
        funcionario = self.selecionar_funcionario()
        if not funcionario:
            return

        try:
            print(f"\nRegistar ponto para {funcionario.nome}")
            print("Data (deixe em branco para hoje):")
            dia_input = input("Dia: ").strip()
            
            if dia_input:
                mes = int(input("Mês: "))
                ano = int(input("Ano: "))
                data_ponto = date(int(dia_input), mes, ano)
            else:
                data_ponto = date.today()
            
            print(f"\nData: {data_ponto.strftime('%d/%m/%Y')}")
            
            inicio_real = input("Hora de Valor (HH:MM): ").strip()
            fim_real = input("Hora de saída (HH:MM): ").strip()
            
            pausas_reais = []
            print("\nDeseja registar pausas? (s/n)")
            if input().strip().lower() == 's':
                while True:
                    print("\nAdicionar pausa (deixe em branco para terminar):")
                    pausa_inicio_str = input("Hora de início da pausa (HH:MM): ").strip()
                    
                    if not pausa_inicio_str:
                        break
                    
                    pausa_fim_str = input("Hora de fim da pausa (HH:MM): ").strip()
                    
                    pausa = IntervaloTempo.init_com_HoraMinuto(
                        HoraMinuto.init_com_str(pausa_inicio_str),
                        HoraMinuto.init_com_str(pausa_fim_str)
                    )
                    pausas_reais.append(pausa)
                    print("Pausa adicionada!")
            
            funcionario.registrar_ponto(data_ponto, inicio_real, fim_real, pausas_reais)
            print(f"\nPonto registado com sucesso para {data_ponto.strftime('%d/%m/%Y')}!")
            
            diferencas = funcionario.calcular_diferenca_diaria(data_ponto)
            if diferencas:
                print(f"\nResumo do dia:")
                print(f"Previsto: {formatar_timedelta(diferencas['tempo_trabalhado_previsto'])}")
                print(f"Real: {formatar_timedelta(diferencas['tempo_trabalhado_real'])}")
                print(f"Atraso: {formatar_timedelta(diferencas['atraso'])}")
                print(f"Diferença: {formatar_timedelta(diferencas['tempo_extra'])}")

        except (ValueError, IndexError):
            print(f"Valor inválido!")

    def ver_registos_ponto(self):
        funcionario = self.selecionar_funcionario()
        if not funcionario:
            return

        try:
            mes_ano = self.obter_mes_ano()
            mes = mes_ano[0]
            ano = mes_ano[1]
            registros = funcionario.listar_registros_ponto_mes(mes, ano)
            
            if not registros:
                print(f"\nNenhum registro de ponto para {mes}/{ano}")
            else:
                print(f"\nRegistos de Ponto de {funcionario.nome} - {mes:02d}/{ano:04d}:")
                print(f"Data / Dia / Previsto / Real / Atraso / Diferença")
                
                for registro in registros:
                    print(f"{registro['data'].strftime('%d/%m/%Y')} / {registro['dia_semana']} / {registro['trabalhado_previsto']} / {registro['trabalhado_real']} / {registro['atraso']} / {registro['extra_falta']}")

        except (ValueError, IndexError):
            print(f"Valor inválido!")

if __name__ == "__main__":
    print("\nBem-vindo ao Sistema Hospitalar!")    
    interface = InterfaceHospital()
    interface.inicializar_dados_padrao()