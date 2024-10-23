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


CREATE TABLE CATEGORIEDECHET (
  id_Type INT AUTO_INCREMENT PRIMARY KEY,
  nom_Type VARCHAR(42)
);

CREATE TABLE ENTREPRISE (
  id_Entreprise INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Entreprise VARCHAR(42)
);

CREATE TABLE UTILISATEUR (
  id_Utilisateur  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Utilisateur VARCHAR(42),
  mail VARCHAR(42),
  numtel INT,
  motdepasse VARCHAR(42),
  id_Entreprise INT,
  FOREIGN KEY (id_Entreprise) REFERENCES ENTREPRISE (id_Entreprise)
);

CREATE TABLE POINT_DE_COLLECTE (
  id_point_collecte INT AUTO_INCREMENT PRIMARY KEY,
  Adresse VARCHAR(42) UNIQUE,
  pos_x DECIMAL(10,4),
  pos_y DECIMAL(10,4),
  qte_max INT
);



CREATE TABLE DECHET (
  id_Dechet  INT AUTO_INCREMENT PRIMARY KEY,
  nom_Dechet VARCHAR(42),
  id_Type INT NOT NULL,
  qte INT,
  FOREIGN KEY (id_Type) REFERENCES CATEGORIEDECHET (id_Type)
);

CREATE TABLE DEPOSER (
  id_Dechet INT,
  id_Utilisateur INT,
  id_point_collecte INT ,
  PRIMARY KEY (id_Dechet, id_Utilisateur, id_point_collecte),
  FOREIGN KEY (id_Dechet) REFERENCES DECHET (id_Dechet),
  FOREIGN KEY (id_Utilisateur) REFERENCES UTILISATEUR (id_Utilisateur),
  FOREIGN KEY (id_point_collecte) REFERENCES POINT_DE_COLLECTE (id_point_collecte)
);

CREATE TABLE TRAITER (
  id_point_collecte INT NOT NULL,
  id_Type       INT NOT NULL,
  dateCollecte DATETIME,
  qtecollecte   INT,
  PRIMARY KEY (id_point_collecte, id_Type, dateCollecte),
  FOREIGN KEY (id_point_collecte) REFERENCES POINT_DE_COLLECTE (id_point_collecte),
  FOREIGN KEY (id_Type) REFERENCES CATEGORIEDECHET (id_Type)
);

