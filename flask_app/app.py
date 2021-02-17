from flask import Flask, request
from flask_cors import CORS, cross_origin
from owlready2 import *
import io
import pandas as pd
import base64
import os
from TestConcetti.testConcetti import TestOntology
from TestEntita.testEntita import TestEntities
from Estrazione.extract_info import ScriptEstrazione
from jproperties import Properties



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

configs = Properties()


@app.route("/extractInfo", methods=['GET', 'POST'])
@cross_origin()
def extract_info():
    se = ScriptEstrazione()
    ontology_base64 = request.get_json()['ontology']
    pad = len(ontology_base64) % 4
    while pad != 0:
        ontology_base64 += "="
        pad -= 1
    decrypted_onto = base64.b64decode(ontology_base64)
    
    owl_argument = open("test.owl", "wb")
    owl_argument.write(decrypted_onto)
    onto = get_ontology(owl_argument.name).load()
    owl_filepath = owl_argument.name.split("owl")[0]

    try:
        concepts_base64 = request.get_json()['conceptsList']
        decrypted_concepts = base64.b64decode(concepts_base64)
        text_argument = decrypted_concepts.decode('utf-8')
    except:
        text_argument = ""
        
    lista_nuovi_concetti = se.read_concepts(text_argument)
    dict_concetti = se.from_concept_2_dict(lista_nuovi_concetti, onto, owl_filepath)
    excel_argument = "test.xlsx"
    excel_base64 = se.write_excel(dict_concetti, excel_argument)
    owl_argument.close()
    os.remove(owl_argument.name)
    return excel_base64

@app.route("/testConcetti", methods=['GET', 'POST'])
@cross_origin()
def testConcetti():
    print("INIZIO testConcetti")
    to = TestOntology()
    credentials = {}
    excel_base64 = request.get_json()['base64']
    decrypted = base64.b64decode(excel_base64)
    endpoint = request.get_json()['endpoint']
    toread = io.BytesIO()
    toread.write(decrypted)
    toread.seek(0)
    df = pd.read_excel(toread)
    concepts = df['CONCETTO'].values.tolist()
    sentences = df['FRASE'].values.tolist()
    ontologies = df['ONTOLOGIA'].values.tolist()
    if len(concepts) != len(sentences):
        raise Exception("Il numero di frasi non corrisponde al numero di concetti. Controllare il file Excel.") 

    with open('credentials.properties', 'rb') as config_file:
        configs.load(config_file)
    credentials['username'] = configs.get("username").data
    credentials['password'] = configs.get("password").data
    responses = to.check_responses(concepts, sentences, ontologies, credentials, endpoint)
    df['CONCETTO RILEVATO'] = concepts
    df['RISULTATO'] = responses
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False)
    towrite.seek(0)
    base64_bytes = base64.b64encode(towrite.getvalue())
    print("FINE testConcetti")
    return base64_bytes

@app.route("/testEntita", methods=['GET', 'POST'])
@cross_origin()
def testEntita():
    te = TestEntities()
    credentials = {}
    excel_base64 = request.get_json()['base64']
    decrypted = base64.b64decode(excel_base64)
    endpoint = request.get_json()['endpoint']
    toread = io.BytesIO()
    toread.write(decrypted)
    toread.seek(0)
    df = pd.read_excel(toread)
    entities = df['ENTITA'].values.tolist()
    sentences = df['FRASE'].values.tolist()
    types = df['TIPO'].values.tolist()
    expected_results = df['RISULTATO ATTESO'].values.tolist()
    if len(entities) != len(sentences):
        raise Exception("Il numero di frasi non corrisponde al numero di concetti. Controllare il file Excel.") 
    with open('credentials.properties', 'rb') as config_file:
        configs.load(config_file)
    credentials['username'] = configs.get("username").data
    credentials['password'] = configs.get("password").data
    retrieved_entities, responses = te.check_responses(entities, types, sentences, expected_results, credentials, endpoint)
    for i in range(len(expected_results)):
        if expected_results[i] == 'KO' and responses == 'KO':
            retrieved_entities[i] = ''
    df['ENTITA RILEVATA'] = retrieved_entities
    df['RISULTATO'] = responses 
    towrite = io.BytesIO()     
    df.to_excel(towrite, index=False)
    towrite.seek(0)
    base64_bytes = base64.b64encode(towrite.getvalue())
    return base64_bytes