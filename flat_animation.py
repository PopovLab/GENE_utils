import h5py
import numpy as np
import matp.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import sys
import hdf5 

fps = 15
dpi = 100
cmap1 = 'viridis'  # Цветовая схема для первого датасета
cmap2 = 'plasma'   # Цветовая схема для второго датасета
output_gif = 'dual_animation.gif'
file_path = 'densdata_higher_omt_lowres.h5'

R = hdf5.dataset_reader(file_path, '/coord/R')
Z = hdf5.dataset_reader(file_path, '/coord/Z')
density = hdf5.dataset_reader(file_path, '/electron/density')
potential = hdf5.dataset_reader(file_path, 'potential')


# Создание фигуры с двумя панелями
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 6), constrained_layout=True)

# Настройка первого изображения
img1 = ax1.imshow(density[0,:,:], cmap=cmap1, origin='lower')
ax1.set_title('density')
cbar1 = fig.colorbar(img1, ax=ax1)
cbar1.set_label('Интенсивность')

# Настройка второго изображения
img2 = ax2.imshow(potential[0,:,:], cmap=cmap2, origin='lower')
ax2.set_title('potential')
cbar2 = fig.colorbar(img2, ax=ax2)
cbar2.set_label('Интенсивность')

# Общая информация
n_frames = density.shape[0]
time_text = fig.suptitle(f"Кадр 0/{n_frames-1}", fontsize=14)

# Функция обновления кадра
def update(frame):
    try:
        data1 = density[frame,:,:]
        data2 = potential[frame,:,:]
        
        # Обновление изображений
        img1.set_data(data1)
        img2.set_data(data2)
        

        img1.set_clim(np.min(data1), np.max(data1))
        img2.set_clim(np.min(data2), np.max(data2))
        
        # Обновление заголовка
        time_text.set_text(f"Кадр {frame}/{n_frames-1} (Время: {frame})")
        
        return [img1, img2, time_text]
    
    except Exception as e:
        print(f"\nОшибка при обработке кадра {frame}: {str(e)}")
        sys.exit(1)

# Создание анимации
print("Создание анимации...")
step = 1 #max(1, n_frames // 100)  # Ограничение до ~100 кадров
animation = FuncAnimation(
    fig, 
    update, 
    frames=range(0, n_frames, step),
    interval=1000//fps,
    blit=True
)

# Сохранение анимации
print(f"Сохранение GIF ({n_frames//step} кадров)...")
animation.save(
    output_gif,
    writer='pillow',
    dpi=dpi,
    progress_callback=lambda i, n: print(f"\rПрогресс: {i+1}/{n} кадров", end='')
)

print(f"\nАнимация сохранена в {output_gif}")
plt.close()        