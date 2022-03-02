# SchellingSegregation
Simulação do modelo de segregação de Schelling usando python MESA - Computação Experimental 2021/2

## Hipótese
O modelo de Schelling é composto por dois grupos distintos que desejam ter um número mínimo de vizinhos iguais (Homophily). A hipótese é: a partir de certas condições (como um alto número mínimo de vizinhos e uma alta densidade de agentes), é impossível satisfazer todos os agentes.

## Alterações no exemplo original
Para realizar a simulação, foi utilizado um exemplo do [modelo de schelling](https://github.com/projectmesa/mesa/tree/main/examples/schelling) oferecido pelo framework MESA. Para analisar essa hipótese, foram feitas algumas alterações nesse modelo, a saber:

- Os controles dos parâmetros foram alterados para permitir uma maior precisão na simulação dos modelos;
- Foi adicionado um controlador de passos máximos para limitar o tempo de simulação e evitar casos de simulação sem fim;
- Para coletar os dados, foram criados arquivos *.csv* armazenados na pasta results.

## Funcionamento
Para executar as simulações, basta executar o comando `$ mesa runserver` no diretório raiz do projeto.

## Resultados
O programa gera dois tipos de arquivos: _agent_data_ e _model_data_. Esses arquivos contém os resultados das simulações e podem ser encontrados na pasta results. Nesses arquivos, são registradas as seguintes variáveis:

- Density - A quantidade de agentes no grid, variando de 0 a 1;
- MinorityPC - A fração dos dois tipos de agentes, variando de 0 a 1;
- Homophily - A quantidade mínima de vizinhos do mesmo tipo, variando de 0 a 8;
- MaxSteps - O número máximo de passos da simulação, variando de 1 a 400.

## Conclusão
Após realizar as simulações, é evidente que o modelo não encontra soluções quando a densidade é muito alta e/ou a quantidade mínima de vizinhos é muito elevada. Por exemplo, uma simulação com homofilia valor 7, densidade de 0.8 e fração de 0.2 percorre 400 passos, mas não encontra solução, pois a exigência de 7 vizinhos iguais é muito forte.

De forma similar, apenas alterando os dados da densidade para 0.99 e homofilia para 1, a simulação percorre 400 passos e não encontra solução, mesmo com baixa homofilia. Isso ocorre porque indivíduos da minoria ficam isolados entre os da maioria e não conseguem encontrar vizinhos iguais.

Por fim, nota-se que a hipótese é válida. De fato, nota-se uma forte segregação e uma imensa barreira em encontrar vizinhos iguais quando a densidade é extremamente alta ou a homofilia é muito elevada.
