import os
import pandas
import datetime
def artisan_folder(*args):
    return os.path.join('C:\\','users','yanga','desktop','artisan',*args)

def read_airline_file(filename, section=None):
    dm = pandas.read_excel(filename, sheet_name=section)
    if section is None:
        for col in dm:
            dm[col] = dm[col][pandas.notnull(dm[col]['Airline Name'])]
    else:
        dm = dm[pandas.notnull(dm['Airline Name'])]
    return dm

def read_airlines():
    output = list()
    for excel in ['Intra-Europe LCC and Network Carriers 3 days - Truncated.xlsx','Intra-Europe LCC and Network Carriers 60 days - Truncated.xlsx',
                  'Inter-Continental Network Airlines 3 days - Truncated.xlsx','Inter-Continental Network Airlines 60 days - Truncated.xlsx'
                  ]:
        rez = read_airline_file(artisan_folder(excel))
        for col in rez:
            dm = rez[col]
            dates = sorted([x for x in dm.columns if isinstance(x,datetime.datetime)])
            for date in dates:
                subdm = dm[pandas.notnull(dm[date])]
                args = subdm['Airline Code'] + ': ' + subdm['Origin Code'] + ' - ' + subdm['Destination Code'] + ' (' + col + ')'
                output.append(pandas.DataFrame(dict(Frequency='Weekly', Source='Deutsche Bank', Endpoint = f'/data/db/{excel}', 
                                                    Args=args, Number=date.isocalendar()[1], Year = date.year, Value=subdm[date])))
                
    return pandas.concat(output).sort_values(by=['Source','Endpoint','Frequency','Args','Year','Number'])

def read_dbdig_top5():
    filename = 'dbDIG_Top5_ContainerCompaniesTracker_2025_01_23.xlsx'
    dm = pandas.read_excel(artisan_folder(filename), sheet_name=None)
    output = list()
    
    sheet = 'Daily'
    num = dm[sheet]['Date'].dt.strftime('%j').astype(int)
    for col in dm[sheet].columns:
        if col=='Date':continue
        output.append(pandas.DataFrame(dict(Frequency='Daily', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=num, Year=dm[sheet]['Date'].dt.year, Value=dm[sheet][col])))


    for sheet in 'Daily Event Count - China', 'Daily TEU - China':
        for year in [x for x in dm[sheet].columns if len(x)==4]:
            subdm = dm[sheet][pandas.notnull(dm[sheet][year])]
            dates = pandas.to_datetime(year + '-' + subdm['Month-Day'])
            num = dates.dt.strftime('%j').astype(int)
            
            output.append(pandas.DataFrame(dict(Frequency='Daily', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                            Args=sheet, Number=num, Year=dates.dt.year, Value=subdm[year])))
            
    num = dm['Monthly']['Date'].dt.month
    for col in dm['Monthly'].columns:
        if col=='Date':continue
        output.append(pandas.DataFrame(dict(Frequency='Monthly', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=num, Year=dm['Monthly']['Date'].dt.year, Value=dm['Monthly'][col])))
        

    return pandas.concat(output).sort_values(by=['Source','Endpoint','Frequency','Args','Year','Number'])

def read_dbdig_containerthroughput():
    filename = 'dbDIG_ContainerThroughputIndex_Report_2025_01_23.xlsx'
    dm = pandas.read_excel(artisan_folder(filename), sheet_name=None)
    output = list()
    
    sheet = 'Monthly Index'
    for col in dm[sheet]:
        if col.lower() in ('month','year','date','date of reporting'):continue
        
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Month'])*pandas.notnull(dm[sheet][col])]
        
        dates = pandas.to_datetime(subdm['Date'])
        output.append(pandas.DataFrame(dict(Frequency='Monthly', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=dates.dt.month, Year=dates.dt.year, Value=subdm[col])))
    
    sheet = 'Weekly Index'
    for col in dm[sheet]:
        if col.lower() in ('month','berth departure'):continue
        
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Month'])*pandas.notnull(dm[sheet][col])]
        
        dates = pandas.to_datetime(subdm['Berth Departure'])
        output.append(pandas.DataFrame(dict(Frequency='Weekly', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=dates.dt.isocalendar().week, Year=dates.dt.year, Value=subdm[col])))
        
    return pandas.concat(output).sort_values(by=['Source','Endpoint','Frequency','Args','Year','Number'])

def read_dbdig_congestion(filename):
    dm = pandas.read_excel(artisan_folder(filename), sheet_name=None)
    output = list()
    
    sheet = 'Daily'
    for col in dm[sheet].columns:
        if col=='Date':continue
        
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Date'])*pandas.notnull(dm[sheet][col])]
        num = subdm['Date'].dt.strftime('%j').astype(int)
        output.append(pandas.DataFrame(dict(Frequency='Daily', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=num, Year=subdm['Date'].dt.year, Value=subdm[col])))
    sheet = 'Weekly'
    for col in dm[sheet].columns:
        if col=='Date':continue
        
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Date'])*pandas.notnull(dm[sheet][col])]
        output.append(pandas.DataFrame(dict(Frequency='Weekly', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=subdm['Date'].dt.isocalendar().week, Year=subdm['Date'].dt.year, Value=subdm[col])))
        
    sheet = 'Index Vs Freight Rate'
    for col in dm[sheet].columns:
        if col=='Date':continue
        
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Date'])*pandas.notnull(dm[sheet][col])]
        output.append(pandas.DataFrame(dict(Frequency='Weekly', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=subdm['Date'].dt.isocalendar().week, Year=subdm['Date'].dt.year, Value=subdm[col])))
        
    return pandas.concat(output).sort_values(by=['Source','Endpoint','Frequency','Args','Year','Number'])

def read_dbdig_congestion_global():
    return read_dbdig_congestion('dbDIG_Congestion_Global_2025_01_23.xlsx')
def read_dbdig_congestion_la():
    return read_dbdig_congestion('dbDIG_Cogestion_LosAngeles_LongBeach_2025_01_23.xlsx')

def read_dbdig_chems():
    filename = 'dbDIG_Chems_2025_01_23.xlsx'
    dm = pandas.read_excel(artisan_folder(filename), sheet_name=None)
    output = list()

    sheet = 'Daily counts'
    for col in dm[sheet].columns:
        if col=='Date':continue
        
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Date'])*pandas.notnull(dm[sheet][col])]
        num = subdm['Date'].dt.strftime('%j').astype(int)
        output.append(pandas.DataFrame(dict(Frequency='Daily', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=num, Year=subdm['Date'].dt.year, Value=subdm[col])))

    sheet = 'Weekly counts'
    for col in dm[sheet].columns:
        if col=='Date':continue
        
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Date'])*pandas.notnull(dm[sheet][col])]
        output.append(pandas.DataFrame(dict(Frequency='Weekly', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=subdm['Date'].dt.isocalendar().week, Year=subdm['Date'].dt.year, Value=subdm[col])))
        
        
    sheet = 'Monthly counts'
    for col in dm[sheet].columns:
        if col=='Date':continue
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Date'])*pandas.notnull(dm[sheet][col])]
        output.append(pandas.DataFrame(dict(Frequency='Monthly', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=subdm['Date'].dt.month, Year=subdm['Date'].dt.year, Value=subdm[col])))
    
    sheet = 'Quarterly counts'
    for col in dm[sheet].columns:
        if col=='Quarter':continue
        subdm = dm[sheet][pandas.notnull(dm[sheet]['Quarter'])*pandas.notnull(dm[sheet][col])]
        output.append(pandas.DataFrame(dict(Frequency='Quarterly', Source='Deutsche Bank', Endpoint = f'/data/db/{filename}', 
                                        Args=col, Number=subdm['Quarter'].str[0], Year=subdm['Quarter'].str[-4:], Value=subdm[col])))
        
    return pandas.concat(output).sort_values(by=['Source','Endpoint','Frequency','Args','Year','Number'])