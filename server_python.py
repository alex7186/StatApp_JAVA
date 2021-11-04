import uvicorn

from db.db_manager import connect_to_db, add_db_log, search_user_by_access_key, search_user_array, search_user_history, update_date_last_login

from classes.server_functions import make_server_diagrams


from json import dumps, loads
from json.decoder import JSONDecodeError
from io import BytesIO

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Cookie, Response
from starlette.responses import RedirectResponse


from warnings import filterwarnings
filterwarnings('ignore')

app = FastAPI()


db_connection = connect_to_db()
db_cursor = db_connection.cursor()

add_db_log(db_connection, db_cursor, 'I', 'server started')



@app.post("/")
async def server(request : Request):

    request_str = await request.body()
    add_db_log(db_connection, db_cursor, 'I', 'new request')

    try:
        data = loads(request_str)  
        add_db_log(db_connection, db_cursor, 'I', 'request decoded')      
    except JSONDecodeError:
        add_db_log(db_connection, db_cursor, 'E', 'input JSON decoding error')
        return {"status" : "bad", "message" : "input JSON decoding error"}

    server_return = make_server_diagrams(data)

    if not server_return:
        add_db_log(db_connection, db_cursor, 'E', 'wrong req_type '+ data['req_type'])
    add_db_log(db_connection, db_cursor, 'I', 'answer sent')
    
    return {"status" : "ok", "answer" : server_return}

uvicorn.run(
    app, 
    port=8000, 
    host='0.0.0.0',

    )

