#!/bin/bash
killall gvfs-gphoto2-volume-monitor gvfsd-gphoto2 2>/dev/null
gphoto2 --set-config capturetarget=1

for i in {1..60}; do
  echo "📸 Taking photo $i..."
  gphoto2 --capture-image-and-download --filename="photo_$i.jpg"
  if [ $? -ne 0 ]; then
    echo "❌ Failed to capture image $i. Retrying after 3s..."
    sleep 3
    continue
  fi
  sleep 2
  curl http://10.0.2.2:8000/connect
  for i in {1..6}; do
    curl http://10.0.2.2:8000/press
    sleep 3
  done
done
curl http://10.0.2.2:8000/disconnect
