# SchellingSegregation
Simulação do modelo de segregação de Schelling usando python MESA - Computação Experimental 2021/2

## Hipótese
O modelo de Schelling é composto por dois grupos distintos que desejam ter um número mínimo de vizinhos (agentes) iguais (Homophily). Quando um agente alcança condições ideais, ele fica feliz (_happy_). A hipótese é: a partir de certas condições (como um alto número mínimo de vizinhos e uma alta densidade de agentes), é impossível (ou muito mais difícil) satisfazer todos os agentes, principalmente se a tolerância ao medo for muito baixa.

## Alterações no modelo anterior
Para realizar a simulação, foi utilizado uma versão alternativa baseada no [modelo anterior](https://github.com/gustavo-tomas/SchellingSegregation.git). Algumas mudanças consistem na adição das variáveis dependentes `satisfaction index` e da variável `fear`. A variável medo consiste em um valor gerado para cada agente em um dado passo. Se esse valor for maior que um nível de tolerância estabelecido pelo usuário, o agente se muda, mesmo que a condição de homofilia seja satisfeita. Abaixo se encontra uma listagem das mudanças em relação ao modelo anterior:

- Foram adicionadas as seguites variáveis dependentes:

  * `fear` (no agente): o medo gerado para um agente;
  
  * `fear` (no modelo): a tolerância do medo suportado;
  
  * `total_satisfaction_index`: mede o índice de satisfação dos agentes azuis e vermelhos;
  
  * `blue_satisfaction_index`: mede o índice de satisfação dos agentes azuis;
  
  * `red_satisfaction_index`: mede o índice de satisfação dos agentes vermelhos;

  * `total_blue_agents_count`: conta o número total de agentes azuis;

  * `total_red_agents_count`: conta o número total de agentes vermelhos;

  * `happy_blue_agents_count`: o número atual de agentes azuis felizes;

  * `happy_red_agents_count`: o número atual de agentes vermelhos felizes;

- Foi adicionado um controlador da tolerância ao medo `Fear tolerance`;

- Foi retirada a variável `max_steps`;

- Os dados obtidos com as simulações em _batch_ continuam sendo armazenados na pasta _results_ (talvez precise ser criada caso não exista ainda).

Essas mudanças foram feitas, principalmente, para obter um modelo mais interessante para a simulação de um ambiente real e a variável `max_steps` foi retirada porque não produzia um efeito satisfatório sobre o modelo original. 

## Funcionamento
Para executar as simulações, basta executar o comando `$ mesa runserver` no diretório raiz do projeto. O programa irá gerar simulações e, ao final, a interface gráfica será aberta no navegador.

## Resultados
O programa gera dois arquivos diferentes: __agent_data__ e __model_data__. Esses arquivos contém os resultados das simulações e podem ser encontrados na pasta __results__ (que deve ser criada caso ainda não exista). Nesses arquivos, são registradas diversas variáveis em nível de agente e modelo, com destaque para as seguintes:

- `FearTolerance`: a tolerância de cada agente ao medo;

- `Fear`: o medo de cada agente;

- `AgentType`: o tipo de agente (0 - azul e 1 - vermelho);

- `TotalSatisfactionIndex`: o índice de agentes azuis e vermelhos felizes (varia de [0, 1]);

- `BlueSatisfactionIndex`: o índice de agentes azuis felizes (varia de [0, 1]);

- `RedSatisfactionIndex`: o índice de agentes vermelhos felizes (varia de [0, 1]);

## Conclusão
<!-- completar a conclusão -->