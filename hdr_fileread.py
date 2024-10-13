import numpy as np
import struct 
import os

def read_hdr(file, offset, format, size):
    file.seek(offset)
    bytes = f.read(size)
    return struct.unpack(format, bytes)[0]

### название файла для теста
FILENAME = 'npr3_gathers.sgy'

print("Чтение заголовков Python(file.read + struct.unpack)")

cdps = set()
cdp_z = set()

mult = 1.0

with open(FILENAME, 'rb') as f:
    ### число отсчетов из двоичного заголовка
    num_samples = read_hdr(f, 3220, '>h', 2)

    trace_size = (num_samples*4 + 240)
    num_traces = round((os.path.getsize(FILENAME) - 3600)/ trace_size) 
    
    for i in range(num_traces):
        offset = 3600 + i * trace_size   
      
        if i == 0:            
            coef = read_hdr(f, offset + 68, '>h', 2)
            mult = float(abs(coef))**np.sign(coef)        
                
        cdp = read_hdr(f, offset + 20, '>I', 4)       
        if not cdp in cdps:
            cdps.add(cdp)          
            rec_z = read_hdr(f, offset + 40, '>i', 4) * mult
            sou_z = read_hdr(f, offset + 44, '>i', 4) * mult            
            cdp_z.add((rec_z + sou_z)/2)
        
print(f'CDP: мин = {min(cdps)}, макс = {max(cdps)}, всего уникальных: {len(cdps)}')
print(f'CDP_ELEV: мин = {min(cdp_z)}, макс = {max(cdp_z)}, среднее = {sum(cdp_z)/len(cdp_z)}')
