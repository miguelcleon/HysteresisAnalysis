from datetime import datetime
import pandas as pd
import math
import numpy

def interpolateMissingHI(hystIndex,raisingfalling,responseanddis,interval,lastinterval,i,maxWidth,closestopposite=None):
    # find discharge value closest to interval and last interval
    # if raisingfalling == 'raising':
    closestunderrow = None
    closestoverrow = None
    closestoverfallingrow = None
    closestoverraisingrow = None
    lastclosestoverrow = None
    closestunderfallingrow = None
    closestunderraisingrow = None
    lastclosestunderrow = None
    print('length response and dis')

    print(len(responseanddis))
    print('length raising and discharge')
    print(len(raisingfalling))
    print(raisingfalling)
    print('last interval')
    print(lastinterval)
    #rescale interval

    x = 0
    x0 = 0
    xf = 0
    xr = 0
    xf0 = 0
    xr0 = 0
    y = 0
    y0 = 0
    yf = 0
    yr = 0
    yr0 = 0
    yf0 = 0
    for index, row in responseanddis.iterrows():

        if row['datavaluedis'] > 0:
            if closestunderfallingrow is None and raisingfalling == 'raising and falling':
                if row['datavaluedis'] < lastinterval: # This SHOULD probably be enforced
                    if not math.isnan(row['datavalue']):
                        closestunderfallingrow = row
            if closestunderraisingrow is None and raisingfalling == 'raising and falling':
                if row['datavaluedis'] < lastinterval: # This SHOULD probably be enforced
                    if not math.isnan(row['datavalueraising']):
                            closestunderraisingrow = row
            if closestunderrow is None:
                if row['datavaluedis'] < lastinterval: # This SHOULD probably be enforced
                        # print(row)
                    if raisingfalling == 'falling' and not math.isnan(row['datavaluefalling']):
                        # print('HERHEHEHE')
                        closestunderrow = row
                    elif raisingfalling == 'raising' and not math.isnan(row['datavalueraising']):
                        closestunderrow = row

            else:
                if row['datavaluedis'] < lastinterval and row['datavaluedis'] > closestunderrow['datavaluedis']:
                    if raisingfalling == 'falling' and not math.isnan(row['datavaluefalling']):
                        closestunderrow = row
                    elif raisingfalling == 'raising' and not math.isnan(row['datavalueraising']):
                        closestunderrow = row
                    elif raisingfalling =='raising and falling':
                        # print(row)
                        if not math.isnan(row['datavalue']):
                            closestunderfallingrow = row
                        if not math.isnan(row['datavalueraising']):
                            closestunderraisingrow = row
            if closestoverrow is None:
                if row['datavaluedis'] >= interval: # This SHOULD probably be enforced
                    if raisingfalling == 'falling' and not math.isnan(row['datavaluefalling']):
                        closestoverrow = row
                    elif raisingfalling == 'raising' and not math.isnan(row['datavalueraising']):
                        closestoverrow = row
            if raisingfalling == 'raising and falling' and closestoverfallingrow is None:
                if row['datavaluedis'] >= interval: # This SHOULD probably be enforced
                    if not math.isnan(row['datavalue']):
                        closestoverfallingrow = row
                        # closestoverrow = row
            if raisingfalling == 'raising and falling' and closestoverraisingrow is None:
                if row['datavaluedis'] >= interval: # This SHOULD probably be enforced
                    if not math.isnan(row['datavalueraising']):
                        closestoverraisingrow = row
                    # closestoverrow = row
            if closestoverrow is not None:
                if row['datavaluedis'] >= interval and row['datavaluedis'] < closestoverrow['datavaluedis']:
                        if raisingfalling == 'falling' and not math.isnan(row['datavaluefalling']):
                            closestoverrow = row
                        elif raisingfalling == 'raising' and not math.isnan(row['datavalueraising']):
                            closestoverrow = row
            if raisingfalling == 'raising and falling':
                if closestoverfallingrow is not None:
                    # print(closestoverfallingrow['datavaluedis'])
                    # print(closestoverfallingrow['datavalue'])
                    if row['datavaluedis'] >= interval and row['datavaluedis'] < closestoverfallingrow['datavaluedis']:
                        if not math.isnan(row['datavalue']):
                            closestoverfallingrow = row
                if closestoverraisingrow is not None:
                   #  print(closestoverraisingrow['datavaluedis'])
                    # print(closestoverraisingrow['datavalueraising'])
                    if row['datavaluedis'] >= interval and row['datavaluedis'] < closestoverraisingrow['datavaluedis']:
                        if not math.isnan(row['datavalueraising']):
                            print('HERE@@@@&')
                            closestoverraisingrow = row
        if closestunderrow is not None and closestoverrow is not None:
            if raisingfalling == 'raising' :
                if  (math.isnan(row['datavaluedis']) or math.isnan(row['datavalueraising'])):
                    continue
                x0 = closestunderrow['datavaluedis']
                x = closestoverrow['datavaluedis']
                y0 = closestunderrow['datavalueraising']
                y = closestoverrow['datavalueraising']
            elif raisingfalling == 'falling':
                print(closestunderrow['datavaluedis'])
                print(closestoverrow['datavaluedis'])
                print(closestunderrow['datavaluefalling'])
                print(closestoverrow['datavaluefalling'])
                if (math.isnan(row['datavaluedis']) or math.isnan(row['datavaluefalling'])):
                    continue
                x0 = closestunderrow['datavaluedis']
                x = closestoverrow['datavaluedis']
                y0 = closestunderrow['datavaluefalling']
                y = closestoverrow['datavaluefalling']
        if raisingfalling =='raising and falling':
            #if math.isnan(row['datavaluedis']): # or math.isnan(row['datavalueraising'])or math.isnan(row['datavalue'])
            #    continue
            # x0 = closestunderrow['datavaluedis']
            print('NAN????')
            if closestunderraisingrow is not None:
                if not math.isnan(closestunderraisingrow['datavaluedis']):
                    xr0 = closestunderraisingrow['datavaluedis']
            if closestunderfallingrow is not None:
                if not math.isnan(closestunderfallingrow['datavaluedis']):
                    xf0 = closestunderfallingrow['datavaluedis']

            if closestoverraisingrow is not None:
                # print(closestoverraisingrow['datavaluedis'])
                if not math.isnan(closestoverraisingrow['datavaluedis']):
                    xr = closestoverraisingrow['datavaluedis']
            if closestoverfallingrow is not None:
                # print(closestoverfallingrow['datavaluedis'])
                if not math.isnan(closestoverfallingrow['datavaluedis']):
                    xf = closestoverfallingrow['datavaluedis']

            if closestunderraisingrow is not None:
                print(closestunderraisingrow['datavalueraising'])
                if not math.isnan(closestunderraisingrow['datavalueraising']): # or math.isnan(row['datavalueraising'])or math.isnan(row['datavalue'])
                    yr0 = closestunderraisingrow['datavalueraising']

            if not closestunderfallingrow is None:
                print(closestunderfallingrow['datavalue'])
                if not math.isnan(closestunderfallingrow['datavalue']):
                    yf0 = closestunderfallingrow['datavalue']  # this is falling limb; it didn't receive a suffix in this case
                #if not math.isnan(closestunderrow['datavalue']):
                #    yf = closestunderrow['datavalue']

            # print('over!!!')
            # print(interval)
            if closestoverraisingrow is not None:
                if not math.isnan(closestoverraisingrow['datavalueraising']):
                    yr = closestoverraisingrow['datavalueraising']
            if closestoverfallingrow is not None:
                if not math.isnan(closestoverfallingrow['datavalue']): # falling
                    yf = closestoverfallingrow['datavalue']

    xmidpoint = (lastinterval - interval) / 2
    m = 0
    b = 0

    estimatedresponse = 0
    if not raisingfalling == 'raising and falling' and not x == x0:

        m = (y-y0)/(x-x0)
        b = y - m*x
        estimatedresponse = m*xmidpoint +b
    HI = None


    if raisingfalling == 'raising and falling' and not xf == xf0 and not xr == xr0:
        aboveinterval = responseanddis[responseanddis['datavaluedis'] >= interval]
        raisingaboveinterval = aboveinterval[~aboveinterval['datavalueraising'].isnull()]
        belowlastinterval = responseanddis[responseanddis['datavaluedis'] < lastinterval]
        fallingaboveinterval = responseanddis[responseanddis['datavaluedis'] > interval]
        fallingaboveintervalnonan = aboveinterval[~aboveinterval['datavalue'].isnull()]
        print('yf0: ' + str(yf0))
        print('yr: ' + str(yr))
        print('yf: ' + str(yf))
        print('yr0: ' + str(yr0))

        # print(closestoverrow)
        mr = (yr - yr0) / (xr - xr0)
        yrmidpoint = (yr + yr0) / 2
        xrmidpoint = (xr + xr0) / 2
        br = yrmidpoint - mr * xrmidpoint
        estimatedresponseraising = mr * xrmidpoint + br
        print('midpoint y: ' + str(yrmidpoint))
        print('estimatedresponseraising: ' + str(estimatedresponseraising))
        mf = (yf - yf0) / (xf - xf0)
        yfmidpoint = (yf + yf0) / 2
        xfmidpoint = (xf + xf0) / 2
        bf = yfmidpoint - mf * xfmidpoint
        estimatedresponsefalling = mf * xfmidpoint + bf
        HI = estimatedresponseraising - estimatedresponsefalling
        # print('mr: '+ str(mr))
        # print('br: ' + str(br))
    #closestopposite
    if raisingfalling == 'raising':
        HI = estimatedresponse - closestopposite['datavaluefalling']
        # print('HI: ' +  str(tmp))
    elif raisingfalling == 'falling':
        HI = closestopposite['datavalueraising'] - estimatedresponse

    hystIndex['Interpolated HI for ' + str(i * 2) + '% discharge'] = HI
    # else:
    #     hystIndex['Interpolated HI for ' + str(i * 2) + '% discharge'] = 'no values present'
    if maxWidth and HI:
        if abs(HI) > abs(maxWidth):
            maxWidth = HI
    elif HI:
        maxWidth = HI


    return hystIndex,maxWidth
# discharge_time_spacing amount of time between discharge measurements
# time_spacing_units minutes or hours default to minutes
def hysteresisMetrics(discharge,response, discharge_time_spacing, response_time_spacing, debug=False, interpall=True,
                      discharge_time_spacing_units='minutes', response_time_spacing_units='minutes', ):
    hystdict = {}
    HIsandInterp = []
    #normalize times for discharge

    dtimeagg = discharge_time_spacing # dischargetsr.intendedtimespacing
    dtimeaggunit = discharge_time_spacing_units # dischargetsr.intendedtimespacingunitsid.unitsname
    dischargepdf = discharge # pd.DataFrame(list(discharge.values()))
    if 'minute' in dtimeaggunit or 'Minutes' in dtimeaggunit:
        # print(responsenormpdf['valuedatetime'])
        #print(str(dtimeaggunit))
        #print(str(dischargetsr.resultid))
        dischargepdf['valuedatetime'] = dischargepdf['valuedatetime'].apply(
            lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                int((dtimeagg * round((float(dt.minute) + float(
                                    dt.second) / 60)) / dtimeagg))))
    if 'hour' in dtimeaggunit:
        dtimeagg = dtimeagg * 60
        dischargepdf['valuedatetime'] = dischargepdf['valuedatetime'].apply(
            lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                int((dtimeagg * round((float(dt.minute) + float(
                                    dt.second) / 60) / dtimeagg)))))

    maxdischargerow = dischargepdf.loc[dischargepdf['datavalue'].idxmax()] # discharge.aggregate(Max('datavalue'))
    maxdischarge = maxdischargerow['datavalue']
    hystdict['Peak Q'] = maxdischarge
    hystdict['discharge_units'] = str(discharge[0].resultid.resultid.unitsid.unitsabbreviation)
    # print('units!!')
    # print(discharge[0].resultid.resultid.unitsid.unitsabbreviation)
    hystdict['Normalized slope of response'] = None
    hystdict['Max width of response'] = None
    hystdict['Hysteresis_Index'] = {}
    hystdict["HI_mean"] = None
    hystdict["HI_standard_deviation"] = None
    hystdict["HI_count"] = 0
    hystdict["HI values missing due to no raising limb measurement"] = 0
    hystdict["HI values missing due to no falling limb measurement"] = 0
    hystdict["HI values missing due to no raising and no falling limb measurement"] = 0
    hystdict['interpolated Max width of response'] = float('nan')
    hystdict["HI_mean_with_Interp"] = None
    hystdict["HI_standard_deviation_with_Interp"] = None
    hystdict['HI_count_and_interp'] = None
    if maxdischarge:
        # print(maxdischarge['datavalue__max'])
        # normalize discharge
        maxdischargerecord = discharge.order_by('-datavalue')[0]# .get(datavalue=float(maxdischarge['datavalue__max']))
        mindischargerecord = discharge.order_by('datavalue')[0]
        # dischargenorm = []
       #  dischargepdf = pd.DataFrame(list(discharge.values()))
        dischargepdf['datavalue'] = (dischargepdf['datavalue']- mindischargerecord.datavalue)/(maxdischargerecord.datavalue - mindischargerecord.datavalue)
        # print(dischargepdf['datavalue'])
        maxdisrow = dischargepdf.loc[dischargepdf['datavalue'].idxmax()]
        mindisrow = dischargepdf.loc[dischargepdf['datavalue'].idxmin()]
        maxnormdischargerecord = maxdisrow['datavalue']
        maxnormdischargedate = maxdisrow['valuedatetime']
        minnormdischargerecord = mindisrow['datavalue']
        minnormdischargedate = mindisrow['valuedatetime']

        maxresponse = response.loc[response['datavalue'].idxmax()]
        minresponse = response.loc[response['datavalue'].idxmin()]
        hystdict["Max response"] = maxresponse['datavalue']
        hystdict["Min response"] = minresponse['datavalue']
        # responsenorm = []
        responsenormpdf = response
        responsenormpdf['datavalue'] = (responsenormpdf['datavalue']- minresponse.datavalue)/(maxresponse.datavalue - minresponse.datavalue)

        # responsetsr = Timeseriesresults.objects.filter(resultid=response[0].resultid.resultid).get()
        timeagg =response_time_spacing # responsetsr.intendedtimespacing
        timeaggunit = response_time_spacing_units # responsetsr.intendedtimespacingunitsid.unitsname
        # print('timeaggunit')
        # print(timeaggunit)
        if 'minute' in timeaggunit or 'Minutes' in timeaggunit:
            # print(responsenormpdf['valuedatetime'])

            responsenormpdf['valuedatetime'] = responsenormpdf['valuedatetime'].apply(lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                                                           int(timeagg * round((float(dt.minute) + float(
                                                                               dt.second) / 60) / timeagg))))
        if 'hour' in timeaggunit:
            timeagg = timeagg * 60
            responsenormpdf['valuedatetime'] = responsenormpdf['valuedatetime'].apply(lambda dt: datetime(dt.year, dt.month, dt.day, dt.hour,
                                                                           int(timeagg * round((float(dt.minute) + float(
                                                                               dt.second) / 60) / timeagg))))

        raisinglimbresponse = responsenormpdf[(responsenormpdf['valuedatetime'] <= maxnormdischargedate)] # response.filter(valuedatetime__lte=maxdischargerecord.valuedatetime)
        fallinglimbresponse = responsenormpdf[(responsenormpdf['valuedatetime'] > maxnormdischargedate)]  # response.filter(valuedatetime__gt=maxdischargerecord.valuedatetime)

        hystIndex = []
        # 5% intervals of discharge for hysteresis index 20 bucket
        if not len(raisinglimbresponse.index) == 0 and not len(fallinglimbresponse.index) == 0:

            dischargerange = maxnormdischargerecord- minnormdischargerecord
            dischargeinterval = dischargerange / 50
            hystIndex = {}
            maxWidth = None
            premaxWidth = None
            countMissingRaising = 0
            countMissingFalling = 0
            countHIs = 0
            countHIsandInterp = 0
            countMissingBoth = 0
            firstRaisingResponse = None
            firstRaisingDis = None
            lastRaisingResponse = None
            lastRaisingDis = None
            for i in range(1,51):
                if i == 1:
                    lastinterval = 0
                else:
                    lastinterval = interval
                interval = dischargeinterval*i

                dischargeintervalvals = dischargepdf[(dischargepdf['datavalue'] <= interval) & (dischargepdf['datavalue'] > lastinterval)]
                # find matching response records
                # keys = list(dischargeintervalvals['valuedatetime'])
                dischargeandraisingresponse = pd.merge(dischargeintervalvals, raisinglimbresponse, on='valuedatetime', how='left', suffixes=('dis','raising'))
                dischargeandfallingresponse = pd.merge(dischargeintervalvals, fallinglimbresponse, on='valuedatetime', how='left', suffixes=('dis','falling'))

                if debug:
                    print('for interval: ' + str(interval))
                    print(dischargeintervalvals.head())
                    print(raisinglimbresponse.head())
                    print('falling limb')
                    print(fallinglimbresponse.head())
                    print('raising response ' + str(len(dischargeandraisingresponse.index)))
                    # print(dischargeandraisingresponse['datavalueraising'])
                    #print(dischargeandraisingresponse.head())
                    print('falling response ' + str(len(dischargeandfallingresponse.index)))
                    # print(dischargeandfallingresponse['datavaluefalling'])
                closestraisingrow = None
                closestfallingrow = None
                closestraisingdistance = None
                closestfallingdistance = None


                for index, raisingrow in dischargeandraisingresponse.iterrows():
                    # for slope calculation
                    if not firstRaisingDis:
                        if raisingrow['datavaluedis'] > 0:
                            firstRaisingDis = raisingrow['datavaluedis']
                    if not firstRaisingResponse:
                        if  raisingrow['datavalueraising'] > 0:
                            firstRaisingResponse = raisingrow['datavalueraising']
                    else:
                        if raisingrow['datavaluedis'] > 0:
                            lastRaisingDis = raisingrow['datavaluedis']
                        if raisingrow['datavalueraising'] > 0:
                            lastRaisingResponse = raisingrow['datavalueraising']

                    # for HI caclulation
                    if raisingrow['datavalueraising'] > 0:
                        if closestraisingdistance:
                            if abs(interval - raisingrow['datavaluedis']) < closestraisingdistance:
                                closestraisingdistance =  abs(interval - raisingrow['datavaluedis'])
                                closestraisingrow = raisingrow
                        else:
                            closestraisingdistance =  abs(interval - raisingrow['datavaluedis'])
                            closestraisingrow = raisingrow


                for index2, fallingrow in dischargeandfallingresponse.iterrows():
                    if fallingrow['datavaluefalling'] > 0: #and raisingrow['datavalueraising'] == fallingrow['datavaluefalling'] :
                        if closestfallingdistance:
                            if abs(interval - fallingrow['datavaluedis']) < closestfallingdistance:
                                closestfallingdistance = abs(interval - raisingrow['datavaluedis'])
                                closestfallingrow = fallingrow
                        else:
                            closestfallingdistance = abs(interval - raisingrow['datavaluedis'])
                            closestfallingrow = fallingrow

                dischargeandraisingresponseall = pd.merge(dischargepdf, raisinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('dis', 'raising'))
                dischargeandfallingresponseall = pd.merge(dischargepdf, fallinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('dis', 'falling'))
                dischargeriaisingandfallingresponseall = pd.merge(dischargeandraisingresponseall, fallinglimbresponse, on='valuedatetime',
                                                          how='left', suffixes=('', 'raising'))
                if interpall:
                    countMissingBoth += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising and falling', dischargeriaisingandfallingresponseall,interval,lastinterval,i,maxWidth)
                elif not closestraisingrow is None and not closestfallingrow is None:

                    tmp = closestraisingrow['datavalueraising'] - closestfallingrow['datavaluefalling']
                    # print('HI: ' +  str(tmp))
                    countHIs += 1
                    hystIndex['HI for ' + str(i*2) + '% discharge'] = tmp
                    if maxWidth:
                        if abs(tmp) > abs(maxWidth):
                            maxWidth = tmp
                    elif tmp:
                        maxWidth = tmp
                elif closestfallingrow is None and not closestraisingrow is None:
                    countMissingFalling += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'falling',dischargeandfallingresponseall,interval,lastinterval,i,maxWidth,closestraisingrow)
                elif closestraisingrow is None and not closestfallingrow is None:
                    countMissingRaising += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising',dischargeandraisingresponseall,interval,lastinterval,i,maxWidth,closestfallingrow)
                else:
                    countMissingBoth += 1
                    premaxWidth = maxWidth
                    hystIndex,maxWidth = interpolateMissingHI(hystIndex,'raising and falling', dischargeriaisingandfallingresponseall,interval,lastinterval,i,maxWidth)
                    # hystdict = interpolateMissingHI(hystdict,'raising', dischargeandraisingresponseall)
                if premaxWidth != maxWidth:
                    hystdict['interpolated Max width of response'] = maxWidth
                else:
                    hystdict['Max width of response'] = maxWidth
                # print('Max width ' + str(maxWidth))
                # print(hystIndex)
            if lastRaisingResponse > 0 and firstRaisingResponse > 0:
                hystdict['Normalized slope of response'] = (
                            lastRaisingResponse - firstRaisingResponse)  # / (lastRaisingDis - firstRaisingDis)

            hystdict["HI_count"] = countHIs
            hystdict["HI values missing due to no raising limb measurement"] = countMissingRaising
            hystdict["HI values missing due to no falling limb measurement"] = countMissingFalling
            hystdict["HI values missing due to no raising and no falling limb measurement"] = countMissingBoth
            HIs = []
            HIsandInterp = []
            for key, values in hystIndex.items():
                print('key!!!')
                print(key)
                if not 'Interpolated' in key:
                    if values:
                        HIs.append(values)
                    # print('here here')
                    # print(values)
                #else:
                print(values)
                if values:
                    HIsandInterp.append(values)
                print('interper val')
                print(values)
                if 'Hysteresis_Index' in hystdict:
                    if values:
                        hystdict['Hysteresis_Index'][key] = values
                        # print('HYST Index:' + key + ' val: ' + str(values))
                elif values:
                    tmpdict = {}

                    tmpdict[key ] = values
                    hystdict['Hysteresis_Index'] = tmpdict
                    # 3print('tmpdict: ' + key + 'val: ' +str(values))
            hystAvg = numpy.mean(HIs) #sum(values) / float(len(values))
            hystStd = numpy.std(HIs)
            hystAvgInterp = float('NaN')
            hystStdInterp = float('NaN')
            hystAvgInterp = numpy.mean(HIsandInterp) #sum(values) / float(len(values))
            hystStdInterp = numpy.std(HIsandInterp)

            print(HIsandInterp)
            hystdict["HI_count_and_interp"] = str(len(HIsandInterp))
            hystdict["HI_mean"] = str(hystAvg)
            hystdict["HI_standard_deviation"] = str(hystStd)

            hystdict["HI_mean_with_Interp"] = str(hystAvgInterp)
            hystdict["HI_standard_deviation_with_Interp"] = str(hystStdInterp)

        if HIsandInterp:
            if len(HIsandInterp) < 50:
                print('hystdict asdf')
                print('HIs and Interp count: ' + str(len(HIsandInterp)))
                print('max date discharge: ' + str(maxnormdischargedate))
                print('max response date: ' +str(maxresponse['valuedatetime']))
                # print('max response id: ' + str(maxresponse.resultid.resultid.resultid))
                for key, value in hystdict.items():
                    print(str(key) + ': ' + str(value))
    return hystdict