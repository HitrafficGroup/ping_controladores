
import datetime
tiempo = datetime.datetime.now()
hora = tiempo.hour



delta_time = hora
aux_time = hora
while True:
    tiempo = datetime.datetime.now()
    hora = tiempo.hour
    delta_time = hora
    if delta_time == aux_time:
        if aux_time < 24:
            aux_time = delta_time+1
            print(aux_time)
    