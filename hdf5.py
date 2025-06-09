import h5py
import numpy as np

def load_dataset(file_path, dataset_name):
    try:
        # Открываем файл в режиме чтения
        with h5py.File(file_path, 'r') as f:
            # Проверяем существование набора данных
            if dataset_name not in f:
                raise ValueError(f"Набор данных '{dataset_name}' не найден в файле")
            
            dataset = f[dataset_name]
                      
            # Выводим информацию о массиве
            print(f"Успешно прочитан массив: {dataset_name}")
            print(f"Размерность: {dataset.shape}")
            print(f"Тип данных: {dataset.dtype}")
            
            # Читаем весь массив в память (осторожно с большими данными!)
            return np.array(dataset)

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        exit(1)


# тест чтения файла с данными и рисование картинки
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    #  путь к HDF5 файлу
    file_path = 'densdata_higher_omt_lowres.h5'
    R = load_dataset(file_path, '/coord/R')
    Z = load_dataset(file_path, '/coord/Z')
    density = load_dataset(file_path, '/electron/density')
    potential = load_dataset(file_path, 'potential')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.pcolormesh(R, Z, density[0,:,:], cmap= 'viridis', shading='gouraud')
    ax1.set_aspect('equal')
    ax1.set_title('density')
    ax2.pcolormesh(R, Z, potential[0,:,:], cmap= 'plasma', shading='gouraud')
    ax2.set_aspect('equal')
    ax2.set_title('potential')
    fig.savefig('double_disk.png')  
    plt.show()
