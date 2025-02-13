import readers
import pandas
import pandas.core.groupby.generic as grouping

airlines = readers.read_airlines()
dbdig_top5 = readers.read_dbdig_top5()
container = readers.read_dbdig_containerthroughput()
congestion_global = readers.read_dbdig_congestion_global()
congestion_la = readers.read_dbdig_congestion_la()
dbdig_chems = readers.read_dbdig_chems()

dm = pandas.concat([airlines, dbdig_top5, container, congestion_global, congestion_la, dbdig_chems]).sort_values(by=['Source','Endpoint','Frequency','Args','Year','Number'])
columns = 'Frequency','Source','Endpoint','Args','Number','Year','Value'

weekly = dm[dm['Frequency']=='Weekly']
dates = pandas.to_datetime(weekly['Year'].astype(str) + '-W' + weekly['Number'].astype(str) + '-6', format='%Y-W%W-%w')
weekly['Quarter'] = pandas.PeriodIndex(dates, freq='Q')
del weekly['Year']
del weekly['Number']
output = list()
for arg, func in [('Sum',grouping.DataFrameGroupBy.sum),('Min',grouping.DataFrameGroupBy.min),('Max',grouping.DataFrameGroupBy.max),('Median',grouping.DataFrameGroupBy.median),('Mean',grouping.DataFrameGroupBy.mean)]:
    agg = func(weekly.groupby(['Frequency','Source','Endpoint','Args','Quarter'])).reset_index()
    agg['Args'] = f'{arg}('+agg['Args']+')'
    output.append(agg)
weeklyagg = pandas.concat(output)
weeklyagg['Number'] = weeklyagg['Quarter'].dt.quarter
weeklyagg['Year'] = weeklyagg['Quarter'].dt.year
del weeklyagg['Quarter']
weeklyagg = weeklyagg.reindex(columns = ['Frequency', 'Source', 'Endpoint', 'Args', 'Number', 'Year', 'Value'])
weeklyagg['Frequency'] = 'Quarter'
weeklyagg.to_csv(r'C:\Users\yanga\Desktop\artisan\Weekly Aggregate.csv', index=False, columns=columns)


monthly = dm[dm['Frequency']=='Monthly']
dates = pandas.to_datetime(monthly['Year'].astype(str) + '-' + monthly['Number'].astype(str), format='%Y-%m')
monthly['Quarter'] = pandas.PeriodIndex(dates, freq='Q')
del monthly['Year']
del monthly['Number']
output = list()
for arg, func in [('Sum',grouping.DataFrameGroupBy.sum),('Min',grouping.DataFrameGroupBy.min),('Max',grouping.DataFrameGroupBy.max),('Median',grouping.DataFrameGroupBy.median),('Mean',grouping.DataFrameGroupBy.mean)]:
    agg = func(monthly.groupby(['Frequency','Source','Endpoint','Args','Quarter'])).reset_index()
    agg['Args'] = f'{arg}('+agg['Args']+')'
    output.append(agg)
monthlyagg = pandas.concat(output)
monthlyagg['Number'] = monthlyagg['Quarter'].dt.quarter
monthlyagg['Year'] = monthlyagg['Quarter'].dt.year
del monthlyagg['Quarter']
monthlyagg = monthlyagg.reindex(columns = ['Frequency', 'Source', 'Endpoint', 'Args', 'Number', 'Year', 'Value'])
monthlyagg['Frequency'] = 'Quarter'
monthlyagg.to_csv(r'C:\Users\yanga\Desktop\artisan\Monthly Aggregate.csv', index=False, columns=columns)


daily = dm[dm['Frequency']=='Daily']
dates = pandas.to_datetime(daily['Year'].astype(str) + '-' + daily['Number'].astype(str), format='%Y-%j')
daily['Quarter'] = pandas.PeriodIndex(dates, freq='Q')
del daily['Year']
del daily['Number']
output = list()
for arg, func in [('Sum',grouping.DataFrameGroupBy.sum),('Min',grouping.DataFrameGroupBy.min),('Max',grouping.DataFrameGroupBy.max),('Median',grouping.DataFrameGroupBy.median),('Mean',grouping.DataFrameGroupBy.mean)]:
    agg = func(daily.groupby(['Frequency','Source','Endpoint','Args','Quarter'])).reset_index()
    agg['Args'] = f'{arg}('+agg['Args']+')'
    output.append(agg)
dailyagg = pandas.concat(output)
dailyagg['Number'] = dailyagg['Quarter'].dt.quarter
dailyagg['Year'] = dailyagg['Quarter'].dt.year
del dailyagg['Quarter']
dailyagg = dailyagg.reindex(columns = ['Frequency', 'Source', 'Endpoint', 'Args', 'Number', 'Year', 'Value'])
dailyagg['Frequency'] = 'Quarter'
dailyagg.to_csv(r'C:\Users\yanga\Desktop\artisan\Daily Aggregate.csv', index=False, columns=columns)


for freq in dm['Frequency'].unique():
    subdm = dm[dm['Frequency']==freq]
    subdm.to_csv(r'C:\Users\yanga\Desktop\artisan\%s.csv'%freq, index=False, columns=columns)
    print(freq, subdm['Number'].astype(int).max())