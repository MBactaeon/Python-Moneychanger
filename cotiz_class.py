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