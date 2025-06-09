import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import sys
import hdf5 

fps = 15
dpi = 100
cmap1 = 'viridis'  # Цветовая схема для первого датасета
cmap2 = 'plasma'   # Цветовая схема для второго датасета

file_path = 'densdata_higher_omt_lowres.h5'

R = hdf5.load_dataset(file_path, '/coord/R')
Z = hdf5.load_dataset(file_path, '/coord/Z')
dataset = hdf5.load_dataset(file_path, '/electron/density')
#dataset = hdf5.load_dataset(file_path, 'potential')
title = 'density'
output_gif = f'{title}_disk.gif'
# Получаем глобальные диапазоны для стабильной цветовой карты (опционально)
try:
    global_min1 = np.min(dataset)
    global_max1 = np.max(dataset)
    use_global_scale = True
except:
    use_global_scale = False
    print("Не удалось вычислить глобальные диапазоны, будет использоваться динамическое масштабирование")

fig, ax1 = plt.subplots(figsize=(7, 6))
fig.subplots_adjust(right=0.99,wspace=0.01, hspace=0.01)

n_frames = dataset.shape[0]

img1 = ax1.pcolormesh(R, Z, dataset[0,:,:], cmap=cmap1, shading='gouraud')
ax1.set_title(f"{title} 0/{n_frames-1}", fontsize=14)
ax1.set_aspect('equal')
ax1.set_ylabel('Z(m)')
ax1.set_xlabel('R(m)')
cbar1 = fig.colorbar(img1, ax=ax1)
#cbar1.set_label('Интенсивность')

# frame update
def update(frame):
    data1 = dataset[frame,:,:]
    img1.set_array(data1)
    if use_global_scale:
        img1.set_clim(global_min1, global_max1)
    else:
        img1.set_clim(np.min(data1), np.max(data1))
    ax1.set_title(f"{title} {frame}/{n_frames-1}", fontsize=14)
    return [img1]


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