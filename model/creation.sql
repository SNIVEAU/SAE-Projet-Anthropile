-- Supprimer les tables dans l'ordre inverse de leur création
DROP TABLE IF EXISTS DEPOSER;
DROP TABLE IF EXISTS TRAITER;
DROP TABLE IF EXISTS TRAVAILLER;
DROP TABLE IF EXISTS DECHET;
DROP TABLE IF EXISTS POINT_DE_COLLECTE;
DROP TABLE IF EXISTS COLLECTE;
DROP TABLE IF EXISTS UTILISATEUR;
DROP TABLE IF EXISTS ENTREPRISE;
DROP TABLE IF EXISTS CATEGORIEDECHET;

-- Créer les tables sans clés étrangères en premier
CREATE TABLE CATEGORIEDECHET (
  Id_Type  INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Nom_Type VARCHAR(42)
);

CREATE TABLE ENTREPRISE (
  id_Entreprise  INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Entreprise VARCHAR(42)
);

CREATE TABLE UTILISATEUR (
  id_Utilisateur  INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Utilisateur VARCHAR(42),
  mail            VARCHAR(42),
  numtel          VARCHAR(42)
);

CREATE TABLE POINT_DE_COLLECTE (
  Idptscollecte INTEGER NOT NULL AUTO_INCREMENT,
  Adresse       VARCHAR(42),
  pos_x         VARCHAR(42),
  pos_y         VARCHAR(42),
  qte_max       VARCHAR(42),
  qte           VARCHAR(42),
  PRIMARY KEY(Idptscollecte,adresse)
);

CREATE TABLE COLLECTE (
  id_Collecte   INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Date_Collecte VARCHAR(42)
);

-- Créer les tables avec des clés étrangères
CREATE TABLE DECHET (
  id_Dechet  INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Dechet VARCHAR(42),
  Id_Type    INTEGER NOT NULL,
  FOREIGN KEY (Id_Type) REFERENCES CATEGORIEDECHET (Id_Type)
);

CREATE TABLE DEPOSER (
  id_Dechet      INTEGER NOT NULL,
  id_Utilisateur INTEGER NOT NULL,
  Idptscollecte  INTEGER NOT NULL,
  PRIMARY KEY (id_Dechet, id_Utilisateur, Idptscollecte),
  FOREIGN KEY (id_Dechet) REFERENCES DECHET (id_Dechet),
  FOREIGN KEY (id_Utilisateur) REFERENCES UTILISATEUR (id_Utilisateur),
  FOREIGN KEY (Idptscollecte) REFERENCES POINT_DE_COLLECTE (Idptscollecte)
);

CREATE TABLE TRAITER (
  Idptscollecte INTEGER NOT NULL,
  id_Collecte   INTEGER NOT NULL,
  Id_Type       INTEGER NOT NULL,
  qtecollecte   VARCHAR(42),
  PRIMARY KEY (Idptscollecte, id_Collecte, Id_Type),
  FOREIGN KEY (Idptscollecte) REFERENCES POINT_DE_COLLECTE (Idptscollecte),
  FOREIGN KEY (id_Collecte) REFERENCES COLLECTE (id_Collecte),
  FOREIGN KEY (Id_Type) REFERENCES CATEGORIEDECHET (Id_Type)
);

CREATE TABLE TRAVAILLER (
  id_Utilisateur INTEGER NOT NULL,
  id_Entreprise  INTEGER NOT NULL,
  PRIMARY KEY (id_Utilisateur, id_Entreprise),
  FOREIGN KEY (id_Utilisateur) REFERENCES UTILISATEUR (id_Utilisateur),
  FOREIGN KEY (id_Entreprise) REFERENCES ENTREPRISE (id_Entreprise)
);

-- Trigger pour vérifier que la quantité d'une collecte ne dépasse pas la quantité entière
DELIMITER |
CREATE TRIGGER check_qte_collecte
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