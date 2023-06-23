import mysql.connector
import os
from datetime import datetime


# Estabelece a conexão com o banco de dados
conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="cadastro"
)

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

def cadastro_usuario():
    try:
        # Definir os valores dos atribuos
        nome = input("Digite o nome: ")
        email = input("Digite o email: ")
        matricula = input("Digite a matrícula: ")
        
        # Executar os comandos sql com o cursor e insere os elementos acima no banco de dados nas devidas posições
        sql_insertion = "INSERT INTO alunos (nome, email, matricula) VALUES (%s, %s, %s)"
        cursor.execute(sql_insertion, (nome, email, matricula))
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
    except Exception as error:
        print("Ocorreu um erro durante o cadastro. Tente novamente.", error)

def exibir_usuarios():
    # Selecionar todos os elementos da tabela alunos por meio do cursor e exibe cada elemento de cada posição
    sql_query = "SELECT * FROM alunos"
    cursor.execute(sql_query)
    usuarios = cursor.fetchall()
    if usuarios:
        print("Usuários cadastrados:")
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Matrícula: {usuario[3]}")
    else:
        print("Nenhum usuário cadastrado.")

def buscar_usuarios():
    while True:
        # Estabeler o critério de busca e seleciona a tabela respectiva
        criterio = input("Digite o critério de busca (nome, matricula ou email): ")
        valor = input("Digite o valor a ser buscado: ")
        if criterio.lower() == "nome":
            # Retornar valores parecidos para nome e identicos para matricula e email
            sql_query = "SELECT * FROM alunos WHERE nome LIKE %s"
            valor = f"%{valor}%"
        elif criterio.lower() == "matricula":
            sql_query = "SELECT * FROM alunos WHERE matricula = %s"
        elif criterio.lower() == "email":
            sql_query = "SELECT * FROM alunos WHERE email = %s"
        else:
            print("Critério de busca inválido. Tente novamente.")
            continue
        
        try:
            # Executar o cursor e pegar todas as informações presentes no valor especificado pelo critério
            cursor.execute(sql_query, (valor,))
            usuarios = cursor.fetchall()
            # mostrar na tela os elementos encontrados baseados em suas posições
            if usuarios:
                print(f"Usuários encontrados com base no critério '{criterio}':")
                for usuario in usuarios:
                    print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Matrícula: {usuario[3]}")
            else:
                print("Nenhum usuário encontrado com base no critério especificado.")
            break
        except mysql.connector.Error as error:
            print("Ocorreu um erro ao buscar os usuários:", error)
            
def excluir_usuario():
    # Exibir a lista de usuários disponíveis e selecionar o ID para exclusão
    exibir_usuarios()
    id_usuario = input("Digite o ID do usuário que deseja excluir: ")
    # Fazer a verificação de digitos numericos
    if not id_usuario.isdigit():
        print("ID inválido. Digite um valor numérico válido.")
        return
    
    sql_query = "DELETE FROM alunos WHERE id_aluno = %s"
    
   
    try:
        # Chamar o cursor para executar o comando sql com os parametros especificados pelo id
        cursor.execute(sql_query, (id_usuario,))
        conexao.commit()
        affected_rows = cursor.rowcount
        if affected_rows == 0:
            print("Nenhum usuário encontrado com o ID fornecido.")
        else:
            print("Usuário excluído com sucesso!")
    except mysql.connector.Error as error:
        print("Ocorreu um erro ao excluir o usuário:", error)

def cadastro_maquina():
    try:
        # Executar inicialmente a verificação do laboratório para registro da maquina
        sql_query = "SELECT * FROM laboratorio"
        cursor.execute(sql_query)
        laboratorio = cursor.fetchone()
        # Definir valores de nome e estado da maquina
        if laboratorio:
            nome_maquina = input("Digite o nome da maquina: ")
            status_maquina = "0"
            
            # Exibir os laboratórios existentes para escolha do ID e solicitar ao usuario
            sql_query = "SELECT id_laboratorio, nome_lab FROM laboratorio"
            cursor.execute(sql_query)
            laboratorios = cursor.fetchall()
            print("Laboratórios existentes:")
            for lab in laboratorios:
                print(f"ID: {lab[0]}, Nome: {lab[1]}")
                
            id_laboratorio = input("Digite o ID do laboratório ao qual a máquina pertence: ")
            
            # Verificar se o ID do laboratório é válido
            sql_query = "SELECT id_laboratorio FROM laboratorio WHERE id_laboratorio = %s"
            cursor.execute(sql_query, (id_laboratorio,))
            lab_exist = cursor.fetchone()
            if lab_exist:
                # Inserir as novas informações na tabela com auxilio da cursor e comando sql
                sql_insertion = "INSERT INTO maquina (nome_maquina, status_maquina, id_laboratorio) VALUES (%s, %s, %s)"
                cursor.execute(sql_insertion, (nome_maquina, status_maquina, id_laboratorio))
                conexao.commit()
                print("Máquina cadastrada com sucesso.")
            else:
                print("ID do laboratório é invalido.")
        else:
            print("Nenhum laboratório encontrado.")
    except mysql.connector.Error as error:
        print("ocorreu um erro durante o cadastro da maquina: ", error)

def exibir_maquinas():
    # Selecionar todas as maquinas da tabela maquinas e exibir baseado em suas posições
    sql_query = "SELECT * FROM maquina"
    cursor.execute(sql_query)
    maquinas = cursor.fetchall()
    if maquinas:
        print("Máquinas cadastradas:")
        for maquina in maquinas:
            print(f"ID: {maquina[0]}, Nome: {maquina[1]}, Status: {maquina[2]}, Id_lab: {maquina[3]}")
    else:
        print("Nenhuma máquina cadastrado.")

def excluir_maquinas():
    # Buscar e exibir todas as maquinas para exclusão por ID
    sql_query_check = "SELECT COUNT(*) FROM maquina"
    cursor.execute(sql_query_check)
    count = cursor.fetchone()[0]
    if count == 0:
        print("Nenhuma máquina cadastrada.")
        return

    id_maquina = input("Digite o ID da máquina que deseja excluir (ou 'C' para cancelar): ")
    # Fazer uma verificação de numeração e opção para cancelamento da ação
    if id_maquina.upper() == 'C':
        print("Operação cancelada.")
        return
    if not id_maquina.isdigit():
        print("ID inválido. Digite um valor numérico válido.")
        return
    
    sql_query = "DELETE FROM maquina WHERE id_maquina = %s"
    
    try:
        # Inserir as novas informações na tabela com auxilio da cursor e comando sql 
        cursor.execute(sql_query, (id_maquina,))
        conexao.commit()
        affected_rows = cursor.rowcount
        if affected_rows == 0:
            print("Nenhuma máquina encontrada com o ID fornecido.")
        else:
            print("Máquina excluída com sucesso!")
    except mysql.connector.Error as error:
        print("Ocorreu um erro ao excluir a máquina:", error)
   
def info_lab():
    try:
        # Selecionar todos os elementos de laboratorio e printar as informações na tela
        sql_query = "SELECT * FROM laboratorio"
        cursor.execute(sql_query)
        laboratorio = cursor.fetchall()
        
        if laboratorio:
            for info in laboratorio:
                print(f"ID: {info[0]}, Nome: {info[1]}, Capacidade: {info[2]}, Cidade: {info[3]}, Campus: {info[4]}")
        # Caso não exista, iniciar o processo de cadastro do laboratório preenchendo seus atributos
        else:
            print("Nenhum Laboratório registrado.")
            resposta_lab = input("Deseja registrar um novo Laboratório? (S/N): ")
            if resposta_lab.upper() == 'S':
                nome_lab = input("Digite o nome do laboratório: ")
                capacidade_lab = int(input("Digite a capacidade do laboratório: "))
                cidade_lab = input("Digite a cidade do laboratório: ")
                campus_lab = input("Digite o Campus do laboratório: ")
                # Inserir as novas informações na tabela com auxilio da cursor e comando sql
                sql_insertion = "INSERT INTO laboratorio (nome_lab, capacidade_lab, cidade_lab, campus_lab) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_insertion, (nome_lab, capacidade_lab, cidade_lab, campus_lab))
                conexao.commit()
                print("Informações do laboratório cadastradas com sucesso!")
            else:
                print("Operação cancelada.")
    except mysql.connector.Error as error:
        print("Ocorreu um erro ao buscar as informações do laboratório:", error)
    trava = input("Pressione qualquer botão para continuar...")

def fazer_emprestimo(): 
    try:
        # Exibir os alunos disponíveis para escolha
        exibir_usuarios()
        id_aluno = input("Digite o ID do aluno que deseja realizar o empréstimo: ")
        
        # Verificar se o ID do aluno é válido
        sql_query = "SELECT id_aluno FROM alunos WHERE id_aluno = %s"
        cursor.execute(sql_query, (id_aluno,))
        aluno_exist = cursor.fetchone()
        if not aluno_exist:
            print("ID do aluno é inválido. Operação cancelada.")
            return
        
        # Verificar se o aluno já possui um empréstimo em andamento
        sql_query = "SELECT id_emprestimo FROM emprestimo WHERE id_aluno = %s"
        cursor.execute(sql_query, (id_aluno,))
        emprestimo_ativo = cursor.fetchone()
        if emprestimo_ativo:
            print("O aluno já possui um empréstimo em andamento. Não é possível solicitar outro empréstimo.")
            return
        
        # Exibir as máquinas disponíveis para escolha
        sql_query = "SELECT id_maquina, nome_maquina FROM maquina WHERE status_maquina = '0'"
        cursor.execute(sql_query)
        maquinas = cursor.fetchall()
        if not maquinas:
            print("Não há máquinas disponíveis para empréstimo no momento. Operação cancelada.")
            return
        
        print("Máquinas disponíveis para empréstimo:")
        for maquina in maquinas:
            print(f"ID: {maquina[0]}, Nome: {maquina[1]}")
        
        id_maquina = input("Digite o ID da máquina que deseja emprestar: ")
        
        # Verificar se o ID da máquina é válido e está disponível
        sql_query = "SELECT id_maquina FROM maquina WHERE id_maquina = %s AND status_maquina = '0'"
        cursor.execute(sql_query, (id_maquina,))
        maquina_exist = cursor.fetchone()
        if not maquina_exist:
            print("ID da máquina é inválido ou a máquina não está disponível para empréstimo. Operação cancelada.")
            return
        
        # Atualizar o status da máquina para '1' (emprestada)
        sql_update = "UPDATE maquina SET status_maquina = '1' WHERE id_maquina = %s"
        cursor.execute(sql_update, (id_maquina,))
        conexao.commit()
        
        # Registrar o empréstimo na tabela de empréstimos
        data_emprestimo = datetime.now().date()
        hora_emprestimo = datetime.now().time()
        
        sql_insertion = "INSERT INTO emprestimo (id_aluno, id_maquina, data_emprestimo, hora_emprestimo) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_insertion, (id_aluno, id_maquina, data_emprestimo, hora_emprestimo))
        conexao.commit()
        
        print("Empréstimo iniciado com sucesso!")
    except Exception as error:
        print(f"Ocorreu um erro ao analisar o empréstimo: {str(error)}")
        conexao.rollback

def exibir_emprestimos():
    sql_query = "SELECT id_emprestimo, id_maquina, id_aluno, data_emprestimo, hora_emprestimo FROM emprestimo"
    cursor.execute(sql_query)
    emprestimos = cursor.fetchall()

    if emprestimos:
        print("Empréstimos realizados:")
        for emprestimo in emprestimos:          
            print(f"ID: {emprestimo[0]}, id_aluno: {emprestimo[1]}, id_maquina: {emprestimo[2]}, Data: {emprestimo[3]}, Hora: {emprestimo[4]}")
    else:
        print("Nenhum empréstimo realizado.")
        
def desfazer_emprestimo():
    try:
        # Exibir os empréstimos ativos
        sql_query = "SELECT emprestimo.id_emprestimo, alunos.nome, maquina.nome_maquina FROM emprestimo JOIN alunos ON emprestimo.id_aluno = alunos.id_aluno JOIN maquina ON emprestimo.id_maquina = maquina.id_maquina"
        cursor.execute(sql_query)
        emprestimos = cursor.fetchall()
        
        if not emprestimos:
            print("Nenhum empréstimo ativo encontrado.")
            return
        
        print("Empréstimos ativos:")
        for emprestimo in emprestimos:
            print(f"ID Empréstimo: {emprestimo[0]}, Aluno: {emprestimo[1]}, Máquina: {emprestimo[2]}")
        
        id_emprestimo = input("Digite o ID do empréstimo que deseja desfazer: ")
        
        # Verificar se o ID do empréstimo é válido
        sql_query = "SELECT id_emprestimo FROM emprestimo WHERE id_emprestimo = %s"
        cursor.execute(sql_query, (id_emprestimo,))
        emprestimo_exist = cursor.fetchone()
        if not emprestimo_exist:
            print("ID do empréstimo é inválido. Operação cancelada.")
            return
        
        # Obter informações do empréstimo
        sql_query = "SELECT id_aluno, id_maquina FROM emprestimo WHERE id_emprestimo = %s"
        cursor.execute(sql_query, (id_emprestimo,))
        emprestimo_info = cursor.fetchone()
        
        id_aluno = emprestimo_info[0]
        id_maquina = emprestimo_info[1]
        
        # Atualizar o status da máquina para '0' (disponível)
        sql_update = "UPDATE maquina SET status_maquina = '0' WHERE id_maquina = %s"
        cursor.execute(sql_update, (id_maquina,))
        
        # Excluir o registro do empréstimo
        sql_delete = "DELETE FROM emprestimo WHERE id_emprestimo = %s"
        cursor.execute(sql_delete, (id_emprestimo,))
        
        conexao.commit()
        
        print("Empréstimo desfeito com sucesso!")
    except Exception as error:
        print(f"Ocorreu um erro ao analisar o empréstimo: {str(error)}")
        conexao.rollback

def resetar_emprestimos():
    try:
        # Deletar todos os registros da tabela emprestimo
        sql_delete = "DELETE FROM emprestimo"
        cursor.execute(sql_delete)
        conexao.commit()

        # Resetar o status das máquinas para 0
        sql_update = "UPDATE maquina SET status_maquina = '0'"
        cursor.execute(sql_update)
        conexao.commit()

        print("Os empréstimos foram resetados com sucesso.")
    except Exception as error:
        print(f"Ocorreu um erro ao resetar os empréstimos: {str(error)}")
        conexao.rollback()
# To do
# Completar função de criação e exclusão das tabelas
# Editar tipo de conexão

def start():
    while True:
        os.system('cls')
        print("1 - Sessão Usuários")
        print("2 - Sessão Maquinas")
        print("3 - Sessão Emprestimo")
        print("8 - Outros")
        print("9 - Informações Laboratório")
        print("0 - Fechar")
        escolha_menu = input("Digite uma opção: ")
        os.system('cls')
        # ----------- SESSÃO DOS USUARIOS ----------- #
        if escolha_menu == '1':
            os.system('cls')
            print("#-- Sessão Usuários --#")
            print("1 - Cadastrar usuários")
            print("2 - Exibir usuários")
            print("3 - Buscar usuário")
            print("4 - Excluir usuário")
            print("5 - Voltar")
            escolha_user = input("Digite uma opção: ")
            os.system('cls')
            if escolha_user == '1':
                print("#-- Cadastrar usuários --#")
                cadastro_usuario()
            elif escolha_user == '2':
                print("#-- Exibir usuários --#")
                exibir_usuarios()
            elif escolha_user == '3':
                print("#-- Buscar usuário --#")
                buscar_usuarios()
            elif escolha_user== '4':
                print("#-- Excluir usuário --#")
                excluir_usuario()
            else:
                continue
        # ----------- SESSÃO DAS MAQUINAS ----------- #
        elif escolha_menu == '2':
            os.system('cls')
            print("#-- Sessão Maquina --#")
            print("1 - Cadastrar Máquina")
            print("2 - Exibir Máquinas")
            print("3 - Deletar Máquinas")
            print("4 - Voltar")
            escolha_maq = input("Digite uma opção: ")
            os.system('cls')
            if escolha_maq == '1':
                print("#--Cadastrar máquina --#")
                cadastro_maquina()
            elif escolha_maq == '2':
                print("#-- Exibir máquinas --#")
                exibir_maquinas()
            elif escolha_maq == '3':
                print("#-- Excluir Máquina --#")
                excluir_maquinas()
            else:
                continue
        # ----------- SESSÃO DO EMPRESTIMO ----------- #
        elif escolha_menu == '3':
            os.system('cls')
            print("#-- Sessão Emprestimo --#")
            print("1 - Realizar Emprestimo")
            print("2 - Exibir Emprestimos")
            print("3 - Cancelar Emprestimo")
            print("4 - Voltar")
            escolha_emp = input("Digite uma opção: ")
            if escolha_emp == '1':
                print("#-- Realizar Emprestimo --#")
                fazer_emprestimo()
            elif escolha_emp =='2':
                exibir_emprestimos()
            elif escolha_emp == '3':
                print("#-- Desfazer Empréstimo --#")
                desfazer_emprestimo()
            else:
                continue
        # ----------- SESSÃO CONTROLE ----------- #
        elif escolha_menu == '8':
            os.system('cls')
            print("#-- Sessão Outros --#")
            print("1 - Resetar Emprestimos")
            print("0 - Voltar")
            escolha_ctrl = input("Digite uma opção: ")
            if escolha_ctrl == '1':
                resetar_emprestimos()
            else:
                continue
        elif escolha_menu == '9':
            os.system('cls')
            info_lab()  
        else:
            break

if __name__ == "__main__":
    start()
    
cursor.close()
conexao.close()