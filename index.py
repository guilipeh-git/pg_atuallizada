from flask import Flask,render_template,request,redirect,url_for,flash,abort,session,jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'gfpa'

@app.route('/',methods=["POST","GET"])
def index():
    if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
                return render_template('index.html',t = urls)
                
    return render_template('index.html',t = session.keys())
res = " "
@app.route('/tt',methods=["POST","GET"])
def index1():     
    res = False
    if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
                return render_template('index.html',t = urls)
    return render_template('index.html')
    
    


@app.route('/pg2',methods=["POST","GET"])
def pg2():
    res = True
    if request.method == "POST":
        urls = dict()

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        #===========================================================
        
        if request.form['texto'] in urls.keys(): 
                     
            resp = request.form['texto']
            resp2 = urls.keys()
            
          #return render_template('index.html',t = urls.keys(),rp1 = resp,rp2 = resp2)

        #=======================================================  
       
        if 'url' in request.form.keys():
            urls[request.form['texto']] = {'url':request.form['url']}
            with open('urls.json','w') as urls_file:
                json.dump(urls,urls_file)
                session[request.form['texto']] = True
            flash('URL exportada com Sucesso')
            return redirect(url_for('index'))
        if res == True:
            session[request.form['texto']] = True
            flash('URL exportada com Sucesso')
            f = request.files['file']
            full_name = request.form['texto'] + ".png"
            f.save("/home/pi/Desktop/url-shortener/static/imgs_file/"+ full_name)           
            urls[request.form['texto']] = {'file':full_name}
            

            with open('urls.json','w') as urls_file:
                json.dump(urls,urls_file)
        
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/<string:texto>')
def minha_url(texto):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            
            if texto in urls.keys():
                if 'url' in urls[texto]:
                    return redirect(urls[texto]['url'])
                else:
                    return redirect(url_for('static', filename = 'imgs_file/' + urls[texto]['file']))
    return abort(404)


@app.errorhandler(404)
def pg_not_found(error):
    return render_template('pg_not_found.html'),404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))



apis = list()
@app.route('/r_api')
def r_api():
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            
            for k,v in urls.items():
                api = f'{k} = {v}'
                if api not in apis:
                    apis.append(api)
      
        return render_template('pg2.html',titulo='Lista de API Encontrada', url=apis)
    return render_template('pg2.html',titulo='Nenhuma API Encontrada')


app.run(port=8080,debug=True)