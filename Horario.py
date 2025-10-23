from datetime import datetime, timedelta, date
from enum import Enum
import calendar

Inicio_Turno_noturno = timedelta(hours=22)
Fim_Turno_noturno = timedelta(hours=7)
data_base = datetime.now().date()
max_pausas = 24

class Dias_Semana(Enum):
    Domingo = 0
    Segunda = 1
    Terca   = 2
    Quarta  = 3
    Quinta  = 4
    Sexta   = 5
    Sabado  = 6

    def __str__(self):
        return self.name
    def __int__(self):
        return self.value
    
class HoraMinuto:
    def __init__(self, hora: int, minuto: int):
        self.hora = hora
        self.minuto = minuto

    @classmethod
    def init_com_str(cls, hora_minuto_str: str):
        try:
            parts = hora_minuto_str.split(':')
            if len(parts) == 2:
                h = int(parts[0])
                m = int(parts[1])
                return cls(h, m)
        except Exception:
            pass
        return cls(0, 0)
    
    def obter_timedelta(self) -> timedelta:
        return timedelta(hours=self.hora, minutes=self.minuto)

    def __str__(self):
        return f"{self.hora:02d}:{self.minuto:02d}"

    def __lt__(self, outra_hm): # Quando se usa <
        return self.obter_timedelta() < outra_hm.obter_timedelta()

    def __eq__(self, outra_hm): # Quando se usa ===
        return self.obter_timedelta() == outra_hm.obter_timedelta()

class IntervaloTempo:
    def __init__(self, inicio: timedelta, fim: timedelta):
        if inicio > fim:
            (inicio, fim) = (fim, inicio)

        self.inicio = inicio
        self.fim = fim

    @classmethod
    def init_com_HoraMinuto(cls, inicio_hm: HoraMinuto, fim_hm: HoraMinuto):
        inicio = inicio_hm.obter_timedelta()
        fim = fim_hm.obter_timedelta()

        # Se o fim é antes do início (turno noturno) ou dura 24h
        if fim <= inicio:
            fim += timedelta(days=1)

        return cls(inicio, fim)

    def duracao_total(self) -> timedelta:
        return self.fim - self.inicio

    def esta_dentro_do_limite(self, limite: 'IntervaloTempo') -> bool:
        if limite is None:
            return True
        return self.inicio >= limite.inicio and self.fim <= limite.fim

    @staticmethod
    def intersecao_tempo(intervalo1: 'IntervaloTempo', intervalo2: 'IntervaloTempo') -> timedelta:
        ultimo_comeco = max(intervalo1.inicio, intervalo2.inicio)
        primeiro_fim = min(intervalo1.fim, intervalo2.fim)
        
        intersecao = primeiro_fim - ultimo_comeco
        return max(intersecao, timedelta(0))
    
class Pausas:
    def __init__(self, pausas: list = None, limite: IntervaloTempo = None):
        self.pausas = []
        self.limite = limite
        if pausas:
            for pausa in pausas:
                if isinstance(pausa, IntervaloTempo):
                    self.adicionar_pausa(pausa)

    def duracao_total_pausas(self) -> timedelta:
        total = timedelta(0)
        for pausa in self.pausas:
            total += pausa.duracao_total()
        return total
    
    def adicionar_pausa(self, nova_pausa: IntervaloTempo) -> bool:
        if len(self.pausas) >= max_pausas or not nova_pausa.esta_dentro_do_limite(self.limite):
            return False

        for pausa in self.pausas:
            if IntervaloTempo.intersecao_tempo(pausa, nova_pausa) > timedelta(0):
                return False
            
        self.pausas.append(nova_pausa)
        self.pausas.sort(key=lambda p: p.inicio)
        return True
    
    def atualizar_limite(self, novo_limite: IntervaloTempo):
        self.limite = novo_limite
        self.pausas = [p for p in self.pausas if p.esta_dentro_do_limite(novo_limite)]

class Horario:
    def __init__(self, intervalo: IntervaloTempo, pausas: list = None):
        self._intervalo = intervalo
        self._pausas = Pausas(pausas, self._intervalo)

    @property
    def inicio(self) -> timedelta:
        return self._intervalo.inicio

    @property
    def fim(self) -> timedelta:
        return self._intervalo.fim

    def tempo_trabalhado(self) -> timedelta:
        return self._intervalo.duracao_total() - self._pausas.duracao_total_pausas()

    def _obter_segmentos_trabalho(self) -> list:
        segmentos = []
        inicio_seg = self.inicio

        for pausa in self._pausas.pausas:
            if inicio_seg < pausa.inicio:
                segmentos.append(IntervaloTempo(inicio_seg, pausa.inicio))
            inicio_seg = max(inicio_seg, pausa.fim)

        if inicio_seg < self.fim:
            segmentos.append(IntervaloTempo(inicio_seg, self.fim))

        return segmentos

    def _gerar_intervalos_noturnos(self) -> list:
        intervalos_noturnos = []
        dia_zero = timedelta(days=0)
        um_dia = timedelta(days=1)
        dois_dias = timedelta(days=2)

        # Noturno do primeiro dia (ex: 22:00 a 24:00)
        intervalos_noturnos.append(IntervaloTempo(Inicio_Turno_noturno, um_dia))
        # Noturno da manhã do dia seguinte (ex: 00:00 a 07:00)
        intervalos_noturnos.append(IntervaloTempo(um_dia, um_dia + Fim_Turno_noturno))
        
        # Se o turno de trabalho se estende por mais de um dia
        if self.fim > um_dia:
            # Noturno da noite do segundo dia (ex: 22:00 de D+1 a 24:00 de D+1)
            intervalos_noturnos.append(IntervaloTempo(um_dia + Inicio_Turno_noturno, dois_dias))
            # Noturno da manhã do terceiro dia (ex: 00:00 de D+2 a 07:00 de D+2)
            intervalos_noturnos.append(IntervaloTempo(dois_dias, dois_dias + Fim_Turno_noturno))

        # Noturno da manhã do primeiro dia (ex: 00:00 a 07:00)
        intervalos_noturnos.append(IntervaloTempo(dia_zero, Fim_Turno_noturno))
        
        return intervalos_noturnos

    def calcular_tempo_noturno(self) -> timedelta:
        tempo_noturno = timedelta(0)
        segmentos_trabalho = self._obter_segmentos_trabalho()
        intervalos_noturnos = self._gerar_intervalos_noturnos()

        for segmento in segmentos_trabalho:
            for noite in intervalos_noturnos:
                tempo_noturno += IntervaloTempo.intersecao_tempo(segmento, noite)

        return tempo_noturno

    def calcular_tempo_diurno(self) -> timedelta:
        return self.tempo_trabalhado() - self.calcular_tempo_noturno()
    
class Horario_Semanal:
    def __init__(self):
        self.horarios = {dia: None for dia in Dias_Semana}

    def adicionar_horario(self, dia_semana: Dias_Semana, horario: Horario):
        if dia_semana in self.horarios:
            self.horarios[dia_semana] = horario

    def calcular_totais_semanais(self) -> dict:
        total_trabalhado = timedelta()
        total_diurno = timedelta()
        total_noturno = timedelta()

        for horario in self.horarios.values():
            if horario:
                total_trabalhado += horario.tempo_trabalhado()
                total_diurno += horario.calcular_tempo_diurno()
                total_noturno += horario.calcular_tempo_noturno()
         
        return {
            "trabalhado": total_trabalhado,
            "diurno": total_diurno,
            "noturno": total_noturno
        }

class Horario_Mensal:
    def __init__(self, ano: int, mes: int, horario_semanal: Horario_Semanal):
        if not (1 <= mes <= 12):
            agora = datetime.now()
            ano = agora.year
            mes = agora.month
            horario_semanal = Horario_Semanal()

        self.ano = ano
        self.mes = mes
        self.horario_semanal = horario_semanal      

    def obter_detalhes_Mensais(self) -> str:
        total_trabalhado = timedelta()
        total_diurno = timedelta()
        total_noturno = timedelta()
        
        num_dias = calendar.monthrange(self.ano, self.mes)[1]
        data_inicial = date(self.ano, self.mes, 1)

        for i in range(num_dias):
            data_atual = data_inicial + timedelta(days=i)
            
            dia_da_semana_vindo_da_data = data_atual.weekday() + 1
            if dia_da_semana_vindo_da_data == 7:
                dia_da_semana_vindo_da_data = 0
            dia_da_semana_enum = Dias_Semana(dia_da_semana_vindo_da_data)
        
            horario_do_dia = self.horario_semanal.horarios.get(dia_da_semana_enum)

            if horario_do_dia:
                total_trabalhado += horario_do_dia.tempo_trabalhado()
                total_diurno += horario_do_dia.calcular_tempo_diurno()
                total_noturno += horario_do_dia.calcular_tempo_noturno()
        
        resultado = {
            "trabalhado": total_trabalhado,
            "diurno": total_diurno,
            "noturno": total_noturno
        }

        saida_formatada = f"{self.mes}/{self.ano}:\n"
        for key, valor in resultado.items():
            saida_formatada += f"  {key.capitalize()}: {valor}\n"
        return saida_formatada
    
    def obter_detalhes_Diarios(self) -> list:
        detalhes_dict = {}
        calendar.setfirstweekday(calendar.SUNDAY)
        semanas_do_mes = calendar.monthcalendar(self.ano, self.mes)
        
        for i, semana in enumerate(semanas_do_mes):
            num_semana = i + 1
            if num_semana not in detalhes_dict:
                detalhes_dict[num_semana] = []

            for dia_do_mes in semana:
                if dia_do_mes == 0:
                    continue

                data_atual = date(self.ano, self.mes, dia_do_mes)

                dia_da_semana_vindo_da_data = data_atual.weekday() + 1
                if dia_da_semana_vindo_da_data == 7:
                    dia_da_semana_vindo_da_data = 0

                dia_da_semana_enum = Dias_Semana(dia_da_semana_vindo_da_data)
                
                horario_do_dia = self.horario_semanal.horarios.get(dia_da_semana_enum)

                if horario_do_dia:
                    detalhes_dict[num_semana].append({
                        "data": data_atual,
                        "dia_semana": dia_da_semana_enum.name,
                        "trabalhado": horario_do_dia.tempo_trabalhado(),
                        "diurno": horario_do_dia.calcular_tempo_diurno(),
                        "noturno": horario_do_dia.calcular_tempo_noturno()
                    })
        
        saida_formatada = []
        for num_semana in sorted(detalhes_dict.keys()):
            dias_da_semana = detalhes_dict[num_semana]
            if not dias_da_semana:
                continue
            
            semana_formatada = [f"Semana {num_semana}"]
            for dia in dias_da_semana:
                dia_str = (
                    f" {dia['dia_semana']} - {dia['data'].strftime('%d/%m')}:\n" +
                    f"  Total:    {dia['trabalhado']}\n" +
                    f"  Diurno:   {dia['diurno']}\n" +
                    f"  Noturno:  {dia['noturno']}"
                )
                semana_formatada.append(dia_str)
            saida_formatada.append(semana_formatada)
            
        return saida_formatada
    def obter_detalhes_Semanais(self) -> list:
        saida_formatada = []
        calendar.setfirstweekday(calendar.SUNDAY)
        semanas_do_mes = calendar.monthcalendar(self.ano, self.mes)

        for i, semana in enumerate(semanas_do_mes):
            total_trabalhado_sem = timedelta()
            total_diurno_sem = timedelta()
            total_noturno_sem = timedelta()
            dias_trabalhados_na_semana = []

            for dia_do_mes in semana:
                if dia_do_mes == 0:
                    continue

                data_atual = date(self.ano, self.mes, dia_do_mes)

                dia_da_semana_vindo_da_data = data_atual.weekday() + 1

                if(dia_da_semana_vindo_da_data==7):
                    dia_da_semana_vindo_da_data = 0

                dia_da_semana_enum = Dias_Semana(dia_da_semana_vindo_da_data)
                
                horario_do_dia = self.horario_semanal.horarios.get(dia_da_semana_enum)

                if horario_do_dia:
                    dias_trabalhados_na_semana.append(data_atual)
                    total_trabalhado_sem += horario_do_dia.tempo_trabalhado()
                    total_diurno_sem += horario_do_dia.calcular_tempo_diurno()
                    total_noturno_sem += horario_do_dia.calcular_tempo_noturno()

            if dias_trabalhados_na_semana:
                inicio_semana_str = dias_trabalhados_na_semana[0].strftime('%d/%m')
                fim_semana_str = dias_trabalhados_na_semana[-1].strftime('%d/%m')
                num_semana_real = i + 1
                
                semana_str = (
                    f"Semana {num_semana_real} ({inicio_semana_str} a {fim_semana_str}):\n"
                    f"  Total:    {total_trabalhado_sem}\n"
                    f"  Diurno:   {total_diurno_sem}\n"
                    f"  Noturno:  {total_noturno_sem}"
                )
                saida_formatada.append(semana_str)
                
        return saida_formatada
    
def teste():
    # Teste do Horario Mensal
    horario_semanal = Horario_Semanal()
    horario_0 = Horario (
        intervalo = IntervaloTempo.init_com_HoraMinuto(
            inicio_hm = HoraMinuto.init_com_str("09:00"),
            fim_hm = HoraMinuto.init_com_str("19:00")
        ),
        pausas = [
            IntervaloTempo.init_com_HoraMinuto (
                HoraMinuto.init_com_str("12:30"),
                HoraMinuto.init_com_str("13:30"),
            ),
        ]
    )    

    horario_1 = Horario(
        intervalo = IntervaloTempo.init_com_HoraMinuto (
            inicio_hm = HoraMinuto.init_com_str("11:05"),
            fim_hm = HoraMinuto.init_com_str("23:05")
        ),
        pausas = [
            IntervaloTempo.init_com_HoraMinuto (
                HoraMinuto.init_com_str("13:15"),
                HoraMinuto.init_com_str("14:15")
            )
        ]
    )

    horario_2 = Horario (
        intervalo = IntervaloTempo.init_com_HoraMinuto (
            inicio_hm = HoraMinuto.init_com_str("10:30"),
            fim_hm = HoraMinuto.init_com_str("20:30")
        ),
        pausas = [
            IntervaloTempo.init_com_HoraMinuto (
                HoraMinuto.init_com_str("11:55"),
                HoraMinuto.init_com_str("12:55")
            )
        ]
    )

    horario_3 = Horario (
        intervalo = IntervaloTempo.init_com_HoraMinuto (
            inicio_hm = HoraMinuto.init_com_str("07:30"),
            fim_hm = HoraMinuto.init_com_str("17:30")
        ),
        pausas = [
            IntervaloTempo.init_com_HoraMinuto (
                HoraMinuto.init_com_str("13:55"),
                HoraMinuto.init_com_str("14:55")
            )
        ]
    )
    
    horario_4 = Horario (
        intervalo = IntervaloTempo.init_com_HoraMinuto (
            inicio_hm = HoraMinuto.init_com_str("10:10"),
            fim_hm = HoraMinuto.init_com_str("22:10")
        ),
        pausas = [
            IntervaloTempo.init_com_HoraMinuto (
                HoraMinuto.init_com_str("13:15"),
                HoraMinuto.init_com_str("14:15")
            )
        ]
    )
    
    horario_5 = Horario (
        intervalo = IntervaloTempo.init_com_HoraMinuto (
            inicio_hm = HoraMinuto.init_com_str("09:30"),
            fim_hm = HoraMinuto.init_com_str("19:30")
        ),
        pausas = [
            IntervaloTempo.init_com_HoraMinuto (
                HoraMinuto.init_com_str("11:30"),
                HoraMinuto.init_com_str("12:30")
            )
        ]
    )
    
    horario_6 = Horario (
        intervalo = IntervaloTempo.init_com_HoraMinuto (
            inicio_hm = HoraMinuto.init_com_str("10:00"),
            fim_hm = HoraMinuto.init_com_str("20:00")
        ),
        pausas = [
            IntervaloTempo.init_com_HoraMinuto (
                HoraMinuto.init_com_str("12:45"),
                HoraMinuto.init_com_str("13:45")
            )
        ]
    )

    horario_semanal.adicionar_horario( Dias_Semana.Domingo,horario_0 )
    horario_semanal.adicionar_horario( Dias_Semana.Segunda,horario_1 )
    horario_semanal.adicionar_horario( Dias_Semana.Terca,horario_2   )
    horario_semanal.adicionar_horario( Dias_Semana.Quarta,horario_3  )
    horario_semanal.adicionar_horario( Dias_Semana.Quinta,horario_4  )
    horario_semanal.adicionar_horario( Dias_Semana.Sexta,horario_5   )
    horario_semanal.adicionar_horario( Dias_Semana.Sabado,horario_6  )
    
    horario_mensal = Horario_Mensal(
        ano = datetime.now().year,
        mes = datetime.now().month,
        horario_semanal= horario_semanal
    )
    print("\nDetalhes por dia")
    detalhes_diarios = horario_mensal.obter_detalhes_Diarios()
    for semana in detalhes_diarios:
        for item in semana:
            print(item)
        print()

    print("\nDetalhes por semana")
    detalhes_semanais = horario_mensal.obter_detalhes_Semanais()
    for item in detalhes_semanais:
        print(item)

    print("\nDetalhes por Mês")
    print(horario_mensal.obter_detalhes_Mensais())

if __name__ == "__main__":
    teste()