Projeto Final de Estrutura de Dados 3° semestre – Análise e Desenvolvimento de Sistemas – UNIMAR Prof. Me. Gustavo Marttos

Integrantes Nome: Ana Karla de Souza Moretão - RA: 1986881

Como parte do projeto final da disciplina de Estrutura de Dados, foi desenvolvido um sistema de gerenciamento de cursos. Dentre as principais funcionalidades, estão: cadastro de alunos com nome e e-mail, cadastro de cursos com nome e nome do instrutor, matrícula de alunos em cursos previamente cadastrados, cancelamento de matrícula de alunos em cursos, listagem de alunos, cursos e matrículas organizadas por curso, registro de histórico das últimas 50 ações realizadas e desfazer da última ação (matrícula, cancelamento).

Durante o desenvolvimento, foram utilizadas as seguintes estruturas de dados: Dicionário para armazenar alunos, cursos e matrículas devido à eficiência na busca de dados por chaves como IDs; Tupla para armazenar os dados constantes de cada aluno (nome, e-mail), escolha feita pela imutabilidade das tuplas; Conjunto para armazenar os IDs dos alunos matriculados em cada curso, evitando duplicatas automaticamente; Lista Encadeada para armazenar o histórico das últimas 50 ações realizadas no sistema, a estrutura de fila FIFO (First-In, First-Out) garante que apenas os 50 registros mais recentes sejam mantidos, e a remoção do elemento mais antigo seja eficiente; Pilha para implementar o recurso de “desfazer última ação”, armazenando ações (matrícula, cancelamento) e operando em modo LIFO (Last-In, First-Out) que é ideal para desfazer ações na ordem inversa à que foram armazenadas.

Para a execução do sistema:
1- Certifique-se de que em sua maquina esteja istalado quaisquer executores da linguagem Python.
2- Salve o código fornecido e rode o arquivo.
3- Siga o menu interativo.

LINK PARA O FLUXOGRAMA:
https://app.diagrams.net/#G1P75bGR0dkFWzEPeQyVOnES-ZRXjdbO01#%7B%22pageId%22%3A%22BJLczNaBKpbr6gB3zUHF%22%7D

---

Foi adicionada a Estrutura de Dados Lista Duplamente Encadeada para o gerenciamento de pré-requisitos de cursos, permitindo a adição e remoção eficiente de dependências, além de facilitar a verificação de cadeias de pré-requisitos para matrícula.
