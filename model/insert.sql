DELETE FROM DEPOSER;
DELETE FROM TRAITER;
DELETE FROM DECHET;
DELETE FROM COLLECTE;
DELETE FROM POINT_DE_COLLECTE;
DELETE FROM UTILISATEUR;
DELETE FROM ENTREPRISE;
DELETE FROM CATEGORIEDECHET;

ALTER TABLE CATEGORIEDECHET AUTO_INCREMENT = 1;
ALTER TABLE ENTREPRISE AUTO_INCREMENT = 1;
ALTER TABLE UTILISATEUR AUTO_INCREMENT = 1;
ALTER TABLE POINT_DE_COLLECTE AUTO_INCREMENT = 1;
ALTER TABLE COLLECTE AUTO_INCREMENT = 1;
ALTER TABLE DECHET AUTO_INCREMENT = 1;
ALTER TABLE DEPOSER AUTO_INCREMENT = 1;
ALTER TABLE TRAITER AUTO_INCREMENT = 1;


INSERT INTO CATEGORIEDECHET (nom_Type) VALUES ('Déchet organique');
INSERT INTO CATEGORIEDECHET (nom_Type) VALUES ('Déchet recyclable');
INSERT INTO CATEGORIEDECHET (nom_Type) VALUES ('Déchet non recyclable');

INSERT INTO ENTREPRISE (nom_Entreprise) VALUES ('Entreprise A');
INSERT INTO ENTREPRISE (nom_Entreprise) VALUES ('Entreprise B');
INSERT INTO ENTREPRISE (nom_Entreprise) VALUES ('Entreprise C');

INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel, motdepasse, id_Entreprise) VALUES ('Utilisateur 1', 'utilisateur1@example.com', 1234567890, 'password1', 1);
INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel, motdepasse, id_Entreprise) VALUES ('Utilisateur 2', 'utilisateur2@example.com', 1234567891, 'password2', 2);
INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel, motdepasse, id_Entreprise) VALUES ('Utilisateur 3', 'utilisateur3@example.com', 1234567892, 'password3', 3);

INSERT INTO POINT_DE_COLLECTE (Adresse, pos_x, pos_y, qte_max) VALUES ('Adresse 1', 12.3456, 78.9012, 100);
INSERT INTO POINT_DE_COLLECTE (Adresse, pos_x, pos_y, qte_max) VALUES ('Adresse 2', 23.4567, 89.0123, 200);
INSERT INTO POINT_DE_COLLECTE (Adresse, pos_x, pos_y, qte_max) VALUES ('Adresse 3', 34.5678, 90.1234, 300);

INSERT INTO COLLECTE (Date_Collecte) VALUES ('2024-01-01');
INSERT INTO COLLECTE (Date_Collecte) VALUES ('2024-02-01');
INSERT INTO COLLECTE (Date_Collecte) VALUES ('2024-03-01');

INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 1', 1, 10);
INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 2', 2, 20);
INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 3', 3, 30);
INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 4', 3, 30);


INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (1, 1, 1);
INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (2, 2, 2);
INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (3, 3, 3);
INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (4, 3, 3);


INSERT INTO TRAITER (id_point_collecte, id_Collecte, id_Type, qtecollecte) VALUES (1, 1, 1, 5);
INSERT INTO TRAITER (id_point_collecte, id_Collecte, id_Type, qtecollecte) VALUES (2, 2, 2, 15);
INSERT INTO TRAITER (id_point_collecte, id_Collecte, id_Type, qtecollecte) VALUES (3, 3, 3, 25);
