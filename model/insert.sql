DELETE FROM DEPOSER;
DELETE FROM TRAITER;
DELETE FROM DECHET;
DELETE FROM POINT_DE_COLLECTE;
DELETE FROM UTILISATEUR;
DELETE FROM ENTREPRISE;
DELETE FROM CATEGORIEDECHET;

ALTER TABLE CATEGORIEDECHET AUTO_INCREMENT = 1;
ALTER TABLE ENTREPRISE AUTO_INCREMENT = 1;
ALTER TABLE UTILISATEUR AUTO_INCREMENT = 1;
ALTER TABLE POINT_DE_COLLECTE AUTO_INCREMENT = 1;
ALTER TABLE DECHET AUTO_INCREMENT = 1;
ALTER TABLE DEPOSER AUTO_INCREMENT = 1;
ALTER TABLE TRAITER AUTO_INCREMENT = 1;


INSERT INTO CATEGORIEDECHET (nom_Type) VALUES ('Déchet organique');
INSERT INTO CATEGORIEDECHET (nom_Type) VALUES ('Déchet recyclable');
INSERT INTO CATEGORIEDECHET (nom_Type) VALUES ('Déchet non recyclable');

INSERT INTO ENTREPRISE (nom_Entreprise) VALUES ('Entreprise A');
INSERT INTO ENTREPRISE (nom_Entreprise) VALUES ('Entreprise B');
INSERT INTO ENTREPRISE (nom_Entreprise) VALUES ('Entreprise C');

INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel, motdepasse, nom_role) VALUES ('Utilisateur 1', 'utilisateur1@example.com', 1234567890, 'password1','Administrateur');
INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel, motdepasse, nom_role) VALUES ('Utilisateur 2', 'utilisateur2@example.com', 1234567891, 'password2','Visiteur');
INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel, motdepasse, nom_role) VALUES ('Utilisateur 3', 'utilisateur3@example.com', 1234567892, 'password3','Utilisateur');
INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel, motdepasse, nom_role) VALUES ('Utilisateur 4', 'utilisateur4@example.com', 282567892, 'password3', 'Utilisateur');


-- INSERT INTO POINT_DE_COLLECTE (adresse, nom_pt_collecte, pos_x, pos_y, qte_max) VALUES ('Adresse 1', 'Nom Point Collecte 1', 12.3456, 78.9012, 100);
-- INSERT INTO POINT_DE_COLLECTE (adresse, nom_pt_collecte, pos_x, pos_y, qte_max) VALUES ('Adresse 2', 'Nom Point Collecte 2', 23.4567, 89.0123, 200);
-- INSERT INTO POINT_DE_COLLECTE (adresse, nom_pt_collecte, pos_x, pos_y, qte_max) VALUES ('Adresse 3', 'Nom Point Collecte 3', 34.5678, 90.1234, 300);
INSERT INTO POINT_DE_COLLECTE (adresse, nom_pt_collecte, pos_x, pos_y, qte_max) VALUES 
('14 Rue Lethière, Basse-Terre 97100, Guadeloupe', 'Point Collecte A', 15.993210956167616, -61.72562080359923, 400),
('7 Rue Hyacinthe Bastaraud, Baie-Mahault 97122, Guadeloupe', 'Point Collecte B', 16.237367097712497, -61.58691688829211, 400),
("D 118, Saint-François 97118, Guadeloupe", 'Point Collecte C', 16.25376888483855, -61.27198821893571, 400);



INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 1', 1, 10);
INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 2', 2, 20);
INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 3', 3, 30);
INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 4', 3, 30);

INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 5', 1, 500);
INSERT INTO DECHET (nom_Dechet, id_Type, qte) VALUES ('Déchet 6', 2, 50);




INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (1, 1, 1);
INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (2, 2, 2);
INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (3, 3, 3);
INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (4, 3, 3);

INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (6, 1, 3);


--INSERTION POUR TESTER LE TRIGGER check_qte_deposee
--INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, id_point_collecte) VALUES (5, 2, 3);

-- Insertion des données dans la table TRAITER avec un jour entre chaque insertion
INSERT INTO TRAITER (id_point_collecte, id_Type, dateCollecte, qtecollecte) 
VALUES (1, 1, '2024-10-23 10:00:00', 5);
INSERT INTO TRAITER (id_point_collecte, id_Type, dateCollecte, qtecollecte) 
VALUES (2, 2, '2024-10-24 10:00:00', 15);
INSERT INTO TRAITER (id_point_collecte, id_Type, dateCollecte, qtecollecte) 
VALUES (3, 3, '2024-10-25 10:00:00', 25);
INSERT INTO TRAITER (id_point_collecte, id_Type, dateCollecte, qtecollecte) 
VALUES (3, 3, '2024-10-26 10:00:00', 61);
-- Insertion pour tester le trigger check_qte_collecte
INSERT INTO TRAITER (id_point_collecte, id_Type, dateCollecte, qtecollecte) 
VALUES (3, 3, '2024-10-27 10:00:00', 50);
INSERT INTO TRAITER (id_point_collecte, id_Type, dateCollecte, qtecollecte) 
VALUES (1, 1, '2024-10-27 14:00:00', 50);

