-- Create profil Table
CREATE TABLE profil (
    id_profil INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) CHARACTER SET utf8mb4,
    linkedin_url VARCHAR(255)
);

-- Create ville Table
CREATE TABLE ville (
    id_ville INT PRIMARY KEY AUTO_INCREMENT,
    ville VARCHAR(255)
);

-- Create competence Table
CREATE TABLE competence (
    id_competence INT PRIMARY KEY AUTO_INCREMENT,
    nom_competence VARCHAR(255)
);

-- Create entreprise Table
CREATE TABLE entreprise (
    id_entreprise INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255),
    url_entreprise VARCHAR(255)
);

-- Create experience_pro Table
CREATE TABLE experience_pro (
    id_exp INT PRIMARY KEY AUTO_INCREMENT,
    id_profil INT,
    titre_poste VARCHAR(255),
    domaine VARCHAR(255),
    date_debut VARCHAR(50),
    date_fin VARCHAR(50),
    duree VARCHAR(50),
    url_company VARCHAR(255),
    name_company VARCHAR(255),
    duration_num INT,
    id_ville INT,
    FOREIGN KEY (id_profil) REFERENCES profil (id_profil),
    FOREIGN KEY (id_ville) REFERENCES ville (id_ville)
);

-- Create Education Table
CREATE TABLE education (
    id_edu INT PRIMARY KEY AUTO_INCREMENT,
    id_profil INT,
    nom_ecole VARCHAR(255),
    date_debut VARCHAR(50),
    date_fin VARCHAR(50),
    etape_diplome VARCHAR(255),
    niveau VARCHAR(255),
    annee_diplome VARCHAR(255),
    FOREIGN KEY (id_profil) REFERENCES profil (id_profil)
);

-- Create experience_competence Table
CREATE TABLE experience_competence (
    id_exp INT,
    id_competence INT,
    FOREIGN KEY (id_exp) REFERENCES experience_pro (id_exp),
    FOREIGN KEY (id_competence) REFERENCES competence (id_competence)
);

-- Create experience_entreprise Table
CREATE TABLE experience_entreprise (
    id_exp INT,
    id_entreprise INT,
    FOREIGN KEY (id_exp) REFERENCES experience_pro (id_exp),
    FOREIGN KEY (id_entreprise) REFERENCES entreprise (id_entreprise)
);