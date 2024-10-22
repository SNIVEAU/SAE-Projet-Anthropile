
--VÉRIFIÉ
-- Trigger pour vérifier que la quantité d'une collecte ne dépasse pas la quantité entière
DELIMITER |
CREATE OR REPLACE TRIGGER check_qte_deposee
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
CREATE OR REPLACE TRIGGER check_qte_deposee
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
BEFORE INSERT ON TRAITER
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
BEFORE UPDATE ON TRAITER
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

select quantite_point_collecte_filtree(2,3);
