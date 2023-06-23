CREATE TABLE laboratorio (
  id_laboratorio INT UNIQUE AUTO_INCREMENT PRIMARY KEY,
  nome_lab VARCHAR(30) NOT NULL CHECK (nome_lab REGEXP '^[A-Za-zÀ-ÿ ]+$'),
  capacidade_lab INT NOT NULL,
  cidade_lab VARCHAR(30) NOT NULL CHECK (cidade_lab REGEXP '^[A-Za-zÀ-ÿ ]+$'),
  campus_lab VARCHAR(50) NOT NULL CHECK (campus_lab REGEXP '^[A-Za-zÀ-ÿ ]+$')
);