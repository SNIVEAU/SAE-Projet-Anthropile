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
  Id_Type  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Nom_Type VARCHAR(42)
);

CREATE TABLE ENTREPRISE (
  id_Entreprise  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Entreprise VARCHAR(42)
);

CREATE TABLE UTILISATEUR (
  id_Utilisateur  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Utilisateur VARCHAR(42),
  mail            VARCHAR(42),
  numtel          INT
);

CREATE TABLE POINT_DE_COLLECTE (
  Idptscollecte INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Adresse       VARCHAR(42) UNIQUE,
  pos_x         DECIMAL(10,4),
  pos_y         DECIMAL(10,4),
  qte_max       INT
);

CREATE TABLE COLLECTE (
  id_Collecte   INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Date_Collecte DATE
);

-- Créer les tables avec des clés étrangères
CREATE TABLE DECHET (
  id_Dechet  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nom_Dechet VARCHAR(42),
  Id_Type INT NOT NULL,
  qte INT,
  FOREIGN KEY (Id_Type) REFERENCES CATEGORIEDECHET (Id_Type)
);

CREATE TABLE DEPOSER (
  id_Dechet      INT NOT NULL,
  id_Utilisateur INT NOT NULL,
  Idptscollecte  INT NOT NULL,
  PRIMARY KEY (id_Dechet, id_Utilisateur, Idptscollecte),
  FOREIGN KEY (id_Dechet) REFERENCES DECHET (id_Dechet),
  FOREIGN KEY (id_Utilisateur) REFERENCES UTILISATEUR (id_Utilisateur),
  FOREIGN KEY (Idptscollecte) REFERENCES POINT_DE_COLLECTE (Idptscollecte)
);

CREATE TABLE TRAITER (
  Idptscollecte INT NOT NULL,
  id_Collecte   INT NOT NULL,
  Id_Type       INT NOT NULL,
  qtecollecte   INT,
  PRIMARY KEY (Idptscollecte, id_Collecte, Id_Type),
  FOREIGN KEY (Idptscollecte) REFERENCES POINT_DE_COLLECTE (Idptscollecte),
  FOREIGN KEY (id_Collecte) REFERENCES COLLECTE (id_Collecte),
  FOREIGN KEY (Id_Type) REFERENCES CATEGORIEDECHET (Id_Type)
);

CREATE TABLE TRAVAILLER (
  id_Utilisateur INT NOT NULL,
  id_Entreprise  INT NOT NULL,
  PRIMARY KEY (id_Utilisateur, id_Entreprise),
  FOREIGN KEY (id_Utilisateur) REFERENCES UTILISATEUR (id_Utilisateur),
  FOREIGN KEY (id_Entreprise) REFERENCES ENTREPRISE (id_Entreprise)
);
