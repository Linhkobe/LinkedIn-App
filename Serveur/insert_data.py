import json
import pandas as pd
import mysql.connector
import re
from datetime import datetime
from sqlalchemy import create_engine
import os

# Function to establish a database connection
def connection(host, user, password, database, port):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
    return mydb

mydb = connection("localhost", "root", "root", "linkedin_project_app", 8889)
mycursor = mydb.cursor()

script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, 'new_all_data_profiles.json')

with open(file_path, encoding='utf-8') as file:
    data = json.load(file)

# Combine experience and education entries
combined_entries = []
for person_data in data:
    education_entries = []
    for edu in person_data.get('education', []):
        # Extract year using regex
        year_match = re.search(r'\d{4}', str(edu.get('date_end_edu', '')))
        year_part = year_match.group() if year_match else None

        education_entry = {
            'school_title': edu.get('school_title'),
            'date_start_edu': edu.get('date_start_edu'),
            'date_end_edu': year_part,
            'etape_diplome': edu.get('etape_diplome')
        }
        education_entries.append(education_entry)

    # Les personnes qui ont un diplôme de Master 2 MIAGE à l'université Côte d'Azur
    if any(
        edu_entry['date_end_edu'] is not None and int(edu_entry['date_end_edu']) <= datetime.now().year
        and edu_entry.get('school_title') is not None and "Universit\u00e9 C\u00f4te d\u2019Azur" in edu_entry['school_title']
        and edu_entry.get('etape_diplome') is not None and 'Master 2 MIAGE' in edu_entry['etape_diplome'] 
        or edu_entry.get('etape_diplome') is not None and 'Master 2 (M2)' in edu_entry['etape_diplome']
        or edu_entry.get('etape_diplome') is not None and 'Master MIAGE' in edu_entry['etape_diplome']
        or edu_entry.get('etape_diplome') is not None and 'MASTER 2' in edu_entry['etape_diplome'] 
        or edu_entry.get('etape_diplome') is not None and 'MASTER 2 MIAGE' in edu_entry['etape_diplome']
        for edu_entry in education_entries
    ):
        combined_entry = {
            'id': person_data.get('id'),
            'name': person_data.get('name'),
            'lien': person_data.get('lien'),
            'education': education_entries,
            'experience': person_data.get('expérience', [])
        }
        combined_entries.append(combined_entry)


# Create a DataFrame from the filtered data
df_filtered = pd.DataFrame(combined_entries)

##################################################
# Writing the filtered data to a JSON file - START
##################################################

# Assuming df_filtered contains the filtered data
# filtered_data_json = df_filtered.to_json(orient='records', default_handler=str)

# Writing the JSON data to a file
# with open('filtered_data.json', 'w', encoding='utf-8') as json_file:
#     json.dump(json.loads(filtered_data_json), json_file, ensure_ascii=False, indent=4)

##################################################
# Writing the filtered data to a JSON file - END
##################################################

##############################################################################

##################################################
############# Transform data - START #############
##################################################

# Transform JSON data into a list of dictionaries
df_filtered_2 = df_filtered.to_dict('records')
transformed_data = []
for person in df_filtered_2:
    # Filter person 
    person_data = {
        'id': person['id'],
        'name': person['name'],
        'lien': person['lien'],
        'experience': [],
        'education': []
    }

    # Transform experience data
    for indx, exp in enumerate(person['experience'], start=1):
        experience_entry = {
            'id': indx,
            'title_job': exp['title_job'].encode().decode('unicode_escape'),
            'date début': exp['date d\u00e9but'].encode().decode('unicode_escape'),
            'date fin': exp['date fin'].encode().decode('unicode_escape') if exp['date fin'] else None,
            'durée': exp['durée'].encode().decode('unicode_escape'),
            'url_company': exp['url_company'][0] if exp['url_company'] else None,
            'name_company': exp['name_company'][0].encode().decode('unicode_escape') if exp['name_company'] and exp['name_company'][0] else None
        }
        person_data['experience'].append(experience_entry)

    for idx, exp in enumerate(person['experience'], start=1):
        competence_entry = {
            'id': idx,
            'competence': exp['comp\u00e9tences'],
            'date_end_edu': edu['date_end_edu'],
            'etape_diplome': edu['etape_diplome']
        }
        person_data['experience'].append(competence_entry)

    for idx, exp in enumerate(person['experience'], start=1):
        ville_entry = {
            'id': idx,
            'ville': exp['ville'].encode().decode('unicode_escape'),
            'date_end_edu': edu['date_end_edu'],
            'etape_diplome': edu['etape_diplome']
        }
        person_data['experience'].append(ville_entry)

    for idx, exp in enumerate(person['experience'], start=1):
        ent_entry = {
            'id': idx,
            'ent': exp['name_company'],
            'url_ent': exp['url_company'],
            'date_end_edu': edu['date_end_edu'],
            'etape_diplome': edu['etape_diplome']
        }
        person_data['experience'].append(ent_entry)

    # Transform education data
    for idx, edu in enumerate(person['education'], start=1):
        education_entry = {
            'id': idx,
            'school_title': edu['school_title'],
            'date_start_edu': edu['date_start_edu'],
            'date_end_edu': edu['date_end_edu'],
            'etape_diplome': edu['etape_diplome']
        }
        person_data['education'].append(education_entry)

    for idx, edu in enumerate(person['education'], start=1):
        diplome_entry = {
            'id': idx,
            'school_title': edu['school_title'],
            'etape_diplome': edu['etape_diplome'],
            'date_end_edu': edu['date_end_edu']
        }
        person_data['education'].append(diplome_entry)


    transformed_data.append(person_data)
    

##################################################
############# Transform data - END ###############
##################################################

##############################################################################

##################################################################################
##---------------------------------- TABLE PROFIL -------------------- START #######
##################################################################################

###-------------------- DATAFRAME TABLE PROFIL ----------- START ###

person_data = []

for person in df_filtered_2:
    person_data.append({
        'id_profil': person['id'],
        'name': person['name'],
        'linkedin_url': person['lien']
    })

df_person = pd.DataFrame(person_data, columns=['id_profil', 'name', 'linkedin_url'])

###-------------------- DATAFRAME TABLE PROFIL ----------- END ###

#---------------------INSERT TABLE PROFIL---------------------START#

ids = df_person['id_profil'].tolist()
names = df_person['name'].tolist()
links = df_person['linkedin_url'].tolist()

# Prepare the INSERT query template
sql = "INSERT INTO `profil` VALUES (%s, %s, %s)"

# Iterate through each profile and execute the INSERT command
for i in range(len(names)):
    val = (ids[i], names[i], links[i])
    mycursor.execute(sql, val)

# Commit changes to the database
mydb.commit()


#---------------------INSERT TABLE PROFIL---------------------END# """

##################################################################################
##---------------------------------- TABLE PEROFIL -------------------- END ######
##################################################################################

########################################################################################

##################################################################################
##-------------------------------- TABLE VILLE -------------------- START ########
##################################################################################

###-------------------- DATAFRAME TABLE VILLE ----------- START ###

villes = [exp.get('ville', 'inconnu') for person in df_filtered_2 for exp in person['experience']]

ville_to_id = {ville: idx for idx, ville in enumerate(set(villes), start=1)}

ville_data = []

for ville, id_ville in ville_to_id.items():
    ville_name = ville if ville else "inconnu"
    if any(substring in ville_name for substring in ["mars", "déc", "\xa0an", "mois", "sept", "févr", "oct", "janv", "mai","juin", "août", "avr", "juil", "nov"]):
        ville_name = "inconnu"
    ville_data.append({
        'id_ville': id_ville,
        'ville': ville_name
    })

df_ville = pd.DataFrame(ville_data, columns=['id_ville', 'ville'])
#print(df_ville)
###-------------------- DATAFRAME TABLE VILLE ----------- END ###

#---------------------INSERT TABLE VILLE---------------------START#

id_ville = df_ville['id_ville'].tolist()
ville = df_ville['ville'].tolist()


# Prepare the INSERT query template
sql = "INSERT INTO `ville` VALUES (%s, %s)"

# Iterate through each profile and execute the INSERT command
for i in range(len(id_ville)):
    val = (id_ville[i],ville[i])
    mycursor.execute(sql, val)

# Commit changes to the database
mydb.commit()


#---------------------INSERT TABLE VILLE---------------------END#

##################################################################################
##-------------------------------- TABLE VILLE -------------------- END ##########
##################################################################################

##################################################################################
##------------------------------ TABLE EXPERIENCE_PRO ------------------- START ##
##################################################################################

###------------------- DATAFRAME TABLE EXPERIENCE_PRO ----------- START ###
from datetime import timedelta

villes = [exp.get('ville', 'inconnu') for person in df_filtered_2 for exp in person['experience']]

ville_to_id = df_ville.set_index('ville')['id_ville'].to_dict()

transformed_data = []
id_exp = 1

for person in df_filtered_2:
    for exp in person['experience']:
        ville = exp.get('ville', 'inconnu')
        if any(substring in ville for substring in ["mars", "déc", "\xa0an", "mois", "sept", "févr", "oct", "janv", "mai","juin", "août", "avr", "juil", "nov"]):
            ville = "inconnu"
        if ville not in ville_to_id:
            ville_to_id[ville] = len(ville_to_id) + 1
        transformed_data.append({
            'id_exp': id_exp,
            'id_person': person['id'],
            'title_job': exp['title_job'],
            'date_debut': exp['date début'],
            'date_fin': exp['date fin'],
            'duree': exp['durée'],
            'url_company': exp['url_company'] if exp['url_company'] else None,
            'name_company': exp['name_company'],
            'ville': ville,
            'id_ville': ville_to_id[ville]
        })
        id_exp += 1

df_experience = pd.DataFrame(transformed_data, columns=['id_exp', 'id_person', 'title_job', 'date_debut', 'date_fin', 'duree', 'url_company', 'name_company','ville', 'id_ville'])
df_experience['id_ville'] = df_experience['ville'].map(ville_to_id)
df_experience['id_ville'] = df_experience['id_ville'].where(df_experience['ville'].isin(ville_to_id), other=None)
def convert_duration(text):
    text = text.replace('\xa0', ' ')
    parts = text.split()

    if "moins" in parts and "an" in parts:
        return timedelta(days=364)  # Assuming 364 days for less than a year

    years = 0
    if "an" in parts:
        try:
            years_index = parts.index("an")
            years = int(parts[years_index - 1].strip())
        except ValueError:
            pass

    months = 0
    if "mois" in parts:
        try:
            months_index = parts.index("mois")
            months = int(parts[months_index - 1].strip())
        except ValueError:
            pass

    return timedelta(days=years * 365 + months * 30)

# Apply the function to the "duree" column
df_experience['duration'] = df_experience['duree'].apply(convert_duration)
df_experience['duration_num'] = df_experience['duration'].dt.days

df_experience['domaine'] = 'Autre'  # Default value for jobs not matching any domain

# Define keyword-based domain classification
domain_keywords = {
    'Développement logiciels': ['Web developper','Ingénieur en technologies de l’information','Ingénieur full stack','Pega Business Analyst', 'Pega Senior System Architect', 'JAVA/J2EE', 'Ingénieur d’études et de développement', 'Backend Engineer', 'linux', 'Java developer', 'Software Engineer for France Telecom R&D', 'Software Architect / Lead DevelopperTeam Manager and lead developper', 'Cloud Developer Operations and Infrastructure Engineer for Orange', 'Ingénieur système informatique', 'Software Development', 'Web Application Developer', 'Ingénieur débutant', 'Software Engineering', 'C# / JavaScript', "Chargée d'application", 'Informatique', 'DUT Informatique', 'Ingénieur Étude et Développement', 'Développement', 'Node.JS & Graph QL', 'Php', 'Information Systems Intern', 'Concepteur / Développeur', 'MOA des outils connectés ( IOT)', 'Created communication tool (PHP)', "Développement d'application Mobile (Android et BlackBerry)", 'IPhone et Android', 'Développeur de logiciels informatiques', 'Développeur applications mobiles', 'développement informatique', 'Assistant technique', 'CAO', 'Ingénieur coordination techniques et développement logiciels', 'Chargée de projets SI, télécoms et numériques', "Appui Opérationnel du Délégué de la Filière des Systèmes d'Informations", 'NET Software Engineer - IOT (Amadeus)', 'Analyste fonctionelle', 'Software Development Engineer', 'Front-end Developer', 'développement', 'Apprenti Assistant en Sécurite des Systèmes d’Information', 'C++ Developer', 'développement logiciel', 'Technicien télécommunications', 'DevOps', 'Testeuse', "Agent des Systèmes d'Informations", 'Dev ops', 'Ingénieur informatique', 'Test', 'Administrateur réseaux et systèmes', 'Développeur', 'Webmaster', 'Développeuse', 'Testeur', 'Software', 'back-end developer', 'JAVAProgrammeur informatique', 'Développeur web front-end / back-end', 'Fullstack JS developer', 'Angular', 'Développeur Java EE', 'Développeur Java/Groovy', 'Java', 'Ingénieur R&D', 'logiciel', 'Software Engineer', 'Developer'],
    'Management': ['Account Manager','Analyste - Gestion','Chief Technology Officer','Responsable','Analyste de la performance commerciale','Président','Vice-Président','Responsable marketing','Business Analyst','Direction de programme Cybersecurite' 'Technical Group Manager','Business Unit Manager','Technical Account Manager','Chef de produit','Responsable technique sur le projet KARMA' 'Responsable technique','CHARGE DE MISSION','Assistant de gestion technique','Project leader','Responsable methode et organisation','Directeur','Directeur de projet','Directeur de mission','Assistant Configuration Manager - Business Improvement','Configuration Manager- process & tools','Stage de mise en situation entrepreneuriale','Chargé d\'Affaires','Chargée de projet','Manager de Programme Innovation Collaborative','Responsable Projets Digitaux','Assistant Chef Projet','Management','Responsable Commercial','Product Owner','Gestionnaire','Evolution fonctionnel ERP','Chargée de projet informatique','Chef de projet informatique','Ingénieur D\'affaires','Project Manager', 'Scrum Master', 'Project Coordinator', 'Program Manager', 'PMO', 'Chef de projet', 'Chargé de projet', 'Chargé de mission Commercial et Chef de projet', 'Responsable fonctionnel', 'Chargé de mission', 'Scrum master', 'Chef de Projets Informatiques', 'Chef de projet SI & Analyste BI', 'Chef de projet systèmes d’information', 'Chef de projet - Co founder', 'CEO - Co founder', 'Chef de projet Agile/ Commercial', 'Chef de projet Junior/Scrum Master', 'Chef de projet MOA'],
    'Données et analyses': ['Big Data Architect /  Lead Developper','Cloud Engineering Lead / Data & Machine Learning Architect','Data Science Engineer','SQL Developer','BIG Data','Statistiques et Informatique Décisionnelle','Analyste Développement Production Statistiques','Quantitative Risk Analyst','Analyste bases de données','SQL and .NET developer','Apprenti développeur Backend & BigData','Ingénieur Data','Analyste de données', 'Data Analyst', 'Data Engineer', 'CONSULTANT Data Engineer', 'Data Scientist','bases de données','Développeur BI'],
    'IT Consulting': ['Consulant Fonctionnel  AU SEIN D\'AXA ASSURANCE','Business Intelligence Developer','Responsable système d\'information','Expert technique','Consultant', 'Consultant junior', 'Consultant en gestion projet informatique - Front-end Developer', 'IT Consultant', 'Consultant SII - Ingénieur test et validation logiciel', 'Consultant SII - Ingénieur étude et développement logiciel', 'IT Business Analyst', 'Data Integration Consultant', 'Advanced IT Consultant / PMO - Test manager', 'Advanced IT consultant - Business Analyst Pricing', 'Consultant communications marketing', 'Consultant certifiée / Chef de Projets', 'Consultant Big Data', 'Big Data Consultant for Amadeus', 'Advanced IT consultant - Business Analyst Pricing', 'Consultant décisionnelle'],
    'Cyber-sécurité': ['Agent de prevention et de Securité','Agent de sécurité confirmé','Consulante cyber sécurité','sécurité informatique','Consultant en cybersécurité', 'Analyste cybersécurité', 'Apprenti en formation sur les outils de test de sécurité', "Apprenti développeur en sécurité des systèmes d'informations", "Stagiaire en développement de sécurité des systèmes d'informations", 'Consultant technique Compliance', 'Chargé Sécurité et Risques de l’Information', 'QA Automatisation & Développeur Java/React', 'QA Automatisation', 'Testeur QA & Intégrateur Logiciel', 'Cyber Security Consultant', 'Chargé Sécurité et Risques de l\’Information']
}

# Classify domains based on keywords
for domain, keywords in domain_keywords.items():
    escaped_keywords = [re.escape(keyword) for keyword in keywords]
    pattern = '|'.join(escaped_keywords)
    df_experience.loc[df_experience['title_job'].str.contains(pattern, case=False), 'domaine'] = domain
# print(df_experience)
# print(df_experience.columns)
###------------------- DATAFRAME TABLE EXPERIENCE_PRO ----------- END ###

#---------------------INSERT TABLE EXPERIENCE_PRO ---------------------START#

id_exp = df_experience['id_exp'].tolist()
id_profil = df_experience['id_person'].tolist()
titre_poste = df_experience['title_job'].tolist()
domaine = df_experience['domaine'].tolist()
date_debut = df_experience['date_debut'].tolist()
date_fin = df_experience['date_fin'].tolist()
duree = df_experience['duree'].tolist()
url_company = df_experience['url_company'].tolist()
name_company = df_experience['name_company'].tolist()
duration_num = df_experience['duration_num'].tolist()
id_ville = df_experience['id_ville'].tolist()


# Prepare the INSERT query template
sql = "INSERT INTO `experience_pro` VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s)"

# Iterate through each profile and execute the INSERT command
for i in range(len(id_exp)):
    date_fin_ = date_fin[i] if date_fin[i] is not None else 'N/A'
    url_company_ = url_company[i] if url_company[i] is not None else 'N/A'

    val = ( id_exp[i], id_profil[i], titre_poste[i], domaine[i], date_debut[i], date_fin_, duree[i], url_company_, name_company[i], duration_num[i], id_ville[i])
    mycursor.execute(sql, val)

# Commit changes to the database
mydb.commit()


#---------------------INSERT TABLE EXPERIENCE_PRO ---------------------END#

##################################################################################
##------------------------------ TABLE EXPERIENCE_PRO -------------------- END ###
##################################################################################

###########################################################################################

#############################################################################################

##################################################################################
##-------------------------------- TABLE EDUCATION -------------------- START ####
##################################################################################

###-------------------- DATAFRAME TABLE EDUCATION ----------- START ###

import numpy as np
df_education = []
id_edu = 1

for person in df_filtered_2:
    for edu in person['education']:
        df_education.append({
            'id_edu': id_edu,
            'id_person': person['id'],
            'school_title': edu['school_title'],
            'date_start_edu': edu['date_start_edu'],
            'date_end_edu': edu['date_end_edu'],
            'etape_diplome': edu['etape_diplome']
        })
        id_edu += 1

df_education = pd.DataFrame(df_education, columns=['id_edu','id_person', 'school_title', 'date_start_edu', 'date_end_edu', 'etape_diplome'])
# Define the conditions
conditions = [
    df_education["etape_diplome"].str.contains("PhD|Doctorat",na=False),
    df_education["etape_diplome"].str.contains("Master 2|M2|MASTER 2",case=False, na=False),
    df_education["etape_diplome"].str.contains("M1|Master 1|MASTER 1",case=False, na=False),
    df_education["etape_diplome"].str.contains("Master|MASTER", case=False, na=False),
    df_education["etape_diplome"].str.contains("DUT|iut|Diplôme universitaire de technologie|DUT, Informatique", case=False, na=False),
    df_education["etape_diplome"].str.contains("BTS|Brevet de technicien supérieur|bts|brevet de technicien supérieur|Brevet Technicien Supérieur",case=False, na=False),
    df_education["etape_diplome"].str.contains("Bachelor|Licence|Licence pro|Licence professionnelle|LICENCE|L3|Licence Pro",case=False, na=False),
    df_education["etape_diplome"].str.contains("Bac|Baccalauréat",case=False, na=False),
    df_education["etape_diplome"].str.contains("Classe préparatoire aux grandes écoles",case=False, na=False)
]
if "BTS" in df_education["etape_diplome"].values:
    conditions[4] = df_education["etape_diplome"].str.contains("BTS")
else:
    conditions[4] = False

# Define the choices
choices = ["PhD","Master 2", "Master 1", "Master", "DUT", "BTS", "Licence", "Baccalauréat", "CPGE"]

# Create the new column 'niveau' based on the conditions and choices
df_education["niveau"] = np.select(conditions, choices, default="non classifié")
df_education["anne_diplome"] = df_education["date_end_edu"].str.extract(r'(\d{4})')
df_education["anne_diplome"] = df_education["anne_diplome"].fillna("inconnu")
#print(df_education)
###-------------------- DATAFRAME TABLE EDUCATION ----------- END ###

#---------------------INSERT TABLE EDUCATION---------------------START#

id_edu = df_education['id_edu'].tolist()
id_profil = df_education['id_person'].tolist()
nom_ecole = df_education['school_title'].tolist()
date_debut = df_education['date_start_edu'].tolist()
date_fin = df_education['date_end_edu'].tolist()
etape_diplome = df_education['etape_diplome'].tolist()
niveau = df_education['niveau'].tolist()
anne_diplome = df_education['anne_diplome'].tolist()


# Prepare the INSERT query template
sql = "INSERT INTO `education` VALUES (%s, %s,%s, %s, %s,%s, %s,%s)"

# Iterate through each profile and execute the INSERT command
for i in range(len(id_edu)):
    date_debut_ = date_debut[i] if date_debut[i] is not None else 'N/A'
    date_fin_ = date_fin[i] if date_fin[i] is not None else 'N/A'
    etape_diplome_ = etape_diplome[i] if etape_diplome[i] is not None else 'N/A'

    val = (id_edu[i], id_profil[i],nom_ecole[i], date_debut_, date_fin_,etape_diplome_,niveau[i],anne_diplome[i])
    mycursor.execute(sql, val)

# Commit changes to the database
mydb.commit()


#---------------------INSERT TABLE EDUCATION---------------------END#

##################################################################################
##-------------------------------- TABLE EDUCATION -------------------- END ######
##################################################################################

#############################################################################################



#############################################################################################

###############################################################################################
##----------- JUNCTION TABLE EXPERIENCE_COMPETENCE / TABLE COMPETENCE ---------- START ########
###############################################################################################

##----------------- JUNCTION TABLE EXPERIENCE_COMPETENCE ---------- START ###

# Extract 'compétences' values from each person's experiences
competences = [comp for person in df_filtered_2 for exp in person['experience'] for comp in exp['compétences']]

comp_to_id = {comp: idx+1 for idx, comp in enumerate(dict.fromkeys(competences))}

#Create df_competence from comp_to_id
df_competence = pd.DataFrame(list(comp_to_id.items()), columns=['nom_competence', 'id_competence'])
exp_comp_data = []
id_exp = 1
id_compe = 1

for person in df_filtered_2:
    for exp in person['experience']:
        for comp in exp['compétences']:
            exp_comp_data.append({
                'id_exp': id_exp,
                'id_competence': comp_to_id[comp]
            })
            id_compe += 1
        id_exp += 1

exp_comp = pd.DataFrame(exp_comp_data, columns=['id_exp', 'id_competence'])
#print(exp_comp)
##----------------- JUNCTION TABLE EXPERIENCE_COMPETENCE ---------- END ###

#---------------------INSERT TABLE COMPETENCE---------------------START#

id_competence = df_competence['id_competence'].tolist()
nom_competence = df_competence['nom_competence'].tolist()

# Prepare the INSERT query template
sql = "INSERT INTO `competence` VALUES (%s, %s)"

# Iterate through each profile and execute the INSERT command
for i in range(len(id_competence)):
    val = ( id_competence[i], nom_competence[i])
    mycursor.execute(sql, val)

# Commit changes to the database
mydb.commit()

#---------------------INSERT TABLE COMPETENCE---------------------END#

#---------------------INSERT JUNCTION TABLE EXPERIENCE_COMPETENCE ---------------------START#

id_exp = exp_comp['id_exp'].tolist()
id_competence = exp_comp['id_competence'].tolist()

# Prepare the INSERT query template
sql = "INSERT INTO `experience_competence` VALUES (%s, %s)"

# Iterate through each profile and execute the INSERT command
for i in range(len(id_exp)):
    val = (id_exp[i], id_competence[i])
    mycursor.execute(sql, val)

# Commit changes to the database
mydb.commit()

#---------------------INSERT JUNCTION TABLE EXPERIENCE_COMPETENCE ---------------------END#


#############################################################################################
##----------- JUNCTION TABLE EXPERIENCE_COMPETENCE / TABLE COMPETENCE ---------- END ########
#############################################################################################

#############################################################################################

#############################################################################################
##----------- JUNCTION TABLE EXPERIENCE_ENTREPRISE / TABLE ENTREPRISE ---------- START ######
#############################################################################################

##----------------- JUNCTION TABLE EXPERIENCE_ENTREPRISE ---------- START ###

# Extract 'id_exp', 'name_company', and 'url_company' values from df_experience
companies = [(row['id_exp'], row['name_company'], row['url_company']) for index, row in df_experience.iterrows()]

# Convert companies to a DataFrame
df_exp_ent = pd.DataFrame(companies, columns=['id_exp', 'name_company', 'url_company'])

# Add an 'id_ent' column to df_exp_ent
df_exp_ent['id_entreprise'] = range(1, len(df_exp_ent) + 1)

# Create df_ent from df_exp_ent
df_ent = df_exp_ent[['id_entreprise', 'name_company', 'url_company']].drop_duplicates()
df_ent['name_company'] = df_ent['name_company'].replace('Junior MIAGE Concept', 'Junior MIAGE Concept Nice Sophia-Antipolis')

# Ensure that 'id_exp' corresponds exactly to 'name_company' and 'url_company'
df_exp_ent = df_exp_ent[['id_exp', 'id_entreprise']]

##----------------- JUNCTION TABLE EXPERIENCE_ENTREPRISE ---------- END ###

#---------------------INSERT TABLE ENTREPRISE---------------------START#

id_ent = df_ent['id_entreprise'].tolist()
name_company = df_ent['name_company'].tolist()
url_company = df_ent['url_company'].tolist()

# Prepare the INSERT query template
sql = "INSERT INTO `entreprise` VALUES (%s, %s, %s)"

# Iterate through each profile and execute the INSERT command
for i in range(len(id_ent)):
    url = url_company[i] if url_company[i] is not None else 'N/A'
    val = ( id_ent[i], name_company[i], url)
    mycursor.execute(sql, val)

# Commit changes to the database
mydb.commit()

#---------------------INSERT TABLE ENTREPRISE---------------------END#

#---------------------INSERT TABLE EXPERIENCE_ENTREPRISE---------------------START#

id_exp = df_exp_ent['id_exp'].tolist()
id_ent = df_exp_ent['id_entreprise'].tolist()

# Prepare the INSERT query template
sql = "INSERT INTO `experience_entreprise` VALUES (%s, %s)"

# Iterate through each profile and execute the INSERT command
for i in range(len(id_exp)):
    val = (id_exp[i], id_ent[i])
    mycursor.execute(sql, val)

# Commit changes to the database
mydb.commit()

#---------------------INSERT TABLE EXPERIENCE_ENTREPRISE---------------------END#

#############################################################################################
##----------- JUNCTION TABLE EXPERIENCE_ENTREPRISE / TABLE ENTREPRISE ---------- END ########
#############################################################################################