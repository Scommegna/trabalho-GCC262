# GCC262 - Grafos e suas aplicações

## Trabalho Prático 


    Prof:   Mayron César O. Moreira
    
    Aluno: Lucas Scommegna - 202310208
            

### Primeira Etapa:
Para essa primeira etapa, foram solicitadas a modelagem, leitura, visualização e retorno da lista de dados estatísticos de um grafo cuja problemática pode ser descrita da seguinte maneira:

Os nós desse problema representam as intersecções em uma região e suas arestas ou arcos serão suas vias de acesso. Para cada aresta ou arco, temos um custo  demanda associados.
O problema visa encontrar um conjunto de viagens de veículos com custo mínimo, tal que cada viagem comece e termine em um nó depósito, cada aresta requerida seja atendida em uma única viagem, e a demanda total para qualquer veículo não exceda uma determinada capacidade.

1. Quantidade de vértices;
2. Quantidade de arestas;
3. Quantidade de arcos;
4. Quantidade de vértices requeridos;
5. Quantidade de arestas requeridas;
6. Quantidade de arcos requeridos;
7. Densidade do grafo (order strength);
8. Componentes conectados; (Foram considerados componentes fracamente conectados)
9. Grau mínimo dos vértices;
10. Grau máximo dos vértices;
11. Intermediação;
12. Caminho médio;
13. Diâmetro.

---

### Instalação:
1. Clone esse repositório na sua máquina:

   ```bash
    git clone git@github.com:Scommegna/trabalho-GCC262.git
   
2. Após, caso não tenha um Ambiente Virtual (venv) já criado, crie um pelos seguintes comandos na pasta do projeto (É necessário ter o Python3 e o pip instalados e atualizados na sua máquina):

    ```bash
    python -m venv venv

3. Logo após, ative a venv pelo terminal:

    Para Windows(CMD):
   ```bash
    venv\Scripts\activate
   ```

   Para Linux/MacOS
   ```bash
    source venv/bin/activate
   ```
   
4. Após ativada a venv, instale as dependências com o seguinte comando:

   ```bash
    pip install -r requirements.txt
   ```

### Utilização:
Após concluída a instalação, o programa pode ser utilizado ou pelo próprio editor de texto executando o arquivo main.py, ou então pelo Jupyter, que pode ser inicializado pelo seguinte comando:

   ```bash
    jupyter notebook
   ```
