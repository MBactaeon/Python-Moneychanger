# Class functions
from datetime import datetime, date
import json
from urllib.request import urlopen
def get(url):
    with urlopen(url) as resource:
        return json.load(resource)

class BilleteraDivisa(object):
    def __init__(self, pesos):
        self.__disp_pesos = pesos
        self.__disp_dolarO = 1000
        self.__historico_dolar_of = []  #dolar oficial
        self.__hoy = date.today().strftime('%d, %m, %Y')
        self.__cotizaciones = get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        self.__Impuesto_pais = 30
    def comp_oficial(self, cant):
        cant_req = cant
        impuesto = ((cant * self.__Impuesto_pais)/100)
        if cant_req <= (self.__disp_pesos+impuesto):
            for cot in self.__cotizaciones:
                if cot['casa']['nombre'] == "Dolar Oficial":
                    cotiz_json = cot['casa']['venta']
                    cotiz = cotiz_json.replace(',', '.')
                    cotiz_oficial = float(cotiz)
                    operacion = cant_req / cotiz_oficial
                    self.__disp_pesos -=(impuesto+cant_req)
                    self.__disp_dolarO += operacion
                    self.__historico_dolar_of.append({"Acción": "Compra","Fecha":self.__hoy, "Datos":{"Cant": operacion, "ValComp": cotiz_json}})
                    return "Se han añadido a su tenencia: usd"+str(operacion)
                else:
                    continue
        else:
            return "No tiene disponible para realizar la operación"
    def vend_oficial(self, cant):
        cant_req = cant
        if cant_req <= self.__disp_dolarO:
            for cot in self.__cotizaciones:
                if cot['casa']['nombre'] == "Dolar Oficial":
                    cotiz_json = cot['casa']['compra']
                    cotiz = cotiz_json.replace(',', '.')
                    cotiz_oficial = float(cotiz)
                    operacion = cant_req * cotiz_oficial
                    self.__disp_pesos +=cant_req
                    self.__disp_dolarO -= operacion
                    self.__historico_dolar_of.append({"Acción": "Venta","Fecha":self.__hoy, "Datos":{"Cant": cant_req, "ValComp": cotiz_json}})
                    return "Se han añadido a su tenencia: $"+str(operacion)+ " y se han debitado usd"+str(cant_req)
                else:
                    continue
        else:
            return "No tiene disponible para realizar la operación"
    def get_ver_disp_pesos(self):
        return "Monto disponible en pesos: $"+str(self.__disp_pesos)
    def get_ver_disp_dolar(self):
        return "Monto disponible en dólares: usd"+str(self.__disp_dolarO)
    def get_imp_pais(self):
        return str(self.__Impuesto_pais)
    def get_historico(self):
        return self.__historico_dolar_of
############################
#Console test
billetera = BilleteraDivisa(10000)
desicion = input("Operación a realizar: '1' Comprar dólares | '2' Vender dólares:  ")
while desicion == '1' or desicion == '2':
    if desicion == '1':
        print(billetera.get_ver_disp_pesos())
        try:
            print("Recuerde que se debitará un "+billetera.get_imp_pais()+"% adicional por el Impuesto P.A.I.S")
            cant = input("Indique la cantidad de pesos a usar: ")
            cant_compra = int(cant)
            print(billetera.comp_oficial(cant_compra))
        except:
            print("La cantidad indicada es errónea")
    elif desicion == '2':
        print(billetera.get_ver_disp_dolar())
        cant = input("Indique la cantidad de dólares a usar: ")       
        try:
            cant_venta = int(cant)
            print(billetera.vend_oficial(cant_venta))
        except:
            print("La cantidad indicada es errónea")
    desicion = input("Operación a realizar: '1' Comprar dólares | '2' Vender dólares:  ")

print("Historico de Operatoria: ")
for oper in billetera.get_historico():
    print(oper)
