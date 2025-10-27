Relatório do Sistema Hospitalar da diciplina de Programação de Sistemas de Informação Módulo 11 para o Curso Técnico De Gestão e Programação De Sistemas Informáticos 

Professor: Breno Sousa 
Alunos: Rafael Belchior e Tiago Guerreiro 
Data: 26/10/2025 

# 1. Introdução
## 1.1. Contextualização do Projeto
Este relatório descreve o desenvolvimento de um Sistema de Gestão Hospitalar, um projeto prático realizado para a diciplina de Programação e Sistemas de informação. O sistema foi implementado inteiramente em Python e é usado através de uma interface de linha de comandos.

O tema do projeto foi proposto pelo professor e comum a todos os alunos, servindo como um caso de estudo para aplicar e explorar os conhecimentos ensinados em aula. A abordagem do nosso grupo foi a de criar a versão mais completa e detalhada possível, para isso demos um especial foco ás operações como o registo de pacientes, a gestão de diferentes tipos de funcionários, a alocação de salas e, especialmente, uma complexa gestão de horários e pagamentos.

Esta ambição, no entanto, foi confrontada com a limitação de tempo. Como resultado, embora o sistema seja funcionalmente rico, algumas decisões de design levaram a um maior acoplamento entre certos componentes, um compromisso que será refletido e detalhado ao longo do relatório. Para manter o foco nos objetivos de aprendizagem, o projeto foi desenvolvido de forma local, sem recorrer a bases de dados externas, com todos os dados geridos em memória.


## 1.2. Objetivos
Para alcançar a complexidade desejada e cumprir as exigências da unidade curricular, o objetivo principal foi demonstrar a aplicação prática dos seguintes conceitos obrigatórios de POO:

Classes Abstratas: Utilizar classes abstratas para definir "moldes" ou contratos para outras classes, como foi feito para Pessoa e Sala.
Herança Simples e Múltipla: Criar uma hierarquia de classes, usando herança simples para especializar tipos (como um Medico que é um tipo de Funcionario) e herança múltipla para combinar papéis (como no caso do EnfermeiroChefe).
Polimorfismo: Permitir que o sistema interagisse com objetos de diferentes classes através de uma interface comum. Este princípio é central na arquitetura, visível na capacidade da classe SistemaHospital de gerir todos os funcionários (Medico, Enfermeiro, etc.) numa única coleção, tratando-os de forma homogénea como Funcionario. Adicionalmente, foi aplicado na sobrescrita de métodos como __str__ para que personalizar a exibição de cada tipo de pessoa e na implementação do cálculo de pagamentos, onde diferentes regras são executadas através da mesma chamada ao método calcular().
Encapsulamento: Proteger os dados internos das classes, usando properties e setters para controlar o acesso e validar informações, como garantir que uma idade não seja negativa.
Modularização: Organizar o código em ficheiros separados (Program.py, Horario.py, Console.py), dividindo o projeto em partes lógicas: o modelo de dados, o sistema de horários e a interface do utilizador.

Em resumo, o objetivo foi construir um programa funcional que, fosse o mais detalhado/completo possivel, do modo a demonstrar o máximo do nosso conhecimento.


## 2. Desenvolvimento e Implementação
A secção seguinte apresenta em detalhe o código que constitui o Sistema de Gestão Hospitalar. A análise será feita de forma estruturada, seguindo a organização dos ficheiros descrita anteriormente (Program.py, Horario.py, e Console.py), para facilitar a compreensão de como cada módulo contribui para o funcionamento do projeto.

A apresentação seguirá a seguinte ordem:

Program.py (Módulo da lógica principal: Este ficheiro é o coração do sistema. Contém a representação de todas as entidades e conceitos do hospital. Aqui são definidas as estruturas de dados para Pessoa, Paciente, Funcionario, Sala e as suas variantes. Toda a lógica de negócio necessária para esses entidades, como as regras que definem um funcionário ou as ações de uma sala, está nesse módulo.

Horario.py (Módulo da gestão do Tempo): Este módulo foi criado para isolar e gerir toda a complexa lógica relacionada com a manipulação de tempo. Ele lida com a representação de horas, intervalos de tempo, pausas, e o cálculo de horas de trabalho diurnas e noturnas. Ao separar esta funcionalidade, o Módulo da Lógica (Program.py) mantém-se mais limpo e focado.

Console.py (Módulo da interface de linha de comando): Este módulo é a única parte do sistema que interage diretamente com o utilizador. A sua responsabilidade é exibir menus, recolher dados de entrada e fazer as chamadas aos outros módulos. Ele controla como os outros módulos são usados, traduzindo as ações do utilizador em comandos para o Módulo da Lógica, mas sem conter ele próprio a lógica. Esta separação tem como objetivo que se futuramente vá-se substituir a interface por outra seja mais facil, pois a maioria das alterações necessárias podem ser alteradas apenas substituindo este arquivo, mas devido ao tempo não foi possivel separar completamente a lógica da interface de linha de comandos da lógica principal.

Para cada classe analisada, o texto irá descrever o seu propósito, os seus dados principais e a funcionalidade de cada um dos seus métodos, mostrando como as ideias de desenho discutidas anteriormente foram aplicadas na prática.

# 3. Desenvolvimento dos módulos de separação da lógica

# 3.1. Módulo Principal: Módulo Principal (Program.py)
## 3.1.1 Enumerações e Constantes
Para garantir a consistência, legibilidade e manutenibilidade do código no módulo principal, foram definidas constantes globais e enumerações (Enum) centralizando valores fixos e representam estados, evitando o uso de números/strings dispersas pelo código repetidamente.

Constantes Globais
Inicio_Turno_noturno e Fim_Turno_noturno: Definidas como objetos timedelta, estas constantes estabelecem um intervalo de tempo fixo para o que é considerado "turno noturno" em todo o sistema. A sua utilização centralizada é usada para que os cálculos de horas noturnas sejam consistentes.
max_pausas: Uma constante inteira que provavelmente serve como um limite ou parâmetro de configuração para a gestão de pausas nos horários.
Enumerações (Enum)

O uso de Enum promove a segurança de tipos e torna o código legivel

StatusAtendimento: Esta enumeração define os vários estados possíveis de um paciente dentro do atendimento do hospital (ex: Espera, Atendimento). A sua utilização permite um controlo de estado robusto e legível.
StatusSala: Define os estados de disponibilidade de uma sala (ex: Disponivel, Ocupado), facilitando a gestão pelos estados das salas.
Cargo: Esta estrutura é particularmente notável pela sua organização hierárquica. Em vez de uma única e extensa enumeração, Cargo atua como uma classe que agrupa enumerações agrupadas por área de funcionamento (Administrativo, Apoio, Saude). A categoria Saude contém, por sua vez, a enumeração Medico para especialidades médicas. Esta separação organiza os cargos, tornando a seleção de cargos mais intuitiva e estruturada. Mas devido á limitação do tempo não foi possivel adicionar multi-cargos então para o EnfermeiroChefe foi necessário uma lógica manual para a verificação no módulo da interface de linha de comandos.


## 3.1.2. Classe Abstrata Pessoa
A classe Pessoa serve como a base para as representações no sistema de gestão hospitalar, como pacientes e funcionários. Foi projetada como uma classe abstrata, herdando de ABC (Abstract Base Class), o que impede a sua instanciação direta. Esta abordagem garante que qualquer classe use desta representação desta base de pessoa que tem o o mínimo de atributos e comportamentos.

Construtor e Atributos

O construtor __init__ é responsável por inicializar os atributos base comuns a todas as subclasses:

_nome: Uma string que armazena o nome da pessoa.
_idade: Um inteiro que armazena a idade da pessoa.
Ambos os atributos são prefixados com um underscore (_), uma convenção em Python para indicar que são protegidos e que o seu acesso deve ser mediado pela própria classe.

Encapsulamento e Validação de Dados
O acesso e a modificação dos atributos são rigorosamente controlados através de properties e setters, o que permite a integração de regras de validação.

idade:
O setter @idade.setter implementa uma regra de validação crucial: a idade só pode ser atualizada se o novo valor for positivo e inferior a 100. Esta validação previne dados inconsistentes.

Polimorfismo 
O método __str__ é definido como um método abstrato através do @abstractmethod. Esta declaração obriga a que todas as classes que herdem de Pessoa (como Paciente ou Funcionario) implementem a sua própria versão deste método. Esta é um uso de polimorfismo que assegura que cada tipo de pessoa possa ser representado como uma string de forma distinta e adequada ao seu contexto (por exemplo, um paciente pode exibir o seu número de utente, enquanto um funcionário pode exibir o seu cargo).


## 3.1.3. Classe Paciente
A classe Paciente é uma implementação concreta que herda da classe abstrata Pessoa. Representa um utente do hospital, que tem não só os seus dados pessoais básicos, mas também métodos para aceder ao historico médico. Esta classe é um exemplo claro do princípio da herança simples.

Construtor (__init__) e Atributos
O construtor da classe Paciente usa o construtor da sua classe-mãe, Pessoa.__init__(self, nome, idade), para inicializar os atributos herdados. Adicionalmente, introduz os seguintes atributos específicos:
_numero_utente: Um inteiro que serve como identificador único do paciente no sistema.
status: Utiliza a enumeração StatusAtendimento para guarda o estado atual do paciente no atendimento (ex: aguardando em sala de espera, em atendimento, etc.). Inicializa-se como Sem_Sala.
area_atendimento, sala_atendimento, senha: Atributos utilizados para gerir o local e a ordem de chamada do paciente..

Implementação de Polimorfismo (__str__)
A classe Paciente fornece uma implementação concreta para o método abstrato __str__, herdado de Pessoa. Esta é uma demonstração de polimorfismo, permitindo que um objeto do tipo Paciente tenha uma representação específica. Em vez de apenas listar nome e idade, este método gera um relatório detalhado que inclui o número de utente, o status atual e, interagindo com a classe SistemaHospitalar para obter e exibir o histórico completo de atendimentos e os funcionários que os realizaram.

Encapsulamento e Validação de Dados (numero_utente)
A property @numero_utente não expõe diretamente o valor inteiro. Em vez disso, formata-o sempre como uma string de 9 dígitos com zeros à esquerda (f"{self._numero_utente:09d}"). Esta abstração garante um formato de exibição consistente em todo o sistema, independentemente da forma como o dado é armazenado internamente.
O setter @numero_utente.setter implementa uma regra de validação que assegura que o número de utente se encontra dentro de um intervalo válido (entre 0 e 999.999.999), protegendo a integridade dos dados e prevenindo a atribuição de valores incorretos.

Métodos Adicionais e Gestão de Histórico
A classe inclui métodos auxiliares para gerir o ciclo de vida do paciente no hospital:
atribuir_senha(senha, area_nome): Método que associa uma senha de atendimento e uma área ao paciente, o que é fundamental para que o cliente possa ser atendido.
historico_medico_Ids e obter_historico_medico_id(id_historico): Estes métodos trabalham em conjunto para fornecer acesso ao histórico médico. A property historico_medico_Ids formata uma lista de todos os registos, enquanto obter_historico_medico_id recupera um registo específico. A sua funcionalidade depende da colaboração com a classe SistemaHospitalar, o que mostra interação entre diferentes componentes do sistema.


## 3.1.4. Classe Base Funcionario
A classe Funcionario, que herda diretamente de Pessoa, serve como a classe base para todos os tipos de profissionais do hospital, como médicos, enfermeiros e pessoal administrativo. Ela expande a classe de Pessoa adicionando atributos e comportamentos específicos do contexto profissional, como salário, cargo, gestão de horários e cálculo do salário.

Construtor (__init__) e Atributos
O construtor usa do inicializador da classe Pessoa.__init__ para os atributos nome e idade e adiciona os atributos esenciais para a gestão de um funcionário:
_numero_funcionario: Identificador único do funcionário.
_salario_base: Armazena o salário base. Notavelmente, a atribuição max(0, salario) no construtor garante que o salário nunca pode ser um valor negativo, reforçando a integridade dos dados.
_cargo: Um objeto do tipo Cargo que define a função do funcionário.
horario_semanal: Um objeto Horario_Semanal que define o horário padrão.
horario_funcionario: Instancia um objeto FuncionarioHorario. A classe Funcionario não tem nenhuma lógica do horário pois esta variável é que tem toda lógica complexa de gestão de horários, registo de ponto e cálculo de horas trabalhadas, o que mostra separação de responsabilidades e um uso dos módulos
atendimentos_realizados: Uma lista para armazenar um registo de todos os atendimentos efetuados.
regras_pagamento: Uma lista que é inicializada com a RegraSalarioBase, permitindo que o cálculo de pagamento seja dinamicamente extensível adicionando outras regras.

Implementação de Polimorfismo (__str__)
O Funcionario implementa o método __str__ para fornecer uma representação  detalhada. Este método polimórfico não se limita a dados pessoais, mas invoca outros métodos internos (obter_atendimentos e calcular_pagamento) para gerar uma exibição completa, incluindo cargo, salário e um resumo dos últimos atendimentos.

Encapsulamento e Acesso a Dados
O encapsulamento é mantido através de properties de acesso apenas de leitura (@property sem setter) para atributos essenciais como numero_funcionario, salario, cargo e salario_base. Esta abordagem protege os dados de modificações externas que não sigam as regras de validação.

Cálculo de Pagamento Flexível
O sistema do salário é um dos aspetos mais complexos da classe:
adicionar_regra_pagamento(regra): Este método permite adicionar dinamicamente novas regras de cálculo ao funcionário (ex: bónus por atendimentos, pagamento de horas noturnas). Isso torna o sistema extensível sem necessidade de alterar o código da classe Funcionario.
calcular_pagamento(...): Este método controla o cálculo. Ele junta o contexto necessário (mês, ano, horas trabalhadas, número de atendimentos) e, em seguida, faz um loop pela lista das regras_pagamento, chamando o método calcular() de cada RegraDePagamento. O funcionário não precisa de saber como cada componente do salário é calculado; ele apenas deixa essa responsabilidade aos objetos correspondentes.

Gestão de Horários
O sistema de Horários também é um dos aspetos mais complexos da classe:
registrar_ponto(...), definir_horario_especifico(...) e calcular_diferenca_diaria(...): Estes métodos atuam como uma fachada, simplesmente reencaminhando as chamadas para os métodos correspondentes no objeto self.horario_funcionario. Esta estrutura mantém a classe Funcionario focada na sua responsabilidade principal, enquanto a lógica de horários é mantida em uma classe especificamente feita para isso.

Gestão de Atendimentos
registrar_atendimento(...) e obter_atendimentos(): Métodos que gerem a lista de atendimentos realizados pelo funcionário.
obter_resumo_horas_mes(...) e listar_registros_ponto_mes(...): Métodos que transformam os dados de uma resultado para que possam ser usados facilmente. Eles junta dados obtidos do objeto horario_funcionario com dados próprios da classe (como o número de atendimentos) para produzir relatórios mensais detalhados sobre o funcionário.


## 3.1.5. Subclasses de Funcionario: Medico, Enfermeiro, Administrativo
Para representar os diferentes papéis profissionais dentro do hospital, foram criadas subclasses especializadas que herdam da classe base Funcionario. Cada uma destas subclasses (Medico, Enfermeiro, Administrativo) é um exemplo de herança simples e especialização, adicionando atributos e comportamentos específicos ou modificando os herdados para se adequarem ao seu contexto.

Classe Medico
A classe Medico representa um profissional médico e especializa a classe Funcionario das seguintes formas:

Construtor (__init__): O construtor usa o inicializador da classe-mãe (Funcionario.__init__) para inicializar os atributos comuns. A principal adição é a configuração de uma regra de pagamento específica: através do método adicionar_regra_pagamento, uma instância de RegraBonusPorAtendimento é automaticamente adicionada a cada objeto Medico. Esta ação demonstra como as subclasses podem personalizar o comportamento herdado (neste caso, o sistema de cálculo de pagamento). O parâmetro especialidade, do tipo Cargo, é um cargo mas como o médico tem as suas especialidade mas não havia tempo suficiente a opção que tomamos foi usar como se fosse um cargo apenas usando outro nome nos parametros e na exibição confiando que seria uma especialidade do médico, mas futuramente poderiamos fazer um enum proprio para o caso.

Polimorfismo (__str__): O método __str__ é sobrescrito para fornecer uma representação mais adequada a um médico. Ele altera o tratamento para "Dr./Dra." e destaca informações como a "Especialidade" e o valor do bónus por atendimento. Este uso é um claro exemplo de polimorfismo, onde a mesma chamada de método (str(objeto)) produz um resultado diferente dependendo do tipo concreto do objeto (Funcionario ou Medico).

Classe Enfermeiro
A classe Enfermeiro constitui uma especialização da classe Funcionario, criada através do mecanismo de herança simples. O seu propósito é modelar as responsabilidades e características específicas do pessoal de enfermagem dentro da estrutura do hospital.

Análise do Construtor (__init__):
A classe implementa uma regra de negócio automatizada para a definição do atributo _turno. Em vez de ser um parâmetro de entrada, o seu valor ("dia" ou "noite") é defindo com base no horário. O método analisa o objeto horario_semanal e, através da chamada a calcular_totais_semanais(), compara o total de horas diurnas e noturnas para determinar qual é o turno com mais horas.
O construtor usa da lógica dos pagamentos do Funcionario. Se o turno for determinado como "noite", uma nova instância de RegraBonusFixo é adicionada à lista de regras de pagamento do funcionário. Esta abordagem exemplifica a personalização da lógica do programa.

Análise do Polimorfismo (__str__):
A classe apresenta uma implementação do método __str__, que sobrescreve o comportamento da classe Funcionario. O resultado é uma representação, que inclui um tratamento formal ("Enfermeiro(a)"), a indicação do turno e a exibição condicional de um "Bónus Noturno".
A chamada ao método self.calcular_pagamento() dentro da formatação da string assegura que o salário total apresentado ao utilizador é o valor final, já processado com todas as regras de pagamento aplicáveis, incluindo os bónus.

Análise do Encapsulamento (turno):
O atributo _turno é obtido apenas para leitura através da property @turno, e a unica forma de altera-lo é editando o horario semanal esta lógica previne modificações externas e garante que o turno do enfermeiro permanece corresponda aos valores do horário de trabalho.

Classe Administrativo
A classe Administrativo é outra especialização da classe base Funcionario, implementada através de herança simples. Ela define a base para os funcionários do setor administrativo do hospital, que, embora não estejam diretamente envolvidos no atendimento clínico, possuem as suas próprias regras de negócio e atributos específicos.

Análise do Construtor (__init__):
O construtor inicializa o objeto chamando Funcionario.__init__. O cargo é fixado como Cargo.Administrativo.Coordenador, garantindo a correta categorização do funcionário dentro do sistema.
São inicializados atributos específicos desta classe: setor (uma string que descreve a área de atuação, como "Finanças" ou "Recursos Humanos") e horas_registradas (um valor numérico para registo de horas).
De forma semelhante à classe Medico, o construtor personaliza o sistema de remuneração. Através do método self.adicionar_regra_pagamento(), é adicionada RegraPagamentoPorHora. Esta ação demonstra, mais uma vez, a aplicação da lógica de pagamento, onde as classes que heram o funcionário podem definir as proprias lógicas do cálculo do pagamento .

Análise do Polimorfismo (__str__):
O método __str__ é sobrescrito para fornecer uma representação detalhada e adequada ao contexto administrativo, um claro exemplo de polimorfismo. A string resultante inclui informações pertinentes como o setor, o cargo específico, o salário base e o valor do pagamento por hora.
O valor de pagamento['total_a_pagar'] na saída é o resultado do cálculo final da remuneração, definido pela soma do resultado de todo método calcular_pagamento() de todas as regras de pagamento.
Esta classe, em conjunto com as outras subclasses de Funcionario, motram como a lógica está bem separada. As responsabilidades comuns são centralizadas na classe base, enquanto as especificidades de cada papel profissional são definidas nas suas respetivas subclasses, reutilizando código e mantendo uma separação clara.


## 3.1.6. Herança Múltipla: Classe EnfermeiroChefe
A classe EnfermeiroChefe é atualmente o unico caso de herança múltipla no projeto. Ao herdar simultaneamente de Enfermeiro e Administrativo, esta classe cria um novo tipo de funcionário que combina as competências clínicas de um com as responsabilidades de gestão do outro.

Análise do Construtor (__init__) e Gestão da Herança Múltipla:
O construtor da classe demonstra uma abordagem cuidadosa para lidar com uma herança onde EnfermeiroChefe herda de duas classes que, por sua vez, herdam de uma mesma base, Funcionario. Para evitar a inicialização duplicada e conflituosa da classe Funcionario, o construtor usa do Construtor do Enfermeiro.__init__(...) primeiro. Esta chamada garante que toda a cadeia de inicialização até Pessoa é executada corretamente uma única vez, configurando os atributos de base e a lógica específica do enfermeiro (como a determinação do turno).
Em seguida, o construtor inicializa manualmente os atributos que são da classe Administrativo (self.setor e self.horas_registradas). Esta lógica serve para evitar problemas e simplificar a lógica.
A classe é um bom exemplo da junção de diversas regras de pagamento. Ela não só herda as regras que são definidas pelo Construtor do Enfermeiro (como o bónus noturno), mas também adiciona múltiplas novas regras (RegraBonusPorAtendimento, RegraBonusPercentual, RegraPagamentoPorHora). O resultado é um funcionário com o sistema de remuneração mais complexo do sistema.

Análise do Polimorfismo (__str__):
O método __str__ é novamente sobrescrito de forma polimórfica para criar uma representação que lida com a lógica tanto do Enfermeiro tanto do Administrativo.
A sua implementação é um espelho da sua herança: exibe informações provenientes do seu lado Enfermeiro (o turno), do seu lado Administrativo (o setor) e do seu papel de chefia (a listagem de múltiplos bónus).
Ao apresentar o "Salário Total", o método demonstra o resultado final, onde o método calcular_pagamento (herdado de Funcionario) processa a lista acumulada de todas as regras de pagamento para chegar a um valor final, encapsulando toda a complexidade do cálculo.

## 3.1.7. Regras de Pagamento
O cálculo da remuneração dos funcionários é implementado tendo uma classe abstrata demodo a que todas as regras possam ser tratadas da mesma forma. Esta abordagem permite que o método de calcular o pagamento de um funcionário seja definido sem depender de uma forma fixa. O sistema é desenhado para ser extensível, permitindo a adição de novas formas de cálculo (bónus, comissões, etc.) sem modificar o código da classe Funcionario.

A Interface da Estratégia: RegraDePagamento
A classe abstrata RegraDePagamento serve como o contrato ou a interface para todas as estratégias de cálculo.
Ela define um único método abstrato, calcular(funcionario, contexto), que obriga todas as subclasses concretas a implementar a sua própria lógica de cálculo. O método recebe o objeto funcionario sobre o qual opera e um dicionário de contexto para dados adicionais (como mês e ano), tornando a regra flexível.

Implementações Concretas (As Estratégias)
Cada classe a seguir é uma estratégia concreta que implementa a interface RegraDePagamento:
RegraSalarioBase: A estratégia mais fundamental. Simplesmente retorna o salario_base do funcionário. É a regra inicial para todos os funcionários.
RegraBonusFixo: Uma estratégia configurável que adiciona um valor monetário fixo. O valor do bónus é passado no seu construtor, permitindo a criação de diferentes bónus fixos (ex: bónus noturno, bónus de assiduidade).
RegraBonusPorAtendimento: Implementa uma lógica de negócio mais complexa. Esta regra:
Verifica se o funcionário é de um tipo elegível (Medico ou EnfermeiroChefe) através de isinstance.
Utiliza o dicionário contexto para filtrar os atendimentos realizados apenas no mês e ano especificados, demonstrando como as estratégias podem usar dados contextuais.
Calcula o bónus multiplicando o número de atendimentos elegíveis por um valor fixo, definido no seu construtor.
RegraPagamentoPorHora: Similarmente, esta regra aplica-se apenas a tipos de funcionários específicos (Administrativo e EnfermeiroChefe) que possuem o atributo horas_registradas. Ela calcula um pagamento com base no número de horas multiplicado por um valor/hora definido no seu construtor.
RegraBonusPercentual: Calcula um bónus como uma percentagem do salário base do funcionário. A percentagem é configurada no construtor da regra, permitindo a criação de bónus de liderança ou de desempenho variáveis.
A combinação destas regras, adicionadas dinamicamente à lista regras_pagamento de cada objeto Funcionario, permite a construção de sistemas de remuneração altamente personalizados e complexos de forma modular e limpa.


## 3.1.8. Hierarquia de Salas (Sala, SalaAtendimento, SalaEspera, SalaCirurgia)
A gestão dos espaços físicos do hospital é modelada através de uma hierarquia de classes, iniciada pela classe abstrata Sala. Esta abordagem de herança permite definir um comportamento e atributos comuns a todas as salas, enquanto as subclasses concretas implementam as funcionalidades específicas para cada tipo de espaço (atendimento, espera, cirurgia, etc.), aplicando os princípios de polimorfismo e especialização.

Classe Abstrata Sala

A classe Sala serve como a base para todos os tipos de salas no sistema.

Propósito e Abstração: Sendo uma Classe Base Abstrata (ABC), Sala não pode ser instanciada diretamente. A sua função é garantir que qualquer objeto que represente uma sala no hospital partilhe um conjunto mínimo de características, formalizando a estrutura do modelo.
Construtor e Atributos: O construtor __init__ inicializa os atributos usados em todas as salas: id_sala (identificador único), nome e capacidade.
Método Abstrato e Polimorfismo: O método detalhar_sala é definido com o decorador @abstractmethod. Isto obriga a que todas as subclasses concretas forneçam a sua própria implementação deste método, o que é uma aplicação direta de polimorfismo. Garante-se, assim, que cada tipo de sala pode ser "descrito" de uma forma adequada à sua função específica.

Classe SalaAtendimento
Esta classe é uma implementação concreta que herda de Sala e modela uma sala de consulta ou exame.

Construtor e Especialização: O construtor usa do construtor da Sala (Sala.__init__) para os atributos base e introduz atributos de estado que especializam a sua função:
funcionarios: Uma lista para associar o pessoal clínico (Médicos, Enfermeiros) que pode usar a sala.
paciente_atual e funcionario_atual: Armazenam o estado da ocupação em tempo real.
status: Utiliza a enumeração StatusSala para um controlo de estado claro (Disponivel, Ocupado).
atendimentos_realizados: Um registo de histórico específico da sala.
detalhar_sala: A classe implementa este método que é um método abstrato da classe sala, ele cria uma descrição detalhada, incluindo o seu status atual e, se aplicável, o paciente e o funcionário que a ocupam.

Encapsulamento de Lógica de Negócio: Os métodos desta classe juntam as regras da lógica de atendimento:
adicionar_funcionario e remover_funcionario: Gerem a lista de pessoal autorizado, incluindo uma validação de negócio importante: através de isinstance(funcionario, Administrativo), o método proíbe a associação de funcionários administrativos a salas de cariz clínico.
chamar_paciente: Orquestra o início de um atendimento. Este método é um exemplo de interação entre objetos: ele verifica e altera o status da própria sala, altera o status do objeto Paciente e estabelece as ligações entre sala, paciente e funcionario.
finalizar_atendimento: Finaliza de uma consulta, deixando a lógica principal disso para o método self.funcionario_atual.registrar_atendimento(), fazendo o objeto Funcionario atualizar o seu próprio registo. Em seguida, atualiza o seu próprio histórico e redefine o estado da sala para Disponivel, preparando-a para o próximo atendimento.

Classe SalaEspera
Esta classe, herda de Sala, modela uma área de espera e funciona como um centro que centraliza a lógica de receber os pacientes e gerir a fila de espera e encaminhando os pacientes para as salas de atendimento disponíveis.

Gestão de Estado: O construtor define os atributos necessários para esta Sala para além dos atributos base da classe Sala:
salas_atendimento: Uma lista que armazena as SalaAtendimento, que são adicionados pelo método adicionar_sala_atendimento.
fila_espera: Uma lista de Paciente que funciona como uma fila que ao entrar o paciente vai para o fim.
contador_senhas e prefixo_senha: Atributos para a criação de senhas sequenciais e únicas.
Implementação Polimórfica (detalhar_sala): O método cria a lógica que a Sala "pede" ao ter abstractmethod. Fornecer uma descrição com o estado, número de pacientes em espera, número de salas de atendimento associadas e total de senhas já atribuidas.
Lógica de atendimentos: Os métodos desta classe fazem os objetos de Paciente, Funcionario e Sala de atendimento interagirem:
pegar_senha: Este método inicia a jornada do paciente na área de atendimento. Ele cria uma senha, e chama o método atribuir_senha do Paciente para atualizar o seu estado e, em seguida, adiciona o paciente à sua fila_espera interna.
chamar_proximo: Este é o método principal da classe. Ele faz um loop pela salas_atendimento, procurando alguma que tenha o status "Disponível". Ao encontrar uma, ele remove o primeiro paciente da fila e delega a responsabilidade da chamada ao método chamar_paciente do objeto SalaAtendimento apropriado. 
mostrar_painel: Simula um painel de chamadas, agregando e exibindo informações de estado de múltiplos objetos: o status de cada SalaAtendimento vinculada e a própria fila_espera.

Classe SalaCirurgia
A classe SalaCirurgia é outra especialização de Sala, projetada para o contexto específico de procedimentos cirúrgicos, com um conjunto de regras e funcionalidades distintas.

Construtor e Atributos Específicos: O construtor, além de chamar o da classe base, adiciona o atributo equipamentos, uma lista de strings para catalogar os equipamentos disponíveis na sala.
Encapsulamento de Lógica de Negócio (operar): O método principal, operar, para além disso tem uma regra que faz com que apenas funcionários do tipo EnfermeiroChefe ou Medico podem ser designados como chefes de uma operação, validação essa que é feita através de isinstance. Este método também demonstra a delegação de responsabilidade, pois invoca chefe_operacao.registrar_atendimento(), atribuindo ao objeto Funcionario a tarefa de registar o procedimento no seu próprio histórico.
Implementação Polimórfica (detalhar_sala): A implementação deste método para a SalaCirurgia é um exemplo claro de polimorfismo. Em vez de mostrar o status de ocupação como uma sala de atendimento, a sua descrição foca-se em listar os equipamentos disponíveis.


## 3.1.9. Classe Orquestradora: SistemaHospital
A classe SistemaHospital é o ponto central de controlo de toda a aplicação. Gerindo os dados em memória.

Gestão Centralizada de Dados em Memória

A principal função da SistemaHospital é gerir a interação entre as variáveis/Classes do sistema.

Estrutura de Dados: O construtor __init__ estabelece a base para esta gestão ao inicializar um conjunto de dicionários. A escolha por dicionários permite um acesso rápido e eficiente a qualquer objeto através de uma chave única:
self.pacientes: Utiliza o número de utente como chave, permitindo a recuperação imediata de qualquer paciente.
self.funcionarios: Usa o número de funcionário como chave, facilitando a gestão do pessoal.
self.salas_espera e self.salas_cirurgia: Indexam as salas pelo seu nome, o que é mais intuitivo para as operações do utilizador.
Controlo de Identidade: A classe assume a responsabilidade pela geração de identificadores únicos para os pacientes através do atributo _proximo_numero_utente. Separar este contador, a SistemaHospital garante que não haverá repetições de identificadores durante a criação de novos pacientes.

Interface Simplificada

Criação de Entidades (Padrão Factory Simples):
registrar_paciente: Este método pode funcionar tanto com a variável ddo paciente tanto com os dados.
criar_area_especializada: Este é um bom exemplo do padrão Factory. Com uma única chamada, o método orquestra um processo de configuração de múltiplos passos: (1) instancia um objeto SalaEspera; (2) cria múltiplos objetos SalaAtendimento; e (3) estabelece a relação entre a sala de espera e as suas salas de atendimento através do método adicionar_sala_atendimento. O cliente que invoca este método não precisa de conhecer estes detalhes.
Recuperação e Interação:
obter_paciente e obter_funcionario: Fornecem um ponto de acesso único aos dados. A lógica de formatação do número de utente em obter_paciente está aqui centralizada, garantindo consistência.
gerar_relatorio_funcionario e gerar_relatorio_paciente: Estes métodos são uma demonstração do uso de polimorfismo a partir de uma classe gestora. A SistemaHospital não contém nenhuma lógica condicional para verificar o tipo de funcionário (Medico, EnfermeiroChefe, etc.). Ela confia no contrato estabelecido pela classe Pessoa, que obriga todas as subclasses a implementar o método __str__. Ao invocar str(funcionario), o Python seleciona a implementação correta do método, resultando num código mais limpo e extensível.

# 3.2. Módulo de Gestão de Horários (Horario.py)
O ficheiro Horario.py constitui um módulo especializado e altamente coeso, cuja única responsabilidade é modelar e gerir todos os aspetos relacionados com a gestão do tempo, horários de trabalho e registos de ponto. A sua modularização é um exemplo claro de separação de responsabilidades, pois isola a complexa lógica temporal do módulo principal (pacientes, funcionários), permitindo que a classe Funcionario deixe essas tarefas para este módulo ao invés de as implementar internamente.

## 3.2.1. Enumeração Dias_Semana
No topo do módulo, a enumeração Dias_Semana serve como uma estrutura de dados fundamental para a representação dos dias da semana, sendo mais legivel e facilitando a lógica, substituindo a utilização de números inteiros (0-6) diretamente no código.

Definição e Valores: A enumeração define os nomes de dias (ex: Domingo, Segunda) associando-os aos valores inteiros correspondentes, seguindo uma convenção onde Domingo é 0 e Sábado é 6.

Polimorfismo e Reutilização de Métodos Especiais:

__str__(): Ao sobrescrever este método especial, a enumeração garante que, ao ser convertida para uma string (ex: str(Dias_Semana.Segunda)), o resultado seja o nome do membro ("Segunda"), e não a representação padrão, tornando a sua utilização em relatórios e saídas de texto mais intuitiva.
__int__(): A sobrescrita deste método permite que um membro da enumeração possa ser utilizado diretamente em contextos numéricos (ex: int(Dias_Semana.Segunda)), retornando o seu valor inteiro (1).

Método Utilitário Estático:
data_para_enum(data): Este método estático (@staticmethod) é um convertor. Ele recebe um objeto date do Python e converte o resultado do método .weekday() (que segue a convenção Segunda=0 a Domingo=6) para a conversão utilizada pela enumeração (Domingo=0). Este método centraliza a conversão, evitando a duplicação desta lógica em outras partes do sistema e tornando a interação entre objetos date e a enumeração Dias_Semana simples e livre de erros.


## 3.2.2. Classes Utilitárias de Tempo: HoraMinuto e IntervaloTempo
Para manipular unidades de tempo de forma mais abstrata e segura, o módulo implementa classes utilitárias especializadas. A primeira e mais fundamental é a HoraMinuto.

Classe HoraMinuto

A classe HoraMinuto é uma abstração que representa um ponto específico no tempo dentro de um dia de 24 horas, desvinculado de uma data específica. O seu principal objetivo é fornecer uma forma robusta e conveniente de lidar com horas e minutos, oferecendo validação de dados, múltiplos métodos de construção e suporte a operações de comparação.

Construtor (__init__) e Validação de Dados:

O construtor principal recebe hora e minuto como inteiros.
Crucialmente, ele aplica uma lógica de validação e saneamento de dados no momento da atribuição. As expressões max(min(valor, LIMITE), 0) garantem que a hora seja sempre confinada ao intervalo [0, 23] e o minuto ao intervalo [0, 59], prevenindo a criação de objetos com estados inválidos (ex: hora 25 ou minuto -10).
Métodos de Fábrica Alternativos (@classmethod):

A classe demonstra um uso de métodos de classe (@classmethod) para fornecer construtores alternativos. Isso permite que um objeto HoraMinuto seja criado a partir de diferentes tipos de dados de forma intuitiva:
init_com_str(cls, hora_minuto_str): Converte uma string no formato "HH:MM" para um objeto HoraMinuto.
init_com_datetime(cls, dt): Extrai a hora e o minuto de um objeto datetime do Python.
init_com_deltatime(cls, dt): Converte um objeto timedelta para a sua representação em HoraMinuto.
Esta abordagem melhora significativamente a usabilidade da classe, pois o código cliente pode escolher o método de construção mais conveniente para a sua situação, em vez de realizar a conversão manualmente.

Interoperabilidade e Conversão:
O método obter_timedelta() serve como uma ponte para o tipo timedelta do Python, retornando a representação do objeto HoraMinuto como uma duração a partir da meia-noite. Esta conversão é a base para as operações de comparação.

Sobrescrita de Métodos Especiais:
__str__(): Sobrescrito para fornecer uma representação formatada e padronizada (ex: "09:05"), facilitando a sua exibição.
__lt__, __le__, __eq__: A sobrescrita destes operadores de comparação (<, <=, ==) é um exemplo de subscrita de operadores. Em vez de comparar os atributos hora e minuto manualmente, a lógica é feita pela comparação dos objetos timedelta correspondentes. Isso permite que duas instâncias de HoraMinuto sejam comparadas de forma natural e intuitiva no código (ex: if hora_inicio < hora_fim:), aumentando a legibilidade.

Classe IntervaloTempo
A classe IntervaloTempo baseia-se na abstração HoraMinuto (e nos tipos timedelta do Python) para modelar um período de tempo contínuo, definido por um início e um fim. Esta classe é fundamental para representar turnos de trabalho, pausas ou qualquer outro evento com duração definida.

Construtor (__init__) e Representação Interna:
O construtor principal armazena o inicio e o fim do intervalo como objetos timedelta. A escolha de timedelta como a representação interna é melhor pois permite é mais detalhada, facilitnado o controle e verificações das durações e intervalos que podem atravessar a meia-noite (ex: um turno das 22:00 às 06:00).

Método de criação (@classmethod) e Lógica de Negócio:
init_com_HoraMinuto(cls, inicio_hm, fim_hm): Este método de classe (@classmethod) funciona como um construtor alternativo e mais intuitivo, aceitando dois objetos HoraMinuto.
Crucialmente, ele detecta e o trata dos intervalos que cruzam a meia-noite. Se a hora de fim (fim_hm) for anterior à hora de início (inicio_hm), o método assume que o intervalo se estende para o dia seguinte e adiciona 24 horas (timedelta(days=1)) ao timedelta de fim. Este método é importante, pois simplifica a criação de turnos noturnos, escondendo a complexidade do tratamento de datas do código cliente.

Métodos de Instância:
duracao_total(): Um método simples que calcula e retorna a duração total do intervalo subtraindo o início do fim. É uma forma simple e legível de obter a duração, em vez de realizar a subtração externamente.
esta_dentro_do_limite(limite): Este método de validação verifica se o intervalo atual está completamente dentro de outro intervalo de limite. É uma função essencial para, por exemplo, garantir que uma pausa ocorre dentro do horário de trabalho.

Método Utilitário Estático (@staticmethod):
intersecao_tempo(intervalo1, intervalo2): Este método estático (@staticmethod) calcula a duração da sobreposição (interseção) entre dois objetos IntervaloTempo.
O cálculo (max(inicio1, inicio2) e min(fim1, fim2)) é uma forma de encontrar a intersecção. O retorno de max(intersecao, timedelta(0)) garante que o resultado nunca será um timedelta negativo, retornando uma duração de zero se não houver sobreposição. Este método é fundamental para cálculos mais avançados, como determinar quantas horas de um turno de trabalho ocorreram durante o período noturno.


## 3.2.3. Gestão de Pausas: Classe Pausas
A classe Pausas é uma classe que tem como objetivo gerir uma lista de IntervaloTempo que representam as pausas dentro de um turno de trabalho. Ela tem a lógica para adicionar, validar e calcular as pausas de forma organizada.

Construtor (__init__):
O construtor inicializa a classe com uma lista opcional de objetos IntervaloTempo e um limite, que é um outro IntervaloTempo representando o horário de trabalho no qual as pausas devem ocorrer.
O construtor demonstra uma inicialização segura e robusta: em vez de simplesmente atribuir a lista de pausas fornecida, ele itera sobre ela e utiliza o método adicionar_pausa para cada item. Isso garante que todas as pausas iniciais passem pelas mesmas regras de validação que novas pausas adicionadas posteriormente.

Encapsulamento de Regras de Negócio (adicionar_pausa):
Este método é o coração da classe e junta várias regras essenciais para a gestão de pausas:
Limite de Quantidade: Verifica se o número de pausas já atingiu a constante global max_pausas, impedindo a adição de pausas excessivas.
Validação de Limite Temporal: Usa o método nova_pausa.esta_dentro_do_limite(self.limite), fazendo o IntervaloTempo verificar se a pausa está contida no horário de trabalho definido.
Prevenção de Sobreposição: Utiliza o método estático IntervaloTempo.intersecao_tempo() para garantir que a nova pausa não se sobreponha a nenhuma pausa já existente.
Ao final, se a pausa for válida, ela é adicionada à lista e a lista self.pausas é ordenada com base na hora de início. Esta ordenação automática simplifica futuras iterações e a representação cronológica das pausas.

Métodos Utilitários:
duracao_total_pausas(): Um método de que faz um loop pela lista de pausas e soma as suas durações individuais, retornando um único timedelta que representa o tempo total de pausa.
atualizar_limite(novo_limite): Permite a modificação do intervalo de trabalho limite. Ao ser chamado, o método não apenas atualiza o limite, mas também revalida a lista de pausas existente, removendo aquelas que ficaram fora do novo intervalo. Este comportamento garante que as Pausas estejam a seguir as regras corretamente.


## 3.2.4. Representação de Horário Diário: Classe Horario
A classe Horario é uma das mais importantes do módulo, pois tem as classes utilitárias IntervaloTempo e Pausas para modelar um único turno de trabalho completo. A sua principal responsabilidade é calcular o tempo de trabalho efetivo, distinguindo entre horas diurnas e noturnas.

Construtor (__init__) e Composição de Objetos:

O construtor da classe Horario é um exemplo claro de composição. Ele recebe um IntervaloTempo (o turno bruto) e uma lista opcional de pausas.
Em vez de gerir a lista de pausas diretamente, ele instancia um objeto Pausas, passando-lhe a lista de pausas e o intervalo do turno como limite. Esta delegação encapsula toda a lógica de validação e gestão das pausas dentro da classe Pausas, mantendo a classe Horario mais limpa e focada em cálculos de alto nível.
Encapsulamento e Acesso a Dados:
Os atributos _intervalo e _pausas são protegidos. O acesso ao início e fim do turno é fornecido através das properties @inicio e @fim, que chamamm os atributos do _intervalo subjacente. Esta lógica tem como objetivo esconder a estrutura interna da classe.

Cálculos de Duração:
tempo_trabalhado(): Este método calcula o tempo de trabalho. Ele obtém a duração total do turno a partir do _intervalo e subtrai a duração total das pausas, obtida a partir do objeto _pausas. A classe Horario não precisa de saber como essas durações são calculadas, ela aapenas chama os métodos das classes que contêm a lógica.

Lógica de Negócio Complexa: Cálculo de Horas Noturnas
A funcionalidade mais complexa da classe é a diferença entre tempo de trabalho diurno e noturno, implementada através de um conjunto de métodos;
_obter_segmentos_trabalho(): Este método privado calcula os períodos de trabalho efetivo, "subtraindo" as pausas do intervalo de trabalho principal. Ele retorna uma lista de objetos IntervaloTempo que representam os blocos de tempo contínuo em que o funcionário esteve a trabalhar.
_gerar_intervalos_noturnos(): Este método cria uma lista de objetos IntervaloTempo que representam os períodos noturnos (definidos pelas constantes Inicio_Turno_noturno e Fim_Turno_noturno), para lidar com a possibilidade de o turno de trabalho se estender por mais de 24 horas.
calcular_tempo_noturno(): Este é obtém os segmentos de trabalho e os intervalos noturnos. Em seguida, faz um loop por ambos, utilizando o método estático IntervaloTempo.intersecao_tempo() para calcular a sobreposição entre cada segmento de trabalho e cada período noturno. A soma de todas estas interseções resulta no tempo total de trabalho noturno.
calcular_tempo_diurno(): Uma vez calculado o tempo noturno, o tempo diurno é obtido por uma simples subtração do tempo total trabalhado.
Esta abordagem para o cálculo das horas noturnas é um excelente exemplo de como decompor um problema complexo em partes menores e mais manejáveis, utilizando as classes utilitárias para construir uma solução robusta e precisa.

## 3.2.5. Classes Horario_Semanal e Horario_Mensal
Para expandir a lógica de um único Horario diário para períodos de tempo mais longos, o módulo tem as classes Horario_Semanal e Horario_Mensal.

Classe Horario_Semanal
Esta classe modela o horário de trabalho padrão para uma semana inteira, associando um Horario específico a cada Dias_Semana.

Estrutura: O construtor inicializa um dicionário, self.horarios, que usa os membros da enumeração Dias_Semana como chaves. Esta é uma forma limpa e semântica de representar a estrutura de uma semana de trabalho. O método adicionar_horario serve como a interface para popular este dicionário.
Cálculos Agregados: O método calcular_totais_semanais demonstra a agregação de comportamentos. Ele itera sobre todos os objetos Horario definidos para a semana e delega a cada um deles a responsabilidade de calcular o seu próprio tempo trabalhado, diurno e noturno. A classe Horario_Semanal apenas soma os resultados, agindo como um gestor sem precisar de conhecer a complexidade dos cálculos subjacentes.

Classe Horario_Mensal

Horario_Mensal representa a expansão da classe Horario_Semanal padrão ao longo de um mês e ano específicos.

Composição e Lógica de Calendário: A classe compõe-se de um objeto Horario_Semanal. A sua principal responsabilidade é aplicar a estrutura semanal repetidamente aos dias de um determinado mês, utilizando o calendar do Python para lidar com a complexidade de durações de meses e o mapeamento dos dias da semana.

Cálculos e Projeções:
calcular_totais_mensais(): Este método projeta o horário semanal para um mês inteiro. Ele faz um loop por cada dia do mês, determina o dia da semana correspondente, encontra o Horario previsto para esse dia no horario_semanal e, novamente, e passa 

o cálculo das durações a esse objeto Horario, somando os totais.
Geração de Dados e Relatórios:
obter_dados_diarios(): Funciona como um gerador de dados brutos, criando uma lista de dicionários, onde cada dicionário contém informações detalhadas sobre o horário previsto para cada dia de trabalho no mês.
gerar_relatorio_diario() e gerar_relatorio_semanal(): Estes métodos vão além de uma simples junção de dados e focam-se na formatação e apresentação. Eles utilizam o módulo calendar para agrupar os dias em semanas e produzem listas de strings já formatadas, prontas para serem exibidas ao utilizador.
Em conjunto, estas duas classes demonstram camadas: Horario_Mensal contém um Horario_Semanal, que por sua vez contém múltiplos objetos Horario. Cada camada usa os cálculos à camada inferior, resultando em uma estrutura modular para a projeção de horários de trabalho.

## 3.2.6. Controlador de Horários do Funcionário: Classe FuncionarioHorario
A classe FuncionarioHorario é a classe responsável pela maioria da utilização de todo o módulo Horario.py. Ela serve como um ponto principal entre o Funcionario e a complexidade da gestão de tempo. Um Funcionario tem de um FuncionarioHorario, deixando toda a responsabilidade de gerir o seu horário previsto, registar o seu horário real e calcular as discrepâncias entre ambos para ele.

Construtor e Gestão de Estado:
O construtor recebe um horario_semanal_base, que representa o horário padrão do funcionário.
Inicializa dois dicionários essenciais para a sua função:
horarios_especificos: Permite sobrescrever do horário padrão para datas específicas (ex: feriados, trocas de turno).
registros_diarios: Armazena os dados reais de ponto, guardando a data em um dicionário que contém tanto o horário "previsto" como o "real" para esse dia.

Gestão de Horários Previstos:
definir_horario_especifico: Interface simples para adicionar exceções ao horário padrão.
_obter_horario_previsto_para_data: Este método privado tem toda a lógica que determina qual o horário previsto para uma dada data. Ele demonstra uma hierarquia de precedência: primeiro verifica se existe um horário específico para a data, caso contrário usa o horario_semanal_base para encontrar o horário padrão para aquele dia da semana. Isto torna o sistema flexível e capaz de lidar com exceções.
horario_mensal e obter_horario_mensal: Estes métodos gerem a criação de objetos Horario_Mensal. Implementando um mecanismo para evitar processamento desnecessário, pois armazenam o último Horario_Mensal calculado (_horario_mensal_atual) e só geram um novo se o mês ou ano solicitado for diferente do que está guardado, evitando cálculos repetidos.

Registo do Trabalho Realizado:
registrar_ponto: Este método é a entrada para os dados reais. Ele recebe os horários de início e fim como strings, deixa a criação dos HoraMinuto e IntervaloTempo às suas respetivas classes, e cria um Horario para representar o turno real. Armazenando tanto o horário previsto como o horário real no dicionário registros_diarios.

Análise e Comparação (Previsto vs. Real):
calcular_diferencas: Este método compara o horário previsto com o real para uma data específica. Ele calcula dados como o atraso na entrada e tempo_extra trabalhado. Toda a lógica de comparação é mantida aqui.
obter_resumo_mensal: O método mais abrangente da classe. Ele cria um resumo completo da atividade de um funcionário num dado mês:
Obtém o Horario_Mensal para calcular os totais previstos.
Loop pelos registros_diarios do mês para calcular os totais reais, usando o método do Horario real fazer o cálculo do seu tempo de trabalho, diurno e noturno.
Junta todos os dados (previstos, reais, diferença, dias trabalhados) num único dicionário, fornecendo um saida completo pronta para ser utilizado pela classe Funcionario para gerar relatórios ou calcular pagamentos.
Basicamente, FuncionarioHorario é um exemplo primoroso de separação de responsabilidades e do padrão Fachada (Facade). Ele abstrai toda a complexidade do módulo de horários, fornecendo à classe Funcionario uma forma para lidar com todas as suas necessidades de gestão de tempo, desde a definição de horários até à análise detalhada dos registos de ponto.

# 3.3. Módulo de Interface do Utilizador (Console.py)
O ficheiro Console.py lida com a apresentação e controle da aplicação. Ele lida com a interação com o utilizador através de uma interface de linha de comandos. Este módulo usa tanto o módulo principal tanto o módulo do horário.

## 3.3.1. Funções Auxiliares e Ponto de Entrada
Fora da classe principal InterfaceHospital, foram definidas várias funções de suporte que auxiliam na gestão da interface e na criação de dados complexos, além do ponto de entrada padrão da aplicação.
Funções de Gestão da Consola
limpar_console(), aguardar_e_limpar() e linhas_vazias(): São funções simples para melhorar a exibição do console. limpar_console() usando comandos do sistema operativo para limpar o ecrã (os.system('cls')), enquanto aguardar_e_limpar() combina esta ação com uma pausa, melhorando a experiência do utilizador ao permitir que leia as informações antes de prosseguir. o que torna o código mais legível, substituindo chamadas diretas a os.system ou input e evita a repetição de mensagens o que pode levar a frases incorretas, facilitando o acesso às operações por meio de uma função.

Funções de criação de Horários
Estes métodos funcionam para criar as variáveis do Horario_Semanal, uma tarefa que, de outra forma, seria complexa e repetitiva, assim fica dentro de uma função que pode ser facilmente chamada.
criar_horario_padrao(...): Esta função usada de dados predefinidos, usando-os e criando a variável da classe Horario_Semanal que representa um horário de trabalho típico (Segunda a Sexta, das 09:00 às 18:00 com uma hora de almoço) e após a criação essa variável é retornada, simplificando a criação de funcionários com horários pré feitas, evitando a necessidade de configurar o horário manualmente em cada ocasião.
criar_horario_interativo(): Esta função guia o utilizador passo a passo através da criação de um Horario_Semanal personalizado.
Interatividade: A função solicita ao utilizador os horários de início e fim, bem como os detalhes de múltiplas pausas, repetindo o processo por cada dia da semana.
Validação de Entrada: Embora a validação principal esteja nas classes do módulo de horários, esta função realiza verificações básicas de entrada (ex: se um campo foi deixado em branco) e utiliza um bloco try-except para capturar erros durante a conversão das strings de tempo, tornando a interface menos propensa a erros do utilizador.
Resposta ao Utilizador: Após a configuração de cada dia e no final do processo, a função calcula e exibe os totais do tempo trabalhado.
Ponto de Entrada (if __name__ == "__main__":)
Este é o bloco de código padrão em Python que é executado quando o ficheiro Console.py é chamado como o script principal.
 As suas responsabilidades são:
Exibir uma mensagem de boas-vindas.
Criar uma variável para a classe principal da interface, InterfaceHospital, que por sua vez pergunta ao utilizador se pretende usar os dados padrão ou inserir manualmente, se o utilizador aceitar o usar os dados padrão, chama o método interface.inicializar_dados(), que é responsável por preencher o sistema com os dados iniciais para testes (funcionários, salas, etc.).
Gestão de Encerramento: O código está envolvido num bloco try-except KeyboardInterrupt, o que permite personalizar a finalização do programa se o utilizador pressionar Ctrl+C. Em vez de terminar abruptamente, o programa limpa a consola e exibe uma mensagem de encerramento, melhorando a experiência do utilizador, ainda mais porque quase todos os inputs também estão dentro de blocos de try-except o que leva a exibir um erro quando o utilizador finaliza o programa com Ctrl+C.

## 3.3.1.2. Métodos de Interação
Este primeiro conjunto de métodos atua como blocos de construção reutilizáveis para a interface, juntando a lógica repetitiva de apresentar uma lista de opções ao utilizador e ler a sua escolha. São métodos essenciais para a construção dos menus.

selecionar_funcionario(mensagem):
Propósito: Apresentar ao utilizador uma lista numerada de todos os funcionários registados no sistema e permitir que ele escolha um.
Implementação: O método primeiro obtém a lista de funcionários do self.sistema. Em seguida, faz um loop pelos valores do dicionário de funcionários, mostrando o nome de cada um com um número sequencial que é um Id a representar o funcionário. A leitura escolha do utilizador está dentro de um try-except ValueError para lidar com entradas não numéricas. A lógica para mapear o número escolhido de volta para o objeto Funcionario correto é feita através de uma segunda iteração. Retorna o objeto Funcionario selecionado ou None em caso de erro ou escolha inválido.

selecionar_paciente(mensagem, filtro):
Propósito: Similar ao anterior, mas com uma funcionalidade adicional: a capacidade de filtrar a lista de pacientes antes de a exibir.
Implementação: A característica mais notável deste método é o parâmetro filtro. Se um filtro que é uma função lambda for fornecido, o método faz um loop pelos pacientes e aplica a função de filtro a cada um, construindo uma nova lista apenas com os pacientes que estiverem na condição. Se nenhum filtro for fornecido, todos os pacientes são listados. O filtro torna o método versátil, permitindo que seja usado para selecionar "todos os pacientes", "pacientes maiores de 18 anos", "pacientes em espera", etc., sem duplicar código. O resto da lógica da seleção e tratamento de erros é igual à da função selecionar_funcionario.

selecionar_area(mensagem):
Propósito: Separar a lógica da seleção de uma área de atendimento (representada por um objeto SalaEspera).
Implementação: O método faz um loop pelas chaves do dicionário self.sistema.salas_espera (os nomes das áreas) para exibir as opções. Uma vez que o utilizador faz uma escolha numérica, o método usa essa escolha retornando a SalaEspera correspondente do dicionário.

obter_mes_ano():
Propósito: Um pequeno método auxiliar para obter um mês e um ano do utilizador, com a conveniência de usar os valores da data atual como padrão se a entrada for deixada em branco.
Implementação: Utiliza a função input() para obter os valores e, em seguida, aplica uma lógica condicional para converter a entrada para inteiro ou manter os valores padrão obtidos de datetime.now().

exibir_menu_generico(titulo, opcoes, sair_texto):
Propósito: Este é o método mais importante da clase, pois é centro de todos os menus. É um método genérico e reutilizável para criar qualquer menu de opções.
Implementação: Recebe um titulo e um dicionário de opcoes. O dicionário é a chave para a sua flexibilidade: as chaves são as strings numéricas da opção (ex: "1", "2") e os valores são tuplos contendo (descrição_da_opção, função_a_ser_executada).
O método entra num ciclo while True, limpa a consola, exibe o título e faz um loop pelas opções do dicionario para as mostrar de forma ordenada. Ele então aguarda a entrada do utilizador. Se a opção for "0", o while(true) é parado. Se a opção for uma chave válida no dicionário, ele usa a função associada (acao) e executa-a (acao())..

## 3.3.1.3. Inicialização e Navegação Principal
Esta parte da classe InterfaceHospital é responsável pelo arranque da aplicação e pela apresentação do menu principal, que serve como o ponto de partida para todas as funcionalidades do sistema.
Método inicializar_dados():
Propósito: Este método é responsável pelo início da interação com o utilizador. A sua função é determinar se o programa deve começar com um conjunto de dados predefinidos ou com sem dados para que sejam preenchidos manualmente.
Implementação: O método pergunta ao utilizador ("Deseja inicializar os dados padrão?"). Com base na resposta:
Se afirmativa ('s'), ele chama o método self.configuracao_padrao(), que preenche o sistema com um conjunto de dados pré definidos.
Caso contrário, o sistema permanece vazio.
Independentemente da escolha, e então inicia o self.menu_principal(), que efetivamente inicia a aplicação

Método configuracao_padrao():
Propósito: Este método tem como objetivo prencher o de dados pré-definidos, cujo único objetivo é preencher o SistemaHospital com os dados essenciais para testes e demonstrações.
Implementação: O método é uma sequência de chamadas á classe SistemaHospitalar e às funções auxiliares, usando:
Criação de Estruturas: criar_area_especializada() múltiplas vezes para criar as diferentes áreas de atendimento do hospital.
Criação de Horários: criar_horario_padrao() para criar um Horario_Semanal que será reutilizado por vários funcionários.
Registo de Funcionários: Instancia e regista vários funcionários de todos os tipos (Medico, Enfermeiro, EnfermeiroChefe, Administrativo), cada um com os seus atributos específicos.
Configuração de Salas: Cria salas de cirurgia através de self.sistema.criar_sala_cirurgia() e, em seguida, utiliza os métodos das SalaCirurgia para adicionar equipamentos.
Registo de Pacientes: Invoca self.sistema.registrar_paciente() para adicionar um conjunto inicial de pacientes ao sistema.
Este método, embora extenso, é um exemplo perfeito de como a camada de interface utiliza o SstemaHospitalar para a criação de sistema complexo sem precisar de conhecer os detalhes internos de como esses objetos são armazenados ou geridos.

Método menu_principal():
Propósito: Este é o ponto inicial da navegação. Apresenta ao utilizador as principais áreas funcionais do sistema.
Implementação: Usando o método genérico self.exibir_menu_generico() como todos os menus fazem.
Um dicionário opções é criado, onde cada entrada é a o numero de uma opção que corresponde a um tuplo contendo a descrição do menu (ex: "Funcionários") e uma referência ao método da própria classe que deve ser executado (ex: menu_funcionarios).
Quando o utilizador seleciona uma opção, o exibir_menu_generico encarrega-se de invocar o método correspondente, transferindo assim o controlo para o submenu apropriado. Esta estrutura, baseada na passagem de funções, é extremamente modular e fácil de estender: para adicionar uma nova área ao menu principal, basta adicionar uma nova entrada ao dicionário opções.

## 3.3.1.4. Gestão de Menus e Navegação: Submenus de Funcionários e Salas
Esta secção abrange os métodos que implementam os submenus para a gestão de funcionários e dos diferentes tipos de salas, demonstrando a estrutura de navegação hierárquica da aplicação.

Método menu_funcionarios():
Propósito: Apresenta um menu consolidado com todas as operações relacionadas com os funcionários.
Implementação: Utiliza o método exibir_menu_generico para criar o submenu. Cada opção ("Listar funcionários", "Registar novo funcionário", etc.) é mapeada a um método específico da própria classe InterfaceHospital que implementa essa funcionalidade. Esta estrutura modular permite que cada ação seja contida no seu próprio método, mantendo o código organizado.

Método menu_salas():
Propósito: Oferece um ponto de entrada para a gestão de áreas de atendimento e salas de consulta.
Implementação: Segue o mesmo padrão de menu_funcionarios, utilizando exibir_menu_generico para fazer as descrições de ações (como "Listar salas" ou "Criar nova área") corresponderem aos métodos correspondentes. A opção "Gerenciar funcionário da sala" leva a um outro nível de submenu, aprofundando a navegação.

Método gerenciar_funcionario_sala():
Propósito: Fornecer uma interface focada para gerir a associação de funcionários a uma sala de atendimento específica.
Implementação: Este método demonstra uma técnica de programação funcional para lidar com a passagem de argumentos para as funções de callback do menu.
Primeiro, ele obtém a sala de atendimento específica que o utilizador deseja gerir, encadeando chamadas a obter_Id_Area() e obter_Sala_por_Area().
Depois, ao definir o dicionário opções para exibir_menu_generico, as funções de ação são definidas como expressões lambda. Por exemplo, lambda: self.adicionar_Funcionario_Sala(sala).
O uso de lambda é essencial pois permite obter a variável sala (a sala que o utilizador acabou de selecionar) e passá-la como argumento para o método de ação (adicionar_Funcionario_Sala) quando este for eventualmente executado pelo exibir_menu_generico. Sem a lambda, não haveria uma forma direta de passar o contexto da sala selecionada para secundárias funções.

Métodos obter_Id_Area() e obter_Sala_por_Area():
Propósito: Estes são métodos auxiliares de seleção encadeada, projetados para guiar o utilizador na escolha de uma SalaAtendimento específica, primeiro selecionando a área e depois a sala dentro dessa área.
Implementação: Ambos seguem o padrão de apresentar uma lista numerada, capturar a entrada do utilizador e mapear o número de volta ao objeto ou índice desejado, com tratamento de erros try-except. Eles demonstram como dividir uma tarefa de seleção complexa em passos mais simples e guiados.

Métodos adicionar_Funcionario_Sala(), remover_Funcionario_Sala(), definir_Funcionario_Sala(), listar_Funcionarios_Sala():
Propósito: São os métodos de ação que implementam a lógica final para gerir os funcionários numa sala.
Implementação: Estes métodos são exemplos claros da camada de interface a atuar como um "controlador". A sua lógica é simples:
Usam o método selecionar_funcionario() para obter o funcionário alvo.
Invocam o método apropriado diretamente no objeto sala (ex: sala.adicionar_funcionario(funcionario)).
Toda a lógica de negócio (como verificar se o funcionário já está na sala ou se é de um tipo permitido) está encapsulada na própria classe SalaAtendimento, e não na interface. A interface apenas trata a chamada, respeitando a separação de responsabilidades. listar_Funcionarios_Sala simplesmente extrai e formata a informação do objeto sala.

Método menu_salas_cirurgia():
Propósito: Apresenta as opções de gestão específicas para as salas de cirurgia.
Implementação: Novamente, utiliza exibir_menu_generico para mapear ações como "Criar sala de cirurgia" ou "Adicionar equipamento" aos seus respetivos métodos de implementação, mantendo a consistência de todos os menus do sistema.

## 3.3.1.5. Gestão de Pacientes e Customização Manual
Esta parte da InterfaceHospital foca-se na gestão de pacientes e, de forma crucial, na criação manual e detalhada de novas varáveis no sistema, como áreas e funcionários, oferecendo uma alternativa à configuração padrão.

Método menu_pacientes():
Propósito: Centraliza as operações relacionadas com os pacientes.
Implementação: Segue o padrão de menu genérico, correspondendo opções como "Registar novo paciente" e "Ver todos os pacientes" aos seus respetivos métodos. Inclui também o acesso a "Estatísticas do hospital", ligando a gestão de pacientes a uma visão mais ampla do sistema.

## 3.3.1.6. Operações de Registo e Gestão (Funcionários, Pacientes, Salas)
Esta lista de métodos implementa as funcionalidades de ao nível da interface do utilizador. São as funções que permitem visualizar o estado do sistema e adicionar novas entidades.

Métodos de Listagem e Visualização:
listar_areas() e listar_status_salas(): Ambos os métodos fazem um loop pelas áreas de atendimento (salas_espera) registadas no sistema. listar_areas fornece um resumo, enquanto listar_status_salas oferece uma visão mais detalhada, percorrendo as salas de atendimento dentro de cada área e exibindo o seu estado (Disponível/Ocupada) e, se aplicável, o paciente que a ocupa.
listar_funcionarios(): Este método é um excelente exemplo da utilização do polimorfismo a partir da camada de interface. Ele simplesmente faz um loop pelos funcionários e invoca str(funcionario) para cada um. A responsabilidade de formatar a saída de forma adequada para um Medico, Enfermeiro ou EnfermeiroChefe é inteiramente deixada às suas respetivas classes, resultando num código de interface limpo e que não precisa de conhecer os detalhes de cada tipo de funcionário.
listar_salas_cirurgia() e ver_detalhes_sala_cirurgia(): O primeiro método fornece uma listagem resumida, enquanto o segundo utiliza o método de seleção padrão para escolher uma sala e, em seguida, chama sala_selecionada.detalhar_sala(), sendo um outro exemplo de polimorfismo, onde a interface pede ao objeto que se "descreva" a si mesmo.

Métodos de Criação e Registo:
registar_novo_paciente(): Uma função de interação simples que solicita o nome e a idade, realiza validações básicas (nome não vazio, idade positiva) e depois delega a criação e registo ao self.sistema.registrar_paciente(). A função então exibe os detalhes do paciente recém-criado, incluindo o número de utente que foi gerado automaticamente pelo sistema, fornecendo uma resposta imediata ao utilizador.
criar_sala_cirurgia(): Um método interativo para criar uma nova SalaCirurgia. Solicita os dados ao utilizador, realiza validações (nome não pode ser vazio ou duplicado, capacidade deve ser positiva) e, por fim, invoca self.sistema.criar_sala_cirurgia() para efetivar a criação, mais uma vez demonstrando a separação entre a coleta de dados da interface e a lógica de  do sistema.

Métodos de Modificação:
adicionar_equipamento_sala(): Este método implementa a lógica para adicionar um equipamento a uma sala de cirurgia existente. A sua lógica segue um padrão muito usado na interface das salas de cirurgia:
Verifica se existem salas de cirurgia.
Apresenta uma lista numerada das salas disponíveis para seleção.
Lê a escolha do utilizador e encontra a sala_selecionada correspondente.
Solicita o nome do novo equipamento.
Deixa a ação de adicionar ao equipamentto para a classe, chamando sala_selecionada.adicionar_equipamento(equipamento). A lógica de verificar se o equipamento já existe e adicioná-lo à lista está corretamente classe SalaCirurgia, não na interface assim evitando repetição de código.
Esta lista de métodos mostra o papel da InterfaceHospital como uma camada de controlo que trata da interação, recolhe dados do utilizador e invoca os métodos apropriados na camada do Sistema (SistemaHospital) ou nos próprios objetos do modelo, mantendo uma estrutura limpa e com responsabilidades bem definidas.

## 3.3.1.7. Lógica de atendimento / operação
Esta parte da InterfaceHospital implementa os métodos que simulam as operações e atendimentos de um hospital, como o processo de receção, e fornece interfaces para consultar informações detalhadas e complexas sobre os funcionários.

Métodos ver_horario_funcionario() e ver_pagamento_funcionario():
Propósito: Fornecer uma visualização detalhada das informações de tempo e remuneração de um funcionário para um mês específico.
Implementação: Ambos os métodos seguem um padrão claro:
Seleção: Utilizam selecionar_funcionario() para que o utilizador escolha o funcionário alvo.
Contexto Temporal: Invocam obter_mes_ano() para definir o período da consulta.
Delegação da Lógica: A etapa crucial é a delegação. ver_horario_funcionario invoca funcionario.obter_resumo_horas_mes(), e ver_pagamento_funcionario invoca funcionario.calcular_pagamento(). Toda a complexidade de agregar dados de ponto, calcular horas noturnas, aplicar regras de pagamento, etc., está completamente encapsulada nas classes Funcionário e FuncionarioHorario.
Apresentação: A responsabilidade da interface é apenas receber o dicionário de resultados e formatá-lo de maneira legível para o utilizador, utilizando a função auxiliar formatar_timedelta quando necessário. Este design demonstra uma excelente separação de responsabilidades entre a lógica de negócio (nos modelos) e a apresentação (na interface).

Método menu_recepcao():
Propósito: Simular o balcão da receção, centralizando as tarefas iniciais de gestão de um paciente: o seu registo e o seu encaminhamento para uma área de atendimento.
Implementação: É um menu padrão que utiliza exibir_menu_generico para apresentar as opções. Uma verificação inicial assegura que existam áreas de atendimento (salas_espera) criadas, prevenindo informações que possam causar erros no sistema.

Método registar_novo_paciente() (Contexto da Recepção):
Propósito: Implementa a lógica de registo de um novo paciente a partir da interface.
Implementação: Embora o nome seja idêntico a um método anterior, esta implementação parece ser a principal utilizada nos menus. Solicita interativamente os dados do paciente, realiza validações básicas e delega a criação ao self.sistema.registrar_paciente(), exibindo uma resposta clara do sucesso da operação e do número de utente criados.

Método listar_pacientes():
Propósito: Fornecer uma lista detalhada de todos os pacientes registados, incluindo o seu estado atual na lógica do atendimento.
Implementação: Itera sobre os pacientes no sistema e, para cada um, exibe não apenas os dados básicos, mas também o seu status, area_atendimento e sala_atendimento, se definidos. Isto oferece uma visão geral e em tempo real da localização e do estado de cada paciente no hospital.

Método enviar_paciente_para_atendimento():
Propósito: Organizar o processo de dar uma senha a um paciente e colocá-lo na fila de uma área de atendimento específica. Este é uma das lógicas de trabalho mais importantes do sistema.
Implementação: O método demonstra uma lógica de interação sofisticada:
Seleção de Contexto: Primeiro, o utilizador seleciona a sala_espera (área) de destino.
Seleção Filtrada: Em seguida, o método selecionar_paciente é invocado com uma função lambda como filtro. Este filtro é crucial: lambda paciente: paciente.status != StatusAtendimento.Atendimento and paciente.senha is None. Ele garante que apenas os pacientes que estão "livres" (sem senha e não em atendimento) sejam apresentados como opções, prevenindo que um paciente seja colocado em duas filas ao mesmo tempo.
Delegação da Ação: Uma vez selecionado o paciente, a ação é delegada ao objeto sala_espera através da chamada sala_espera.pegar_senha(paciente). A lógica de gerar a senha, atualizar o estado do paciente e adicioná-lo à fila está corretamente encapsulada na classe SalaEspera, e a interface apenas inicia o processo.

## 3.3.1.8. Gestão de Áreas de Atendimento e Geração de Relatórios
Esta secção final da InterfaceHospital implementa o lógica de atendimento dentro de uma área de atendimento específica (chamar pacientes, finalizar atendimentos) e fornece funcionalidades para a geração de relatórios e estatísticas gerais do sistema.

Método menu_areas():
Propósito: Funciona como um navegador para as diferentes áreas de atendimento do hospital.
Implementação: Diferente dos outros menus principais, este método não utiliza exibir_menu_generico. Em vez disso, implementa o seu próprio ciclo while para listar as áreas. Após o utilizador selecionar uma área pelo nome, o método transfere o controlo para self.gerenciar_area(area_selecionada), passando o contexto da área escolhida.

Método gerenciar_area(area_nome):
Propósito: Apresenta o menu de ações específicas para uma área de atendimento.
Implementação: Uma vez dentro do contexto de uma área, este método volta a utilizar o exibir_menu_generico. De forma semelhante a gerenciar_funcionario_sala, ele usa expressões lambda para passar o objeto sala_espera (que representa a área) como argumento para os métodos de ação (chamar_proximo_paciente e finalizar_atendimento). Isto permite que as ações sejam executadas no contexto correto da área que foi selecionada.

Método chamar_proximo_paciente(sala_espera):
Propósito: Orquestrar a chamada de um paciente da fila de espera para uma sala de atendimento.
Implementação:
Filtragem de Funcionários: O método primeiro constrói uma lista de funcionários válidos para realizar o atendimento, aplicando um filtro isinstance para excluir o pessoal administrativo.
Seleção do Atendente: Apresenta a lista de funcionários clínicos ao utilizador para que ele escolha quem irá realizar o atendimento.
Delegação da Ação: Após a seleção, a ação final é delegada ao objeto sala_espera através da chamada sala_espera.chamar_proximo(funcionario_selecionado). A interface não precisa de saber qual sala está livre ou qual paciente é o próximo; essa lógica está corretamente encapsulada na classe SalaEspera.

Método finalizar_atendimento(sala_espera):
Propósito: Implementar a lógica para finalizar um atendimento em andamento dentro de uma área.
Implementação: O método primeiro percorre as salas de atendimento da área para encontrar uma que esteja ocupada. Em seguida, solicita ao utilizador uma descrição opcional do atendimento e, por fim, delega a ação ao objeto sala_com_atendimento através da chamada sala_com_atendimento.finalizar_atendimento(descricao). A lógica de atualizar os status, registar o atendimento no funcionário e libertar a sala está encapsulada na classe SalaAtendimento.

Métodos relatorio_funcionario() e relatorio_paciente():
Propósito: Fornecer uma interface simples para gerar e exibir relatórios textuais detalhados para um funcionário ou paciente específico.
Implementação: Ambos os métodos utilizam os helpers selecionar_funcionario ou selecionar_paciente para escolher o alvo. Em seguida, invocam os métodos gerar_relatorio_* da fachada self.sistema. A responsabilidade de, por sua vez, chamar o método polimórfico __str__ do objeto correto é do sistema, mantendo a interface simples.

Método estatisticas_hospital():
Propósito: Apresentar um painel de estatísticas gerais sobre o estado atual do hospital.
Implementação: Este método demonstra como a interface pode agregar dados de diferentes partes do sistema para criar uma visão consolidada. Ele acede diretamente aos dicionários em self.sistema para obter contagens (número de pacientes, funcionários) e também itera sobre os objetos para calcular estatísticas mais complexas, como o total de atendimentos realizados e a distribuição dos pacientes pelos diferentes StatusAtendimento.

## 3.3.1.9. Gestão de Histórico Médico
Esta secção da interface é dedicada a interagir com o histórico médico dos pacientes. De um ponto de vista estrutural, é uma das mais interessantes, pois todos os seus métodos interagem primariamente com o subsistema estático da classe InterfaceHospital, em vez que agir diretamente com o SistemaHospitalar. Esta abordagem de design cria uma separação clara entre o estado "ao vivo" da simulação hospitalar e um registo de histórico mais persistente e global.

Método menu_historico_medico():
Propósito: Serve como o portal de entrada para todas as funcionalidades relacionadas com a consulta e registo de históricos médicos.
Implementação: Utiliza exibir_menu_generico para mapear as opções do menu (como "Registrar atendimento" ou "Ver histórico") aos seus métodos de implementação correspondentes, que por sua vez invocam método da classe SistemaHospital.

Método adicionar_funcionario_historico():
Propósito: Atua como uma "ponte" entre o sistema de simulação ao vivo e o sistema de histórico estático.
Implementação: O método primeiro seleciona um funcionário do sistema ativo (SistemaHospitalar). Em seguida, invoca o método SistemaHospital.adicionar_funcionario(funcionario). Esta chamada não adiciona o funcionário à simulação atual, mas sim regista-o no dicionário de classe SistemaHospital.Funcionarios, tornando-o disponível para ser associado a registos de histórico.

Método registrar_atendimento_historico():
Propósito: Guiar o utilizador no processo de criação de um novo registo de histórico, associando um funcionário, um paciente e uma descrição.
Implementação: Este método demonstra claramente a interação com o estado estático:
Após a seleção do funcionário e do paciente, o método solicita os detalhes do atendimento (ID do histórico e descrição).
A ação final é uma chamada ao método estático SistemaHospital.adicionar_historico(...), que manipula a estrutura de dados global SistemaHospital.Historico_Medico para persistir o registo. A interface apenas orquestra a recolha de dados e delega toda a lógica de armazenamento.

Método ver_historico_paciente():
Propósito: Implementar a funcionalidade de consulta de histórico para um paciente específico.
Implementação: Após a seleção do paciente através do helper self.selecionar_paciente(), o método invoca o método estática através de SistemaHospital.obter_historicos_paciente(paciente.numero_utente). A responsabilidade da interface é, então, simplesmente receber o dicionário de resultados e formatá-lo de maneira legível, iterando sobre as suas chaves e valores para exibir o histórico ao utilizador. A lógica de busca e agregação dos dados está completamente encapsulada na camada de sistema.
Esta separação entre a instância self.sistema (para a simulação dinâmica) e os métodos/atributos estáticos SistemaHospital.* (para o histórico) é um padrão de design sofisticado. Ele permite que o histórico médico exista como um estado global e partilhado, que pode ser acedido e modificado a partir de diferentes partes da aplicação sem a necessidade de passar uma referência da instância principal, ao mesmo tempo que permite que a simulação ao vivo (pacientes em espera, salas ocupadas) seja gerida de forma independente.

Método ver_pacientes_funcionario():
Propósito: Realizar a consulta inversa ao histórico: dado um funcionário, listar todos os pacientes que ele atendeu e os detalhes desses atendimentos.
Implementação: Este método primeiramente lista os funcionários registados no sistema de histórico (SistemaHospital.Funcionarios), permite a seleção e, em seguida, encadeia chamadas aos métodos estáticos: primeiro SistemaHospital.obter_pacientes_funcionario() para obter a lista de utentes, e depois SistemaHospital.obter_historicos_funcionario_paciente() para obter os registos específicos de cada par funcionário-paciente. A responsabilidade da interface é apenas orquestrar estas chamadas e formatar a informação agregada para exibição.

Método listar_todos_historicos():
Propósito: Exibir um relatório completo de todos os registos de histórico existentes no sistema.
Implementação: Este método é um exemplo máximo de delegação. A sua implementação é uma única linha: print(SistemaHospital.listar_todos_historicos()). Toda a complexidade de fazer um loop pela estrutura de dados do histórico, obter os nomes de funcionários e pacientes e formatar o relatório completo numa única string está inteiramente encapsulada no método estático da classe SistemaHospital. A interface limita-se a solicitar e exibir o resultado final.

## 3.3.1.10. Gestão de Horários e Ponto
Esta secção da interface é dedicada a fornecer ao utilizador ferramentas para visualizar e gerir os horários dos funcionários, interagindo com a classe Funcionário e, portanto, com todo o módulo Horario.py.

Método menu_horarios():
Propósito: É o menu central para todas as operações relacionadas com a gestão de tempo.
Implementação: Utiliza o exibir_menu_generico para mapear as funcionalidades de visualização e edição de horários aos seus métodos de implementação correspondentes.

Método ver_horario_semanal():
Propósito: Apresentar uma visão detalhada do horário de trabalho previsto para uma semana padrão de um funcionário.
Implementação: Após a seleção de um funcionário, o método acede ao seu atributo horario_semanal. A sua principal responsabilidade é apresentação: ele itera sobre os dias da semana, extrai os objetos Horário e Pausas e formata as informações de forma legível. É importante notar que todos os cálculos (calcular_totais_semanais, tempo_trabalhado, calcular_tempo_diurno, etc.) são delegados aos métodos dos objetos do módulo de horário. A interface também demonstra a necessidade de converter os dados internos (timedelta) de volta para um formato amigável ao utilizador (HoraMinuto) para exibição.

Método ver_horario_mensal_detalhado():
Propósito: Fornecer um relatório tabular, dia a dia, do horário previsto de um funcionário para um mês específico.
Implementação: Semelhante à visualização semanal, este método atua primariamente como uma camada de apresentação.
Ele seleciona o funcionário e obtém o mês/ano.
Invoca funcionario.horario_funcionario.obter_horario_mensal() e, em seguida, horario_mensal.obter_dados_diarios() para obter uma lista de dicionários contendo os dados brutos.
A lógica principal do método é fazer um loop pela estrutura de dados e realizar uma formatação complexa para criar uma tabela de texto legível, incluindo a conversão de timedelta para HoraMinuto e a formatação das pausas.
No final, invoca calcular_totais_mensais() para exibir um resumo. Este método exemplifica o papel da interface em transformar dados estruturados do modelo numa apresentação compreensível.

Método editar_horario_semanal():
Propósito: Fornecer uma interface para modificar o horário de trabalho padrão de um funcionário para um dia específico da semana.
Implementação: O método guia o utilizador através da seleção de um funcionário e de um dia da semana. A sua lógica de interação para recolher os novos horários de início, fim e pausas é, na prática, uma reutilização da lógica vista em criar_horario_interativo. Após construir um novo objeto Horário com os dados fornecidos, ele o atribui ao dia correspondente no horario_semanal do funcionário. A etapa final, funcionario.horario_funcionario = FuncionarioHorario(funcionario.horario_semanal), é de crucial importância: ela recria o objeto FuncionarioHorario com o novo horário semanal base, garantindo que todas as futuras comparações entre tempo previsto e tempo real utilizem a estrutura de horários atualizada.

Método definir_horario_especifico():
Propósito: Permitir a definição de um horário de trabalho excecional para uma data específica, sobrepondo-se ao horário semanal padrão. É a ferramenta para gerir feriados, dias de compensação ou turnos especiais.
Implementação: Após a seleção do funcionário e da data, o método solicita os detalhes do horário para esse dia. Uma vez que o objeto Horário correspondente é criado, a ação é delegada a uma única chamada de alto nível: funcionario.definir_horario_especifico(data_especifica, horário). A interface não precisa de saber como ou onde esta exceção é armazenada; ela usa a função do Funcionário, que por sua vez usa a lógica FuncionarioHorario.

Método registar_ponto():
Propósito: Implementar a funcionalidade de "bater o ponto", ou seja, registar as horas de início e fim efetivamente trabalhadas por um funcionário numa data específica.
Implementação: Este método demonstra uma excelente preocupação com a experiência do utilizador.
Contextualização: Antes de solicitar os dados, ele obtém e exibe o horário previsto para a data em questão, fornecendo um contexto útil.
Entrada Facilitada: Permite que o utilizador deixe os campos de entrada/saída em branco para automaticamente utilizar os horários previstos, agilizando o processo.
Delegação Total: Após recolher todos os dados (início, fim e pausas reais), a interface invoca um único método, funcionario.registrar_ponto(...), delegando toda a complexidade de criar os objetos de tempo e armazenar o registo.
Resposta Imediata: Logo após o registo, o método invoca funcionario.calcular_diferenca_diaria() e exibe um resumo do dia (atraso, tempo extra), confirmando ao utilizador que o registo foi processado e mostrando os resultados imediatos.

Método ver_registos_ponto():
Propósito: Apresentar um relatório de todos os registos de ponto de um funcionário para um determinado mês.
Implementação: Este método é um exemplo perfeito da separação entre lógica e apresentação. Ele seleciona o funcionário e o período, e depois faz uma única chamada a funcionario.listar_registros_ponto_mes(mês, ano). Este método, pertencente à camada de modelo, é responsável por toda a lógica de negócio: aceder aos registos, calcular as diferenças diárias e retornar uma estrutura de dados limpa (uma lista de dicionários). A única responsabilidade da InterfaceHospital é então faz um loop pela estrutura de dados e formatar a sua apresentação numa tabela legível para o utilizador.

Com estes métodos, a InterfaceHospital conclui o seu papel como a camada de controlo e apresentação do sistema, servindo como uma interface que usa dos módulos seja do horário seja do principal, demodo a criar uma aplicação de linha de comandos funcional, modular, e estruturada.

# 4. Conclusão
## 4.1. Resultado
Este projeto resultou na implementação de um protótipo funcional de um sistema de informação para gestão hospitalar, cumprindo os objetivos definidos na diciplina de Programação e Sistemas de Informação. Sendo um projeto funcional, completo e modular.

Os principais resultados da implementação foram:

Modelação de Dados: Foram definidas as estruturas de dados centrais do sistema (Pessoa, Sala), que serviram como base para representar a lógica base do problema de forma consistente.
Reutilização e Especialização: Foram aplicadas técnicas de programação para especializar as estruturas de dados base (ex: um Medico é uma forma especializada de Funcionario), otimizando a reutilização de código.
Segmentação Funcional: O código-fonte foi organizado em módulos com responsabilidades distintas (Program.py para a lógica de negócio, Horario.py para a lógica da gestão do tempo e Console.py para a interface com o utilizador), separando as diferentes funções do sistema.

## 4.2. Desafios e Aprendizagens
O desenvolvimento focou-se em criar um sistema modular e detalhado. Os principais desafios e aprendizagens foram:

Composição das classes: A criação da entidade EnfermeiroChefe, que agrega atributos e funcionalidades de duas outras entidades distintas, exigiu uma solução cuidada na sua inicialização para assegurar a consistência dos dados resultantes.
Complexidade da Lógica Temporal: A implementação do módulo de gestão de horários (Horario.py) representou um desafio significativo devido à complexidade inerente ao cálculo de durações e intervalos, especialmente em cenários que envolviam a transição da meia-noite.

## 4.3. Propostas de Evolução
A base funcional implementada permite a evolução do sistema em diversas frentes:

Implementação de Persistência de Dados: Usar um sistema de armazenamento de dados de forma permanente (ex: em ficheiros estruturados como JSON ou numa base de dados como SQLite), garantindo a sua durabilidade entre utilizações.
Evolução da Camada de Apresentação: Desenvolver uma interface gráfica para o utilizador para simplificar a interação, ou reaproveitar a lógica para uma versão web.
Testes automatizados: Construir um conjunto de testes automatizados para validar a correção funcional do sistema de forma contínua, assegurando que futuras modificações não introduzam regressões.
Refatoração para Redução do Acoplamento: A forma como o módulo de histórico acede à informação gera uma forte dependência entre os componentes do sistema. Propõe-se uma refatoração para que as dependências sejam geridas de forma explícita, o que aumentaria o isolamento dos módulos e a sua testabilidade.
