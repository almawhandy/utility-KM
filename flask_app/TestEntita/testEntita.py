import requests
from collections import defaultdict 
from difflib import SequenceMatcher





class TestEntities:
    
    def __init__(self):
        pass

    def similar(self, normalized_entity, retrieved_entities):
        temp_dict = {}
        for entity in retrieved_entities:
            temp_score = SequenceMatcher(None, normalized_entity, entity).ratio()
            temp_dict[entity] = temp_score
        sorted_dict = {k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1], reverse=True)}
        return sorted_dict.keys()

    def get_json_response(self, documentText, credentials, endpoint):
        try:
            print('INIZIO invocazione servizio AnalyzedDocument')
            session = requests.Session()
            url = endpoint + "/api/analyze/analyzedDocument"
            headers={'Content-type':'application/json', 'Accept':'application/json'}
            params = dict(
                documentText=documentText
            )
            session.auth = (credentials['username'], credentials['password'])
            response = session.post(url=url, headers=headers, json = params)
            print('FINE invocazione servizio AnalyzedDocument')
            return response.json()
        except Exception as ex:
            print("Errore durante l'\invocazione del servizio AnalyzedDocument")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            raise Exception(message)
    
    def check_responses(self, entities, types, sentences, expected_results, credentials, endpoint):
        try:
            print('INIZIO controllo entità')
            check_responses = []
            check_entities = []
            te = TestEntities()
            for i in range(len(sentences)):
                json_resp = te.get_json_response(sentences[i], credentials, endpoint)
                type_to_entity = defaultdict(list)
                for annot in json_resp['annotations']:
                    if annot['name'] == 'Named entity':
                        entity_type = annot['properties']['type'].strip().lower()
                        entity_text = annot['properties']['text'].strip().lower()
                        type_to_entity[entity_type].append(entity_text)
                normalized_type = types[i].lower().strip()
                normalized_entity = entities[i].lower().strip()
                if normalized_type in type_to_entity.keys():
                    if normalized_entity in type_to_entity[normalized_type]:
                        check_entities.append(normalized_entity)
                        check_responses.append('OK')
                    else:
                        sorted_entity_list = te.similar(normalized_entity, type_to_entity[normalized_type])
                        check_entities.append(", ".join(sorted_entity_list))
                        check_responses.append('KO')
                else:
                    check_entities.append('')
                    check_responses.append('KO')
            print('FINE controllo entità')
            return check_entities, check_responses
        except Exception as ex:
            print("Errore durante il controllo delle entità")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            raise Exception(message)
