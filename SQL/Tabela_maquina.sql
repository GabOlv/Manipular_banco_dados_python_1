CREATE TABLE maquina (
  id_maquina INT UNIQUE AUTO_INCREMENT PRIMARY KEY,
  nome_maquina VARCHAR(30) NOT NULL CHECK (nome_maquina REGEXP '^[A-Za-zÀ-ÿ0-9]+$'),
  status_maquina BOOLEAN NOT NULL CHECK (status_maquina IN (0, 1)),
  id_laboratorio INT, FOREIGN KEY (id_laboratorio) REFERENCES laboratorio (id_laboratorio)
);
