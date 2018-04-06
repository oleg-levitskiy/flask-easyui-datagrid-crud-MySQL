from flask import Flask, request, render_template
import json
import string
from flaskext.mysql import MySQL 

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'flasktest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'flaskpass'
app.config['MYSQL_DATABASE_DB'] = 'flasktest_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def datagrid():
    return render_template("Items.html")

@app.route("/Items_get", methods=['GET', 'POST'])
def Items_get():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT *  FROM extens")
    data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    resultarray = {}
    resultarray["total"] = str(cursor.rowcount)
    resultarray["rows"] = []
    for record in data:        
        fullresult = zip(column_names, record)
        dict = {}
        for (name, value) in fullresult:
            dict[name] = value
        resultarray["rows"].append(dict)
    return json.dumps(resultarray)
	
@app.route("/Items_save", methods=['GET', 'POST'])
def Items_save():
    connection = mysql.get_db()
    cursor = connection.cursor()
    save_query = "insert into extens(NAME) values('%s')" % request.form['NAME']
    app.logger.info(save_query)
    cursor.execute(save_query)
    connection.commit()
    cursor.close()
    resultarray = {}
    return json.dumps(resultarray)	
	
@app.route("/Items_destroy", methods=['GET', 'POST'])
def Items_destroy():
    id = request.form['id']
    delete_query = "DELETE FROM `extens` WHERE id='%s'" % id
    connection = mysql.get_db()
    cursor = connection.cursor()  
    app.logger.info(delete_query)
    cursor.execute(delete_query)
    connection.commit()
    cursor.close()		
    resultarray = {}
    resultarray["success"] = True
    return json.dumps(resultarray)
	
@app.route("/Items_update", methods=['GET', 'POST'])
def Items_update():
    connection = mysql.get_db()
    cursor = connection.cursor() 
    update_query = "UPDATE `extens` SET NAME = '%s' WHERE id= '%s'" % (request.form['NAME'], request.args['id'])
    app.logger.info(update_query)
    app.logger.info(request.form['NAME'])
    cursor.execute(update_query)
    connection.commit()
    cursor.close()
    resultarray = {}
    return json.dumps(resultarray)
	
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5010,debug=True)
