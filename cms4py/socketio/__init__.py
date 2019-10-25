import socketio

sio = socketio.AsyncServer(async_mode='tornado')
socketio_tornado_handler = socketio.get_tornado_handler(sio)
