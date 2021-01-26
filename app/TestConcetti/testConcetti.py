import requests

class TestOntology:
    
    def __init__(self):
        pass
    
    def get_json_response(self, documentText, ontology, credentials, endpoint):
        try:
            ontologies = []
            temp_vector = ontology.split(",")
            if len(temp_vector) == 0:
                ontologies.append(ontology.strip())
            else:
                for vec in temp_vector : 
                    ontologies.append(vec.strip())
            print('INIZIO invocazione servizio AnalyzedDocument')
            session = requests.Session()
            url = endpoint + "/api/analyze/analyzedDocument"
            headers={'Content-type':'application/json', 'Accept':'application/json'}
            params = dict(
                documentText=documentText,
                ontologies=ontologies,
            )
            session.auth = (credentials['username'], credentials['password'])
            response = session.post(url=url, headers=headers, json = params)
            print('FINE invocazione servizio AnalyzedDocument')
            return response.json()
        except:
            raise Exception('Errore durante l\'invocazione del servizio AnalyzedDocument')
    
    def check_responses(self, concepts, sentences, ontologies, credentials, endpoint):
        try:
            print('INIZIO controllo concetti')
            check_responses = []
            to = TestOntology()
            for i in range(len(concepts)):
                json_resp = to.get_json_response(sentences[i], ontologies[i], credentials, endpoint)
                temp_concepts_mapper = []
                for annot in json_resp['annotations']:
                    if annot['name'] == 'Concept Mapper':
                        temp_concepts_mapper.append(annot['properties']['resource uri'].split('#')[1].strip().lower())
                if concepts[i].lower().strip() in temp_concepts_mapper:
                        check_responses.append('OK')
                else:
                    check_responses.append('KO')
            print('FINE controllo concetti')
            return check_responses
        except:
            raise Exception('Errore durante il controllo dei concetti')
