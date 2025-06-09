import numpy as np
import pandas as pd
import hdf5 

file_path = 'densdata_higher_omt_lowres.h5'
output_filename = 'out2.txt'

R = hdf5.load_dataset(file_path, '/coord/R').flatten()
Z = hdf5.load_dataset(file_path, '/coord/Z').flatten()
density = hdf5.load_dataset(file_path, '/electron/density')
potential = hdf5.load_dataset(file_path, 'potential')

n_frames, height, width = density.shape
total_elements = n_frames * height * width
print(f"Размер датасета: {n_frames}, {height}, {width}")
print(f"Всего {total_elements:,} точек...")
density = [ density[i,:,:].flatten() for i in range(n_frames)]
potential = [ potential[i,:,:].flatten() for i in range(n_frames)]

# Создаем формат для научной записи
col_width = 25
precision = 12
sci_format = "{" + f":<{col_width}.{precision}e" + '}'
print(sci_format)

with open(output_filename, 'w', buffering=1000000) as f:
        
        header = ('Frame ' 
            f"{'R':<{col_width}}"
            f"{'Z':<{col_width}}"
            f"{'density':<{col_width}}"
            f"{'potential':<{col_width}}\n")
        f.write(header)
        
        for t in range(n_frames):
            dataset = pd.DataFrame({'R': R, 'Z': Z})
            #print(dataset.head)
            df_string = dataset.to_string()
            f.write(df_string)
            print(f"\rПрогресс: {t+1}/{n_frames}", end='')
    
print(f"\nДанные сохранены в {output_filename}")