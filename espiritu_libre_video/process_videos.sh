#!/bin/bash
set -e

for file in IMG_2423 IMG_2425 IMG_2426; do
  echo "Processing $file..."
  ffmpeg -y -i assets/videos/${file}.mp4 -filter:v "setpts=2.0*PTS,minterpolate='mi_mode=blend'" -c:v libx264 -preset fast assets/videos/${file}_slow.mp4
  
  echo "Removing background for $file..."
  npx hyperframes remove-background assets/videos/${file}_slow.mp4 -o assets/videos/${file}_cutout.webm --quality balanced
done

echo "Done!"
