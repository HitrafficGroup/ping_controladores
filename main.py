import platform, subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
# Use a service account.
cred = credentials.Certificate('credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

users_ref = db.collection("historial_controladores")
def ping(host_or_ip, packets=1, timeout=500):
    #The ping command is the same for Windows and Linux, except for the "number of packets" flag.
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=0x08000000)
        return result.returncode == 0 and b'TTL=' in result.stdout
    else:
        command = ['ping', '-c', str(packets), '-w', str(timeout), host_or_ip]
        # run parameters: discard output and error messages
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0


def updateStateController(id,estado):
    controller_ref = db.collection("historial_controladores").document(id)   
    controller_ref.update({"online": estado})




while True:
    controllers_ip = []
    docs = users_ref.stream()
    for doc in docs:
        controllers_ip.append(doc.to_dict())
    for controller in controllers_ip:
        if ping(controller["ip"]):
            updateStateController(controller["id"],True)
            print("tenemos ping del controlador: ",controller["ip"])
        else:
            updateStateController(controller["id"],False)
            print("no tenemos ping del controlador: ",controller["ip"])
    time.sleep(360)
