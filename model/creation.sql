DROP TABLE IF EXISTS AVIS;
DROP TABLE IF EXISTS APPARTENIR;
DROP TABLE IF EXISTS DEPOSER;
DROP TABLE IF EXISTS COLLECTER;
DROP TABLE IF EXISTS DECHET;
DROP TABLE IF EXISTS POINT_DE_COLLECTE;
DROP TABLE IF EXISTS TRAVAILLER;
DROP TABLE IF EXISTS UTILISATEUR;
DROP TABLE IF EXISTS ENTREPRISE;
DROP TABLE IF EXISTS CATEGORIEDECHET;
DROP TABLE IF EXISTS TOURNEE;
DROP TABLE IF EXISTS HISTORIQUE_DECHET;

CREATE TABLE CATEGORIEDECHET (
  id_Type INT AUTO_INCREMENT PRIMARY KEY,
  nom_Type VARCHAR(42), 
  priorite INT CHECK (priorite BETWEEN 1 AND 5)
);

CREATE TABLE ENTREPRISE (
  id_Entreprise INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Entreprise VARCHAR(42) UNIQUE
);

CREATE TABLE UTILISATEUR (
  id_Utilisateur INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Utilisateur VARCHAR(42),
  mail VARCHAR(42),
  numtel BIGINT,
  motdepasse VARCHAR(255),
  nom_role ENUM('Administrateur', 'Utilisateur', 'Visiteur') DEFAULT 'Utilisateur' 
);

CREATE TABLE TRAVAILLER (
id_utilisateur INT,
id_Entreprise INT,
PRIMARY KEY (id_utilisateur, id_Entreprise),
FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR (id_Utilisateur),
FOREIGN KEY (id_Entreprise) REFERENCES ENTREPRISE (id_Entreprise)

);

CREATE TABLE POINT_DE_COLLECTE (
  id_point_collecte INT AUTO_INCREMENT PRIMARY KEY,
  adresse VARCHAR(200) UNIQUE,
  nom_pt_collecte VARCHAR(42) UNIQUE,
  pos_x DECIMAL(10,4),
  pos_y DECIMAL(10,4),
  qte_max DECIMAL(10,4)
);

CREATE TABLE DECHET (
  id_Dechet INT AUTO_INCREMENT PRIMARY KEY,
  nom_Dechet VARCHAR(42),
  id_Type INT NOT NULL,
  qte DECIMAL(10,4),
  FOREIGN KEY (id_Type) REFERENCES CATEGORIEDECHET (id_Type)
);

CREATE TABLE TOURNEE (
  id_Tournee INT AUTO_INCREMENT PRIMARY KEY,
  date_collecte TIMESTAMP,
  duree INT
);

CREATE TABLE DEPOSER (
  id_Dechet INT,
  id_Utilisateur INT,
  id_point_collecte INT,
  PRIMARY KEY (id_Dechet, id_Utilisateur, id_point_collecte),
  FOREIGN KEY (id_Dechet) REFERENCES DECHET (id_Dechet),
  FOREIGN KEY (id_Utilisateur) REFERENCES UTILISATEUR (id_Utilisateur),
  FOREIGN KEY (id_point_collecte) REFERENCES POINT_DE_COLLECTE (id_point_collecte)
);

CREATE TABLE COLLECTER (
  id_point_collecte INT,
  id_Tournee INT,
  id_Type INT,
  qtecollecte DECIMAL(10,4),
  PRIMARY KEY (id_point_collecte, id_Tournee, id_Type),
  FOREIGN KEY (id_point_collecte) REFERENCES POINT_DE_COLLECTE (id_point_collecte),
  FOREIGN KEY (id_Tournee) REFERENCES TOURNEE (id_Tournee),
  FOREIGN KEY (id_Type) REFERENCES CATEGORIEDECHET (id_Type)
);

CREATE TABLE AVIS (
  id_Avis INT AUTO_INCREMENT PRIMARY KEY,
  id_Utilisateur INT NOT NULL,
  avis TEXT NOT NULL, 
  note INT CHECK (note BETWEEN 1 AND 5), 
  date_Avis TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
  FOREIGN KEY (id_Utilisateur) REFERENCES UTILISATEUR (id_Utilisateur)
);

CREATE TABLE HISTORIQUE_DECHET (
  id_dechet int,
  nom_dechet varchar(42),
  id_type int,
  nom_type varchar(42),
  quantite decimal(10,4), 
  id_utilisateur int
);

CREATE TABLE APPARTENIR (
  id_point_de_collecte INT,
  id_utilisateur INT,
  PRIMARY KEY (id_point_de_collecte, id_utilisateur),
  FOREIGN KEY (id_point_de_collecte) REFERENCES POINT_DE_COLLECTE (id_point_collecte),
  FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR (id_Utilisateur)
);

