import pyodbc  
import pandas as pd
import datetime
import time
import os



print('====================================================================')
print('                  Activity y Payments daily csv                     ')
print('====================================================================')

date = input(r'Fecha de registro: formato YYYY/mm/dd: ')
try:
    year, month, day = map(int, date.split('/'))
    date1 = datetime.date(year, month, day)
except Exception as ex:
    print('Respete el formato de fecha (YYYY/mm/dd', ex)
    time.sleep(5.0)
    quit()

question = input(r'Si quiere cargar el archivo activity marque 1, si quiere cargar el archivo payments marque 2, si quiere cargar ambos archivos marque 3.:   ')
if question != '1' and question != '2' and question != '3':
    print('Debe marcar una de las 3 opciones: 1,2 o 3')
    time.sleep(3.0)
    print('El proceso debe comenzar de nuevo. Vuelva a ejecutar la aplicación.')
    quit()



absolute_path = os.getcwd()


def EjecutarActivity():
    def detect_path_activity(absolute_path):
        for i in os.listdir(absolute_path):
            if 'activity' in i.lower():
                activity_csv = absolute_path + '\\' + i
        return activity_csv


    act = detect_path_activity(absolute_path)
    activity_csv = pd.read_csv(act,sep = ',')
    activity_csv.iloc[:,4] = activity_csv.iloc[:,4].apply(lambda x: x.split(':'))
    activity_csv.iloc[:,5] = activity_csv.iloc[:,5].apply(lambda x: x.split(':'))
    activity_csv.iloc[:,4] = activity_csv.iloc[:,4].apply(lambda x: (int(x[1])*60) + int(x[2]))
    activity_csv.iloc[:,5] = activity_csv.iloc[:,5].apply(lambda x: (int(x[1])*60) + int(x[2]))
    activity_csv['date']  = [date1 for el in range(len(activity_csv))]

    try:
        activity_csv.rename(columns={
            'UUID del conductor': 'paydriver_uuid',
            'Nombre del conductor': 'dr_firstname',
            'Apellido del conductor': 'dr_lastname',
            'Viajes completados': 'per_numviaje',
            'Tiempo conectado (días: horas: minutos)': 'minutes_online',
            'Tiempo de viaje (días: horas: minutos)': 'minutes_on_trip',
        }, inplace=True)

        order_columns = ['date', 'paydriver_uuid', 'dr_firstname','dr_lastname','per_numviaje','minutes_online','minutes_on_trip']

        activity_csv = activity_csv[order_columns]
    except Exception as ex:
        print('El numero de columnas o nombre, no esta siendo respetado como en el modelo, configura las columnas previamente.', ex)
        print('Las columnas requeridas son: \nUUID del conductor',
        'Nombre del conductor',
        'Apellido del conductor',
        'Viajes completados',
        'Tiempo conectado (días: horas: minutos)',
        'Tiempo de viaje (días: horas: minutos)')
        time.sleep(5.0)
        quit()



    return activity_csv

def EjecutarPayments():
    def detect_path_payments(absolute_path):
        for i in os.listdir(absolute_path):
            if 'payments' in i.lower():
                payments_csv = absolute_path + '\\' + i
        return payments_csv
    
    try:     
        payments = detect_path_payments(absolute_path)  
    except Exception as ex:
        print('El archivo csv no pudo cargarse, asegurese de que el documento esta cerrado, que conserva su nombre o que el archivo no esta corrupto', ex)
        time.sleep(5.0)
        quit()



    data = ""

    with open(payments, encoding="utf8") as file:
        data = file.read().replace('"Reembolsos y gastos:Reembolsos:Infracciones, multas y gastos de remolque"','Reembolsos y gastos:Reembolsos:Infracciones multas y gastos de remolque')
    try:
        with open(payments, 'w', encoding="utf8") as file:
            file.write(data)
    except Exception as ex:
        print('El archivo no permite la escritura, asegurese de que el documento esta cerrado, que conserva su nombre o que el archivo no esta corrupto', ex)
        time.sleep(5.0)
        quit()

    try:
        csv_payments = pd.read_csv(payments, sep=',')
        cols = ['UUID del conductor', 'Nombre del conductor', 'Apellido del conductor','Ganancias totales', 'Ganancias totales : Precio neto','Pagos : Efectivo cobrado','Ganancias totales:Propina']
        csv_payments = csv_payments[cols]
        csv_payments.fillna('NULL', inplace=True)
        csv_payments.rename(columns={
        'UUID del conductor': 'paydriver_uuid',
        'Nombre del conductor': 'dr_firstname',
        'Apellido del conductor': 'dr_lastname',
        'Ganancias totales': 'revenue',
        'Ganancias totales : Precio neto' :'net_revenue',
        'Pagos : Efectivo cobrado': 'cash_balance',
        'Ganancias totales:Propina': 'tips'
    }, inplace=True)
    except Exception as ex:
        print('El numero de columnas o nombre, no esta siendo respetado como en el modelo, configura las columnas previamente.', ex)
        print('Las columnas requeridas son: \nUUID del conductor',
        'Nombre del conductor',
        'Apellido del conductor',
        'Ganancias totales',
        'Ganancias totales : Precio neto',
        'Reembolsos y gastos',
        'Pagos',
        'Pagos : Transferido a una cuenta bancaria',
        'Pagos : Efectivo cobrado',
        'Pagado a terceros',
        'Pagado a Uber',
        'Ganancias totales:Propina',
        'Ganancias totales:Otros precios:Ajuste',
        'Ganancias totales:Promociones',
        'Ganancias totales:Otras ganancias:Ajuste',
        'Pagado a Uber:Ajuste de redondeo de efectivo',
        'Pagado a Uber:División de precio',
        'Pagado a Uber:Recargo de Uber por eventos especiales',
        'Pagado a terceros:Precio por recogida en el aeropuerto',
        'Pagado a terceros:Ajustes posteriores al viaje',
        'Reembolsos y gastos:Reembolsos:Peaje', ex)
        time.sleep(5.0)
        quit()


    return csv_payments



if question == '1':
    activity = EjecutarActivity()
    activity.to_csv('activityparacargar.csv')
    print('Proceso finalizado correctamente')
elif question == '2':
    payments = EjecutarPayments()
    payments.to_csv('paymentsparacargar.csv')
    print('Proceso finalizado correctamente')
elif question == '3':
    activity = EjecutarActivity()
    activity.to_csv('activityparacargar.csv')
    payments = EjecutarPayments()
    payments.to_csv('paymentsparacargar.csv')
    print('Proceso finalizado correctamente')








