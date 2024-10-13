import numpy as np
import os

def read_hdr(file, offset, format):
    file.seek(offset)
    return np.fromfile(file, dtype=format, count=1)[0]

### название файла для теста
FILENAME = 'npr3_gathers.sgy'

print("Чтение заголовков Python(numpy.fromfile)")

cdps = set()
cdp_z = set()

mult = 1.0

with open(FILENAME, 'rb') as f:
    ### число отсчетов из двоичного заголовка
    num_samples = read_hdr(f, 3220, '>u2')

    trace_size = (num_samples*4 + 240).astype('int64')
    num_traces = round((os.path.getsize(FILENAME) - 3600)/ trace_size)
    
    for i in range(num_traces):
        offset = 3600 + i * trace_size   
      
        if i == 0:            
            coef = read_hdr(f, offset + 68, '>i2')
            mult = float(abs(coef))**np.sign(coef)               
        cdp = read_hdr(f, offset + 20, '>u4')
        if not cdp in cdps:
            cdps.add(cdp)          
            rec_z = read_hdr(f, offset + 40, '>u4') * mult
            sou_z = read_hdr(f, offset + 44, '>u4') * mult
            cdp_z.add((rec_z + sou_z)/2)
        
print(f'CDP: мин = {min(cdps)}, макс = {max(cdps)}, всего уникальных: {len(cdps)}')
print(f'CDP_ELEV: мин = {min(cdp_z)}, макс = {max(cdp_z)}, среднее = {sum(cdp_z)/len(cdp_z)}')
