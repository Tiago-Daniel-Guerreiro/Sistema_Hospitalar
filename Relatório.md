1. Introdução
1.1. Contextualização do Projeto
Este relatório descreve o desenvolvimento de um Sistema de Gestão Hospitalar, um projeto prático realizado para a diciplina de Programação e Sistemas de informação. O sistema foi implementado inteiramente em Python e é usado através de uma interface de linha de comandos.

O tema do projeto foi proposto pelo professor e comum a todos os alunos, servindo como um caso de estudo para aplicar e explorar os conhecimentos ensinados em aula. A abordagem do nosso grupo foi a de criar a versão mais completa e detalhada possível, para isso demos um especial foco ás operações como o registo de pacientes, a gestão de diferentes tipos de funcionários, a alocação de salas e, especialmente, uma complexa gestão de horários e pagamentos.

Esta ambição, no entanto, foi confrontada com a limitação de tempo. Como resultado, embora o sistema seja funcionalmente rico, algumas decisões de design levaram a um maior acoplamento entre certos componentes, um compromisso que será refletido e detalhado ao longo do relatório. Para manter o foco nos objetivos de aprendizagem, o projeto foi desenvolvido de forma local, sem recorrer a bases de dados externas, com todos os dados geridos em memória.


1.2. Objetivos
Para alcançar a complexidade desejada e cumprir as exigências da unidade curricular, o objetivo principal foi demonstrar a aplicação prática dos seguintes conceitos obrigatórios de POO:

Classes Abstratas: Utilizar classes abstratas para definir "moldes" ou contratos para outras classes, como foi feito para Pessoa e Sala.
Herança Simples e Múltipla: Criar uma hierarquia de classes, usando herança simples para especializar tipos (como um Medico que é um tipo de Funcionario) e herança múltipla para combinar papéis (como no caso do EnfermeiroChefe).
Polimorfismo: Permitir que o sistema interagisse com objetos de diferentes classes através de uma interface comum. Este princípio é central na arquitetura, visível na capacidade da classe SistemaHospital de gerir todos os funcionários (Medico, Enfermeiro, etc.) numa única coleção, tratando-os de forma homogénea como Funcionario. Adicionalmente, foi aplicado na sobrescrita de métodos como __str__ para que personalizar a exibição de cada tipo de pessoa e na implementação do cálculo de pagamentos, onde diferentes regras são executadas através da mesma chamada ao método calcular().
Encapsulamento: Proteger os dados internos das classes, usando properties e setters para controlar o acesso e validar informações, como garantir que uma idade não seja negativa.
Modularização: Organizar o código em ficheiros separados (Program.py, Horario.py, Console.py), dividindo o projeto em partes lógicas: o modelo de dados, o sistema de horários e a interface do utilizador.

Em resumo, o objetivo foi construir um programa funcional que, fosse o mais detalhado/completo possivel, do modo a demonstrar o máximo do nosso conhecimento.


2. Desenvolvimento e Implementação
A secção seguinte apresenta em detalhe o código que constitui o Sistema de Gestão Hospitalar. A análise será feita de forma estruturada, seguindo a organização dos ficheiros descrita anteriormente (Program.py, Horario.py, e Console.py), para facilitar a compreensão de como cada módulo contribui para o funcionamento do projeto.

A apresentação seguirá a seguinte ordem:

Program.py (Módulo da lógica principal: Este ficheiro é o coração do sistema. Contém a representação de todas as entidades e conceitos do hospital. Aqui são definidas as estruturas de dados para Pessoa, Paciente, Funcionario, Sala e as suas variantes. Toda a lógica de negócio necessária para esses entidades, como as regras que definem um funcionário ou as ações de uma sala, está nesse módulo.

Horario.py (Módulo da gestão do Tempo): Este módulo foi criado para isolar e gerir toda a complexa lógica relacionada com a manipulação de tempo. Ele lida com a representação de horas, intervalos de tempo, pausas, e o cálculo de horas de trabalho diurnas e noturnas. Ao separar esta funcionalidade, o Módulo da Lógica (Program.py) mantém-se mais limpo e focado.

Console.py (Módulo da interface de linha de comando): Este módulo é a única parte do sistema que interage diretamente com o utilizador. A sua responsabilidade é exibir menus, recolher dados de entrada e fazer as chamadas aos outros módulos. Ele controla como os outros módulos são usados, traduzindo as ações do utilizador em comandos para o Módulo da Lógica, mas sem conter ele próprio a lógica. Esta separação tem como objetivo que se futuramente vá-se substituir a interface por outra seja mais facil, pois a maioria das alterações necessárias podem ser alteradas apenas substituindo este arquivo, mas devido ao tempo não foi possivel separar completamente a lógica da interface de linha de comandos da lógica principal.

Para cada classe analisada, o texto irá descrever o seu propósito, os seus dados principais e a funcionalidade de cada um dos seus métodos, mostrando como as ideias de desenho discutidas anteriormente foram aplicadas na prática.

3.1. Módulo Principal: Modelo de Domínio (Program.py)

3.1.1 Enumerações e Constantes
Para garantir a consistência, legibilidade e manutenibilidade do código no módulo principal, foram definidas constantes globais e enumerações (Enum) centralizando valores fixos e representam estados, evitando o uso de números/strings dispersas pelo código repetidamente.

Constantes Globais
Inicio_Turno_noturno e Fim_Turno_noturno: Definidas como objetos timedelta, estas constantes estabelecem um intervalo de tempo fixo para o que é considerado "turno noturno" em todo o sistema. A sua utilização centralizada é usada para que os cálculos de horas noturnas sejam consistentes.
max_pausas: Uma constante inteira que provavelmente serve como um limite ou parâmetro de configuração para a gestão de pausas nos horários.
Enumerações (Enum)

O uso de Enum promove a segurança de tipos e torna o código legivel

StatusAtendimento: Esta enumeração define os vários estados possíveis de um paciente dentro do atendimento do hospital (ex: Espera, Atendimento). A sua utilização permite um controlo de estado robusto e legível.
StatusSala: Define os estados de disponibilidade de uma sala (ex: Disponivel, Ocupado), facilitando a gestão pelos estados das salas.
Cargo: Esta estrutura é particularmente notável pela sua organização hierárquica. Em vez de uma única e extensa enumeração, Cargo atua como uma classe que agrupa enumerações agrupadas por área de funcionamento (Administrativo, Apoio, Saude). A categoria Saude contém, por sua vez, a enumeração Medico para especialidades médicas. Esta separação organiza os cargos, tornando a seleção de cargos mais intuitiva e estruturada. Mas devido á limitação do tempo não foi possivel adicionar multi-cargos então para o EnfermeiroChefe foi necessário uma lógica manual para a verificação no módulo da interface de linha de comandos.


3.1.2. Classe Abstrata Pessoa
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


3.1.3. Classe Paciente
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


3.1.4. Classe Base Funcionario
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


3.1.5. Subclasses de Funcionario: Medico, Enfermeiro, Administrativo
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


3.1.6. Herança Múltipla: Classe EnfermeiroChefe
A classe EnfermeiroChefe é atualmente o unico caso de herança múltipla no projeto. Ao herdar simultaneamente de Enfermeiro e Administrativo, esta classe cria um novo tipo de funcionário que combina as competências clínicas de um com as responsabilidades de gestão do outro.

Análise do Construtor (__init__) e Gestão da Herança Múltipla:
O construtor da classe demonstra uma abordagem cuidadosa para lidar com uma herança onde EnfermeiroChefe herda de duas classes que, por sua vez, herdam de uma mesma base, Funcionario. Para evitar a inicialização duplicada e conflituosa da classe Funcionario, o construtor usa do Construtor do Enfermeiro.__init__(...) primeiro. Esta chamada garante que toda a cadeia de inicialização até Pessoa é executada corretamente uma única vez, configurando os atributos de base e a lógica específica do enfermeiro (como a determinação do turno).
Em seguida, o construtor inicializa manualmente os atributos que são da classe Administrativo (self.setor e self.horas_registradas). Esta lógica serve para evitar problemas e simplificar a lógica.
A classe é um bom exemplo da junção de diversas regras de pagamento. Ela não só herda as regras que são definidas pelo Construtor do Enfermeiro (como o bónus noturno), mas também adiciona múltiplas novas regras (RegraBonusPorAtendimento, RegraBonusPercentual, RegraPagamentoPorHora). O resultado é um funcionário com o sistema de remuneração mais complexo do sistema.

Análise do Polimorfismo (__str__):
O método __str__ é novamente sobrescrito de forma polimórfica para criar uma representação que lida com a lógica tanto do Enfermeiro tanto do Administrativo.
A sua implementação é um espelho da sua herança: exibe informações provenientes do seu lado Enfermeiro (o turno), do seu lado Administrativo (o setor) e do seu papel de chefia (a listagem de múltiplos bónus).
Ao apresentar o "Salário Total", o método demonstra o resultado final, onde o método calcular_pagamento (herdado de Funcionario) processa a lista acumulada de todas as regras de pagamento para chegar a um valor final, encapsulando toda a complexidade do cálculo.

3.1.7. Regras de Pagamento
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


3.1.8. Hierarquia de Salas (Sala, SalaAtendimento, SalaEspera, SalaCirurgia)
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


3.1.9. Classe Orquestradora: SistemaHospital
A classe SistemaHospital é o ponto central de controlo de toda a aplicação. Gerindo os dados em memória.

1. Gestão Centralizada de Dados em Memória

A principal função da SistemaHospital é gerir a interação entre as variáveis/Classes do sistema.

Estrutura de Dados: O construtor __init__ estabelece a base para esta gestão ao inicializar um conjunto de dicionários. A escolha por dicionários permite um acesso rápido e eficiente a qualquer objeto através de uma chave única:
self.pacientes: Utiliza o número de utente como chave, permitindo a recuperação imediata de qualquer paciente.
self.funcionarios: Usa o número de funcionário como chave, facilitando a gestão do pessoal.
self.salas_espera e self.salas_cirurgia: Indexam as salas pelo seu nome, o que é mais intuitivo para as operações do utilizador.
Controlo de Identidade: A classe assume a responsabilidade pela geração de identificadores únicos para os pacientes através do atributo _proximo_numero_utente. Separar este contador, a SistemaHospital garante que não haverá repetições de identificadores durante a criação de novos pacientes.

2. Interface Simplificada

Criação de Entidades (Padrão Factory Simples):
registrar_paciente: Este método pode funcionar tanto com a variável ddo paciente tanto com os dados.
criar_area_especializada: Este é um bom exemplo do padrão Factory. Com uma única chamada, o método orquestra um processo de configuração de múltiplos passos: (1) instancia um objeto SalaEspera; (2) cria múltiplos objetos SalaAtendimento; e (3) estabelece a relação entre a sala de espera e as suas salas de atendimento através do método adicionar_sala_atendimento. O cliente que invoca este método não precisa de conhecer estes detalhes.
Recuperação e Interação:
obter_paciente e obter_funcionario: Fornecem um ponto de acesso único aos dados. A lógica de formatação do número de utente em obter_paciente está aqui centralizada, garantindo consistência.
gerar_relatorio_funcionario e gerar_relatorio_paciente: Estes métodos são uma demonstração do uso de polimorfismo a partir de uma classe gestora. A SistemaHospital não contém nenhuma lógica condicional para verificar o tipo de funcionário (Medico, EnfermeiroChefe, etc.). Ela confia no contrato estabelecido pela classe Pessoa, que obriga todas as subclasses a implementar o método __str__. Ao invocar str(funcionario), o Python seleciona a implementação correta do método, resultando num código mais limpo e extensível.

4. Conclusão
4.1. O que foi feito
Este projeto resultou num programa de gestão hospitalar que funciona, onde aplicámos os conhecimentos da disciplina de Programação e Sistemas de Informação. Conseguimos cumprir os objetivos principais e o código ficou bem organizado.

As ideias principais que usámos foram:

Criámos modelos base para as pessoas e para as salas, para garantir que todos seguiam uma estrutura comum.
Aproveitámos código já existente para criar especializações, como um Medico que é um tipo de Funcionario, e para juntar responsabilidades, como no caso do EnfermeiroChefe.
O sistema consegue lidar com diferentes tipos de funcionários e objetos de forma igual, e cada um sabe como se apresentar de forma diferente.
Protegemos os dados para evitar valores inválidos, como por exemplo, garantir que uma idade não pode ser negativa.
O código foi separado em ficheiros diferentes (Program.py, Horario.py, Console.py) para dividir as responsabilidades: um para a lógica, um para os horários e outro para a interação com o utilizador. Isto tornou o projeto mais limpo.
4.2. Desafios e o que aprendemos
Este foi um trabalho para aprender e aplicar os conceitos de PSI. Por isso, não usámos bases de dados nem interfaces gráficas, para nos focarmos apenas na lógica do programa, que era o objetivo.

Um dos desafios foi a classe EnfermeiroChefe, porque tivemos de juntar características de Enfermeiro e de Administrativo e fazer tudo funcionar bem.

Outro grande desafio foi o módulo de horários (Horario.py), porque lidar com tempo, durações e turnos que passam da meia-noite é complicado. A solução foi dividir o problema em partes mais pequenas.

Por fim, foi uma boa aprendizagem gerir ao mesmo tempo os dados que acontecem em tempo real no sistema e os dados que ficam guardados no histórico.

4.3. O que pode ser feito a seguir
Com a base que já temos, o projeto pode ser melhorado no futuro com as seguintes ideias:

Guardar os Dados: Fazer com que o programa guarde as informações em ficheiros ou numa base de dados, para não se perder tudo quando se fecha a aplicação.
Melhorar a Interface: Criar uma interface com botões e janelas para ser mais fácil de usar, ou uma API para que outros sistemas se possam ligar ao nosso.
Fazer Testes Automáticos: Adicionar testes ao código para garantir que tudo funciona como esperado e que futuras alterações não estragam nada.
Reorganizar o Código do Histórico: A forma como o histórico é guardado deixa as partes do código muito ligadas umas às outras. Podíamos mudar isso para tornar o sistema mais flexível e fácil de testar.