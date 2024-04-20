from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import mysql.connector
from mysql.connector import Error
import subprocess
import os
import datetime
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = False
#si vous utilisez MAMP, ajoutez vous votre password et le port
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/linkedin_project_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app,origins='http://localhost:4200')

db = SQLAlchemy(app)
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func

### Profil table ###
class Profil(db.Model):
    __tablename__ = 'profil'
    id_profil = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(250))

    def serialize(self):
        return {
            "id_profil": self.id_profil,
            "name": self.name,
            "linkedin_url": self.linkedin_url
        }

### Education table ###
class Education(db.Model):
    __tablename__ = 'education'
    id_edu = db.Column(db.Integer, primary_key=True)
    id_profil = db.Column(db.Integer, db.ForeignKey('profil.id_profil'))
    nom_ecole = db.Column(db.String(200))
    date_debut = db.Column(db.String(200))
    date_fin = db.Column(db.String(200))
    etape_diplome = db.Column(db.String(250))
    niveau = db.Column(db.String(200))
    annee_diplome = db.Column(db.String(200))

    def serialize(self):
        return {
            "id_edu": self.id_edu,
            "id_profil": self.id_profil,
            "nom_ecole": self.nom_ecole,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "etape_diplome": self.etape_diplome,
            "niveau": self.niveau,
            "annee_diplome": self.annee_diplome
        }

### Entreprise table ###
class Entreprise(db.Model):
    __tablename__ = 'entreprise'
    id_entreprise = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(250))
    url_entreprise = db.Column(db.String(250))

    def serialize(self):
        return {
            "id_entreprise": self.id_entreprise,
            "nom": self.nom,
            "url_entreprise": self.url_entreprise
        }

### Competence table ###
class Competence(db.Model):
    __tablename__ = 'competence'
    id_competence = db.Column(db.Integer, primary_key=True)
    nom_competence = db.Column(db.Text)

    def serialize(self):
        return {
            "id_competence": self.id_competence,
            "nom_competence": self.nom_competence
        }

#### ExperiencePro ####
class ExperiencePro(db.Model):
    __tablename__ = 'experience_pro'
    id_exp = db.Column(db.Integer, primary_key=True)
    titre_poste = db.Column(db.Text)
    domaine = db.Column(db.String(200))
    date_debut = db.Column(db.String(200))
    date_fin = db.Column(db.String(200))
    id_profil = db.Column(db.Integer, db.ForeignKey('profil.id_profil'))
    id_ville = db.Column(db.Integer, db.ForeignKey('ville.id_ville'))
    duree = db.Column(db.String(200))
    url_company = db.Column(db.String(250))
    name_company = db.Column(db.String(250))
    duration_num = db.Column(db.Integer)

    def serialize(self):
        return {
            "id_exp": self.id_exp,
            "titre_poste": self.titre_poste,
            "domaine": self.domaine,
            "date_debut": self.date_debut,
            "date_fin": self.date_fin,
            "id_profil": self.id_profil,
            "duree":self.duree,
            "url_company":self.url_company,
            "name_company":self.name_company,
            "duration_num":self.duration_num,
            "id_ville":self.id_ville
        }

####  ExperienceEntreprise ####
class ExperienceEntreprise(db.Model):
    __tablename__ = 'experience_entreprise'
    id_exp = db.Column(db.Integer, db.ForeignKey('experience_pro.id_exp'), primary_key=True)
    id_entreprise = db.Column(db.Integer, db.ForeignKey('entreprise.id_entreprise'), primary_key=True)
    def serialize(self):
            return {
                "id_exp": self.id_exp,
                "id_entreprise": self.id_entreprise 
            }
####  ExperienceCompetence #####
class ExperienceCompetence(db.Model):
    __tablename__ = 'experience_competence'
    id_exp = db.Column(db.Integer, db.ForeignKey('experience_pro.id_exp'), primary_key=True)
    id_competence = db.Column(db.Integer, db.ForeignKey('competence.id_competence'), primary_key=True)

    def serialize(self):
        return {
            "id_exp": self.id_exp,
            "id_competence": self.id_competence
        }

#### Ville table ####
class Ville(db.Model):
    __tablename__ = 'ville'
    id_ville = db.Column(db.Integer, primary_key=True)
    ville = db.Column(db.String(250))
    def serialize(self):
        return {
            "id_ville": self.id_ville,
            "ville": self.ville
        }

@app.route('/api/dashboard/num_students', methods=['GET'])
def get_num_students():
    num_students = db.session.query(func.count(Profil.id_profil)).scalar()
    return jsonify(num_students)

@app.route('/api/dashboard/num_experiences', methods=['GET'])
def get_num_experiences():
    num_experiences = db.session.query(func.count(ExperiencePro.id_exp)).scalar()
    return jsonify(num_experiences)

@app.route('/api/dashboard/num_competences', methods=['GET'])
def get_num_competences():
    num_competences = db.session.query(func.count(Competence.id_competence)).scalar()
    return jsonify(num_competences)

@app.route('/api/dashboard/num_entreprises', methods=['GET'])
def get_num_entreprises():
    num_entreprises = db.session.query(
        func.count(func.distinct(ExperiencePro.name_company))
    ).scalar()
    return jsonify(num_entreprises)

@app.route('/api/duration/all', methods=['GET'])
def get_duration_data():
    durations = db.session.query(
        ExperiencePro.duration_num, func.count().label('count')
    ).group_by(
        ExperiencePro.duration_num
    ).order_by(
        ExperiencePro.duration_num
    ).all()

    data = [{'duration_num': d.duration_num, 'count': d.count} for d in durations]
    return jsonify(data)

@app.route('/api/ville/all', methods=['GET'])
def get_ville_data():
    return get_table_data(Ville)

@app.route('/api/profil/all', methods=['GET'])
def get_profil_data():
    return get_table_data(Profil)

@app.route('/api/entreprise/all', methods=['GET'])
def get_entreprise_data():
    return get_table_data(Entreprise)

@app.route('/api/education/all', methods=['GET'])
def get_education_data():
    return get_table_data(Education)


@app.route('/api/competence/all', methods=['GET'])
def get_competence_data():
    return get_table_data(Competence)

@app.route('/api/experience/all', methods=['GET'])
def get_experience_pro_data():
    return get_table_data(ExperiencePro)


@app.route('/api/expcom/all', methods=['GET'])
def get_expcom_data():
    return get_table_data(ExperienceCompetence)

@app.route('/api/expent/all', methods=['GET'])
def get_expent_data():
    return get_table_data(ExperienceEntreprise)

@app.route('/api/top-competences/<int:N>/all', methods=['GET'])
def get_top_competences(N):
    top_competences = db.session.query(
        Competence.nom_competence, func.count(ExperienceCompetence.id_competence).label('count')
    ).join(
        ExperienceCompetence, Competence.id_competence == ExperienceCompetence.id_competence
    ).group_by(
        Competence.nom_competence
    ).order_by(
        func.count(ExperienceCompetence.id_competence).desc()
    ).limit(N).all()

    total_count = sum(c.count for c in top_competences)

    data = [{'nom_competence': c.nom_competence, 'proportion': (c.count / total_count) * 100} for c in top_competences]
    return jsonify(data)

@app.route('/api/top-entreprises/<int:N>/all', methods=['GET'])
def get_top_entreprises(N):
    top_entreprises = db.session.query(
        Entreprise.nom, func.count(ExperienceEntreprise.id_entreprise).label('count')
    ).join(
        ExperienceEntreprise, Entreprise.id_entreprise == ExperienceEntreprise.id_entreprise
    ).group_by(
        Entreprise.nom
    ).order_by(
        func.count(ExperienceEntreprise.id_entreprise).desc()
    ).limit(N).all()

    total_count = sum(e.count for e in top_entreprises)

    data = [{'nom': e.nom, 'proportion': (e.count / total_count) * 100} for e in top_entreprises]
    return jsonify(data)

@app.route('/api/top-domaines/all', methods=['GET'])
def get_top_domaines():
    # Get total count excluding 'Autre'
    total = db.session.query(ExperiencePro).filter(ExperiencePro.domaine != 'Autre').count()

    # Get counts for each domaine excluding 'Autre'
    top_domaines = db.session.query(
        ExperiencePro.domaine, ((func.count(ExperiencePro.domaine) / total)*100).label('proportion')
    ).filter(
        ExperiencePro.domaine != 'Autre'
    ).group_by(
        ExperiencePro.domaine
    ).order_by(
        (func.count(ExperiencePro.domaine) / total).desc()
    ).all()

    data = [{'domaine': d.domaine, 'proportion': d.proportion} for d in top_domaines]
    return jsonify(data)

@app.route('/api/duree_job/all', methods=['GET'])
def get_experience_pro_durations():
    # Get duration_num for each row in the ExperiencePro table
    durations = db.session.query(ExperiencePro.duration_num).all()

    # Convert the result to a list of numbers
    data = [d[0] for d in durations]

    # Calculate min, q1, median, q3, max
    min_val = int(np.min(data))
    q1 = int(np.percentile(data, 25))
    median = int(np.median(data))
    q3 = int(np.percentile(data, 75))
    max_val = int(np.max(data))

    # Return the necessary statistics
    stats = {
        'min': min_val,
        'q1': q1,
        'median': median,
        'q3': q3,
        'max': max_val
    }

    return jsonify(stats)

@app.route('/api/top-jobs/all', methods=['GET'])
def get_top_jobs():
    top_jobs = db.session.query(
        ExperiencePro.titre_poste, func.count(ExperiencePro.titre_poste).label('count')
    ).group_by(
        ExperiencePro.titre_poste
    ).order_by(
        func.count(ExperiencePro.titre_poste).desc()
    ).limit(10).all()

    data = [{'titre_poste': j.titre_poste, 'count': j.count} for j in top_jobs]
    #data = [j.titre_poste for j in top_jobs] 
    return jsonify(data)

@app.route('/api/diplomes-par-annee/all', methods=['GET'])
def get_diplomes_par_annee():
    current_year = datetime.now().year
    total = db.session.query(Education).filter(Education.annee_diplome < current_year).count()
    diplomes = db.session.query(
        Education.annee_diplome, 
        ((func.count(Education.id_edu) / total) * 100).label('proportion')
    ).filter(
        Education.annee_diplome < current_year
    ).group_by(
        Education.annee_diplome
    ).order_by(
        Education.annee_diplome.asc()
    ).all()

    data = [{'annee_diplome': d.annee_diplome, 'proportion': d.proportion} for d in diplomes]
    return jsonify(data)

def get_table_data(model):
    try:
        data = model.query.all()
        return jsonify([item.serialize() for item in data])
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    
def create_database():
    try:
        
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port = 8889
        )

        # Créer un curseur à partir de la connexion
        cursor = connection.cursor()

        # Exécuter une commande SQL pour créer la base de données 
        cursor.execute("CREATE DATABASE IF NOT EXISTS linkedin_project_app")

        print("Base de données 'linkedin_project_app' créée avec succès")

        # Fermer la connexion temporairement
        connection.close()

        #reconnexion 
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="linkedin_project_app",
            port = 8889,
        )

        # Créer un nouveau curseur
        cursor = connection.cursor()

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Join the script directory with the relative path of your file
        file_path = os.path.join(script_dir, 'testDatabase.sql')

        with open(file_path, 'r') as file:
            sql_script = file.read()

        # Exécuter le script SQL pour créer les tables
        print("sql_script:", sql_script)
        for result in cursor.execute(sql_script, multi=True):
            pass
        connection.commit()

        print("Tables créées avec succès dans la base de données 'linkedin_project_app'")


    except Error as e:
        print(f"Erreur lors de la création de la base de données ou des tables : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
                        
# Nouvelle route pour exécuter le script Python
@app.route('/execute-script', methods=['POST'])
def execute_script():
    try:
        # Appel de la fonction create_database() pour créer la base de données et les tables si nécessaire
        create_database()

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Join the script directory with the relative path of your file
        file_path = os.path.join(script_dir, 'new_all_data_profiles.json')
        uploaded_file = request.files['file']

        uploaded_file.save(file_path)

        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Join the script directory with the relative path of your file
        script_path = os.path.join(script_dir, 'insert_data.py')       
        
        subprocess.run(["python", script_path])
        print("Script d'insertion de données exécuté avec succès.")
        
        # # Update the status after successful execution
        global script_execution_status
        script_execution_status = 'done'

        return jsonify({'success': 'Script exécuté avec succès'})

    except Exception as e:
        print(f"Erreur lors de l'exécution du script : {e}")
        return jsonify({'error': 'Erreur lors de l\'exécution du script'})
    
@app.route('/check-database-status', methods=['GET'])
def check_database_status():
    global script_execution_status

    # Check the status and return 'done' or 'pending' accordingly
    if script_execution_status == 'done':
        return jsonify({'status': 'done'})
    else:
        return jsonify({'status': 'pending'})

if __name__ == '__main__':
    app.run(debug=True)