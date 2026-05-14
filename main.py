from fastapi import FastAPI
import sqlite3
app= FastAPI()

def get_connection_database():
    connection = sqlite3.connect("database.db")
    
    return connection

    

@app.get("/api/files")
def list_files():
    result=[]
    connection = get_connection_database()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT name_file FROM pyfiles")
    files=cursor.fetchall()
    for name_file in files:
        cursor.execute("SELECT COUNT(*) FROM pyfiles WHERE  name_file = ? AND type_element= 'function'",(name_file[0],))
        total_functions_in_file=  cursor.fetchone()[0]
        result.append({
            "file name:" :name_file[0],
            "quantity functions in this file:" : total_functions_in_file
        })


    connection.close()
    return result





@app.get("/api/stats")

def get_info():
   connection = get_connection_database()
   cursor = connection.cursor()

   cursor.execute('SELECT COUNT(DISTINCT name_file) FROM pyfiles')
   total_files = cursor.fetchone()[0]

   cursor.execute('SELECT COUNT(*) FROM pyfiles WHERE type_element= "function"')
   total_functions = cursor.fetchone()[0]

   cursor.execute("SELECT COUNT(*) FROM pyfiles WHERE type_element = 'class'")
   total_classes = cursor.fetchone()[0]
   return {
       "total files " : total_files,
       "total functions " : total_functions,
       "total classes " :  total_classes
   } 

@app.get("/api/files/{name}/structure")

def get_structure(name :str):
    connection =get_connection_database()
    cursor =connection.cursor()

    functions =[]  
    cursor.execute("SELECT name_file,name_element, str_begin, str_end, docstring FROM pyfiles WHERE name_file = ? AND type_element='function'",(name,))
    functions = cursor.fetchall()
    result_functions=[]
    for function in functions:
        result_functions.append({
            "name file " : function[0],
            "name element " : function[1],
            "start line " : function[2],
            "end line " : function[3],
            "docstring" :function[4]
        })
    cursor.execute("SELECT name_file, name_element,str_begin,str_end, docstring FROM pyfiles WHERE name_file =? AND type_element = 'class'",(name,))
    classes= cursor.fetchall()
    result_classes =[]
    for clas in classes:
        result_classes.append({
            "name file " : clas[0],
            "name element " : clas[1],
            "start line " : clas[2],
            "end line " : clas[3],
            "docstring " : clas[4] 
        })
    
    methods =[]
    cursor.execute("SELECT name_file, parrent_class,str_begin,str_end,docstring FROM pyfiles WHERE name_file = ? AND type_element = 'method'",(name,))
    methods =cursor.fetchall()
    result_methods = []
    for method in methods:
        result_methods.append({
            "name file " : method[0],
            "parrent class " : method[1],
            "start line " : method[2],
            "end line " : method[3],
            "docstring " : method[4]
        })
    return {
        "name file " : name,
        "functions " : result_functions,
        "classes " : result_classes,
        "methods " :result_methods
    }


@app.get("/api/search")

def search_functions_and_classes(keyword:str):
    connection = get_connection_database()
    cursor=connection.cursor()
    search_word = keyword.lower()
    cursor.execute("SELECT  DISTINCT name_file,type_element,name_element,docstring FROM pyfiles WHERE LOWER(name_element) LIKE ? OR LOWER(docstring) LIKE ?",(f"%{search_word}%", f"%{search_word}%"))
    items=cursor.fetchall()
    all_results=[]
    for item in items:
        all_results.append({
            "file name " : item[0],
            "type element " : item[1],
            "name element " : item[2],
            "docstring " : item[3]
        })
    return all_results
    

