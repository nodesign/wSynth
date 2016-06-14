#!/bin/sh

# Create virtual midi device, index 0 is mu default sound card, index 1 is free
# it will create /dev/midi1 device
modprobe snd-virmidi snd_index=1

# launch websocket server on the port 8080
websocketd --port=8080 ./wSynthGlue/wSynthGlue &

# launch stk eguitare example and listen to the port 2 (virtual midi)
./stk/projects/eguitar/eguitar -or -im 2