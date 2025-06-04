# OMR Checker

## EIM


1. print PDF with each variant, and prepare the .csv with answer key, as in the examples
   - Marker circles should be all visible; circle should not interfere with bubbles
   - CropOnMarkers.py "midh, midw = h1 // 5, w1 // 2" or 
      "midh, midw = h1 // 4, w1 // 2" depending on where in the page the markers are
   - use A4, "fit to page" when printing 
   - check one printed page with "main.py --setLayout" to see if bubbles are properly centered 
   
2. scan using 150dp, only one side, and save as JPEGs. Sanity check - number of pages fed should match what is reported.
	- Best: iscan(Image Scan! from Epson): 150dpi, BW document, Image Controls Contrast +50% 
		* use the flatbed (more reliable), with the page flush in the upper/right corner (near hinge)
		* ADF single sided, B&W - does better in separating pages from feeder
    - Document Scanner (in Ubuntu) seetings: all pages from feeder, Text, 
	    * ADF: face up, head first
		* ADF is unreliable in separating pages 

3. Prepare environment, if necessary. Cleanup. 
```
rm -rf .venv 
python3 -m venv .venv 
source .venv/bin/activate
mkdir res
```

4. Install the requirements:
```
python3 -m pip install --user opencv-python
python3 -m pip install --user rich
python3 -m pip install --user opencv-contrib-python
python3 -m pip install --user -r requirements.txt
```

5. The default run scans fr every .jpg under 'inputs'. Alternative directories 
can be given with '-i'. For a given set, look into its directory in `samples`. For
example, for number 1 we will use `samples/eim_n1`.
5a. Copy the scanned documents to `samples/eim_n1/nr1`

6. Update the response sheet accordingly in `samples/eim_n1/nr1/answer_key.csv`
6.a evaluation.json should contain for example for 10% penalty answers:
	"DEFAULT": { "correct": "1", "incorrect": "-0.1", "unmarked": "0" },
	or if certain answers need to be ignored if all answers are wrong: 
	"MISTAKE13": {
	    "questions": ["q13"],
	    "marking": { "correct": 0, "incorrect": 0, "unmarked": 0 }
	},
6b. check questions & bubbles positions
	`python3 main.py --setLayout -i samples/eim_n1`
6c. adjust `eim_n1/template.json` and rerun 4b. For vertical spaced
A/B/C/D/E options, bubblesGap is the vertical space, and labelsGap is
the horizontal spacing between questions

7. Clean prev output 
   `rm -rf outputs/nr1`

8. Run the grading tool `python3 main.py -i samples/eim_n1 | tee ./log_n1.log`.

8a. Sanity check1: Verify that the result in `Total file(s) processed`
matches the number of phyisical documents

8b. check output with an image viewer in outputs/nr1/CheckedOMRs


8c. You will find the grades in `outputs/nr1/Results/Results.csv`.

> Note, it will actually be called `Results_{Time}.csv`

8d. `cat outputs/nr1/Manual/MultiMarkedFiles.csv` - grading manual. 
Add line in /Results/Results.csv with actual filenames and scores before step 7 

8e. Check `outputs/nr1/Manual/ErrorFiles` for any page that has not been processed


9. To add the grades to the test images: `python3 add_grade.py outputs/nr1/Results/Results{Time}.csv`
9a. check add_grade.py for posible grade adjustment/weighting

10. You will find the processed images with grades in `res/`

