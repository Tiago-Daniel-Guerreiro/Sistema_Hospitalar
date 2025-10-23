
from enum import Enum, auto

class Cargo(Enum):
    class Administrativo(Enum):
        Coordenador = auto()
        Gestor = auto()
        Diretor = auto()   

    class Apoio(Enum):
        Rececionista = auto()
        Auxiliar = auto()
        PessoalGeral = auto()

    class Saude(Enum):
        Fisioterapeuta = auto()
        Nutricionista = auto()
        Enfermeiro = auto()
        Farmaceutico = auto()

        class Medico(Enum):
            Geral = auto()
            Anestesiologia = auto()
            Cardiologia = auto()
            CirurgiaGeral = auto()
            Dermatovenereologia = auto()
            Endocrinologia = auto()
            Gastrenterologia = auto()
            GinecologiaObstetricia = auto()
            MedicinaGeralFamiliar = auto()
            MedicinaInterna = auto()
            Neurologia = auto()
            Ortopedia = auto()
            Pediatria = auto()
            Psiquiatria = auto()
            Radiologia = auto()
            Urologia = auto()

Cargo.Saude.Medico.Geral