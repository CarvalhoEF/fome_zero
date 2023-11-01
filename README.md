# fome_zero
![Logo](https://github.com/CarvalhoEF/fome_zero/blob/main/logo1.png)

### 1. Problema de negócio

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

O Objetivo

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível, a fim auxiliar e à entender a empresa e conseguir tomar as decisões mais assertivas, conforme a solicitação do CEO.
O CEO Guerra é recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder às seguintes perguntas:

### Perguntas Gerais:

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

### Visão por País:

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

### Visão por Cidades:

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?

### Visão por Restaurantes:

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

### Visão por Tipos de Culinárias:

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

### 2. Premissas assumidas para a análise
Marketplace é o modelo de negócio assumido.
As principais visões do negócio são: 
- Visão por País,
- Visão por Cidades,
- Visão Culinária e Restaurantes.
  
### 3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as principais visões do modelo de negócio da empresa:

- Home:
Na página principal apresentamos as informações gerais do Marketplace com opção de seleção de filtro por país, além de uma breve descrição de como interagir com o painel.
- Visão por País:
Identificamos através dos gráficos as distribuições de restaurantes, cidades, média de avaliação e preço de prato por países, além de e uma mapa interativo, em que é possível identificar a localização de cada restaurante com rank de cores e suas principais características (Valor prato para dois, Tipo de Culinária e Nota Média de avaliação).
- Visão por Cidades:
Identificamos através dos gráficos as cidades com mais restaurantes e suas avaliações.
- Visão por Restaurantes e Culinárias:
Identificamos através dos gráficos as culinárias e restaurantes mais avaliadas.

### 4. Top 3 Insights de dados

A maior concentração de Restaurantes está no continente asiático, os Estados Unidos assumi o segundo lugar com mais restaurantes registrados na plataforma
Não há diferença na média de valores dos pratos para duas pessoas em restaurantes que aceitem ou não reservas.
Os restaurantes com pedidos online recebem mais acessos de avaliações na plataforma.

### 5. O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. O painel pode ser acessado através desse link: https://enfe-projects-fomezero.streamlit.app/

### 6. Conclusão

O objetivo desse projeto foi alcançado com a criação de um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

### 7. Próximo passos

1. Reduzir o número de métricas;
2. Dispor de dados com as informações dos clientes (Sexo, Idade e Preferência culinária);
3. Dispor de dados com período/datas de conversão das compras;
4. Adicionar uma feature com a conversão dos valores dos pratos para uma moeda única (utilização por exemplo do Dólar como padrão);
5. Criar modelo para prever satisfação dos clientes;
6. Adicionar novas visões de negócio.
