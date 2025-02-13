import readers
import pandas
airlines = readers.read_airlines()
dbdig_top5 = readers.read_dbdig_top5()
container = readers.read_dbdig_containerthroughput()
congestion_global = readers.read_dbdig_congestion_global()
congestion_la = readers.read_dbdig_congestion_la()
dbdig_chems = readers.read_dbdig_chems()

dm = pandas.concat([airlines, dbdig_top5, container, congestion_global, congestion_la, dbdig_chems]).sort_values(by=['Source','Endpoint','Frequency','Args','Year','Number'])
columns = 'Frequency','Source','Endpoint','Args','Number','Year','Value'
dm.to_csv(r'C:\Users\yanga\Desktop\artisan\output.csv', index=False, columns=columns)