import pickle
import pandas
from hysteresis_metrics import hysteresisMetrics

SonadoraDischargeFile = open('SonadoraDischarge9.p', 'rb')
SonadoraSPFile = open('SonadoraSpecificConductance9.p', 'rb')
SonadoraTurbidityFile = open('SonadoraTurbidity9.p', 'rb')
SonadoraDischarge = pickle.load(SonadoraDischargeFile)
SonadoraSP = pickle.load(SonadoraSPFile)
SonadoraTurbidity = pickle.load(SonadoraTurbidityFile)
print(SonadoraSP.head())
SonadoraDischarge = SonadoraDischarge.drop(columns=['censorcodecv_id', 'qualitycodecv_id'])
SonadoraSP = SonadoraSP.drop(columns=['censorcodecv_id', 'qualitycodecv_id'])
timespacing = 15 # 15 minutes between records
hysdict = hysteresisMetrics(SonadoraDischarge,SonadoraSP, timespacing, timespacing, debug=False, interpall=True,
                      discharge_time_spacing_units='minutes', response_time_spacing_units='minutes', )


print(hysdict)

#hysdictTurbidity = hysteresisMetrics(SonadoraDischarge,SonadoraTurbidity, timespacing, timespacing, debug=False, interpall=True,
#                      discharge_time_spacing_units='minutes', response_time_spacing_units='minutes', )

#print(hysdictTurbidity)
