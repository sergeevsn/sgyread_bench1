import segyio
import numpy as np
import tqdm

### название файла для теста
FILENAME = 'npr3_gathers.sgy'

print("Чтение заголовков Python(SEGYIO)")

cdps = set()
cdp_z = set()

with segyio.open(FILENAME, strict=False) as f:
    f.mmap()
    ### множитель для превышений
    mult = float(abs(f.header[0][69]))**np.sign(f.header[0][69]) 
    
    ### цикл по всем заголовкам
    for h in f.header:  
        cdp = h[21]
        rec_z = h[41] * mult
        sou_z = h[45] * mult     
        if not cdp in cdps:
            cdps.add(cdp)
            cdp_z.add((rec_z + sou_z)/2)


print(f'CDP: мин = {min(cdps)}, макс = {max(cdps)}, всего уникальных: {len(cdps)}')
print(f'CDP_ELEV: мин = {min(cdp_z)}, макс = {max(cdp_z)}, среднее = {sum(cdp_z)/len(cdp_z)}')