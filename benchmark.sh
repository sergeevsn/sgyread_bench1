#!/bin/bash
echo "Поочередный запуск разных способов чтения SEG-Y файла"

time python hdr_fileread.py
time python hdr_numpy.py
time python hdr_segyio.py
time ./hdr_cpp