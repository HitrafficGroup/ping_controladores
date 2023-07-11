import platform, subprocess
import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import firestore
import time
import datetime
tiempo = datetime.datetime.now()
hora = tiempo.hour
cred = credentials.Certificate('credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
token = '6396937914:AAGHJaqKDhFLZmk2tMUUzOVV0Hvqi1690i0'
method = 'sendMessage'   
users_ref = db.collection("historial_controladores")
def ping(host_or_ip, packets=1, timeout=500):
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=0x08000000)
        return result.returncode == 0 and b'TTL=' in result.stdout
    else:
        command = ['ping', '-c', str(packets), '-w', str(timeout), host_or_ip]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0


def updateStateController(id,estado):
    controller_ref = db.collection("historial_controladores").document(id)   
    controller_ref.update({"online": estado})

def enviarNotificacion(msg):
    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
            data={'chat_id': '-914024384', 'text': msg}
        ).json()



while True:
    controllers_ip = []
    controladores_desconectados = []
    docs = users_ref.stream()
    for doc in docs:
        controllers_ip.append(doc.to_dict())
    for controller in controllers_ip:
        if ping(controller["ip"]):
            state = controller['online']
            if state == False:
                msg = 'el siguiente controlador se a Re-Conectado: Nombre: {}  modelo: {} Ip: {} '.format(controller['nombre'],controller['modelo'],controller['ip'])
                enviarNotificacion(msg=msg)
            updateStateController(controller["id"],True)
            print("tenemos ping del controlador: ",controller["ip"])
        else:
            updateStateController(controller["id"],False)
            print("no tenemos ping del controlador: ",controller["ip"])
            controladores_desconectados.append(controller['ip'])

    for ip in controladores_desconectados:
        for controller in controllers_ip:
            if controller['ip'] == ip:
                state = controller['online']
                if state == True:
                    msg = 'el siguiente controlador esta DESCONECTADO !!: Nombre: {}  modelo: {} Ip: {}  '.format(controller['nombre'],controller['modelo'],controller['ip'])
                    enviarNotificacion(msg=msg)
    time.sleep(360)

