
--VÉRIFIÉ
-- Trigger pour vérifier que la quantité d'une collecte ne dépasse pas la quantité entière
DELIMITER |
CREATE OR REPLACE TRIGGER check_qte_deposee_insert
BEFORE INSERT ON DEPOSER
FOR EACH ROW 
BEGIN 
  DECLARE max_qte INT;
  DECLARE quantite_totale_actuelle INT;
  DECLARE qte_Ajoutee INT;

  DECLARE mes VARCHAR(200) DEFAULT 'Le déposé est impossible car la quantité maximale est dépassée !!';

  SELECT qte_max, IFNULL(SUM(qte),0) INTO max_qte, quantite_totale_actuelle
  FROM DEPOSER NATURAL JOIN DECHET NATURAL JOIN POINT_DE_COLLECTE
  WHERE id_point_collecte = NEW.id_point_collecte;

  SELECT qte into qte_Ajoutee
  FROM DECHET
  where id_Dechet=NEW.id_Dechet;

  IF quantite_totale_actuelle + qte_Ajoutee > max_qte THEN
    signal SQLSTATE '45000' set MESSAGE_TEXT=mes;
  END IF; 
END |
DELIMITER ;

DELIMITER |
CREATE OR REPLACE TRIGGER check_qte_deposee_update
BEFORE UPDATE ON DEPOSER
FOR EACH ROW 
BEGIN 
  DECLARE max_qte INT;
  DECLARE quantite_totale_actuelle INT;

  DECLARE qte_Ajoutee INT;

  DECLARE mes VARCHAR(200)  DEFAULT 'Le déposé est impossible car la quantité maximale est dépassée !!';

  SELECT qte_max, IFNULL(SUM(qte),0) INTO max_qte, quantite_totale_actuelle
  FROM DEPOSER NATURAL JOIN DECHET NATURAL JOIN POINT_DE_COLLECTE
  WHERE id_point_collecte = NEW.id_point_collecte;

  SELECT qte INTO qte_Ajoutee
  FROM DECHET
  where id_Dechet=NEW.id_Dechet;

  IF quantite_totale_actuelle + qte_Ajoutee > max_qte THEN
    signal SQLSTATE '45000' set MESSAGE_TEXT=mes;
  END IF; 
END |
DELIMITER ;


-- VÉRIFIÉ
-- Trigger pour vérifier que la quantité d'une collecte ne dépasse pas la quantité entière categorisé par le type
DELIMITER |
CREATE OR REPLACE TRIGGER check_qte_collecte
BEFORE INSERT ON COLLECTER
FOR EACH ROW
BEGIN
  DECLARE max_qte INT;
  DECLARE mes VARCHAR(200) DEFAULT 'La quantité de déchets de ce type à ce point dépasse la quantité maximale de la collecte !!';
  DECLARE current_qte INT;
  
  SELECT IFNULL(SUM(qte),0) INTO current_qte
  FROM POINT_DE_COLLECTE NATURAL JOIN DEPOSER NATURAL JOIN DECHET 
  where id_point_collecte = NEW.id_point_collecte and id_Type=NEW.id_Type;
  
  IF (current_qte > NEW.qtecollecte) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
  END IF;

END |
DELIMITER ;


DELIMITER |
CREATE OR REPLACE TRIGGER check_qte_collecte
BEFORE UPDATE ON COLLECTER
FOR EACH ROW
BEGIN
  DECLARE max_qte INT;
  DECLARE mes VARCHAR(200) DEFAULT 'La quantité de déchets de ce type à ce point dépasse la quantité maximale de la collecte !!';
  DECLARE current_qte INT;
  
  SELECT IFNULL(SUM(qte),0) INTO current_qte
  FROM POINT_DE_COLLECTE natural join DEPOSER natural join DECHET
  where id_point_collecte = NEW.id_point_collecte and id_Type=NEW.id_Type;
  
  IF (current_qte > NEW.qtecollecte) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = mes;
  END IF;

END |
DELIMITER ;

--VÉRIFIÉ
-- fonction pour récuperer la quantité totale d'un point de collecte
DELIMITER |
CREATE OR REPLACE FUNCTION quantite_point_collecte(id_pt_collecte int) RETURNS INT
BEGIN  
  DECLARE quantite INT;
  SELECT IFNULL(SUM(qte),0) into quantite
  FROM DEPOSER NATURAL JOIN DECHET NATURAL JOIN POINT_DE_COLLECTE
  WHERE id_point_collecte = id_pt_collecte;
  RETURN quantite;

END |
DELIMITER ;

select quantite_point_collecte(2);

--VÉRIFIÉ
-- fonction pour récuperer la quantité totale d'un point de collecte
DELIMITER |
CREATE OR REPLACE FUNCTION quantite_point_collecte_filtree(id_pt_collecte int, id_cat int) RETURNS INT
BEGIN  
  DECLARE quantite INT;
  SELECT IFNULL(SUM(qte),0) into quantite
  FROM DEPOSER NATURAL JOIN DECHET NATURAL JOIN POINT_DE_COLLECTE 
  WHERE id_point_collecte = id_pt_collecte and id_Type=id_cat;
  RETURN quantite;

END |
DELIMITER ;

select quantite_point_collecte_filtree(2,2);


DELIMITER |
CREATE OR REPLACE TRIGGER SUPPRIME_DECHET_APRES_ETRE_TRAITE
AFTER INSERT ON COLLECTER
FOR EACH ROW
BEGIN 
  DECLARE dechet INT;
  DECLARE nom_dec VARCHAR(42);
  DECLARE id_ty INT;
  DECLARE nom_ty VARCHAR(42);
  DECLARE quantity DECIMAL(10,4);
  DECLARE id_user INT;
  DECLARE _point INT;
  DECLARE fini BOOLEAN DEFAULT false;
  
  DECLARE lesDechets CURSOR FOR
    SELECT id_Dechet, nom_Dechet, id_Type, nom_Type, qte, id_Utilisateur, id_point_collecte
    FROM DEPOSER NATURAL JOIN DECHET NATURAL JOIN CATEGORIEDECHET NATURAL JOIN POINT_DE_COLLECTE  
    WHERE id_point_collecte = NEW.id_point_collecte AND id_Type = NEW.id_Type;
    
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = true;

  OPEN lesDechets;

  WHILE NOT fini DO
    FETCH lesDechets INTO dechet, nom_dec, id_ty, nom_ty, quantity, id_user,_point;

    IF NOT fini THEN
      DELETE FROM DEPOSER WHERE id_Dechet = dechet AND id_point_collecte = _point;
      DELETE FROM DECHET WHERE id_Dechet = dechet;
      INSERT INTO HISTORIQUE_DECHET(id_dechet, nom_dechet, id_type, nom_type, quantite, id_utilisateur) values (dechet, nom_dec, id_ty, nom_ty, quantity, id_user);
    END IF;
  END WHILE;
  
  CLOSE lesDechets;
END |
DELIMITER ;
