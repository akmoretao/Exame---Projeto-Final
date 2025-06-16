from datetime import datetime

alunos = {}  # Dicionário: id_aluno -> (nome, email)
cursos = {}  # Dicionário: id_curso -> {"nome": nome, "instrutor": instrutor}
matriculas = {}  # Dicionário: id_curso -> set(id_aluno)
pilha_desfazer = []  # Pilha para desfazer ações (LIFO)

# --- Classes para Lista Duplamente Encadeada ---

class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = DoublyNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def remove(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else: # É o head
                    self.head = current.next
                
                if current.next:
                    current.next.prev = current.prev
                else: # É o tail
                    self.tail = current.prev
                
                self.size -= 1
                return True
            current = current.next
        return False

    def contains(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def list_all(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

# Dicionário para armazenar os pré-requisitos: id_curso -> DoublyLinkedList de IDs de pré-requisitos
prerequisitos_cursos = {}

# --- Classes para Lista Encadeada Simples (Histórico) ---

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        if self.size > 50:  # Limite de 50 registros no histórico global
            self.pop_front()

    def pop_front(self):
        if self.head:
            self.head = self.head.next
            self.size -= 1
            if not self.head:  # Se a lista ficou vazia após remover o head
                self.tail = None

    def list_all(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

historico = LinkedList()  # Fila para histórico de ações (máximo 50 registros) (FIFO)

# --- Funções de Gerenciamento ---

def gerar_proximo_id(dicionario_entidades):
    """Gera o próximo ID sequencial para um dicionário de entidades."""
    return max(dicionario_entidades.keys(), default=0) + 1

def registrar_acao(acao: str):
    """Registra uma ação no histórico com timestamp."""
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    historico.append(f"[{timestamp}] {acao}")

def cadastrar_aluno(nome: str, email: str):
    """Cadastra um novo aluno no sistema."""
    if not nome.strip() or not email.strip():
        print("Erro: Nome e e-mail do aluno não podem estar vazios.")
        return

    for id_aluno, dados in alunos.items():
        if dados[1].lower() == email.strip().lower():
            print(f"Erro: Aluno com o e-mail '{email}' já cadastrado (ID: {id_aluno}).")
            return

    id_aluno = gerar_proximo_id(alunos)
    alunos[id_aluno] = (nome.strip(), email.strip())
    acao = f"Aluno '{nome.strip()}' cadastrado com ID {id_aluno}"
    print(f"Aluno '{nome.strip()}' cadastrado com sucesso. ID: {id_aluno}")
    registrar_acao(acao)
    pilha_desfazer.append({"tipo": "cadastro_aluno", "id_aluno": id_aluno})

def cadastrar_curso(nome: str, instrutor: str):
    """Cadastra um novo curso no sistema."""
    if not nome.strip() or not instrutor.strip():
        print("Erro: Nome do curso e instrutor não podem estar vazios.")
        return

    for id_curso, dados in cursos.items():
        if dados['nome'].lower() == nome.strip().lower() and \
           dados['instrutor'].lower() == instrutor.strip().lower():
            print(f"Erro: Curso '{nome.strip()}' com instrutor '{instrutor.strip()}' já cadastrado (ID: {id_curso}).")
            return

    id_curso = gerar_proximo_id(cursos)
    cursos[id_curso] = {"nome": nome.strip(), "instrutor": instrutor.strip()}
    acao = f"Curso '{nome.strip()}' cadastrado com ID {id_curso}"
    print(f"Curso '{nome.strip()}' cadastrado com sucesso. ID: {id_curso}")
    registrar_acao(acao)
    pilha_desfazer.append({"tipo": "cadastro_curso", "id_curso": id_curso})

# --- Funções de Gerenciamento de Pré-requisitos ---

def adicionar_prerequisito(id_curso: int, id_prerequisito: int):
    """Adiciona um pré-requisito a um curso."""
    if id_curso not in cursos:
        print(f"Erro: Curso com ID {id_curso} não encontrado.")
        return
    if id_prerequisito not in cursos:
        print(f"Erro: Curso pré-requisito com ID {id_prerequisito} não encontrado.")
        return
    if id_curso == id_prerequisito:
        print("Erro: Um curso não pode ser pré-requisito de si mesmo.")
        return

    if id_curso not in prerequisitos_cursos:
        prerequisitos_cursos[id_curso] = DoublyLinkedList()

    if prerequisitos_cursos[id_curso].contains(id_prerequisito):
        print(f"Erro: O curso '{cursos[id_prerequisito]['nome']}' já é pré-requisito para '{cursos[id_curso]['nome']}'.")
        return

    prerequisitos_cursos[id_curso].append(id_prerequisito)
    acao = f"Pré-requisito adicionado: Curso '{cursos[id_prerequisito]['nome']}' (ID: {id_prerequisito}) para '{cursos[id_curso]['nome']}' (ID: {id_curso})"
    print(acao)
    registrar_acao(acao)
    pilha_desfazer.append({"tipo": "adicao_prerequisito", "id_curso": id_curso, "id_prerequisito": id_prerequisito})

def remover_prerequisito(id_curso: int, id_prerequisito: int):
    """Remove um pré-requisito de um curso."""
    if id_curso not in cursos:
        print(f"Erro: Curso com ID {id_curso} não encontrado.")
        return
    if id_prerequisito not in cursos:
        print(f"Erro: Curso pré-requisito com ID {id_prerequisito} não encontrado.")
        return

    if id_curso in prerequisitos_cursos and prerequisitos_cursos[id_curso].remove(id_prerequisito):
        acao = f"Pré-requisito removido: Curso '{cursos[id_prerequisito]['nome']}' (ID: {id_prerequisito}) de '{cursos[id_curso]['nome']}' (ID: {id_curso})"
        print(acao)
        registrar_acao(acao)
        pilha_desfazer.append({"tipo": "remocao_prerequisito", "id_curso": id_curso, "id_prerequisito": id_prerequisito})
    else:
        print(f"Erro: O curso '{cursos[id_prerequisito]['nome']}' não é pré-requisito para '{cursos[id_curso]['nome']}'.")

def listar_prerequisitos(id_curso: int):
    """Lista os pré-requisitos de um curso."""
    if id_curso not in cursos:
        print(f"Erro: Curso com ID {id_curso} não encontrado.")
        return

    print(f"\n--- Pré-requisitos para o Curso: {cursos[id_curso]['nome']} (ID: {id_curso}) ---")
    if id_curso in prerequisitos_cursos and prerequisitos_cursos[id_curso].head:
        prereqs_ids = prerequisitos_cursos[id_curso].list_all()
        for p_id in prereqs_ids:
            if p_id in cursos:
                print(f"- {cursos[p_id]['nome']} (ID: {p_id})")
            else:
                print(f"- Curso com ID {p_id} (Removido ou Desconhecido)")
    else:
        print("Nenhum pré-requisito definido para este curso.")

def verificar_prerequisitos_para_matricula(id_aluno: int, id_curso: int):
    """Verifica se um aluno atende a todos os pré-requisitos de um curso."""
    if id_curso not in prerequisitos_cursos or not prerequisitos_cursos[id_curso].head:
        return True # Não há pré-requisitos para este curso, pode matricular

    prereqs_ids = prerequisitos_cursos[id_curso].list_all()
    
    # Set para controlar os pré-requisitos a verificar e evitar ciclos
    cursos_a_verificar = set(prereqs_ids)
    visitados = set()
    
    while cursos_a_verificar:
        current_prereq_id = cursos_a_verificar.pop()
        
        if current_prereq_id in visitados: # Evita ciclos de pré-requisitos
            continue
        
        visitados.add(current_prereq_id)
        
        if current_prereq_id not in cursos:
            print(f"Erro: Pré-requisito de ID {current_prereq_id} não encontrado no sistema. Verifique a configuração.")
            return False

        # Verifica se o aluno está matriculado no curso pré-requisito
        if current_prereq_id not in matriculas or id_aluno not in matriculas[current_prereq_id]:
            print(f"Erro: Aluno '{alunos[id_aluno][0]}' não atende ao pré-requisito: '{cursos[current_prereq_id]['nome']}'.")
            return False
        
        # Se este pré-requisito também tiver seus próprios pré-requisitos, adicioná-los para verificação
        if current_prereq_id in prerequisitos_cursos and prerequisitos_cursos[current_prereq_id].head:
            for next_prereq_id in prerequisitos_cursos[current_prereq_id].list_all():
                if next_prereq_id not in visitados:
                    cursos_a_verificar.add(next_prereq_id)
    
    return True

def matricular_aluno(nome_aluno: str, id_curso: int):
    """Matricula um aluno em um curso existente."""
    id_aluno = None
    for id_a, dados in alunos.items():
        if dados[0].lower() == nome_aluno.strip().lower():
            id_aluno = id_a
            break

    if id_aluno is None:
        print(f"Erro: Aluno '{nome_aluno.strip()}' não encontrado.")
        return

    if id_curso not in cursos:
        print(f"Erro: Curso com ID {id_curso} não encontrado.")
        return

    # --- VERIFICAÇÃO DE PRÉ-REQUISITOS ANTES DA MATRÍCULA ---
    if not verificar_prerequisitos_para_matricula(id_aluno, id_curso):
        return # A função já imprimiu a mensagem de erro

    if id_curso not in matriculas:
        matriculas[id_curso] = set()

    if id_aluno not in matriculas[id_curso]:
        matriculas[id_curso].add(id_aluno)
        acao = f"Aluno '{alunos[id_aluno][0]}' matriculado no curso '{cursos[id_curso]['nome']}'"
        print(f"Aluno '{alunos[id_aluno][0]}' matriculado no curso '{cursos[id_curso]['nome']}'.")
        registrar_acao(acao)
        pilha_desfazer.append({"tipo": "matricula", "id_aluno": id_aluno, "id_curso": id_curso})
    else:
        print(f"Erro: Aluno '{alunos[id_aluno][0]}' já está matriculado neste curso.")

def cancelar_matricula(nome_aluno: str, id_curso: int):
    """Cancela a matrícula de um aluno em um curso."""
    id_aluno = None
    for id_a, dados in alunos.items():
        if dados[0].lower() == nome_aluno.strip().lower():
            id_aluno = id_a
            break

    if id_aluno is None:
        print(f"Erro: Aluno '{nome_aluno.strip()}' não encontrado.")
        return
    
    if id_curso not in cursos:
        print(f"Erro: Curso com ID {id_curso} não encontrado.")
        return

    if id_curso in matriculas and id_aluno in matriculas[id_curso]:
        matriculas[id_curso].discard(id_aluno)
        acao = f"Matrícula cancelada: Aluno '{alunos[id_aluno][0]}' no curso '{cursos[id_curso]['nome']}'"
        print("Matrícula cancelada com sucesso.")
        registrar_acao(acao)
        pilha_desfazer.append({"tipo": "cancelamento", "id_aluno": id_aluno, "id_curso": id_curso})
    else:
        print(f"Erro: Matrícula do aluno '{alunos[id_aluno][0]}' no curso '{cursos[id_curso]['nome']}' não encontrada.")

def desfazer_acao():
    """Desfaz a última ação registrada na pilha de desfazer."""
    if not pilha_desfazer:
        print("Nenhuma ação para desfazer.")
        return

    ultima_acao = pilha_desfazer.pop()
    tipo = ultima_acao["tipo"]

    if tipo == "matricula":
        id_aluno = ultima_acao["id_aluno"]
        id_curso = ultima_acao["id_curso"]
        
        if id_curso in matriculas and id_aluno in matriculas[id_curso]:
            matriculas[id_curso].discard(id_aluno)
            acao = f"Desfeito: Matrícula de '{alunos.get(id_aluno, ('Aluno Desconhecido',))[0]}' no curso '{cursos.get(id_curso, {}).get('nome', 'Curso Desconhecido')}' cancelada"
            print(acao)
            registrar_acao(acao)
        else:
            print("Erro ao desfazer: Matrícula não encontrada. Pode já ter sido desfeita ou não existia.")
    
    elif tipo == "cancelamento":
        id_aluno = ultima_acao["id_aluno"]
        id_curso = ultima_acao["id_curso"]
        
        if id_curso not in matriculas:
            matriculas[id_curso] = set()
        
        if id_aluno not in matriculas[id_curso]:
            matriculas[id_curso].add(id_aluno)
            acao = f"Desfeito: Matrícula de '{alunos.get(id_aluno, ('Aluno Desconhecido',))[0]}' no curso '{cursos.get(id_curso, {}).get('nome', 'Curso Desconhecido')}' restaurada"
            print(acao)
            registrar_acao(acao)
        else:
            print("Erro ao desfazer: Aluno já estava matriculado neste curso. Ação de cancelamento pode já ter sido desfeita.")
    
    elif tipo == "cadastro_aluno":
        id_aluno = ultima_acao["id_aluno"]
        if id_aluno in alunos:
            nome = alunos[id_aluno][0]
            del alunos[id_aluno]
            # Remove o aluno de todas as matrículas
            for alunos_ids_set in matriculas.values():
                alunos_ids_set.discard(id_aluno)
            acao = f"Desfeito: Cadastro do aluno '{nome}' removido"
            print(acao)
            registrar_acao(acao)
        else:
            print("Erro ao desfazer: Aluno não encontrado. Pode já ter sido removido.")
    
    elif tipo == "cadastro_curso":
        id_curso = ultima_acao["id_curso"]
        if id_curso in cursos:
            nome = cursos[id_curso]["nome"]
            del cursos[id_curso]
            matriculas.pop(id_curso, None) # Remove todas as matrículas relacionadas a este curso
            prerequisitos_cursos.pop(id_curso, None) # Remove os pré-requisitos definidos para este curso
            # Remove este curso como pré-requisito de outros cursos
            for curso_id, prereqs_list in list(prerequisitos_cursos.items()): # Usa list() para evitar erro de RuntimeError durante iteração e modificação
                if prereqs_list.remove(id_curso): # Tenta remover o curso como pré-requisito
                    pass # Se removeu, ok. A DLL já cuida da remoção.
            acao = f"Desfeito: Cadastro do curso '{nome}' removido"
            print(acao)
            registrar_acao(acao)
        else:
            print("Erro ao desfazer: Curso não encontrado. Pode já ter sido removido.")
    
    elif tipo == "adicao_prerequisito":
        id_curso = ultima_acao["id_curso"]
        id_prerequisito = ultima_acao["id_prerequisito"]
        if id_curso in prerequisitos_cursos and prerequisitos_cursos[id_curso].remove(id_prerequisito):
            acao = f"Desfeito: Pré-requisito de '{cursos.get(id_prerequisito, {}).get('nome', 'Curso Desconhecido')}' para '{cursos.get(id_curso, {}).get('nome', 'Curso Desconhecido')}' removido"
            print(acao)
            registrar_acao(acao)
        else:
            print("Erro ao desfazer: Pré-requisito não encontrado ou já desfeito.")
    
    elif tipo == "remocao_prerequisito":
        id_curso = ultima_acao["id_curso"]
        id_prerequisito = ultima_acao["id_prerequisito"]
        if id_curso in cursos and id_prerequisito in cursos: # Garante que os cursos ainda existem
            if id_curso not in prerequisitos_cursos:
                prerequisitos_cursos[id_curso] = DoublyLinkedList()
            if not prerequisitos_cursos[id_curso].contains(id_prerequisito): # Só adiciona se não estiver lá
                prerequisitos_cursos[id_curso].append(id_prerequisito)
                acao = f"Desfeito: Pré-requisito de '{cursos.get(id_prerequisito, {}).get('nome', 'Curso Desconhecido')}' para '{cursos.get(id_curso, {}).get('nome', 'Curso Desconhecido')}' restaurado"
                print(acao)
                registrar_acao(acao)
            else:
                print("Erro ao desfazer: Pré-requisito já estava presente.")
        else:
            print("Erro ao desfazer: Curso ou pré-requisito não encontrado.")

# --- Funções de Listagem ---

def listar_alunos():
    """Lista todos os alunos cadastrados."""
    if not alunos:
        print("Nenhum aluno cadastrado.")
    else:
        print("--- Alunos Cadastrados ---")
        for id_aluno, dados in alunos.items():
            print(f"ID: {id_aluno} | Nome: {dados[0]} | Email: {dados[1]}")

def listar_cursos():
    """Lista todos os cursos cadastrados."""
    if not cursos:
        print("Nenhum curso cadastrado.")
    else:
        print("--- Cursos Disponíveis ---")
        for id_curso, dados in cursos.items():
            print(f"ID: {id_curso} | Nome: {dados['nome']} | Instrutor: {dados['instrutor']}")

def listar_matriculas_por_curso():
    """Lista as matrículas agrupadas por curso."""
    if not matriculas:
        print("Nenhuma matrícula realizada.")
    else:
        print("--- Matrículas por Curso ---")
        for id_curso in sorted(matriculas.keys()):
            alunos_ids = matriculas[id_curso]
            curso = cursos.get(id_curso)
            if curso:
                print(f"\nCurso: {curso['nome']} (ID: {id_curso})")
                if alunos_ids:
                    for id_aluno in sorted(list(alunos_ids)):
                        aluno = alunos.get(id_aluno)
                        if aluno:
                            print(f"- {aluno[0]} (ID: {id_aluno})")
                        else:
                            print(f"- Aluno de ID {id_aluno} (removido)")
                else:
                    print("- Nenhum aluno matriculado neste curso.")
            else:
                print(f"\nErro: Curso com ID {id_curso} não encontrado (pode ter sido removido).")

def listar_historico_global():
    """Exibe o histórico de ações do sistema."""
    print("\n--- HISTÓRICO DE AÇÕES ---")
    registros = historico.list_all()
    if not registros:
        print("Nenhum registro no histórico global.")
    else:
        for registro in registros:
            print(registro)

# --- Menu Principal ---

def menu():
    """Exibe o menu principal do sistema e gerencia as opções do usuário."""
    while True:
        print("\n=== SISTEMA DE GERENCIAMENTO DE CURSOS ===")
        print("1. Cadastrar aluno")
        print("2. Cadastrar curso")
        print("3. Matricular aluno em curso")
        print("4. Cancelar matrícula")
        print("5. Listar alunos")
        print("6. Listar cursos")
        print("7. Listar matrículas por curso")
        print("8. Listar histórico global de ações")
        print("9. Desfazer última ação")
        print("10. Adicionar pré-requisito a curso")
        print("11. Remover pré-requisito de curso")
        print("12. Listar pré-requisitos de curso")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do aluno: ").strip()
            email = input("Email do aluno: ").strip()
            cadastrar_aluno(nome, email)
        elif opcao == "2":
            nome = input("Nome do curso: ").strip()
            instrutor = input("Nome do instrutor: ").strip()
            cadastrar_curso(nome, instrutor)
        elif opcao == "3":
            listar_alunos()
            nome_aluno = input("Nome do aluno: ").strip()
            listar_cursos()
            try:
                id_curso = int(input("ID do curso para matricular: "))
                matricular_aluno(nome_aluno, id_curso)
            except ValueError:
                print("Entrada inválida: O ID do curso deve ser um número inteiro.")
        elif opcao == "4":
            listar_alunos()
            nome_aluno = input("Nome do aluno: ").strip()
            listar_cursos()
            try:
                id_curso = int(input("ID do curso para cancelar matrícula: "))
                cancelar_matricula(nome_aluno, id_curso)
            except ValueError:
                print("Entrada inválida: O ID do curso deve ser um número inteiro.")
        elif opcao == "5":
            listar_alunos()
        elif opcao == "6":
            listar_cursos()
        elif opcao == "7":
            listar_matriculas_por_curso()
        elif opcao == "8":
            listar_historico_global()
        elif opcao == "9":
            desfazer_acao()
        elif opcao == "10":
            listar_cursos()
            try:
                id_curso = int(input("ID do curso (avançado/especializado) para adicionar pré-requisito: "))
                id_prerequisito = int(input("ID do curso que será o pré-requisito (base): "))
                adicionar_prerequisito(id_curso, id_prerequisito)
            except ValueError:
                print("Entrada inválida: Os IDs dos cursos devem ser números inteiros.")
        elif opcao == "11":
            listar_cursos()
            try:
                id_curso = int(input("ID do curso para remover pré-requisito: "))
                id_prerequisito = int(input("ID do pré-requisito a ser removido: "))
                remover_prerequisito(id_curso, id_prerequisito)
            except ValueError:
                print("Entrada inválida: Os IDs dos cursos devem ser números inteiros.")
        elif opcao == "12":
            listar_cursos()
            try:
                id_curso = int(input("ID do curso para listar pré-requisitos: "))
                listar_prerequisitos(id_curso)
            except ValueError:
                print("Entrada inválida: O ID do curso deve ser um número inteiro.")
        elif opcao == "0":
            print("Encerrando o sistema. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida do menu.")

# Inicia o menu principal
if __name__ == "__main__":
    menu()