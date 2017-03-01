from bottle import *
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
ws_set = set()

@get('/')
def idx():
    return """
    <!DOCTYPE html>
    <html>
      <head>
        <title>title</title>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <script src="//code.jquery.com/jquery-1.10.2.min.js" type="text/javascript"></script>
      </head>
      <body>
      	<button onClick="location.href='127.0.0.1:8001/machinelearning'">Click me</button>
        <ul id="box"></ul>
        <script>
            // websocket connection
            ws = new WebSocket('ws://127.0.0.1:8001/websocket');
            ws.onopen = function(evt) {
                console.log('connected');
            }
            ws.onmessage = function(evt) {
                console.log('[GOT]' + evt.data);
                $("#box").append("<li>" + evt.data + "</li>");
            }
            function sendToSocket(msg) {
            	ws = new WebSocket('ws://127.0.0.1:8001/websocket');
                return ws.send(msg);
            }
            // send
            function myFunction() {
                ;
            }
        </script>
      </body>
    </html>
    """

@get('/websocket', apply=[websocket])
def chat(ws):
    ws_set.add(ws)
    while True:
        msg = ws.receive()
        if msg is not None:
            for u in ws_set:
                u.send(msg)
        else: break
    ws_set.remove(ws)

@route('/machinelearning')
def idx():
    print "123123123"
    ASLrecognition.Analysis()

if __name__ == '__main__':
    run(host='127.0.0.1', port=8001, server=GeventWebSocketServer)
