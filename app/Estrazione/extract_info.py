from owlready2 import *
import xlsxwriter 
import re
import sys
import os
import base64


class ScriptEstrazione:
    
    def __init__(self):
        pass
    
    def update_dict(self, dict_concetti, concepts_list, onto, owl_filepath):
        if len(concepts_list) != 0:
            for elem in list(onto.classes()):
                temp_labels = ""
                concept_name = str(elem).split(owl_filepath)[1]
                if concept_name in concepts_list:
                    if len(elem.label) != 0:
                        for label in elem.label[:-1]:
                            temp_labels += str(label) + ", "
                        temp_labels += str(elem.label[-1])
                    query = str(onto[elem.name].equivalent_to).replace("&", "AND").replace("|", "OR").replace(owl_filepath, "")[1:-1]
                    dict_concetti[concept_name] = (temp_labels, query)
        else:
            for elem in list(onto.classes()):
                temp_labels = ""
                concept_name = str(elem).split(owl_filepath)[1]
                if len(elem.label) != 0:
                    for label in elem.label[:-1]:
                        temp_labels += str(label) + ", "
                    temp_labels += str(elem.label[-1])
                query = str(onto[elem.name].equivalent_to).replace("&", "AND").replace("|", "OR").replace(owl_filepath, "")[1:-1]
                dict_concetti[concept_name] = (temp_labels, query)
        return dict_concetti

    def read_concepts(self, text_argument):
        try:
            print("Inizio lettura concetti")
            lista_nuovi_concetti = []
            for elem in text_argument.split(","):
                lista_nuovi_concetti.append(elem.strip())
            print("Fine lettura concetti")
            return lista_nuovi_concetti
        except:
            print("Errore durante la lettura dei concetti")
    
    
    def from_concept_2_dict(self, lista_nuovi_concetti, onto, owl_filepath):
        try:
            print("Inizio estrazione labels e query")
            se = ScriptEstrazione()
            dict_concetti = {}
            dict_concetti = se.update_dict(dict_concetti, lista_nuovi_concetti, onto, owl_filepath)
            if len(lista_nuovi_concetti) != 0:
                nested_concepts = []
                word_regex = re.compile(("(\\w+)"), re.IGNORECASE)
                for tuple in dict_concetti.values():
                    temp_concepts = set(re.findall(word_regex, tuple[1]))
                    for nested_concept in temp_concepts:
                        if nested_concept not in ["Not", "OR", "AND"]:
                            nested_concepts.append(nested_concept)
                nested_concepts = list(set(nested_concepts))
                dict_concetti = se.update_dict(dict_concetti, nested_concepts, onto, owl_filepath)
            print("Fine estrazione labels e query")
            return dict_concetti
        except:
            print("Errore durante l'estrazione di labels e query")
    
    def write_excel(self, dict_concetti, excel_filepath):
        try:
            print("Inizio scrittura file Excel")
            workbook = xlsxwriter.Workbook(excel_filepath)
            worksheet = workbook.add_worksheet()
            headers_format = workbook.add_format({'bold': True})
            headers_format.set_pattern(1)
            headers_format.set_bg_color('yellow')
            headers_format.set_border()
            row = 1
            col = 0
            worksheet.write('A1', 'CONCETTO', headers_format)
            worksheet.write('B1', 'LISTA DI LABEL', headers_format)
            worksheet.write('C1', 'QUERY', headers_format)
            cell_format = workbook.add_format()
            cell_format.set_bg_color('white')
            cell_format.set_border()
            for elem in dict_concetti.keys():
                temp_concept_name = elem
                temp_labels = dict_concetti[elem][0]
                temp_query = dict_concetti[elem][1]
                worksheet.write(row, col, temp_concept_name, cell_format)
                worksheet.write(row, col + 1, str(temp_labels), cell_format)
                worksheet.write(row, col + 2, str(temp_query), cell_format)
                row += 1
            workbook.close()
            excel_file = open(excel_filepath, 'rb')
            excel_base64 = base64.b64encode(excel_file.read())
            excel_file.close()
            os.remove(excel_filepath)
            print("Fine scrittura file Excel")
            return excel_base64
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            raise Exception(message)
