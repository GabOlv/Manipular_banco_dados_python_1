CREATE TABLE emprestimo(
	id_emprestimo INT UNIQUE AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT, FOREIGN KEY (id_aluno) REFERENCES alunos (id_aluno),
    id_maquina INT, FOREIGN KEY (id_maquina) REFERENCES maquina (id_maquina),
    data_emprestimo DATE NOT NULL,
    hora_emprestimo TIME NOT NULL
);
