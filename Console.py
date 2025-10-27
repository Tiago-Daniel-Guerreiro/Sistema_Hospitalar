from datetime import datetime, timedelta, date
import os
from Program import (
    SistemaHospital, Funcionario, Medico, Enfermeiro, Paciente,
    Cargo, StatusSala, StatusAtendimento, SalaEspera, SistemaHospital,
    Administrativo, EnfermeiroChefe, SalaCirurgia
)
from Horario import (
    Dias_Semana, HoraMinuto, IntervaloTempo, Horario, Horario_Semanal,
    formatar_timedelta, FuncionarioHorario
)

def aguardar_e_limpar():
    input("\nPressione Enter para continuar...")
    limpar_console()

def limpar_console():
    os.system('cls')

def linhas_vazias():
    print("\n" * 100)

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
    print("Para cada dia da semana, defina o horário de trabalho.")
    print("Deixe o horário de início em branco para marcar o dia como folga.\n")

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
            
            adicionar_pausas = input(f"\nDeseja adicionar pausas para {dia.name}? (s/n): ").strip().lower()
            
            if adicionar_pausas == 's':
                contador_pausas = 0
                while contador_pausas < 24:  # Máximo de 24 pausas por dia
                    print(f"\nPausa {contador_pausas + 1} (deixe em branco para terminar):")
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
                    
                    if horario._pausas.adicionar_pausa(pausa):
                        print(f"Pausa {pausa_inicio_str} - {pausa_fim_str} adicionada!")
                        contador_pausas += 1
                    else:
                        print("Erro: Pausa fora do horário de trabalho ou limite excedido")
                        break
            
            horario_semanal.adicionar_horario(dia, horario)
            
            tempo_trabalhado = horario.tempo_trabalhado()
            print(f"\n{dia.name} configurado: {inicio_str} - {fim_str}")
            print(f"Tempo de trabalho: {formatar_timedelta(tempo_trabalhado)}")
            
        except Exception as ex:
            print(f"Erro ao configurar - {ex} - {dia.name} marcado como folga.")

    print("\nResumo do horário semanal:")

    totais = horario_semanal.calcular_totais_semanais()
    dias_trabalho = len(horario_semanal.horarios)
    
    print(f"Dias de trabalho: {dias_trabalho}")
    print(f"Tempo total semanal: {formatar_timedelta(totais['trabalhado'])}")
    print(f"- Tempo diurno: {formatar_timedelta(totais['diurno'])}")
    print(f"- Tempo noturno: {formatar_timedelta(totais['noturno'])}")
    
    return horario_semanal

class InterfaceHospital:
    @staticmethod
    def selecionar_funcionario(mensagem: str = "Funcionários:"):
        if not SistemaHospital.funcionarios:
            print("\nNenhum funcionário registado!")
            return None

        print(f"\n{mensagem}")
        
        i = 1
        for funcionario in SistemaHospital.funcionarios.values():
            print(f"{i} - {funcionario.nome}")
            i += 1

        try:
            escolha = int(input("\nEscolha o funcionário: "))
            
            contador = 1
            for funcionario in SistemaHospital.funcionarios.values():
                if contador == escolha:
                    return funcionario
                contador += 1
            
            print("Opção inválida!")
        
        except ValueError:
            print("Valor inválido!")
        return None
    
    @staticmethod
    def selecionar_paciente(mensagem: str = "Pacientes:", filtro=None): 
        if not SistemaHospital.pacientes:
            print("\nNenhum paciente registado!")
            return None

        pacientes_filtrados = []
        
        if filtro:
            for paciente in SistemaHospital.pacientes.values():
                if filtro(paciente): # Exemplo de filtro: lambda paciente: paciente.idade > 18
                    pacientes_filtrados.append(paciente)
        else:
            for paciente in SistemaHospital.pacientes.values():
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
    
    @staticmethod
    def obter_mes_ano():
        mes_input = input("Mês (1-12, vazio=atual): ").strip()
        ano_input = input("Ano (vazio=atual): ").strip()

        mes = datetime.now().month
        ano = datetime.now().year
        
        if mes_input:
            mes = int(mes_input)

        if ano_input:
            ano = int(ano_input)

        return mes, ano

    
    @staticmethod
    def selecionar_area( mensagem: str = "Áreas de atendimento:"):
        if not SistemaHospital.salas_espera:
            print("\nNenhuma área de atendimento registada!")
            return None

        print(f"\n{mensagem}")
        
        i = 1
        for nome_area in SistemaHospital.salas_espera.keys():
            print(f"{i} - {nome_area}")
            i += 1

        try:
            escolha = int(input("\nEscolha a área: "))
            
            contador = 1
            for nome_area in SistemaHospital.salas_espera.keys():
                if contador == escolha:
                    return SistemaHospital.salas_espera[nome_area]
                
                contador += 1
            
            print("Opção inválida!")

        except ValueError:
            print("Valor inválido!")

        return None
    
    @staticmethod
    def exibir_menu_generico(titulo: str, opcoes: dict, sair_texto: str = "Voltar"):
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
    
    @staticmethod
    def inicializar_dados():
        print("\nSistema hospitalar - inicialização:")

        resposta = input("Deseja inicializar os dados padrão? (s/n, padrão: n): ").strip().lower()

        if resposta == 's':
            print("\nCarregando dados padrão...")
            InterfaceHospital.configuracao_padrao()
            print("Dados padrão carregados com sucesso!")
        else:
            print("\nSistema inicializado sem dados definidos.")

        InterfaceHospital.menu_principal()

    @staticmethod
    def menu_principal():
        opcoes = {
            "1": ("Funcionários", InterfaceHospital.menu_funcionarios),
            "2": ("Recepção (Registrar/Encaminhar Pacientes)", InterfaceHospital.menu_recepcao),
            "3": ("Áreas de Atendimento", InterfaceHospital.menu_areas),
            "4": ("Salas", InterfaceHospital.menu_salas),
            "5": ("Salas de Cirurgia", InterfaceHospital.menu_salas_cirurgia),
            "6": ("Pacientes", InterfaceHospital.menu_pacientes),
            "7": ("Histórico Médico", InterfaceHospital.menu_historico_medico),
        }
        InterfaceHospital.exibir_menu_generico("Sistema hospitalar - Menu principal", opcoes, sair_texto="Sair")

    @staticmethod
    def configuracao_padrao():
        SistemaHospital.criar_area_especializada("Cardiologia", 3, "C")
        SistemaHospital.criar_area_especializada("Cirurgia Geral", 3, "CG")
        SistemaHospital.criar_area_especializada("Medicina Interna", 3, "MI")
        SistemaHospital.criar_area_especializada("Psiquiatria", 2, "PS")
        SistemaHospital.criar_area_especializada("Medicina Geral", 2, "MG")

        horario_base = criar_horario_padrao() # Cria o horário base padrão (09:00 - 18:00, Segunda a Sexta)

        SistemaHospital.registrar_funcionario(Medico(nome="Doutor João Silva", idade=45, salario=3000, numero_funcionario=1001, especialidade=Cargo.Saude.Medico.Cardiologia, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Medico(nome="Doutora Maria Santos", idade=38, salario=2900, numero_funcionario=1002, especialidade=Cargo.Saude.Medico.CirurgiaGeral, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Medico(nome="Doutor Pedro Costa", idade=50, salario=3100, numero_funcionario=1003, especialidade=Cargo.Saude.Medico.MedicinaInterna, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Medico(nome="Doutora Sofia Ferreira", idade=41, salario=3200, numero_funcionario=1004, especialidade=Cargo.Saude.Medico.Psiquiatria, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Medico(nome="Doutor Rui Lopes", idade=36, salario=2800, numero_funcionario=1005, especialidade=Cargo.Saude.Medico.Geral, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Medico(nome="Doutora Carla Mendes", idade=43, salario=3050, numero_funcionario=1006, especialidade=Cargo.Saude.Medico.Cardiologia, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Medico(nome="Doutor André Almeida", idade=39, salario=2950, numero_funcionario=1007, especialidade=Cargo.Saude.Medico.CirurgiaGeral, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Medico(nome="Doutora Rita Sousa", idade=34, salario=2750, numero_funcionario=1008, especialidade=Cargo.Saude.Medico.MedicinaInterna, horario_semanal=horario_base))

        SistemaHospital.registrar_funcionario(Enfermeiro(nome="Enfermeiro Ana Oliveira", idade=32, salario=1800, numero_funcionario=2001, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Enfermeiro(nome="Enfermeiro Carlos Dias", idade=35, salario=1900, numero_funcionario=2002, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Enfermeiro(nome="Enfermeiro Paula Rodrigues", idade=29, salario=1750, numero_funcionario=2003, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Enfermeiro(nome="Enfermeiro Miguel Tavares", idade=31, salario=1850, numero_funcionario=2004, horario_semanal=horario_base))

        SistemaHospital.registrar_funcionario(Enfermeiro(nome="Enfermeiro Beatriz Martins", idade=27, salario=1700, numero_funcionario=2005, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Enfermeiro(nome="Enfermeiro Gonçalo Pires", idade=33, salario=1950, numero_funcionario=2006, horario_semanal=horario_base))

        SistemaHospital.registrar_funcionario(EnfermeiroChefe(nome="Enfermeiro Chefe Teresa Silva", idade=42, salario=2500, numero_funcionario=2100, setor="UTI", bonus_percentual_chefia=15.0, horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(EnfermeiroChefe(nome="Enfermeiro Chefe Manuel Costa", idade=48, salario=2600, numero_funcionario=2101, setor="Urgências", bonus_percentual_chefia=18.0, horario_semanal=horario_base))

        SistemaHospital.registrar_funcionario(Administrativo(nome="Adminstrador Isabel Cunha",idade=40,salario=1500,numero_funcionario=3001,setor="Recursos Humanos",horas_registradas=40.0,horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Administrativo(nome="Adminstrador Francisco Gomes",idade=37,salario=1600,numero_funcionario=3002,setor="Contabilidade",horas_registradas=40.0,horario_semanal=horario_base))
        SistemaHospital.registrar_funcionario(Administrativo(nome="Adminstrador Luísa Pereira",idade=35,salario=1550,numero_funcionario=3003,setor="Receção",horas_registradas=35.0,horario_semanal=horario_base))

        sala_cirurgia1 = SistemaHospital.criar_sala_cirurgia("Centro Cirúrgico 1", 10)
        sala_cirurgia1.adicionar_equipamento("Bisturi Elétrico")
        sala_cirurgia1.adicionar_equipamento("Mesa Cirúrgica")
        sala_cirurgia1.adicionar_equipamento("Monitor de Sinais Vitais")
        sala_cirurgia1.adicionar_equipamento("Desfibrilador")
        sala_cirurgia1.adicionar_equipamento("Anestesia")
        sala_cirurgia1.adicionar_equipamento("Aspirador Cirúrgico")

        sala_cirurgia2 = SistemaHospital.criar_sala_cirurgia("Centro Cirúrgico 2", 12)
        sala_cirurgia2.adicionar_equipamento("Bisturi Elétrico")
        sala_cirurgia2.adicionar_equipamento("Mesa Cirúrgica")
        sala_cirurgia2.adicionar_equipamento("Monitor de Sinais Vitais")
        sala_cirurgia2.adicionar_equipamento("Desfibrilador")
        sala_cirurgia2.adicionar_equipamento("Raio-X Portátil")
        sala_cirurgia2.adicionar_equipamento("Sistema de Vídeo Cirúrgico")

        sala_cirurgia3 = SistemaHospital.criar_sala_cirurgia("Centro Cirúrgico 3", 8)
        sala_cirurgia3.adicionar_equipamento("Bisturi Elétrico")
        sala_cirurgia3.adicionar_equipamento("Mesa Cirúrgica")
        sala_cirurgia3.adicionar_equipamento("Monitor de Sinais Vitais")
        sala_cirurgia3.adicionar_equipamento("Desfibrilador")

        SistemaHospital.registrar_paciente("Manuel Oliveira", 65)
        SistemaHospital.registrar_paciente("Ana Paula Silva", 42)
        SistemaHospital.registrar_paciente("José Carlos Santos", 58)
        SistemaHospital.registrar_paciente("Maria João Costa", 33)
        SistemaHospital.registrar_paciente("António Ferreira", 71)
        SistemaHospital.registrar_paciente("Helena Lopes", 28)
        SistemaHospital.registrar_paciente("Ricardo Mendes", 45)
        SistemaHospital.registrar_paciente("Inês Almeida", 19)
        SistemaHospital.registrar_paciente("Fernando Sousa", 53)
        SistemaHospital.registrar_paciente("Cristina Rodrigues", 61)
        SistemaHospital.registrar_paciente("Paulo Tavares", 38)
        SistemaHospital.registrar_paciente("Sandra Martins", 47)
        SistemaHospital.registrar_paciente("Vasco Pires", 25)
        SistemaHospital.registrar_paciente("Mariana Cunha", 31)
        SistemaHospital.registrar_paciente("Jorge Gomes", 69)
        SistemaHospital.registrar_paciente("Patrícia Pereira", 36)
        SistemaHospital.registrar_paciente("Tiago Ribeiro", 22)
        SistemaHospital.registrar_paciente("Mónica Carvalho", 54)
        SistemaHospital.registrar_paciente("Daniel Nunes", 40)
        SistemaHospital.registrar_paciente("Vera Correia", 29)
    
    @staticmethod
    def menu_funcionarios():
        opcoes = {
            "1": ("Listar funcionários", InterfaceHospital.listar_funcionarios),
            "2": ("Registar novo funcionário", InterfaceHospital.registar_funcionario_customizado),
            "3": ("Ver histórico de atendimentos de um funcionário", InterfaceHospital.relatorio_funcionario),
            "4": ("Ver horário e horas de um funcionário", InterfaceHospital.ver_horario_funcionario),
            "5": ("Ver pagamento mensal de um funcionário", InterfaceHospital.ver_pagamento_funcionario),
            "6": ("Gerir horários de funcionário", InterfaceHospital.menu_horarios),
            "7": ("Registar ponto", InterfaceHospital.registar_ponto),
        }
        InterfaceHospital.exibir_menu_generico("Funcionários", opcoes)
    
    @staticmethod
    def menu_salas():
        opcoes = {
            "1": ("Listar salas", InterfaceHospital.listar_areas),
            "2": ("Criar nova área (com salas)", InterfaceHospital.criar_area_customizada),
            "3": ("Ver status das salas", InterfaceHospital.listar_status_salas),
            "4": ("Gerenciar funcionário da sala", InterfaceHospital.gerenciar_funcionario_sala),
        }
        InterfaceHospital.exibir_menu_generico("Salas", opcoes)
    
    @staticmethod
    def gerenciar_funcionario_sala():
        sala = InterfaceHospital.obter_Sala_por_Area(InterfaceHospital.obter_Id_Area())

        if sala is None:
            print("Sala não encontrada!")
            return

        opcoes = {
            "1": ("Adicionar funcionário à sala", lambda: InterfaceHospital.adicionar_Funcionario_Sala(sala)),
            "2": ("Remover funcionário da sala", lambda: InterfaceHospital.remover_Funcionario_Sala(sala)),
            "3": ("Definir responsável da sala", lambda: InterfaceHospital.definir_Funcionario_Sala(sala)),
            "4": ("Listar funcionários da sala", lambda: InterfaceHospital.listar_Funcionarios_Sala(sala)),
        }

        InterfaceHospital.exibir_menu_generico(f"Gerenciar Funcionário da Sala: {sala.nome}", opcoes, sair_texto="Voltar")

    @staticmethod
    def obter_Id_Area() -> int:
        if not SistemaHospital.salas_espera:
            print("Nenhuma área criada!")
            return
        
        print("Áreas disponíveis:")
        areas = list(SistemaHospital.salas_espera.keys())

        i = 1
        for nome in areas:
            print(f"{i} - {nome}")
            i += 1

        try:
            id_Area = int(input("Escolha a área: ")) - 1
            if id_Area < 0 or id_Area >= len(areas):
                print("Opção inválida!")
                return
            
        except ValueError:
            print("Valor inválido!")
            return
        
        return id_Area

    @staticmethod
    def obter_Sala_por_Area(id_area: int) -> SalaEspera:
        if id_area is None:
            return
        
        areas = list(SistemaHospital.salas_espera.keys())
        sala_espera = SistemaHospital.salas_espera[areas[id_area]]

        if not sala_espera.salas_atendimento:
            print("Nenhuma sala de atendimento nesta área!")
            return

        print("Salas de atendimento:")
        i = 1
        for sala in sala_espera.salas_atendimento:
            print(f"{i} - {sala.nome}")
            i += 1

        try:
            id_sala = int(input("Escolha a sala: ")) - 1
            if id_sala < 0 or id_sala >= len(sala_espera.salas_atendimento):
                print("Opção inválida!")
                return
            
        except ValueError:
            print("Valor inválido!")
            return

        return sala_espera.salas_atendimento[id_sala]

    @staticmethod
    def adicionar_Funcionario_Sala(sala):
        funcionario = InterfaceHospital.selecionar_funcionario()
        if funcionario:
            sala.adicionar_funcionario(funcionario)

    @staticmethod
    def remover_Funcionario_Sala(sala):
        funcionario = InterfaceHospital.selecionar_funcionario()
        if funcionario:
            sala.remover_funcionario(funcionario)

    @staticmethod
    def definir_Funcionario_Sala(sala):
        funcionario = InterfaceHospital.selecionar_funcionario()
        if funcionario:
            sala.definir_funcionario_atual(funcionario)

    @staticmethod
    def listar_Funcionarios_Sala(sala):
        print("Funcionários na sala:")
        for funcionario in sala.funcionarios:
            print(f"- {funcionario.nome} ({funcionario.cargo.value})")
        if sala.funcionario_atual:
            print(f"Responsável atual: {sala.funcionario_atual.nome}")

    
    @staticmethod
    def menu_salas_cirurgia():
        opcoes = {
            "1": ("Criar sala de cirurgia", InterfaceHospital.criar_sala_cirurgia),
            "2": ("Listar salas de cirurgia", InterfaceHospital.listar_salas_cirurgia),
            "3": ("Adicionar equipamento a sala", InterfaceHospital.adicionar_equipamento_sala),
            "4": ("Ver detalhes de sala", InterfaceHospital.ver_detalhes_sala_cirurgia),
        }
        InterfaceHospital.exibir_menu_generico("Salas de Cirurgia", opcoes)

    @staticmethod
    def menu_pacientes():
        opcoes = {
            "1": ("Registar novo paciente", InterfaceHospital.registar_novo_paciente),
            "2": ("Ver todos os pacientes", InterfaceHospital.listar_pacientes_completo),
            "3": ("Ver histórico de um paciente", InterfaceHospital.relatorio_paciente),
            "4": ("Estatísticas do hospital", InterfaceHospital.estatisticas_hospital),
        }
        InterfaceHospital.exibir_menu_generico("Pacientes", opcoes)

    @staticmethod
    def criar_area_customizada():
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
        
        SistemaHospital.criar_area_especializada(nome, num_salas, sigla)
        print(f"A área {nome} criada com sucesso!")

    @staticmethod
    def registar_funcionario_customizado():
        print("\nRegistar novo funcionário:")
        
        nome = input("Nome do funcionário: ").strip()
        if not nome:
            print("Nome inválido!")
            return
        
        try:
            idade = int(input("Idade: ").strip())
            salario = float(input("Salário (Base): ").strip())
            num_funcionario = int(input("Número do funcionário: ").strip())
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

        cargos_disponiveis.append("Enfermeiro Chefe") # Cargo adicionado manualmente para Enfermeiro Chefe

        print("\nCargos disponíveis:")

        i = 1
        for cargo in cargos_disponiveis:
            if(isinstance(cargo, str)):
                print(f"{i} - {cargo}")
            else:
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
        elif cargo == "Enfermeiro Chefe":
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
        
        SistemaHospital.registrar_funcionario(funcionario)
        print(f"Funcionário {nome} registado com sucesso!")

    
    @staticmethod
    def listar_areas():
        print("\nÁreas especializadas:")
        
        if not SistemaHospital.salas_espera:
            print("Nenhuma área criada ainda.")
            return
        
        for area_nome in SistemaHospital.salas_espera.keys():
            sala_espera = SistemaHospital.salas_espera[area_nome]
            print(f"\n{area_nome}")
            print(f"Salas: {len(sala_espera.salas_atendimento)}")
            print(f"Pacientes em espera: {len(sala_espera.fila_espera)}")
    
    @staticmethod
    def listar_funcionarios():
        print("\nFuncionários registados:")
        
        if not SistemaHospital.funcionarios:
            print("Nenhum funcionário registado ainda.")
            return
        
        i = 1
        for numero_funcionario in SistemaHospital.funcionarios.keys():
            funcionario = SistemaHospital.funcionarios[numero_funcionario]
            print(f"\n{i} - {str(funcionario)}")

            i += 1
    
    @staticmethod
    def listar_pacientes_completo():
        InterfaceHospital.listar_pacientes()

    @staticmethod
    def registar_novo_paciente():
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
        
        paciente = SistemaHospital.registrar_paciente(nome, idade)
        print(f"\nPaciente registado com sucesso!")
        print(f"Nome: {paciente.nome}")
        print(f"Número de utente: {paciente.numero_utente}")
        print(f"Idade: {paciente.idade}")
    
    @staticmethod
    def listar_status_salas():
        print("Status das salas:")
        
        if not SistemaHospital.salas_espera:
            print("Nenhuma área de atendimento criada ainda.")
            return
        
        for area_nome in SistemaHospital.salas_espera.keys():
            sala_espera = SistemaHospital.salas_espera[area_nome]
            print(f"\n{area_nome}")
            print(f"Salas de atendimento: {len(sala_espera.salas_atendimento)}")
            print(f"Pacientes em espera: {len(sala_espera.fila_espera)}")

            i_sala = 1
            for sala in sala_espera.salas_atendimento:
                if sala.status == StatusSala.Disponivel: 
                    status = "Disponível"
                else:
                    status = "Ocupada"

                paciente_info = ""
                if sala.paciente_atual:
                    paciente_info = f"(com {sala.paciente_atual.nome})"

                print(f"- Sala {i_sala}: {status}{paciente_info}")
                i_sala += 1
    
    @staticmethod
    def criar_sala_cirurgia():
        print("\nCriar nova sala de cirurgia:")

        nome = input("Nome da sala (ex: Centro Cirúrgico 1): ").strip()
        if not nome:
            print("Nome inválido!")
            return

        if nome in SistemaHospital.salas_cirurgia:
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
        
        sala = SistemaHospital.criar_sala_cirurgia(nome, capacidade)
        print(f"\nSala de cirurgia {nome} criada com sucesso!")
        print(f"Id: {sala.id_sala}")
        print(f"Capacidade: {sala.capacidade} pessoas")
        
    @staticmethod
    def listar_salas_cirurgia():
        print("\nSalas de Cirurgia:")
        
        if not SistemaHospital.salas_cirurgia:
            print("Nenhuma sala de cirurgia criada ainda.")
            return
        
        for nome in SistemaHospital.salas_cirurgia.keys():
            sala = SistemaHospital.salas_cirurgia[nome]
            print(f"\n{nome}")
            print(f"Id: {sala.id_sala}")
            print(f"Capacidade: {sala.capacidade} pessoas")
            print(f"Equipamentos: {len(sala.equipamentos)}")
    
    @staticmethod
    def adicionar_equipamento_sala():
        if not SistemaHospital.salas_cirurgia:
            print("\nNenhuma sala de cirurgia criada ainda!")
            return

        print("\nSalas de Cirurgia disponíveis:")
        
        i = 1
        for nome_sala in SistemaHospital.salas_cirurgia.keys():
            print(f"{i} - {nome_sala}")
            i += 1
        
        try:
            escolha = int(input("\nEscolha a sala: "))
            
            contador = 1
            sala_selecionada = None

            for nome_sala in SistemaHospital.salas_cirurgia.keys():
                if contador == escolha:
                    sala_selecionada = SistemaHospital.salas_cirurgia[nome_sala]
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
    
    @staticmethod
    def ver_detalhes_sala_cirurgia():
        if not SistemaHospital.salas_cirurgia:
            print("\nNenhuma sala de cirurgia criada ainda!")
            return
        
        print("\nSalas de Cirurgia disponíveis:")
        
        i = 1
        for nome_sala in SistemaHospital.salas_cirurgia.keys():
            print(f"{i} - {nome_sala}")
            i += 1
        
        try:
            escolha = int(input("\nEscolha a sala: "))
            
            contador = 1
            sala_selecionada = None
            
            for nome_sala in SistemaHospital.salas_cirurgia.keys():
                if contador == escolha:
                    sala_selecionada = SistemaHospital.salas_cirurgia[nome_sala]
                    break

                contador += 1
            
            if not sala_selecionada:
                print("Opção inválida!")
                return
            
            detalhes = sala_selecionada.detalhar_sala()
            print(detalhes)
            
        except ValueError:
            print("Valor inválido!")
    
    @staticmethod
    def ver_horario_funcionario():
        funcionario = InterfaceHospital.selecionar_funcionario("Horário de funcionário:")
        if not funcionario:
            return

        try:          
            mes_ano = InterfaceHospital.obter_mes_ano()

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
    
    @staticmethod
    def ver_pagamento_funcionario():
        funcionario = InterfaceHospital.selecionar_funcionario("Pagamento mensal de funcionário:")
        if not funcionario:
            return

        try:
            mes_ano = InterfaceHospital.obter_mes_ano()
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
    
    @staticmethod
    def menu_recepcao():
        if not SistemaHospital.salas_espera:
            print("\nRealize a configuração inicial primeiro!")
            return

        opcoes = {
            "1": ("Registar novo paciente", InterfaceHospital.registar_novo_paciente),
            "2": ("Ver pacientes registados", InterfaceHospital.listar_pacientes),
            "3": ("Enviar paciente para área de atendimento", InterfaceHospital.enviar_paciente_para_atendimento),
        }
        InterfaceHospital.exibir_menu_generico("Recepção - gerenciar pacientes", opcoes)
    
    @staticmethod
    def registar_novo_paciente():
        print("\nRegistar novo paciente:")
        try:
            nome = input("Nome do paciente: ").strip()
            idade = int(input("Idade: "))

            if not nome or idade <= 0:
                print("Dados inválidos!")
                return

            paciente = SistemaHospital.registrar_paciente(nome, idade)
            print(f"\nPaciente registado com sucesso!")
            print(f"Nº Utente: {paciente.numero_utente}")
            print(f"Nome: {paciente.nome}")
            print(f"Idade: {paciente.idade}")

        except ValueError:
            print("Erro ao processar dados!")
    
    @staticmethod
    def listar_pacientes():
        print("\nPacientes registados:")
        if not SistemaHospital.pacientes:
            print("Nenhum paciente registado!")
            return

        print(f"Pacientes registrados({len(SistemaHospital.pacientes)}):\n")
        for numero_utente in SistemaHospital.pacientes.keys():
            paciente = SistemaHospital.pacientes[numero_utente]
            area_info = ""
            sala_info = ""

            if paciente.area_atendimento:
                area_info = f" / Área: {paciente.area_atendimento}"

            if  paciente.sala_atendimento:
                sala_info = f" / Sala: {paciente.sala_atendimento}"

            print(f"{numero_utente} / {paciente.nome} / Idade: {paciente.idade} / Status: {paciente.status.value}{area_info} {sala_info}")
    
    @staticmethod
    def filtro_paciente(paciente):
        # Não mostrar se está em atendimento ou já tem senha
        if paciente.status == StatusAtendimento.Atendimento:
            return False
        if paciente.senha is not None:
            return False
        return True

    @staticmethod
    def enviar_paciente_para_atendimento():
        if not SistemaHospital.pacientes:
            print("Nenhum paciente registado!")
            return

        if not SistemaHospital.salas_espera:
            print("Nenhuma área de atendimento disponível!")
            return

        sala_espera = InterfaceHospital.selecionar_area("Áreas de atendimento disponíveis:")
        if not sala_espera:
            return

        
        paciente = InterfaceHospital.selecionar_paciente(
            "Pacientes disponíveis (sem atendimento e sem senha):",
            filtro=InterfaceHospital.filtro_paciente
        )

        if not paciente:
            return

        try:
            sala_espera.pegar_senha(paciente)
            area_nome_encontrado = "Desconhecida"
            for nome_area in SistemaHospital.salas_espera.keys():
                sala = SistemaHospital.salas_espera[nome_area]
                if sala == sala_espera:
                    area_nome_encontrado = nome_area
                    break
            
            print(f"Paciente {paciente.nome} inserido na fila de {area_nome_encontrado}!")

        except ValueError:
            print("Erro ao processar dados!")

    @staticmethod
    def menu_areas():
        if not SistemaHospital.salas_espera:
            print("Nenhuma área de atendimento configurada!")
            return

        while True:
            print("\nÁreas de atendimento:")

            i = 1
            for area_nome in SistemaHospital.salas_espera.keys():
                print(f"{i} - {area_nome}")
                i += 1

            print("0. Voltar")

            try:
                opcao = int(input("Escolha uma área: "))

                if opcao == 0:
                    break

                contador = 1
                area_selecionada = None

                for area_nome in SistemaHospital.salas_espera.keys():
                    if contador == opcao:
                        area_selecionada = area_nome
                        break

                    contador += 1

                if not area_selecionada:
                    print("Opção inválida!")
                    continue

                InterfaceHospital.gerenciar_area(area_selecionada)

            except ValueError:
                print("Valor inválido!")

    @staticmethod
    def gerenciar_area(area_nome: str):
        sala_espera = SistemaHospital.salas_espera[area_nome]

        opcoes = {
            "1": ("Painel de informações da área", lambda: sala_espera.mostrar_painel()),
            "2": ("Chamar próximo paciente", lambda: InterfaceHospital.chamar_proximo_paciente(sala_espera)),
            "3": ("Finalizar atendimento", lambda: InterfaceHospital.finalizar_atendimento(sala_espera)),
        }
        InterfaceHospital.exibir_menu_generico(f"Opções da área {area_nome}", opcoes)

    @staticmethod
    def chamar_proximo_paciente(sala_espera: SalaEspera):
        # Filtra apenas funcionários que NÃO são administrativos
        funcionarios_validos = []

        for funcionario in SistemaHospital.funcionarios.values():
            if not isinstance(funcionario.cargo, Cargo.Administrativo):
                if funcionario in sala_espera.funcionarios:
                    funcionarios_validos.append(funcionario)

        if not funcionarios_validos:
            print("Nenhum funcionário disponível!")
            return

        print("\nFuncionarios disponíveis:")
        i = 1
        for funcionario in funcionarios_validos:
            print(f"{i} {funcionario.nome} - {funcionario.cargo.name}")
            i += 1

        try:
            escolha = int(input("Escolha um funcionário: "))
            if not (1 <= escolha <= len(funcionarios_validos)):
                print("Opção inválida!")
                return
            funcionario_selecionado = funcionarios_validos[escolha - 1]
            sala_espera.chamar_proximo(funcionario_selecionado)
        except ValueError:
            print("Valor inválido!")

    @staticmethod
    def finalizar_atendimento(sala_espera: SalaEspera):
        sala_com_atendimento = None
        
        for sala in sala_espera.salas_atendimento:
            if sala.status == StatusSala.Ocupado and sala.paciente_atual:
                sala_com_atendimento = sala
                break

        if not sala_com_atendimento:
            print("Nenhuma sala em atendimento!")
            return

        descricao = input("Descrição do atendimento (ou Enter para padrão): ").strip()
        if not descricao:
            descricao = "Atendimento realizado com sucesso"

        sala_com_atendimento.finalizar_atendimento(descricao)

    @staticmethod
    def relatorio_funcionario():
        funcionario = InterfaceHospital.selecionar_funcionario("Relatório de funcionário:")
        if not funcionario:
            return

        relatorio = SistemaHospital.gerar_relatorio_funcionario(funcionario.numero_funcionario)
        print(relatorio)

    @staticmethod
    def relatorio_paciente():
        paciente = InterfaceHospital.selecionar_paciente("Relatório de paciente:")
        if not paciente:
            return

        relatorio = SistemaHospital.gerar_relatorio_paciente(paciente.numero_utente)
        print(relatorio)

    @staticmethod
    def estatisticas_hospital():
        print("\nEstatisticas do hospital:")

        print(f"\nPacientes registados: {len(SistemaHospital.pacientes)}")
        print(f"Funcionários: {len(SistemaHospital.funcionarios)}")
        print(f"Áreas de atendimento: {len(SistemaHospital.salas_espera)}")

        total_atendimentos = 0
        for funcionario in SistemaHospital.funcionarios.values():
            total_atendimentos += len(funcionario.obter_atendimentos())

        print(f"Total de atendimentos realizados: {total_atendimentos}")

        if SistemaHospital.pacientes:
            em_espera = 0
            em_atendimento = 0
            atendidos = 0
            sem_sala = 0
            for paciente in SistemaHospital.pacientes.values():
                if paciente.status == StatusAtendimento.Espera:
                    em_espera += 1
                elif paciente.status == StatusAtendimento.Atendimento:
                    em_atendimento += 1
                elif paciente.status == StatusAtendimento.Atendido:
                    atendidos += 1
                elif paciente.status == StatusAtendimento.Sem_Sala:
                    sem_sala += 1

            print(f"\nStatus dos Pacientes:")
            print(f"Sem sala definida: {sem_sala}")
            print(f"Em espera: {em_espera}")
            print(f"Em atendimento: {em_atendimento}")
            print(f"Atendidos: {atendidos}")

    @staticmethod
    def menu_historico_medico():
        opcoes = {
            "1": ("Adicionar médico/funcionário ao sistema", InterfaceHospital.adicionar_funcionario_historico),
            "2": ("Registrar atendimento médico", InterfaceHospital.registrar_atendimento_historico),
            "3": ("Ver histórico de um paciente", InterfaceHospital.ver_historico_paciente),
            "4": ("Ver pacientes atendidos por funcionário", InterfaceHospital.ver_pacientes_funcionario),
            "5": ("Ver todos os históricos registrados", InterfaceHospital.listar_todos_historicos),
        }
        InterfaceHospital.exibir_menu_generico("Histórico médico", opcoes)

    @staticmethod
    def adicionar_funcionario_historico():
        print("\nAdicionar medico/funcionario ao historico:")

        if not SistemaHospital.funcionarios:
            print("Nenhum funcionário registrado no sistema!")
            return

        funcionario = InterfaceHospital.selecionar_funcionario("Funcionários disponíveis:")
        if not funcionario:
            return

        if SistemaHospital.adicionar_funcionario(funcionario):
            print(f"Funcionario {funcionario.nome} adicionado ao sistema de historico!")
        else:
            print("Erro ao adicionar funcionário!")

    @staticmethod
    def registrar_atendimento_historico():
        print("\nRegistrar atendimento medico:")

        if not SistemaHospital.Funcionarios:
            print("Nenhum médico registrado no histórico!")
            return

        if not SistemaHospital.pacientes:
            print("Nenhum paciente registrado no sistema!")
            return

        print("\nMédicos/Funcionários disponíveis:")
        
        i = 1
        for numero_funcionario in SistemaHospital.Funcionarios.keys():
            funcionario = SistemaHospital.Funcionarios[numero_funcionario]
            print(f"{i} - {funcionario.nome} (#{numero_funcionario})")
            i += 1

        try:
            escolha_funcionario = int(input("\nEscolha o médico: "))
            
            contador = 1
            numero_funcionario_selecionado = None
            for numero_funcionario in SistemaHospital.Funcionarios.keys():
                if contador == escolha_funcionario:
                    numero_funcionario_selecionado = numero_funcionario
                    break
                contador += 1
            
            if not numero_funcionario_selecionado:
                print("Opção inválida!")
                return

            paciente = InterfaceHospital.selecionar_paciente()
            if not paciente:
                return

            # Adiciona o Paciente ao histórico se ainda não existe
            if paciente.numero_utente not in SistemaHospital.Pacientes or SistemaHospital.Pacientes[paciente.numero_utente] is None:
                SistemaHospital.adicionar_paciente(paciente)

            id_historico = int(input("\nId do atendimento (número inteiro): "))
            descricao = input("Descrição do atendimento: ").strip()

            if SistemaHospital.adicionar_historico(numero_funcionario_selecionado, paciente.numero_utente, id_historico, descricao):
                print("Atendimento registrado com sucesso!")
            else:
                print("Erro ao registrar atendimento (Id duplicado ou dados inválidos)!")
        
        except ValueError:
            print("Valor inválido!")
    
    @staticmethod
    def ver_historico_paciente():
        print("\nVer historico de paciente:")

        if not SistemaHospital.pacientes:
            print("Nenhum paciente registrado!")
            return

        paciente = InterfaceHospital.selecionar_paciente()
        if not paciente:
            return

        try:
            historicos = SistemaHospital.obter_historicos_paciente(paciente.numero_utente)
            
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

    @staticmethod
    def ver_pacientes_funcionario():
        print("\nVer pacientes atendidos por funcionario:")

        if not SistemaHospital.Funcionarios:
            print("Nenhum funcionário no histórico!")
            return

        print("\nFuncionários com histórico:")
        
        i = 1
        for numero_funcionario in SistemaHospital.Funcionarios.keys():
            funcionario = SistemaHospital.Funcionarios[numero_funcionario]
            print(f"{i} - {funcionario.nome} (#{numero_funcionario})")
            i += 1

        try:
            escolha = int(input("\nEscolha o funcionário: "))
            
            contador = 1
            numero_funcionario_selecionado = None
            funcionario_selecionado = None
            
            for numero_funcionario in SistemaHospital.Funcionarios.keys():
                if contador == escolha:
                    numero_funcionario_selecionado = numero_funcionario
                    funcionario_selecionado = SistemaHospital.Funcionarios[numero_funcionario]
                    break

                contador += 1
            
            if not numero_funcionario_selecionado:
                print("Opção inválida!")
                return
            
            pacientes_numeros = SistemaHospital.obter_pacientes_funcionario(numero_funcionario_selecionado)
            
            if not pacientes_numeros:
                print(f"\n{funcionario_selecionado.nome} nao atendeu nenhum paciente!")
            else:
                print(f"\nPacientes atendidos por {funcionario_selecionado.nome} (#{numero_funcionario_selecionado}):")
                
                for numero_utente in pacientes_numeros:
                    if numero_utente in SistemaHospital.Pacientes:
                        paciente = SistemaHospital.Pacientes[numero_utente]
                        historicos = SistemaHospital.obter_historicos_funcionario_paciente(numero_funcionario_selecionado, numero_utente)
                        print(f"\n{paciente.nome} (#{numero_utente:09d})")
                        
                        for id_historico in historicos.keys():
                            descricao = historicos[id_historico]
                            print(f"Id {id_historico}: {descricao}")

        except ValueError:
            print("Valor inválido!")

    @staticmethod
    def listar_todos_historicos():
        print(SistemaHospital.listar_todos_historicos())

    @staticmethod
    def menu_horarios():
        opcoes = {
            "1": ("Visualizar horário semanal de um funcionário", InterfaceHospital.ver_horario_semanal),
            "2": ("Visualizar horário mensal de um funcionário", InterfaceHospital.ver_horario_mensal_detalhado),
            "3": ("Editar horário semanal de um funcionário", InterfaceHospital.editar_horario_semanal),
            "4": ("Definir horário específico para um dia", InterfaceHospital.definir_horario_especifico),
            "5": ("Ver registos de ponto de um funcionário", InterfaceHospital.ver_registos_ponto),
        }
        InterfaceHospital.exibir_menu_generico("Gestão de Horários", opcoes)

    @staticmethod
    def ver_horario_semanal():
        func = InterfaceHospital.selecionar_funcionario()
        if not func:
            return

        print(f"\nHorário Semanal de {func.nome}:")
        
        totais = func.horario_semanal.calcular_totais_semanais()
        
        for dia in Dias_Semana:
            horario = func.horario_semanal.horarios.get(dia)
            
            if horario and horario.inicio != timedelta(0):
                inicio_hm = HoraMinuto.init_com_deltatime(horario.inicio)
                fim_hm = HoraMinuto.init_com_deltatime(horario.fim)
                print(f"\n{dia.name}: {inicio_hm} - {fim_hm}")
                
                if horario._pausas.pausas:
                    print(f"Pausas:")
                    for pausa in horario._pausas.pausas:
                        pausa_inicio_hm = HoraMinuto.init_com_deltatime(pausa.inicio)
                        pausa_fim_hm = HoraMinuto.init_com_deltatime(pausa.fim)
                        print(f" - {pausa_inicio_hm} - {pausa_fim_hm}")
                
                print(f"Tempo trabalhado: {formatar_timedelta(horario.tempo_trabalhado())}")
                print(f"Tempo diurno: {formatar_timedelta(horario.calcular_tempo_diurno())}")
                print(f"Tempo noturno: {formatar_timedelta(horario.calcular_tempo_noturno())}")
            else:
                print(f"\n{dia.name}: Folga")
        
        print(f"\n\nTotais Semanais:")
        print(f"Tempo trabalhado: {formatar_timedelta(totais['trabalhado'])}")
        print(f"Tempo diurno: {formatar_timedelta(totais['diurno'])}")
        print(f"Tempo noturno: {formatar_timedelta(totais['noturno'])}\n")

    @staticmethod
    def ver_horario_mensal_detalhado():
        funcionario = InterfaceHospital.selecionar_funcionario()
        if not funcionario:
            return

        try:
            mes, ano = InterfaceHospital.obter_mes_ano()
            
            horario_mensal = funcionario.horario_funcionario.obter_horario_mensal(mes, ano)
            detalhes_diarios = horario_mensal.obter_dados_diarios()
            
            print(f"\nHorário Mensal de {funcionario.nome} - {mes:02d}/{ano}")
            print(f"Data / Dia / Entrada / Saída / Pausas / Trabalhado / Diurno / Noturno")
            
            for detalhe in detalhes_diarios:
                data_str = detalhe['data'].strftime("%d/%m/%Y")
                dia_semana = detalhe['dia_semana']
                
                if detalhe['trabalhado'] == timedelta(0):
                    print(f"{data_str} / {dia_semana} / Folga")
                else:
                    # O símbolo // faz o mesmo do que / mas retorna inteiros
                    entrada = HoraMinuto.init_com_deltatime(detalhe['inicio'])
                    saida = HoraMinuto.init_com_deltatime(detalhe['fim'])
                    
                    pausas_str = ""
                    if detalhe['pausas']:
                        pausas_list = []
                        for pausa in detalhe['pausas']:
                            p_inicio = HoraMinuto.init_com_deltatime(pausa.inicio)
                            p_fim = HoraMinuto.init_com_deltatime(pausa.fim)
                            pausas_list.append(f"{p_inicio}-{p_fim}")
                        pausas_str = ", ".join(pausas_list)
                    else:
                        pausas_str = "Sem pausas"
                    
                    trabalhado_str = formatar_timedelta(detalhe['trabalhado'])
                    diurno_str = formatar_timedelta(detalhe['diurno'])
                    noturno_str = formatar_timedelta(detalhe['noturno'])

                    print(f"{data_str} / {dia_semana} / {str(entrada)} / {str(saida)} / {pausas_str} / {trabalhado_str} / {diurno_str} / {noturno_str}")

            detalhes_mensais = horario_mensal.calcular_totais_mensais()
            print(f"Totais:\n Diurno: {formatar_timedelta(detalhes_mensais['diurno'])}\n Noturno: {formatar_timedelta(detalhes_mensais['noturno'])}\n Tempo trabalhado total: {formatar_timedelta(detalhes_mensais['trabalhado'])}")

        except (ValueError, IndexError):
            print("Valor inválido!")
        
    @staticmethod
    def editar_horario_semanal():
        funcionario = InterfaceHospital.selecionar_funcionario()
        if not funcionario:
            return

        try:
            print("\nDias da semana:")
            i = 1
            for dia in Dias_Semana:
                print(f"{i} - {dia.name}")
                i += 1

            dia_escolha = int(input("\nEscolha o dia da semana: ")) - 1
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
                    
                    if horario._pausas.adicionar_pausa(pausa):
                        print("Pausa adicionada com sucesso!")
                    else:
                        print("Erro ao adicionar pausa (fora do horário de trabalho ou limite excedido)")
            
            funcionario.horario_semanal.adicionar_horario(dia_semana_selecionado, horario)
            funcionario.horario_funcionario = FuncionarioHorario(funcionario.horario_semanal)

            print(f"\nHorário de {dia_semana_selecionado.name} atualizado com sucesso!")

        except (ValueError, IndexError):
            print(f"Valor inválido!")
        
    @staticmethod
    def definir_horario_especifico():
        funcionario = InterfaceHospital.selecionar_funcionario()
        if not funcionario:
            return

        try:
            print("\nDefina a data para o horário específico:")
            dia = int(input("Dia: "))
            mes_ano = InterfaceHospital.obter_mes_ano()

            data_especifica = date(mes_ano[1], mes_ano[0], dia)

            print(f"\nConfigurar horário para {data_especifica.strftime('%d/%m/%Y')}:")
            
            inicio_str = input("Hora de início (HH:MM) (Deixe em branco para marcar como folga): ").strip()
            if not inicio_str:
                funcionario.definir_horario_especifico(data_especifica, Horario(intervalo=IntervaloTempo(timedelta(0),timedelta(0))))
                print(f"{data_especifica.strftime('%d/%m/%Y')} marcado como folga!")
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
                    pausa_fim_str = input("Hora de fim da pausa (HH:MM): ").strip()
                    
                    pausa = IntervaloTempo.init_com_HoraMinuto(
                        HoraMinuto.init_com_str(pausa_inicio_str),
                        HoraMinuto.init_com_str(pausa_fim_str)
                    )
                    
                    if horario._pausas.adicionar_pausa(pausa):
                        print("Pausa adicionada com sucesso!")
                    else:
                        print("Erro ao adicionar pausa")
        
            funcionario.definir_horario_especifico(data_especifica, horario)
            print(f"\nHorário específico para {data_especifica.strftime('%d/%m/%Y')} definido com sucesso!")

        except (ValueError, IndexError):
            print(f"Valor inválido!")

    @staticmethod
    def registar_ponto():
        funcionario = InterfaceHospital.selecionar_funcionario()
        if not funcionario:
            return

        try:
            print(f"\nRegistar ponto para {funcionario.nome}")
            print("Data:")
            dia_input = input("Dia (deixe em branco para hoje): ").strip()
            data_ponto = date.today()

            if dia_input:
                mes_ano = InterfaceHospital.obter_mes_ano()
                data_ponto = date(mes_ano[1], mes_ano[0], int(dia_input))
            
            print(f"\nData: {data_ponto.strftime('%d/%m/%Y')}")
            
            # Obter horário previsto para a data
            dia_semana = Dias_Semana.data_para_enum(data_ponto)
            horario_previsto = None
            inicio_previsto_str = ""
            fim_previsto_str = ""
            
            # Verifica se há algum horário específico para esta data
            if data_ponto in funcionario.horario_funcionario.horarios_especificos:
                horario_previsto = funcionario.horario_funcionario.horarios_especificos[data_ponto]
            elif dia_semana in funcionario.horario_semanal.horarios:
                horario_previsto = funcionario.horario_semanal.horarios[dia_semana]
            
            # Verifica se é um dia de folga
            if not horario_previsto:
                print(f"\nNo dia {data_ponto.strftime('%d/%m/%Y')} está configurado como folga no horário deste funcionário. O ponto não pode ser registado.")
                return

            if horario_previsto and horario_previsto.inicio != timedelta(0):
                inicio_previsto_hm = HoraMinuto.init_com_deltatime(horario_previsto.inicio)
                fim_previsto_hm = HoraMinuto.init_com_deltatime(horario_previsto.fim)

                inicio_previsto_str = str(inicio_previsto_hm)
                fim_previsto_str = str(fim_previsto_hm)

                print(f"\nHorário previsto: {inicio_previsto_str} - {fim_previsto_str}")
                print("(Deixe em branco para usar o horário previsto)")

            inicio_real = input(f"Hora de entrada (HH:MM) [previsto: {inicio_previsto_str}]: ").strip()
            if not inicio_real and inicio_previsto_str:
                inicio_real = inicio_previsto_str
                print(f"Usando horário previsto: {inicio_real}")
            
            fim_real = input(f"Hora de saída (HH:MM) [previsto: {fim_previsto_str}]: ").strip()
            if not fim_real and fim_previsto_str:
                fim_real = fim_previsto_str
                print(f"Usando horário previsto: {fim_real}")
            
            pausas_reais = []
            print("\nDeseja registar pausas? (s/n)")
            if input().strip().lower() == 's':
                # Mostrar pausas previstas se existirem
                if horario_previsto and horario_previsto._pausas.pausas:
                    print("\nPausas previstas:")
                    for pausa in horario_previsto._pausas.pausas:
                        pausa_inicio_hm = HoraMinuto.init_com_deltatime(pausa.inicio)
                        pausa_fim_hm = HoraMinuto.init_com_deltatime(pausa.fim)
                        print(f" - {pausa_inicio_hm} - {pausa_fim_hm}")
                
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

    @staticmethod
    def ver_registos_ponto():
        funcionario = InterfaceHospital.selecionar_funcionario()
        if not funcionario:
            return

        try:
            mes_ano = InterfaceHospital.obter_mes_ano()
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
    try:
        print("\nBem-vindo ao Sistema Hospitalar!")
        InterfaceHospital.inicializar_dados()
    except KeyboardInterrupt:
        limpar_console()
        linhas_vazias()
        print("\nPrograma encerrado.")