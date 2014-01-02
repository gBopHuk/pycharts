import sys #нужно чтоб использовать sys.argv — массив слов вбитых в командную строку вместе со скриптом
from datetime import datetime

functions_for_periods = {
  'M5' : lambda d: datetime(d.year, d.month, d.day, d.hour, (d.minute // 5)*5).strftime("%Y.%m.%d %H:%M"), 
  'M15': lambda d: datetime(d.year, d.month, d.day, d.hour, (d.minute // 15)*15).strftime("%Y.%m.%d %H:%M"), 
  'M30': lambda d: datetime(d.year, d.month, d.day, d.hour, (d.minute // 30)*30).strftime("%Y.%m.%d %H:%M"), 
  'H1' : lambda d: d.strftime("%Y.%m.%d %H:00"), 
  'H4' : lambda d: datetime(d.year, d.month, d.day, (d.hour // 4)*4).strftime("%Y.%m.%d %H:00"), 
  'D1' : lambda d: d.strftime('%Y.%m.%d'),
  'W1' : lambda d: '%(year)dw%(week)02d' % {'year': d.isocalendar()[0], 'week': d.isocalendar()[0]}, 
  'MN' : lambda d: '%(year)d.%(month)02d' % {'year': d.year, 'month': d.month}
}

usage = "usage: bunch.py "+ "|".join(functions_for_periods.keys()) +" [FILE] ...\n"

def process(stream, period): #обрабатываем указанный поток (либо файл, либо stdin)
  get_start_of_period = None
  data = {}
  if period in functions_for_periods:
    get_start_of_period = functions_for_periods[period]
  else:
    print(usage)
    return None
  for line in stream:
    date, time, open, high, low, close, volume = line.split(',')
    year, month, day = map(int,date.split('.'))
    hour, minute = map(int,time.split(':'))
    open = float(open)
    high = float(high)
    low  = float(low)
    close = float(close)
    volume = int(volume)
    key = get_start_of_period(datetime(year, month, day, hour, minute))
    if key in data:
      data[key]['close'] = close
      data[key]['high']  = max(data[key]['high'], high)
      data[key]['low']   = min(data[key]['low'], low)
      data[key]['volume'] += volume
    else:
      data[key] = {
        'close' : close,
        'high'  : high,
        'low'   : low,
        'volume': volume,
        'open'  : open
      }
  return data

argc = len(sys.argv)

result = None

if   argc < 2  : #нужно указать хотя бы период
  print(usage)
  exit
elif argc == 2 :
  result = process(sys.stdin, sys.argv[1])
elif argc == 3 :
  result = process(open(sys.argv[2]), sys.argv[1])
elif argc > 3  :
  for n in range(2, argc):
    if result is None:
      result = process(open(sys.argv[n]), sys.argv[1])
    else:
      result_from_another_file = process(open(sys.argv[n]), sys.argv[1])
      if not result_from_another_file is None:
        result.update(result_from_another_file)


#print(result)

for key in result:
  print(key+','+("%(open)f,%(high)f,%(low)f,%(close)f,%(volume)d" % result[key]))