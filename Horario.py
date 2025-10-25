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
    
    @staticmethod
    def data_para_enum(data:date):
        dia_semana_int = data.weekday() + 1

        if dia_semana_int == 7:
            dia_semana_int = 0

        return Dias_Semana(dia_semana_int)
    
class HoraMinuto:
    def __init__(self, hora: int, minuto: int):
        self.hora = max(min(hora, 23), 0)
        self.minuto = max(min(minuto, 59), 0)

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

    def __lt__(self, outra_hm):
        return self.obter_timedelta() < outra_hm.obter_timedelta()
    
    def __le__(self, outra_hm):
        return self.obter_timedelta() <= outra_hm.obter_timedelta()
    
    def __eq__(self, outra_hm):
        return self.obter_timedelta() == outra_hm.obter_timedelta()

class IntervaloTempo:
    def __init__(self, inicio: timedelta, fim: timedelta):
        self.inicio = inicio
        self.fim = fim

    @classmethod
    def init_com_HoraMinuto(cls, inicio_hm: HoraMinuto, fim_hm: HoraMinuto):
        inicio = inicio_hm.obter_timedelta()
        fim = fim_hm.obter_timedelta()

        if fim_hm < inicio_hm:
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
        self.pausas.sort(key=lambda pausa: pausa.inicio)
        return True
    
    def atualizar_limite(self, novo_limite: IntervaloTempo):
        self.limite = novo_limite
        novas_pausas = []

        for pausa in self.pausas:
            if(pausa.esta_dentro_do_limite(novo_limite)):
                novas_pausas.append(pausa)

        self.pausas = novas_pausas

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

        intervalos_noturnos.append(IntervaloTempo(Inicio_Turno_noturno, um_dia))
        intervalos_noturnos.append(IntervaloTempo(um_dia, um_dia + Fim_Turno_noturno))
        
        if self.fim > um_dia:
            intervalos_noturnos.append(IntervaloTempo(um_dia + Inicio_Turno_noturno, dois_dias))
            intervalos_noturnos.append(IntervaloTempo(dois_dias, dois_dias + Fim_Turno_noturno))

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
        
        if horario_semanal is None:
            horario_semanal = Horario_Semanal()

        self.ano = ano
        self.mes = mes
        self.horario_semanal = horario_semanal      

    def obter_detalhes_Mensais(self) -> dict:
        total_trabalhado = timedelta()
        total_diurno = timedelta()
        total_noturno = timedelta()
        
        num_dias = calendar.monthrange(self.ano, self.mes)[1]
        data_inicial = date(self.ano, self.mes, 1)

        for i in range(num_dias):
            data_atual = data_inicial + timedelta(days=i)
            dia_semana_enum = Dias_Semana.data_para_enum(data_atual)
            horario_do_dia = self.horario_semanal.horarios[dia_semana_enum]

            if horario_do_dia:
                total_trabalhado += horario_do_dia.tempo_trabalhado()
                total_diurno += horario_do_dia.calcular_tempo_diurno()
                total_noturno += horario_do_dia.calcular_tempo_noturno()
        
        return {
            "trabalhado": total_trabalhado,
            "diurno": total_diurno,
            "noturno": total_noturno
        }
    
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
                dia_semana_atual = Dias_Semana.data_para_enum(data_atual)
                horario_do_dia = self.horario_semanal.horarios[dia_semana_atual]

                if horario_do_dia:
                    detalhes_dict[num_semana].append({
                        "data": data_atual,
                        "dia_semana": dia_semana_atual.name,
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
                horario_do_dia = self.horario_semanal.horarios[Dias_Semana.data_para_enum(data_atual)]

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

class FuncionarioHorario:
    def __init__(self, horario_semanal_base: Horario_Semanal):
        self.horario_semanal_base = horario_semanal_base
        self.horarios_especificos = {}
        self.registros_diarios = {}
        
        self._horario_mensal_atual = None
        self._mes_atual = None
        self._ano_atual = None

    @property
    def horario_mensal(self) -> Horario_Mensal:
        mes = datetime.now().month
        ano = datetime.now().year
        
        if (self._horario_mensal_atual is None or 
            self._mes_atual != mes or 
            self._ano_atual != ano):
            self._horario_mensal_atual = Horario_Mensal(ano, mes, self.horario_semanal_base)
            self._mes_atual = mes
            self._ano_atual = ano
        
        return self._horario_mensal_atual
    
    def obter_horario_mensal(self, mes: int = None, ano: int = None) -> Horario_Mensal:
        if mes is None:
            mes = datetime.now().month
        if ano is None:
            ano = datetime.now().year
        
        if (self._horario_mensal_atual and 
            self._mes_atual == mes and 
            self._ano_atual == ano):
            return self._horario_mensal_atual
        
        return Horario_Mensal(ano, mes, self.horario_semanal_base)

    def definir_horario_especifico(self, data: date, horario: Horario):
        self.horarios_especificos[data] = horario

    def _obter_horario_previsto_para_data(self, data: date) -> Horario:
        if data in self.horarios_especificos:
            return self.horarios_especificos[data]
        
        dia_semana_enum = Dias_Semana.data_para_enum(data)
        horario = self.horario_semanal_base.horarios.get(dia_semana_enum)
        
        if horario is None:
            return None
        
        return horario

    def registrar_ponto(self, data: date, inicio_real_str: str, fim_real_str: str, pausas_reais: list = None):
        horario_previsto = self._obter_horario_previsto_para_data(data)
        if not horario_previsto:
            return

        inicio_hm = HoraMinuto.init_com_str(inicio_real_str)
        fim_hm = HoraMinuto.init_com_str(fim_real_str)
        
        intervalo_real = IntervaloTempo.init_com_HoraMinuto(inicio_hm, fim_hm)
        
        horario_real = Horario(intervalo_real, pausas_reais)
        
        self.registros_diarios[data] = {
            "previsto": horario_previsto,
            "real": horario_real
        }

    def calcular_diferencas(self, data: date) -> dict:
        if data not in self.registros_diarios:
            return None

        registro = self.registros_diarios[data]
        horario_previsto = registro["previsto"]
        horario_real = registro["real"]

        if horario_previsto is None:
            return None

        atraso = horario_real.inicio - horario_previsto.inicio
        if atraso < timedelta(0):
            atraso = timedelta(0)

        tempo_trabalhado_real = horario_real.tempo_trabalhado()
        tempo_trabalhado_previsto = horario_previsto.tempo_trabalhado()
        tempo_extra = tempo_trabalhado_real - tempo_trabalhado_previsto

        return {
            "data": data.strftime('%d/%m/%Y'),
            "atraso": atraso,
            "tempo_extra": tempo_extra,
            "tempo_trabalhado_previsto": tempo_trabalhado_previsto,
            "tempo_trabalhado_real": tempo_trabalhado_real
        }
    
    def obter_resumo_mensal(self, mes: int = None, ano: int = None) -> dict:
        if mes is None:
            mes = datetime.now().month
        if ano is None:
            ano = datetime.now().year
        
        horario_mensal = self.obter_horario_mensal(mes, ano)
        
        totais_previstos = horario_mensal.obter_detalhes_Mensais()
        
        horas_reais = timedelta(0)
        horas_diurnas_reais = timedelta(0)
        horas_noturnas_reais = timedelta(0)
        num_dias_com_registro = 0
        
        data_inicial = date(ano, mes, 1)
        num_dias = calendar.monthrange(ano, mes)[1]
        
        for i in range(num_dias):
            data_atual = data_inicial + timedelta(days=i)
            
            if data_atual in self.registros_diarios:
                registro = self.registros_diarios[data_atual]
                horario_real = registro["real"]
                
                horas_reais += horario_real.tempo_trabalhado()
                horas_diurnas_reais += horario_real.calcular_tempo_diurno()
                horas_noturnas_reais += horario_real.calcular_tempo_noturno()
                num_dias_com_registro += 1
        
        return {
            "mes": mes,
            "ano": ano,
            "previstos": totais_previstos,
            "reais": {
                "trabalhado": horas_reais,
                "diurno": horas_diurnas_reais,
                "noturno": horas_noturnas_reais
            },
            "diferenca": horas_reais - totais_previstos["trabalhado"],
            "dias_com_registro": num_dias_com_registro
        }

def formatar_timedelta(td: timedelta) -> str:
    if td is None:
        return "0:00:00"
    
    sinal = ""

    if td < timedelta(0):
        sinal = "-" 
         
    return f"{sinal}{abs(td)}"