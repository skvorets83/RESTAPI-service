import ast
from dataclasses import dataclass
from typing import Optional,  List
import sqlite3
import os

@dataclass
class Data_from_file:
    name_file :str
    type_element:str
    name_element:str
    parrent_class : Optional[str]
    str_begin :int
    str_end :int 
    docstring : str

def analyze_file(file: str):
    with open(file,'r',encoding='utf-8') as fi:
        content = fi.read()
        tree = ast.parse(content)
        elements=[]

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                element = Data_from_file(
                    name_file= os.path.basename(file),
                    type_element= "function",
                    name_element= node.name,
                    parrent_class= None,
                    str_begin= node.lineno,
                    str_end= node.end_lineno or node.lineno,
                    docstring= ast.get_docstring(node) or ""
                )
                elements.append(element)
            elif isinstance(node, ast.ClassDef):
                element =Data_from_file(
                    name_file= os.path.basename(file),
                    type_element="class",
                    name_element=node.name,
                    parrent_class=None,
                    str_begin= node.lineno,
                    str_end= node.end_lineno or node.lineno,
                    docstring= ast.get_docstring(node)or ""
                )
                elements.append(element)
                for inside_node in node.body:
                    if isinstance(inside_node,ast.FunctionDef):
                        element = Data_from_file(
                            name_file= os.path.basename(file),
                            type_element= "method",
                            name_element= inside_node.name,
                            parrent_class= node.name,
                            str_begin= inside_node.lineno,
                            str_end= inside_node.end_lineno or inside_node.lineno,
                            docstring=ast.get_docstring(inside_node) or ""
                        )
                        elements.append(element)
    return elements



def analyze_30_files(files : List[str]):
    all_elements =[]
    for file in files:
        print(f" Analyzing {file} file")
        elements =analyze_file(file)
        all_elements.extend(elements)
    
    return all_elements

def save_to_database_many_files(all_elements, db_path= 'database.db'):
    connection =sqlite3.connect(db_path) 
    cursor= connection.cursor()
    #cursor.execute("DELETE FROM pyfiles")
    cursor.execute("CREATE TABLE IF NOT EXISTS pyfiles (name_file TEXT,type_element TEXT,name_element TEXT, parrent_class TEXT,str_begin INT,str_end INT, docstring TEXT);")
    
    for element in all_elements:
        cursor.execute("INSERT INTO pyfiles(name_file ,type_element ,name_element,parrent_class ,str_begin ,str_end , docstring ) VALUES(?, ?, ?, ?, ?, ?, ?)", (
            element.name_file,
            element.type_element,
            element.name_element,
            element.parrent_class,
            element.str_begin,
            element.str_end,
            element.docstring
        ))
    connection.commit()
    print(f"{len(all_elements)} saved in database")

def reading_pyfiles(directory="pythonfiles",db_path = 'database.db'):
    py_files= []
    for file in os.listdir(directory):
        if file.endswith(".py"):
            path= os.path.join(directory,file)
            py_files.append(path)
    print(f" элементов найдено {len(py_files)}")
    all_elements= analyze_30_files(py_files)    
    save_to_database_many_files(all_elements,db_path)


reading_pyfiles("pythonfiles","database.db")