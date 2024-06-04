#=====================================#
from flask import Flask,jsonify,abort
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
#=====================================#

engine = create_engine('sqlite:///data.db', echo=True)
Base = declarative_base()
class domain(Base):
    __tablename__ = 'domain'
    name = Column(String,primary_key=True)
    tld = Column(String)
    register_date = Column(String)
    ip = Column(String)
    access_key = Column(String)
    author = Column(String)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sessiondb = Session()
app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["90 per minute"],
    storage_uri="memory://",
)
IP_SERVER = "localhost:5000"

TLD = [
    "mf", "btw", "fr", "yap", "dev", "scam", "zip", "root", "web", "rizz", "habibi", "sigma",
    "now", "it", "soy", "lol", "uwu", "ohio","yyy","org","fishe","face","rocket","wtf","syx","fire","what"
]

@app.route("/domain/<name>/<tld>")
@limiter.limit("5/second")
def dns_lookup(name,tld):
    if name == "project" and tld == "openwbx":return jsonify({'tld': tld,'name': name,'ip': f'http://{IP_SERVER}'})  
    elif name == "whois" and tld == "openwbx": return jsonify({'tld': tld,'name': name,'ip': f'http://{IP_SERVER}/whois'}) 
    elif name == "register" and tld == "openwbx": return jsonify({'tld': tld,'name': name,'ip': f'http://{IP_SERVER}/registar'}) 
    else:   
        t = sessiondb.query(domain).filter_by(name=name, tld=tld).first()
        if t is not None:
            return jsonify({
                    'tld': t.tld,
                    'name': t.name,
                    'ip': t.ip
                })
        else:
            try: 
                res = requests.get(f"https://api.buss.lol/domain/{name}/{tld}")
                if res.status_code == 200:
                    print("ok")
                    return jsonify(res.text)
                else:
                    return jsonify({'tld': tld,'name': name,'ip': f'http://{IP_SERVER}/dns/error/404'})
            except:
                return jsonify({'tld': tld,'name': name,'ip': f'http://{IP_SERVER}/dns/error/404'})
            #return jsonify({'tld': tld,'name': name,'ip': f'http://{IP_SERVER}/dns/error/404'})
            
@app.route("/whois")
def dns_whois():
    name = "in"
    tld = "dev"
    return f"""<html>
<head>
    <title>WHOIS</title>
</head>
<body>
    <h1>OpenWebX WHOIS Result for {name}.{tld}</h1>
    <p>Soon 👀</p>
</body>

</html>
"""
@app.route("/")
def home():
    return f'''
<html>
<head>
    <title>OpenWebX-Project</title>
</head>
<body>
    <h1>OpenWebX</h1>
    <p>OpenWebX is a alternative DNS for WebX !</p>
    <p>how to add ? for Bussinga go to settings and type this : http://{IP_SERVER} and press enter and re-launch the browser !</p>
    <p>for WebX Napture you need to modify code and recompile !</p>
    <h1>Cool things :</h1>
    <p>- before checking if the domain exists with us our DNS will contact the official webx API!</p>
    <p>- More TLD !</p>
    <h3>Links :</h3>
    <p>Register a domain : register.openwbx</p>
    <p>Discord : cooming soon 👀</p>
    <p>Github (on the real internet 😓) : https://github.com/EletrixtimeYT/OpenWebX</p>
</body>

</html>
 '''
@app.errorhandler(429) 
def too_many_request(e): 
    return "<html><head><title>OpenWebX - Too many request !</title></head><body><p>Too many request to DNS server ! slow down ! (Try in the next minute ?)</p></body></html>"
@app.route("/dns/error/404")
def error_not_found_dns():
    return """<html><head><title>Not-Found</title></head><body><p>Domain Name not found !</p><p>Powered by OpenWebX</p></body></html>"""
@app.route("/register")
def register():
    return "Soon"
if __name__ == "__main__":
    #t = domain(name="cat",tld="now",ip="http://192.168.4.3:1944",access_key="test",author="eletrix",register_date="03/06/2024")
    #sessiondb.add(t);sessiondb.commit()
    app.run(debug=True)
    
