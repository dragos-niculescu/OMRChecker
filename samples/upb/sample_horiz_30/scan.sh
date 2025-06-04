echo "################## Scanning ###################"
scanimage \
--resolution 150dpi \
--scan-area Maximum \
--source "Automatic Document Feeder" \
	  --batch=scan_%03d.jpg --format=jpeg \
-b \
	  --mode Gray \
	  --brightness 20 \
	  --device-name "epkowa:interpreter:001:006"


#-y 297 -x 210 
#--source "Flatbed" \

