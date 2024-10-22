-- Trigger pour vérifier que la quantité d'une collecte ne dépasse pas la quantité entière
DELIMITER |
CREATE OR REPLACE TRIGGER check_qte_collecte
BEFORE INSERT ON TRAITER
FOR EACH ROW
BEGIN
  DECLARE max_qte INT;
  DECLARE current_qte INT;
  
  SELECT qte_max, qte INTO max_qte, current_qte
  FROM POINT_DE_COLLECTE
  WHERE Idptscollecte = NEW.Idptscollecte;
  
  IF (NEW.qtecollecte + current_qte > max_qte) THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'La quantité de la collecte dépasse la quantité maximale autorisée pour ce point de collecte';
  END IF;
END;
|
DELIMITER ;


DELIMITER |
CREATE OR REPLACE TRIGGER check_qte_deposee
BEFORE INSERT ON DEPOSER
FOR EACH ROW 
BEGIN 
  DECLARE max_qte INT;
  DECLARE quantite_totale_actuelle INT;
  DECLARE mes VARCHAR(100)  default 'Le déposé est impossible car la quantité maximale est dépassée !!';

  SELECT qte_max, SUM(qte) into max_qte, quantite_totale_actuelle
  FROM DEPOSER natural join DECHET NATURAL JOIN POINT_DE_COLLECTE
  WHERE id_point_collecte = new.id_point_collecte;

  IF quantite_totale_actuelle > max_qte THEN
    signal SQLSTATE '45000' set MESSAGE_TEXT=mes;

END |
DELIMITER ;







