from flask import Flask, request

from flask_restx import Api, Resource, fields
from owlready2 import *
import io
import pandas as pd
import base64
from TestConcetti.testConcetti import TestOntology
from TestEntita.testEntita import TestEntities
from Estrazione.extract_info import ScriptEstrazione


app = Flask(__name__)




@app.route("/extractInfo", methods=['GET', 'POST'])
def extract_info():
    se = ScriptEstrazione()
    ontology_base64 = request.get_json()['ontology']
    print(ontology_base64)
    decrypted_onto = base64.b64decode(ontology_base64)
    #onto_toread = io.BytesIO()
    #onto_toread.write(decrypted_onto)
    #onto_toread.seek(0)
    #onto = get_ontology(onto_toread).load() # da testare
    try:
        concepts_base64 = request.get_json()['conceptsList']
        decrypted_concepts = base64.b64decode(concepts_base64)
        text_argument = decrypted_concepts.decode('utf-8')
    except:
        text_argument = []
    lista_nuovi_concetti = se.read_concepts(text_argument)
    dict_concetti = se.from_concept_2_dict(lista_nuovi_concetti, onto)
    #se.write_excel(dict_concetti, excel_argument))

@app.route("/testConcetti", methods=['GET', 'POST'])
def testConcetti():
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
    credentials['username'] = request.authorization['username']
    credentials['password'] = request.authorization['password']
    responses = to.check_responses(concepts, sentences, ontologies, credentials, endpoint)
    df['CONCETTO RILEVATO'] = concepts
    df['RISULTATO'] = responses
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False)
    towrite.seek(0)
    base64_bytes = base64.b64encode(towrite.getvalue())
    return base64_bytes

@app.route("/testEntita", methods=['GET', 'POST'])
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
    credentials['username'] = request.authorization['username']
    credentials['password'] = request.authorization['password']
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