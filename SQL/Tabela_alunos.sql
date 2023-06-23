CREATE TABLE alunos (
  id_aluno INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(30) NOT NULL CHECK (nome REGEXP '^[A-Za-zÀ-ÿ ]+$'),
  email VARCHAR(40) UNIQUE NOT NULL CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
  matricula VARCHAR(12) UNIQUE NOT NULL CHECK (matricula REGEXP '^[0-9]{12}$')
);
