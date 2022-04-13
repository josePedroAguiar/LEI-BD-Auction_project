CREATE TABLE leiloes (
	id_leilao SERIAL,
	titulo		 VARCHAR(512) NOT NULL,
	descricao		 VARCHAR(512),
	detalhes		 VARCHAR(512),
	data_inicial	 TIMESTAMP NOT NULL,
	data_final_	 TIMESTAMP NOT NULL,
	preco_inicial	 BIGINT NOT NULL,
	preco_corrente	 BIGINT,
	cancelado		 BOOL NOT NULL DEFAULT False,
	user_vencedor	 VARCHAR(512),
	terminado		 BOOL NOT NULL DEFAULT false,
	data_user_username VARCHAR(512) NOT NULL,
	produtos_ean	 BIGINT NOT NULL,
	PRIMARY KEY(id_leilao)
);

CREATE TABLE licitacoes (
	valor		 INTEGER NOT NULL,
	data		 TIMESTAMP NOT NULL,
	leiloes_id_leilao	 BIGINT NOT NULL,
	data_user_username VARCHAR(512) NOT NULL
);

CREATE TABLE produtos (
	ean		 BIGINT,
	nome__do_produto VARCHAR(512) NOT NULL,
	quantidade	 INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY(ean)
);

CREATE TABLE mensagem_privada (
	texto		 VARCHAR(512) NOT NULL,
	data		 TIMESTAMP NOT NULL,
	leiloes_id_leilao	 BIGINT NOT NULL,
	data_user_username	 VARCHAR(512) NOT NULL,
	data_user_username1 VARCHAR(512) NOT NULL
);

CREATE TABLE data_admin (
	password VARCHAR(512) NOT NULL,
	username VARCHAR(512) UNIQUE NOT NULL
);

CREATE TABLE data_user (
	username VARCHAR(512),
	password VARCHAR(512) NOT NULL,
	email	 VARCHAR(512) UNIQUE NOT NULL,
	banido	 BOOL NOT NULL DEFAULT False,
	PRIMARY KEY(username)
);

CREATE TABLE mensagem_mural (
	texto		 VARCHAR(512) NOT NULL,
	data		 TIMESTAMP NOT NULL,
	data_user_username VARCHAR(512) NOT NULL,
	leiloes_id_leilao	 BIGINT NOT NULL
);

CREATE TABLE historico (
	data		 TIMESTAMP,
	titulo		 VARCHAR(512),
	descricao	 VARCHAR(512),
	detalhes		 VARCHAR(512),
	leiloes_id_leilao BIGINT NOT NULL

);

CREATE TABLE data_admin_data_user (
	data_user_username VARCHAR(512),
	PRIMARY KEY(data_user_username)
);

ALTER TABLE leiloes ADD CONSTRAINT leiloes_fk1 FOREIGN KEY (data_user_username) REFERENCES data_user(username);
ALTER TABLE leiloes ADD CONSTRAINT leiloes_fk2 FOREIGN KEY (produtos_ean) REFERENCES produtos(ean);
ALTER TABLE licitacoes ADD CONSTRAINT licitacoes_fk1 FOREIGN KEY (leiloes_id_leilao) REFERENCES leiloes(id_leilao);
ALTER TABLE licitacoes ADD CONSTRAINT licitacoes_fk2 FOREIGN KEY (data_user_username) REFERENCES data_user(username);
ALTER TABLE mensagem_privada ADD CONSTRAINT mensagem_privada_fk1 FOREIGN KEY (leiloes_id_leilao) REFERENCES leiloes(id_leilao);
ALTER TABLE mensagem_privada ADD CONSTRAINT mensagem_privada_fk2 FOREIGN KEY (data_user_username) REFERENCES data_user(username);
ALTER TABLE mensagem_privada ADD CONSTRAINT mensagem_privada_fk3 FOREIGN KEY (data_user_username1) REFERENCES data_user(username);
ALTER TABLE mensagem_mural ADD CONSTRAINT mensagem_mural_fk1 FOREIGN KEY (data_user_username) REFERENCES data_user(username);
ALTER TABLE mensagem_mural ADD CONSTRAINT mensagem_mural_fk2 FOREIGN KEY (leiloes_id_leilao) REFERENCES leiloes(id_leilao);
ALTER TABLE historico ADD CONSTRAINT historico_fk1 FOREIGN KEY (leiloes_id_leilao) REFERENCES leiloes(id_leilao);
ALTER TABLE data_admin_data_user ADD CONSTRAINT data_admin_data_user_fk1 FOREIGN KEY (data_user_username) REFERENCES data_user(username);




CREATE FUNCTION licitacao_ultrapassada() RETURNS TRIGGER AS $ultrapassada$
    BEGIN
	  	/*IF NEW.preco_corrente <> OLD.preco_corrente THEN 
			INSERT INTO mensagem_privada
			VALUES('Foi feita uma licitação no seu leilão!', now(),OLD.id_leilao,NEW.user_vencedor,OLD.data_user_username);
		END IF;*/
        IF NEW.preco_corrente <> OLD.preco_corrente and OLD.data_user_username <> OLD.user_vencedor THEN 
            INSERT INTO mensagem_privada
            VALUES('A sua licitação foi ultrapassada!', now(),OLD.id_leilao,NEW.user_vencedor,OLD.user_vencedor);
        END IF;
        RETURN NEW;
    END;
$ultrapassada$ LANGUAGE plpgsql;
CREATE TRIGGER licitacao_ultrapassada
    AFTER UPDATE ON leiloes
    FOR EACH ROW
    EXECUTE PROCEDURE licitacao_ultrapassada();

CREATE FUNCTION historico() RETURNS TRIGGER AS $historico$
    BEGIN
	  	IF NEW.titulo <> OLD.titulo or NEW.detalhes <> OLD.detalhes  or NEW.descricao <> OLD.descricao THEN 
			INSERT INTO historico
			VALUES(now(),OLD.titulo,OLD.descricao,OLD.detalhes,OLD.id_leilao);
		END IF;
        RETURN NEW;
    END;
$historico$ LANGUAGE plpgsql;
CREATE TRIGGER historico
    AFTER UPDATE ON leiloes
    FOR EACH ROW
    EXECUTE PROCEDURE historico();

