import numpy as np
import os
import sys
import hdf5 

file_path = 'densdata_higher_omt_lowres.h5'
output_filename = 'out.txt'

R = hdf5.load_dataset(file_path, '/coord/R')
Z = hdf5.load_dataset(file_path, '/coord/Z')
density = hdf5.load_dataset(file_path, '/electron/density')
potential = hdf5.load_dataset(file_path, 'potential')

n_frames, height, width = density.shape
total_elements = n_frames * height * width
print(f"Размер датасета: {n_frames}, {height}, {width}")
print(f"Всего {total_elements:,} точек...")

# Создаем формат для научной записи
col_width = 25
precision = 12
sci_format = "{" + f":<{col_width}.{precision}e" + '}'
print(sci_format)

with open(output_filename, 'w') as f:
        header = ('Frame ' 
            f"{'R':<{col_width}}"
            f"{'Z':<{col_width}}"
            f"{'density':<{col_width}}"
            f"{'potential':<{col_width}}\n")
        f.write(header)
        
        for t in range(n_frames):
            for y in range(height):
                for x in range(width):
                    line = f"{t:<6}"
                    line+= sci_format.format(R[y, x])
                    line+= sci_format.format(Z[y, x])
                    line+= sci_format.format(density[t, y, x])
                    line+= sci_format.format(potential[t, y, x])
                    f.write(line+'\n')
            print(f"\rПрогресс: {t+1}/{n_frames}", end='')
    
print(f"\nДанные сохранены в {output_filename}")