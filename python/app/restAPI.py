##
# =============================================
# ============== Bases de Dados ===============
# ============== LEI  2020/2021 ===============
# =============================================
# === Department of Informatics Engineering ===
# =========== University of Coimbra ===========
# =============================================
#
# =============================================
# Autores:
#   Diogo Sebastião Cleto (2019198370)
#       uc2019198370@student.uc.pt
#   João Miguel Ferreira Castelo Branco Catré (2019218953)
#       uc2019218953@student.uc.pt
#   José Pedro  Silva Aguiar (2019224624)
#       joseaguiar@student.dei.uc.pt
# =============================================

from flask import Flask, jsonify, request
import logging
import time
import psycopg2
import decrypted
import pytz
import jwt
from functools import wraps
from datetime import datetime, timedelta
import os
import hashlib as hs
from dotenv import load_dotenv
load_dotenv("/Users/josepedroaguiar/.env")

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get("SECRET_KEY"))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']
            logger.debug(f'payload: {token}')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms="HS256")
            username = data["public_id"]
            current_user = username
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def hashing(password):
    salt = os.urandom(32)
    key 
    dk = hs.pbkdf2_hmac('sha256', password.encode('utf-8'), b'salt', 100000)

@app.route('/')
def hello():
    return "BEM VINDO"
    """"

    Hello World!  <br/>
    <br/>
    Check the sources for instructions on how to use the endpoints!<br/>
    <br/>
    BD 2021 Team<br/>
    <br/>
    """


##
# Demo GET
##
# Obtain all departments, in JSON format
##
# To use it, access:
##
# http://localhost:8080/departments/
##
"""@app.route("/departments/", methods=['GET'], strict_slashes=True)
def get_all_departments():
    logger.info("###              DEMO: GET /departments              ###");   

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("SELECT ndep, nome, local FROM dep")
    rows = cur.fetchall()

    payload = []
    logger.debug("---- departments  ----")
    for row in rows:
        logger.debug(row)
        content = {'ndep': int(row[0]), 'nome': row[1], 'localidade': row[2]}
        payload.append(content) # appending to the payload to be returned

    conn.close()
    return jsonify(payload)



##
##      Demo GET
##
## Obtain department with ndep <ndep>
##
## To use it, access: 
## 
## http://localhost:8080/
##

@app.route("/departments/<ndep>", methods=['GET'])
def get_department(ndep):
    logger.info("###              DEMO: GET /departments/<ndep>              ###");   

    logger.debug(f'ndep: {ndep}')

    conn = db_connection()
    cur = conn.cursor()

    #cur.execute("SELECT ndep, nome, local FROM dep where ndep = %s", (ndep,) )
    rows = cur.fetchall()

    row = rows[0]

    logger.debug("---- selected department  ----")
    logger.debug(row)
    #content = {'ndep': int(row[0]), 'nome': row[1], 'localidade': row[2]}

    conn.close ()
    return jsonify(content)"""


##
# Demo POST
##
# Add a new department in a JSON payload
##
# To use it, you need to use postman or curl:
##
# curl -X POST http://localhost:8080/ -H "Content-Type: application/json" -d '{"localidade": "Polo II", "ndep": 69, "nome": "Seguranca"}'
##

@app.route("/dbproj/user", methods=['POST'])
def add_user():
    logger.info("###              DEMO: POST /departments              ###")
    payload = request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.info("---- new user  ----")
    logger.debug(f'payload: {payload}')

    # parameterized queries, good for security and performance
    statement = """
                  INSERT INTO data_user (username, password, email) 
                          VALUES ( %s,   %s,   %s)"""

    values = (payload["username"], payload["password"], payload["email"])

    try:
        cur.execute(statement, values)
        cur.execute("commit")
        result = 'Inserted!'
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = 'Failed!'
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)

# ----------------------------ADD ADMIN----------------------------------


@app.route("/dbproj/admin", methods=['POST'])
def add_admin():
    logger.info("###              DEMO: POST /admin             ###")
    payload = request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.info("---- new admin  ----")
    logger.debug(f'payload: {payload}')

    # parameterized queries, good for security and performance
    statement = """
                  INSERT INTO data_admin (password, username) 
                          VALUES ( %s,   %s)"""

    values = (payload["password"], payload["username"])

    try:
        cur.execute(statement, values)
        cur.execute("commit")
        result = 'admin Inserted!'
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = 'admin Failed!'
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)



##-----------------------GET ALL USERS-----------------------------------------------
@app.route("/user/", methods=['GET'])
def get_all_users():
    logger.info("###              DEMO: GET /USERS            ###")

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * from data_user")
    rows = cur.fetchall()

    payload = []
    logger.debug("---- USERS ----")
    for row in rows:
        logger.debug(row)
        content = {'nome': int(row[0]), 'password': row[1], 'email': row[2]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)

##----------------------------------------------------------------------------------

# -----------------------GET ALL LEILOES EXISTENTES---------------------------------

@app.route("/dbproj/leiloes", methods=['GET'])
def get_all_leiloes():
    logger.info("###              DEMO: GET /Leilões              ###")

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_leilao,descricao from leiloes where terminado=false and cancelado=false")
    rows = cur.fetchall()

    payload = []
    logger.debug("---- leilões ----")
    for row in rows:
        logger.debug(row)
        content = {'id_leilão': int(row[0]), 'descrição': row[1]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)
# -----------------------------------------------------------------------------

# -------------------PESQUISAR LEILOES EXISTENTES------------------------------


@app.route("/dbproj/leiloes/<keyword>", methods=['GET'])
def search_all_leiloes(keyword):
    logger.info("###              DEMO: GET /Leilões/<keyword>              ###")

    conn = db_connection()
    cur = conn.cursor()
    #cur.execute("SELECT ndep, nome, local FROM dep where ndep = %s", (ndep,))
    cur.execute(
        "SELECT id_leilao,descricao from leiloes where produtos_ean=%s and terminado=false and cancelado=false  or descricao=%s and terminado=false and cancelado=false", (keyword, keyword))
    rows = cur.fetchall()

    payload = []
    logger.debug("---- leilões ----")
    for row in rows:
        logger.debug(row)
        content = {'id_leilão': int(row[0]), 'descrição': row[1]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)
# ----------------------------------------------------------------------------

# --------------------CONSULTAR DETALHES DE UM LEILAO-------------------------


@app.route("/dbproj/leilao/<id>", methods=['GET'])
@token_required
def consult_leilao(current_user, id):
    logger.info("###              DEMO: GET /Leilões/<id>              ###")

    conn = db_connection()
    cur = conn.cursor()
    #cur.execute("SELECT ndep, nome, local FROM dep where ndep = %s", (ndep,))
    cur.execute(
        "SELECT id_leilao,descricao from leiloes where id_leilao=%s and terminado=false and cancelado=false", (id,))
    rows = cur.fetchall()
    cur.execute("SELECT texto,data_user_username from mensagem_mural where leiloes_id_leilao=%s",(id,))
    rows_mural = cur.fetchall()
    cur.execute("SELECT valor,data_user_username from licitacoes where leiloes_id_leilao=%s",(id,))
    rows_licitacao = cur.fetchall()
    payload = []
    logger.debug("---- leilões ----")
    for row in rows:
        content = {'id_leilão': int(row[0]), 'descrição': row[1]}
        payload.append(content)
        logger.debug(row)

        for a in rows_mural:
            content={'mensagens_mural : escritor':a[1],'mensagem':a[0]}
            payload.append(content)
            for b in rows_licitacao:
                content = {'licitações : licitador':b[1],'licitação':b[0]}
                payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)
# -------------------------------------------------------------------------------

# -------------Listar todos os leilões em que o utilizador tenha atividade--------------------------------


@app.route("/dbproj/leilao/atividade", methods=['GET'])
@token_required
def get_leilao_user(current_user):
    logger.info("###              DEMO: GET /Leilões/<user>              ###")

    conn = db_connection()
    cur = conn.cursor()
    #cur.execute("SELECT ndep, nome, local FROM dep where ndep = %s", (ndep,))
    cur.execute("SELECT id_leilao,titulo,descricao,data_user_username,preco_corrente from leiloes where leiloes.data_user_username=%s UNION SELECT id_leilao,titulo,descricao,leiloes.data_user_username,preco_corrente from leiloes,licitacoes where leiloes_id_leilao=id_leilao and licitacoes.data_user_username=%s", (current_user, current_user))
    rows = cur.fetchall()

    payload = []
    logger.debug("---- leilões ----")
    if len(rows)==0:
        conn.close()
        return jsonify("User sem atividades")
    for row in rows:
        logger.debug(row)
        content = {'id_leilão': int(row[0]), 'titulo': row[1], 'descrição': row[2], 'Leiloeiro': row[3],'Valor do produto': row[4]}
        payload.append(content)  # appending to the payload to be returned

    conn.close()
    return jsonify(payload)
# --------------------------------------------------------------------------------

# --------------------------ADD PRODUCTS------------------------------------------


@app.route("/dbproj/produtos", methods=['POST'])
@token_required
def add_product(current_user):
    logger.info("###              DEMO: POST /departments              ###")
    payload = request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.info("---- new user ----")
    logger.debug(f'payload: {payload}')

    # parameterized queries, good for security and performance
    statement = '''
                  INSERT INTO produtos (ean, nome__do_produto,quantidade) 
                          VALUES (%s,   %s,   %s)'''

    values = (payload["ean"], payload["nome_do_produto"],
              payload["quantidade"])

    try:
        cur.execute(statement, values)
        cur.execute("commit")
        result = {"mensagem":'Inserted!'}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = {'erro': 'Failed!'}
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)
 ##
 #
 #
 ##-------------------------------------------------------------------------

# ----------------------ADD LEILÕES-----------------------------------------


@app.route("/dbproj/leilao", methods=['POST'])
@token_required
def add_leiloes(current_user):
    logger.info("###              DEMO: POST /leilão              ###")
    payload = request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.info("---- add leilão ----")
    logger.debug(f'payload: {payload}')

    # parameterized queries, good for security and performance
    cur.execute("SELECT banido from data_user where username=%s",
                (current_user,))
    rows_user = cur.fetchall()
    if rows_user[0][0] == False:
        statement = '''
                    INSERT INTO leiloes(titulo,descricao,detalhes,data_inicial,data_final_,preco_inicial,preco_corrente,user_vencedor,data_user_username,produtos_ean) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'''

        values = (payload["titulo"], payload["descricao"], payload["detalhes"], payload["data_inicial"], payload["data_final"], payload["preco_inicial"],
                  payload["preco_corrente"], current_user,current_user, payload["produtos_ean"],)
        # utc = pytz.utc
        lx_tz = pytz.timezone('Europe/Lisbon')
        time_string = (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))
        date_time = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
        date_time_input_i = datetime.strptime(
            payload["data_inicial"], "%Y-%m-%d %H:%M:%S")
        date_time_input_f = datetime.strptime(
            payload["data_final"], "%Y-%m-%d %H:%M:%S")
        if(date_time > date_time_input_i):
            result = 'Failed:data inicial invalida!'
            if conn is not None:
                conn.close()
            return jsonify(result)
        if(date_time_input_i > date_time_input_f):
            result = 'Failed:data inicial e final incompatíveis!'
            if conn is not None:
                conn.close()
            return jsonify(result)
        cur.execute("SELECT quantidade from produtos where ean=%s",
                    (payload["produtos_ean"],))
        quantidade = cur.fetchall()
        if(cur.rowcount==0):
            conn.close()
            return jsonify({'erro':'Failed: produto nao existente!'})
        if quantidade[0][0] <= 0:
            result = 'Failed: quantidade de produto insuficiente!'
            if conn is not None:
                conn.close()
            return jsonify(result)
        statement1 = """
                    UPDATE produtos
                    SET quantidade=%s
                    WHERE ean = %s"""

        values1 = (quantidade[0][0]-1, payload["produtos_ean"])
        try:
            cur.execute(statement, values)
            cur.execute(statement1, values1)
            cur.execute("commit")
            result = 'Inserted!'
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
            result = {'erro': 'Failed!'}
        finally:
            if conn is not None:
                conn.close()

        return jsonify(result)
    else:
        conn.close()
        return jsonify({'erro': 'User Banido!!'})
# -------------------------------------------------------------------------

# ---------------------------Update Leilões--------------------------------


@app.route("/dbproj/leilao/update/<id>", methods=['PUT'])
@token_required
def update_leiloes(current_user, id):
    logger.info("###              DEMO: PUT /Update Leilões             ###")
    content = request.get_json()

    conn = db_connection()
    cur = conn.cursor()
    # utc = pytz.utc
    lx_tz = pytz.timezone('Europe/Lisbon')
    data = (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))

    # if content["ndep"] is None or content["nome"] is None :
    #    return 'ndep and nome are required to update'

    # if "ndep" not in content or "localidade" not in content:
    # return 'ndep and localidade are required to update'

    logger.info("---- update leilão  ----")
    logger.info(f'content: {content}')
    cur = conn.cursor()
    #cur.execute("SELECT ndep, nome, local FROM dep where ndep = %s", (ndep,))
    cur.execute("SELECT titulo,descricao,detalhes from leiloes where leiloes.id_leilao=%s and data_user_username=%s and terminado=false and cancelado=false ", (id,current_user))
    row= cur.fetchall()
    if(cur.rowcount==0):
        conn.close()
        return jsonify("Leilao nao pode ser atualizado")
    # parameterized queries, good for security and performance
    statement = """
                UPDATE leiloes
                SET  titulo=%s,descricao=%s,detalhes=%s
                WHERE id_leilao = %s"""

    values = (content["titulo"], content["descricao"],
              content["detalhes"], id)

    
    try:
        cur.execute(statement,values)
        result = f'Updated: {cur.rowcount}'  # {'Updated': content}
        cur.execute("commit")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = 'Failed!'
    finally:
        if conn is not None:
            conn.close()
            return jsonify(result)
    
# -----------------------------------------------------------------------------

# -----------------------UPDATE PREÇO CORRENTE---------------------------------


def update_price(vencedor,licitacao, LeilaoID):
    logger.info("###              DEMO: PUT /Leilões             ###")
    content = request.get_json()

    conn = db_connection()
    cur = conn.cursor()
    # if content["ndep"] is None or content["nome"] is None :
    #    return 'ndep and nome are required to update'

    # if "ndep" not in content or "localidade" not in content:
    # return 'ndep and localidade are required to update'

    logger.info("---- update price leilão  ----")
    logger.info(f'content: {content}')

    # parameterized queries, good for security and performance
    statement = """
                UPDATE leiloes
                SET preco_corrente=%s,user_vencedor=%s
                WHERE id_leilao = %s"""

    values = (licitacao, vencedor, LeilaoID)
    try:
        res = cur.execute(statement, values)
        result = f'Updated: {cur.rowcount}'
        cur.execute("commit")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = 'Failed!'
    finally:
        if conn is not None:
            conn.close()
    return jsonify(result)
# -----------------------------------------------------------------------------

# -----------------------UPDATE PREÇO CORRENTE 2---------------------------------


def update_price2(licitacao, LeilaoID):
    logger.info("###              DEMO: PUT /Leilões             ###")
    content = request.get_json()

    conn = db_connection()
    cur = conn.cursor()
    # if content["ndep"] is None or content["nome"] is None :
    #    return 'ndep and nome are required to update'

    # if "ndep" not in content or "localidade" not in content:
    # return 'ndep and localidade are required to update'

    logger.info("---- update price leilão  ----")
    logger.info(f'content: {content}')

    # parameterized queries, good for security and performance
    statement = """
                UPDATE leiloes
                SET preco_corrente=%s
                WHERE id_leilao = %s"""

    values = (licitacao, LeilaoID)
    try:
        res = cur.execute(statement, values)
        result = f'Updated: {cur.rowcount}'
        cur.execute("commit")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = 'Failed!'
    finally:
        if conn is not None:
            conn.close()
    return jsonify(result)
# -----------------------------------------------------------------------------

# -----------------------POST LICITAÇÕES---------------------------------------


def post_licitacao(user_licitador, licitacao, data, leilaoID):
    logger.info("###              DEMO: POST /licitação              ###")
    payload = request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.info("---- new licitação ----")
    logger.debug(f'payload: {payload}')
    logger.debug("boas")
    # parameterized queries, good for security and performance
    statement = '''
                  INSERT INTO licitacoes (valor, data,leiloes_id_leilao,data_user_username) 
                          VALUES (%s,   %s,   %s,  %s)'''

    values = (licitacao, data, leilaoID, user_licitador)

    try:
        cur.execute(statement, values)
        cur.execute("commit")
        result = {'Inserted': payload}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = {'erro': 'Failed!'}
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)

# -----------------------------------------------------------------------------

# -----------------------Write Private Mensage---------------------------------


def write_private_message(text, date, leilaoID, write_user, user):
    logger.info("###              DEMO: POST /departments              ###")
    payload = request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    logger.info("---- new mensagem_privada ----")
    logger.debug(f'payload: {payload}')

    # parameterized queries, good for security and performance
    statement = '''
                  INSERT INTO mensagem_privada (texto,data,leiloes_id_leilao,data_user_username,data_user_username1) 
                          VALUES (%s, %s,%s, %s, %s)'''
    values = (text, date, leilaoID, write_user, user)

    try:
        cur.execute(statement, values)
        cur.execute("commit")
        result = {'erro': 'Failed!'}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = {'erro': 'Failed!'}
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)
# -----------------------------------------------------------------------------

# -----------------------------Write licitacao Mural-------------------------------------


def write_licitacao_mural(texto,data,current_user, id):
    logger.info("###              DEMO: POST /MURAL             ###")
    payload = request.get_json()
    conn = db_connection()
    cur = conn.cursor()
    logger.info("---- new user ----")
    logger.debug(f'payload: {payload}')
    # utc = pytz.utc
    lx_tz = pytz.timezone('Europe/Lisbon')
    time_string = (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))
    print(time_string)
    # parameterized queries, good for security and performance
    statement = '''
                  INSERT INTO mensagem_mural(texto,data,data_user_username,leiloes_id_leilao)
                          VALUES (%s, %s, %s, %s)'''

    values = (texto, data, current_user, id)

    cur.execute("SELECT distinct mensagem_mural.data_user_username from mensagem_mural where mensagem_mural.leiloes_id_leilao = %s UNION SELECT leiloes.data_user_username from leiloes where id_leilao = %s", (id, id))
    rows = cur.fetchall()

    ##payload = []
    ##logger.debug("---- departments ----")
    for row in rows:
        logger.debug(row)
        write_private_message(texto, data, id, current_user, row[0])
        # int(row[0]), 'password': row[1], 'email': row[2]}

    try:
        cur.execute(statement, values)
        cur.execute("commit")
        result = {'mensagem': 'Inserted'}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = {'erro': 'Failed!'}
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)
# --------------------------------------------------------------------------

# -----------------------GET LICITAÇÕES----------------------------------------


@app.route("/dbproj/leilao/licitar/<LeilaoID>/<licitacao>", methods=['GET'])
@token_required
def get_licitacao(current_user, LeilaoID, licitacao):
    logger.info("###              DEMO: GET /Leilões/<user>              ###")

    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT banido from data_user where username=%s",
                (current_user,))
    rows_user = cur.fetchall()
    logger.info(f'payload: {rows_user}')
    lx_tz = pytz.timezone('Europe/Lisbon')
    data= (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))
    #cur.execute("SELECT ndep, nome, local FROM dep where ndep = %s", (ndep,))
    cur.execute("SELECT preco_corrente,user_vencedor,terminado,cancelado,data_user_username from leiloes where leiloes.id_leilao=%s and terminado=false and data_inicial<%s and cancelado=false", (LeilaoID,data))
    rows = cur.fetchall()
    cur.execute("SELECT banido from data_user where username=%s",
                (current_user,))
    rows_user = cur.fetchall()
    # utc = pytz.utc
    lx_tz = pytz.timezone('Europe/Lisbon')
    data = (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))
    if rows_user[0][0] == False:
        if(len(rows) == 0):
            return jsonify({"erro": 'Impossivel licitar nesse Leilao!!'})
        if(rows[0][4] == current_user):
            return jsonify({"erro": 'Leiloeiro não pode licitar'})
        if rows[0][2] != True and rows[0][3] != True: # por data
            if int(rows[0][0]) < int(licitacao):
                post_licitacao(current_user,licitacao, data, LeilaoID) 
                write_licitacao_mural("Nova licitação efetuada",data,current_user,LeilaoID)
                update_price(current_user, licitacao, LeilaoID)
                #write_private_message("A sua licitação foi ultrapassada", data, LeilaoID, current_user, rows[0][1])  # por data
                conn.close()
                return jsonify({"Mensagem": 'Licitação aceite!!'})
            else:
                conn.close()
                return jsonify({"erro": 'Licitação baixa!!'})

        else:
            conn.close()
            return jsonify({"erro": 'Licitação inválida!!'})
    else:
        conn.close()
        return jsonify({"erro": 'User Banido!!'})

    # return jsonify(payload)

# -----------------------------------------------------------------------------

# -----------------------------Write Mural-------------------------------------


@app.route("/dbproj/leilao/mural/<id>", methods=['POST'])
@token_required
def write_mural(current_user, id):
    logger.info("###              DEMO: POST /MURAL             ###")
    payload = request.get_json()
    conn = db_connection()
    cur = conn.cursor()
    logger.info("---- new user ----")
    logger.debug(f'payload: {payload}')
    # utc = pytz.utc
    lx_tz = pytz.timezone('Europe/Lisbon')
    time_string = (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))
    print(time_string)
    # parameterized queries, good for security and performance
    statement = '''
                  INSERT INTO mensagem_mural(texto,data,data_user_username,leiloes_id_leilao)
                          VALUES (%s, %s, %s, %s)'''

    values = (payload["texto"], time_string, current_user, id)

    cur.execute("SELECT distinct mensagem_mural.data_user_username from mensagem_mural where mensagem_mural.leiloes_id_leilao = %s UNION SELECT leiloes.data_user_username from leiloes where id_leilao = %s", (id, id))
    rows = cur.fetchall()

    ##payload = []
    ##logger.debug("---- departments ----")
    for row in rows:
        logger.debug(row)
        write_private_message(
            payload["texto"], time_string, id, current_user, row[0])
        # int(row[0]), 'password': row[1], 'email': row[2]}

    try:
        cur.execute(statement, values)
        cur.execute("commit")
        result = {'mensagem': 'Inserted'}
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = {'erro': 'Failed!'}
    finally:
        if conn is not None:
            conn.close()

    return jsonify(result)
# --------------------------------------------------------------------------

# -------------------PUT CANCELAR LEILÃO------------------------------------


def put_cancelar(leilaoID):
    logger.info("###              DEMO: PUT /CANCELAR           ###")
    content = request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    # if content["ndep"] is None or content["nome"] is None :
    #    return 'ndep and nome are required to update'

    # if "ndep" not in content or "localidade" not in content:
    # return 'ndep and localidade are required to update'

    logger.info("---- cancelar leilão  ----")
    logger.info(f'content: {content}')

    # parameterized queries, good for security and performance
    statement = """
                UPDATE leiloes
                  SET cancelado = %s
                WHERE id_leilao = %s"""

    values = (True,leilaoID)

    try:
        res = cur.execute(statement, values)
        result = f'Updated: {cur.rowcount}'
        cur.execute("commit")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = 'Failed!'
    finally:
        if conn is not None:
            conn.close()
    return jsonify(result)
# --------------------------------------------------------------------------


# -----------------------PUT TERMINAR LEILÃO--------------------------------

def put_terminar(data_atual):
    logger.info("###              DEMO: PUT /TERMINAR            ###")
    content = request.get_json()
    logger.info(f'content: {1}')
    conn = db_connection()
    cur = conn.cursor()

    # if content["ndep"] is None or content["nome"] is None :
    #    return 'ndep and nome are required to update'

    # if "ndep" not in content or "localidade" not in content:
    # return 'ndep and localidade are required to update'

    logger.info("---- terminar leilão  ----")
    logger.info(f'content: {data_atual}')

    # parameterized queries, good for security and performance
    statement = """
                UPDATE leiloes
                  SET terminado = %s
                WHERE data_final_ <= %s"""

    values = (True,data_atual)

    try:
        res = cur.execute(statement, values)
        result = f'Updated: {cur.rowcount}'
        cur.execute("commit")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = {'erro': 'Failed!'}
    finally:
        if conn is not None:
            conn.close()
    return jsonify(result)
# --------------------------------------------------------------------------

# -------------------PUT BAN USER-------------------------------------


def put_ban_user(user):
    logger.info("###              DEMO: PUT /BAN         ###")
    content = request.get_json()

    conn = db_connection()
    cur = conn.cursor()

    # if content["ndep"] is None or content["nome"] is None :
    #    return 'ndep and nome are required to update'

    # if "ndep" not in content or "localidade" not in content:
    # return 'ndep and localidade are required to update'

    logger.info("---- Banir User ----")
    logger.info(f'content: {content}')

    # parameterized queries, good for security and performance
    statement = """
                UPDATE data_user
                  SET banido = %s
                WHERE username = %s"""

    values = (True,user)

    try:
        res = cur.execute(statement, values)
        result = f'Updated: {cur.rowcount}'
        cur.execute("commit")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = 'Failed!'
    finally:
        if conn is not None:
            conn.close()
    return jsonify(result)
# --------------------------------------------------------------------------

#--------------------------GET BAN USER-------------------------------------
@app.route("/dbproj/ban/<user_name>", methods=['GET'])
@token_required
def get_ban(current_user, user_name):
    logger.info("###              DEMO: GET /BAN USER        ###")

    conn = db_connection()
    cur = conn.cursor()

    #cur.execute("SELECT ndep, nome, local FROM dep where ndep = %s", (ndep,))
    cur.execute("SELECT username,banido from data_user where username=%s", (user_name,))
    rows = cur.fetchall()
    cur.execute("SELECT username from data_admin where username=%s",
                (current_user,))
    rows_admin = cur.fetchall()
    if(len(rows_admin) == 0):
        conn.close()
        return jsonify('ERRO ao banir user!!')
    if(len(rows)==0):
        conn.close()
        return jsonify('ERRO ao banir user!!')
    elif rows[0][1] == False:
        put_ban_user(user_name)
        cur.execute("SELECT id_leilao from leiloes where data_user_username=%s and terminado=false  and cancelado=false",(user_name,))
        rows_ban=cur.fetchall()
        for a in rows_ban:
            put_cancelar(a[0])
            cur.execute("SELECT distinct mensagem_mural.data_user_username from mensagem_mural where mensagem_mural.leiloes_id_leilao = %s ",(a[0],))
            rows_ban_message=cur.fetchall()
            for b in rows_ban_message:
                # utc = pytz.utc
                lx_tz = pytz.timezone('Europe/Lisbon')
                date = (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))
                write_private_message("Lamentamos o incómodo mas o leilão foi cancelado",date,a[0],b[0],b[0])
         ####       
        cur.execute("SELECT licitacoes.leiloes_id_leilao from licitacoes,leiloes where licitacoes.data_user_username=%s and licitacoes.leiloes_id_leilao=id_leilao and cancelado=false and terminado=false",(user_name,))
        rows_leiloes=cur.fetchall()
        for c in rows_leiloes:
            cur.execute("SELECT user_vencedor,preco_corrente,preco_inicial,data_user_username from leiloes where id_leilao=%s",(c[0],))
            rows_vencedor=cur.fetchall()
            if rows_vencedor[0][0]==user_name:
                cur.execute("SELECT licitacoes.valor,licitacoes.data_user_username from licitacoes,data_user where licitacoes.leiloes_id_leilao=%s and licitacoes.data_user_username=username and banido=false order by valor DESC",(c[0],))
                rows_vencedores_anteriores=cur.fetchall()
                if len( rows_vencedores_anteriores)==0:
                    update_price(rows_vencedor[0][3],rows_vencedor[0][2],c[0])
                else:
                    update_price(rows_vencedores_anteriores[0][1],rows_vencedores_anteriores[0][0],c[0])
            else:
                cur.execute("SELECT valor from licitacoes where leiloes_id_leilao=%s and data_user_username=%s order by valor",(c[0],user_name))
                rows_valor_anterior=cur.fetchall()
                if len(rows_valor_anterior)==0:
                    update_price(rows_vencedor[0][3],rows_vencedor[0][2],c[0])
                else:
                    update_price2(rows_valor_anterior[0][0],c[0])
            

        conn.close()
        return jsonify('User banido com sucesso!!')
    else:
        conn.close()
        return jsonify('ERRO ao banir user!!')
#---------------------------------------------------------------------------

# -------------------------GET CANCELAR LEILÃO------------------------------

@app.route("/dbproj/cancelar/<leilaoID>", methods=['GET'])
@token_required
def get_cancelado(current_user, leilaoID):
    logger.info("###              DEMO: GET /Leilões/cancelar           ###")

    conn = db_connection()
    cur = conn.cursor()

    #cur.execute("SELECT ndep, nome, local FROM dep where ndep = %s", (ndep,))
    cur.execute(
        "SELECT id_leilao,terminado,cancelado from leiloes where leiloes.id_leilao=%s", (leilaoID,))
    rows = cur.fetchall()
    cur.execute("SELECT username from data_admin where username=%s",
                (current_user,))
    rows_admin = cur.fetchall()
    if(len(rows_admin) == 0):
        return jsonify('Erro ao cancelar Leilão!!')
    elif rows[0][1] == False and rows[0][2] == False:
        put_cancelar(leilaoID)
        cur.execute("SELECT distinct mensagem_mural.data_user_username from mensagem_mural where mensagem_mural.leiloes_id_leilao = %s UNION SELECT leiloes.data_user_username from leiloes where id_leilao = %s", (leilaoID, leilaoID))
        rows_cancelar = cur.fetchall()
        # utc = pytz.utc
        lx_tz = pytz.timezone('Europe/Lisbon')
        date = (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))
        for row in rows_cancelar:
            write_private_message("Leilão Cancelado", date, leilaoID, row[0],row[0])
        conn.close()
        return jsonify('Cancelado com sucesso!!')
    else:
        conn.close()
        return jsonify('ERRO ao cancelar Leilão!!')


# --------------------------------------------------------------------------

#-------------------------TOP 5---------------------------------------------
@app.route("/dbproj/top10", methods=['GET'])
@token_required
def get_top10(current_user):
    logger.info("###              DEMO: GET /BAN USER        ###")

    conn = db_connection()
    cur = conn.cursor()
    lx_tz = pytz.timezone('Europe/Lisbon')
    data= ((datetime.now(tz=lx_tz) + timedelta(days=-10)).strftime("%Y-%m-%d %H:%M:%S"))
    logger.info(f'data: {data}')
    cur.execute("Select user_vencedor,COUNT(*) from leiloes where terminado=true and cancelado=false and data_final_ > %s  and user_vencedor <>data_user_username group by user_vencedor order by count(*) desc Limit 10",(data,))
    rows_vencedores = cur.fetchall()
    cur.execute("Select data_user_username,COUNT(*) from leiloes where terminado=true and cancelado=false and data_final_ > %s  group by data_user_username order by count(*) desc Limit 10",(data,))
    rows_leiloeiros = cur.fetchall()
    cur.execute("SELECT username from data_admin where username=%s",
                (current_user,))
    rows_admin = cur.fetchall()
    if(len(rows_admin) == 0):
        conn.close()
        return jsonify('ERRO ao cancelar Leilão!!')
    if(len(rows_leiloeiros)==0):
        conn.close()
        return jsonify('Sem leiloeiros suficientes')
    if(len(rows_vencedores)==0):
        conn.close()
        return jsonify('Sem licitadores suficientes')
    return jsonify({"TOP5-Vencedores":rows_vencedores},{"TOP5-Leiloeiro":rows_leiloeiros})

@app.before_request
def my_background_task():
    logger.info('content')
    # utc = pytz.utc
    lx_tz = pytz.timezone('Europe/Lisbon')
    data_atual = (datetime.now(tz=lx_tz).strftime("%Y-%m-%d %H:%M:%S"))
    put_terminar(data_atual)



##
# Demo PUT
##
# Update a department based on the a JSON payload
##
# To use it, you need to use postman or curl:
##
# curl -X PUT http://localhost:8080/departments/ -H "Content-Type: application/json" -d '{"ndep": 69, "localidade": "Porto"}'
##
"""
@app.route("/departments/", methods=['PUT'])
def update_departments():
    logger.info("###              DEMO: PUT /departments              ###");   
    content = request.get_json()

    conn = db_connection()
    cur = conn.cursor()


    #if content["ndep"] is None or content["nome"] is None :
    #    return 'ndep and nome are required to update'

    if "ndep" not in content or "localidade" not in content:
        return 'ndep and localidade are required to update'


    logger.info("---- update department  ----")
    logger.info(f'content: {content}')

    # parameterized queries, good for security and performance
    statement =
                UPDATE dep 
                  SET local = %s
                WHERE ndep = %s


    values = (content["localidade"], content["leiloes"])

    try:
        res = cur.execute(statement, values)
        result = f'Updated: {cur.rowcount}'
        cur.execute("commit")
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        result = 'Failed!'
    finally:
        if conn is not None:
            conn.close()
    return jsonify(result)"""


##########################################################
# DATABASE ACCESS
##########################################################

def db_connection():

    arr = decrypted.info()
    db = psycopg2.connect(user=arr[0],
                          password=arr[1],
                          host=arr[2],
                          port=arr[3],
                          database=arr[4])
    return db
###


# TESTE


@app.route('/dbproj', methods=['PUT'])
def login_post():
    logger.info("###              DEMO: POST /departments              ###")
    payload = request.get_json()
    conn = db_connection()
    cur = conn.cursor()
    logger.info("---- new user ----")
    logger.debug(f'payload: {payload}')
    cur.execute("SELECT password from data_user where username=%s",
                (payload["username"],))
    logger.debug(f'payload: { payload["username"]}')
    password = cur.fetchall()
    if(len(password) == 0):
        result = {"erro":'Login Invalido'}
        return jsonify(result)
    if password[0][0] != payload["password"]:
        result ={"erro":'Login Invalido'}
        if conn is not None:
            conn.close()
        return jsonify(result)
    token = jwt.encode({'public_id': payload["username"], 'exp': datetime.utcnow(
    ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})


@app.route('/dbproj/admin', methods=['PUT'])
def login_admin():
    logger.info("###              DEMO: POST /departments              ###")
    payload = request.get_json()
    conn = db_connection()
    cur = conn.cursor()
    logger.info("---- new user ----")
    logger.debug(f'payload: {payload}')
    cur.execute("SELECT password from data_admin where username=%s",
                (payload["username"],))
    logger.debug(f'payload: { payload["username"]}')
    password = cur.fetchall()
    if(len(password) == 0):
        result = {"erro":'Login Invalido'}
        return jsonify(result)
    if password[0][0] != payload["password"]:
        result ={"erro":'Login Invalido'}
        if conn is not None:
            conn.close()
        return jsonify(result)
    token = jwt.encode({'public_id': payload["username"], 'exp': datetime.utcnow(
    ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})


##########################################################
# MAIN
##########################################################
if __name__ == "__main__":
   
    # Set up the logging
    logging.basicConfig(filename="logs/log_file.log")
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]:  %(message)s','%H:%M:%S')
    # "%Y-%m-%d %H:%M:%S") # not using DATE to simplify
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    time.sleep(1)  # just to let the DB start before this print :-)
    
    logger.info("\n---------------------------------------------------------------\n" +
                "API v1.0 online: http://localhost:8080\n\n")

    app.run(host="0.0.0.0", debug=True, threaded=True)

# Referencia:
# Nuno Antunes <nmsa@dei.uc.pt>
# BD 2021 Team - https://dei.uc.pt/lei/
# University of Coimbra
