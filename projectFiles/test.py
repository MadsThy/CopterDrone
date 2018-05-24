import socketio
import eventlet
from dronekit import connect as droneconnect, VehicleMode
from flask import Flask, render_template, jsonify
print "Waiting for dronekit import"
from threading import Thread
import socket,sys,math,logging,os,time

logging.info("Dronekit imported.")
from pymavlink import mavutil # Needed for command message definitions

sio = socketio.Server()
app = Flask(__name__)

commands = [
    {
        'command': u'connect',
        'description': 'Connects to a host', 
    },
    {
        'command': 'Not yet made',
        'description': 'TBD'
    }
]

@app.route('/connect', methods=['GET'])
def testing():
    vehicle = droneconnect('udp:127.0.0.1:14550',wait_ready=True)
    print "Server ready."
    vehicle.armed = True

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('my message')
def message(sid, data):
    print('message ', data)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)