INSERT INTO CATEGORIEDECHET (Nom_Type) 
VALUES ('Plastique'),
       ('Métal'),
       ('Verre'),
       ('Papier');

INSERT INTO COLLECTE (Date_Collecte) 
VALUES ('2024-10-21'),
       ('2024-10-22'),
       ('2024-10-23');

INSERT INTO DECHET (nom_Dechet, Id_Type) 
VALUES ('Bouteille en plastique', 1),  -- 1 correspond à 'Plastique'
       ('Canette en aluminium', 2),    -- 2 correspond à 'Métal'
       ('Bouteille en verre', 3),      -- 3 correspond à 'Verre'
       ('Journal', 4);                 -- 4 correspond à 'Papier'

INSERT INTO POINT_DE_COLLECTE (Adresse, pos_x, pos_y, qte_max, qte) 
VALUES ('12 Rue des Recycleurs', '48.8566', '2.3522', '1000', '200'),
       ('24 Avenue du Tri', '48.8567', '2.3523', '800', '400'),
       ('35 Boulevard Vert', '48.8568', '2.3524', '600', '300');



INSERT INTO ENTREPRISE (nom_Entreprise) 
VALUES ('EcoRecyclage'),
       ('RecycMétal'),
       ('VerreClean');



INSERT INTO TRAITER (Idptscollecte, id_Collecte, Id_Type, qtecollecte) 
VALUES (1, 1, 1, '150'),  -- Point de collecte 1, Collecte 1, Type 1 (Plastique)
       (2, 2, 2, '250'),  -- Point de collecte 2, Collecte 2, Type 2 (Métal)
       (3, 3, 3, '100');  -- Point de collecte 3, Collecte 3, Type 3 (Verre)


INSERT INTO UTILISATEUR (nom_Utilisateur, mail, numtel) 
VALUES ('Alice Martin', 'alice.martin@email.com', '0123456789'),
       ('Bob Dupont', 'bob.dupont@email.com', '0987654321'),
       ('Charlie Durand', 'charlie.durand@email.com', '0112233445');


INSERT INTO TRAVAILLER (id_Utilisateur, id_Entreprise) 
VALUES (1, 1),
       (2, 2),
       (3, 3);

INSERT INTO DEPOSER (id_Dechet, id_Utilisateur, Idptscollecte) 
VALUES (1, 1, 1),
       (2, 2, 2),
       (3, 3, 3);