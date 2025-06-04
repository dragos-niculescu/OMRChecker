
# scanner=$(scanimage -L| grep epkowa| awk '{print $2}' | tr -d "[\`\']")

echo "################## Scanning ###################"
scanimage \
    --scan-area A4 \
    -x 210mm \
    -y 297mm \
--source "Flatbed" \
    --batch="scan_%03d.jpg" --format jpeg \
	  --mode Gray \
	  --brightness 20 \
	  --resolution "150dpi" \
	  --device-name "epkowa:interpreter:001:013"


#-y 297 -x 210 
#--source "Automatic Document Feeder" \

