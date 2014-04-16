
from datetime import timedelta
from dumbo import main, MultiMapper,  opt
import os, sys
import pytz
import datetime as dt
from pytz import timezone


class MultiMapperHijo(MultiMapper):

    def __new__(cls):
        if os.environ.get("dumbo_joinkeys", "no") == "yes":
            cls.__call__ = cls.__call__joinkey
        else:
            cls.__call__ = cls.__call__normalkey
        return object.__new__(cls)

    def __call__normalkey(self, data):
        #print >> sys.stderr, "__call__normalkey"
        mappers = self.mappers
        for key, value in data:
            path, key_self = key
            for pattern, mapper in mappers:
                if pattern in path:
                    for output in mapper(key, value):
                        yield output

#Mapper de los fichero ROA (De minerva)
class mapperO:
    #Inicializar el mapper
    #Inicializar el mapper
    def __init__(self):
        self.headline=False


    #llamar al mapper
    def __call__(self, key, value):
    #header:PeriodId,NumAmisco,StartTime,EndTime,Times,X,Y,null,
        #print >> sys.stderr, 'mapper'

        if not self.headline:
            self.headline=True
            yield '0Period,NumPlayer,NamePlayer,Minute,x,y,Intesity', 0
            return
        else:
            fields=value.strip().split(",")
            PeriodId=str(fields[0])
            NumAmisco=str(fields[1])
            Times=str(int(int(fields[4])/600)) #pasar a segundos
            X=str(fields[5])
            Y=str(fields[6])
            #emitir una linea (key,value) como entrada del reducer donde
            yield PeriodId+","+NumAmisco+","+Times+","+X+","+Y, 1





#dumbo start frecuencias.py -input data/*  -output macthOut.csv -overwrite yes
# sed 's/'\''/ /g' macthOut.csv > macthOut2.csv
#sed 's/ //g' macthOut2.csv > macthOut3.csv
#sed 's/ /  /g' macthOut3.csv > macthOut4.csv
#Period,NumPlayer,NamePlayer,Minute,X,Y,Intesity
#la funcion reducer recibe como parametros: key con el formato date-imsi-duration y value que contiene lista de registros salida de los mappers con la misma clave key date-imsi-duration-msisdn
def reducer(key, values):
    cont=0
    #print >> sys.stderr, 'reduce'

    #Cuenta numero de registros con la misma clave
    for v in values:
        cont+=1


    if(key.find('0PeriodId')!=-1): #cabecera
        #print >> sys.stderr, key
        yield key,''
    else:
        yield key,','+str(cont)


def runner(job):


    #print >> sys.stderr, 'runner'
    opts = [("addpath", "yes")]
    mapper = MultiMapperHijo()
    mapper.add("Match-", mapperO)

    #print >> sys.stderr, 'runner'
    #identificamos que funciones o clases seran llamadas como mapper y reducer
    job.additer(mapper, reducer,opts=opts)

    #el resultado del map/reducer se almanena en el fichero indicado en el parametro -output


#funcion main que llama al runner de DUmbo para ejecutar multiples
#processos en caso de usar paralelismo
if __name__ == "__main__":
    #print >> sys.stderr, 'main'
    main(runner)




