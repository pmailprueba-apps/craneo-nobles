#!/bin/bash
cd /Volumes/MiDisco1TB/Proyectos/37-craneo-nobles/assets

# Crear carpeta temporal
mkdir -p trace_temp

# Probar umbrales del 35% al 70%
for thresh in 35 40 45 50 55 60 65 70; do
  # Recortar, pasar a escala de grises, aplicar umbral, negar (invertir) para que el logo sea negro y guardar en BMP
  magick original_design.jpg -crop 821x530+0+80 -colorspace gray -threshold ${thresh}% -negate trace_temp/skull_${thresh}.bmp
  
  # Vectorizar con potrace
  potrace -s -o trace_temp/skull_${thresh}.svg trace_temp/skull_${thresh}.bmp
  
  # Convertir el SVG resultante a PNG para poder visualizarlo con el agente
  magick -background none trace_temp/skull_${thresh}.svg -resize 400x trace_temp/skull_${thresh}.png
done

echo "Proceso completado. Archivos generados en assets/trace_temp/"
