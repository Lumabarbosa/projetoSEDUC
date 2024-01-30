CREATE TABLE Escola 
( 
 cnpj_escola BIGINT PRIMARY KEY,  
 nome_escola VARCHAR(90) NOT NULL, 
 telefone_escola VARCHAR(15),
 fk_endereco INT  
); 

CREATE TABLE Aluno 
( 
 id_matricula_aluno INT PRIMARY KEY AUTO_INCREMENT,  
 nome_aluno VARCHAR(30) NOT NULL,  
 data_nasc_aluno DATE NOT NULL,  
 fk_escola BIGINT,  
 fk_turma INT  
); 

CREATE TABLE Aplicador 
( 
 id_matricula_aplicador INT PRIMARY KEY AUTO_INCREMENT,  
 nome_aplicador VARCHAR(50) NOT NULL,  
 cpf_aplicador BIGINT NOT NULL,  
 email_aplicador VARCHAR(40) NOT NULL,  
 fk_escola BIGINT NOT NULL
);

CREATE TABLE Turma 
( 
 id_turma INT PRIMARY KEY AUTO_INCREMENT,  
 nome_turma CHAR(3) NOT NULL,  
 turno_turma VARCHAR(6) NOT NULL,  
 ano_letivo INT NOT NULL,  
 qntd_alunos_turma INT NOT NULL,  
 fk_escola BIGINT,  
 fk_avaliacao INT
); 

CREATE TABLE Avaliacao 
( 
 id_avaliacao INT PRIMARY KEY AUTO_INCREMENT,  
 tipo_avaliacao VARCHAR(30) NOT NULL,  
 data_inicio DATE NOT NULL,  
 data_fim DATE,  
 arquivo_audio VARCHAR(30) NOT NULL,  
 resultado_avaliacao VARCHAR(30) NOT NULL,  
 fk_aplicador INT  
); 

CREATE TABLE Endereco 
( 
 id_endereco INT PRIMARY KEY AUTO_INCREMENT,  
 rua_escola VARCHAR(100) NOT NULL,  
 numero_escola INT NOT NULL,  
 complemento_escola VARCHAR(100),  
 bairro_escola VARCHAR(50) NOT NULL 
); 

ALTER TABLE Endereco
ADD fk_escola BIGINT;

ALTER TABLE Endereco ADD FOREIGN KEY(fk_escola) REFERENCES Escola (cnpj_escola);
ALTER TABLE Escola ADD FOREIGN KEY(fk_endereco) REFERENCES Endereco (id_endereco);
ALTER TABLE Aluno ADD FOREIGN KEY(fk_escola) REFERENCES Escola (cnpj_escola);
ALTER TABLE Aluno ADD FOREIGN KEY(fk_turma) REFERENCES Turma (id_turma);
ALTER TABLE Aplicador ADD FOREIGN KEY(fk_escola) REFERENCES Escola (cnpj_escola);
ALTER TABLE Turma ADD FOREIGN KEY(fk_escola) REFERENCES Escola (cnpj_escola);
ALTER TABLE Turma ADD FOREIGN KEY(fk_avaliacao) REFERENCES Avaliacao (id_avaliacao);
ALTER TABLE Avaliacao ADD FOREIGN KEY(fk_aplicador) REFERENCES Aplicador (id_matricula_aplicador);

