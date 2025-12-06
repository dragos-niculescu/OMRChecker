# OMR Checker

### EIM

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
		* ADF can be convinced to properly scan from the top if the stack 
		is tucked in just after the scanner finished a scan swipe. 
    - Document Scanner (in Ubuntu) seetings: all pages from feeder, Text, ADF: face up, head first
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


#### SETUP of the MCQ blocks  

5. The default run scans for every .jpg under 'inputs/partial'. Alternative directories can be given with '-i'. Put some jpegs in './inputs/partial' and add all files from 'upb/mcq_block_012'. This is the standard running of original OMRChecker

5b. check questions & bubbles positions
	`python3 main.py --setLayout -i inputs/partial`
5c. adjust `template.json` and rerun 5b. For vertical spaced
A/B/C/D/E options, bubblesGap is the vertical space, and labelsGap is
the horizontal spacing between questions. When content, update 'upb/mcq_block_012'
with the new template that will be used for all variants. 

5d. Alternatively, update directories 'upb/mcq_block_0' and 'upb/mcq_block_012' based on a sample from 'samples/upb'. 
Block 'mcq_block_0' is the first block and is used to classify the exam in an 
output directory. Block 'mcq_block_1' and 'mcq_block_2' are for actual test questions.


6. Update the response sheet accordingly in `upb/mcq_block_012/answer_key.csv` 
using multiple columns, one for each variant A..F 
Check the csv file that it doesn't have any spaces, and all fields are case sensitive (Nr, A, q1) 

6.a evaluation.json should contain for example for 10% penalty answers:
```json
	"DEFAULT": { "correct": "1", "incorrect": "-0.1", "unmarked": "0" },
	or if certain answers need to be ignored if all answers are wrong: 
	"MISTAKE13": {
	    "questions": ["q13"],
	    "marking": { "correct": 0, "incorrect": 0, "unmarked": 0 }
	},
```

#### Running 

7. Bring all jpegs to be graded in './inputs/partial'. 

7a. classify images to directories (takes a while)
    `python3 upb/classify.py > classify.log`
    Populates directories 'partial/A..F' with classified jpegs, and with 
    proper evaluation.json and answer_key.csv specific to the variant    

7b. Clean prev output 
   `rm -rf outputs/* res/*`

7c. 'python3 main.py -i inputs/[A-F] | tee ./grading.log'


#### Sanity Checks 

8a. Sanity check1: Verify that the result in `Total file(s) processed`
matches the number of phyisical documents
`grep 'Total file' ./grading.log`


8b. check output with an image viewer in outputs/CheckedOMRs


8c. You will find the grades in `outputs/Results/Results.csv`.

> Note, it will actually be called `Results_{Time}.csv` one for each variant 

8d. `cat outputs/Manual/MultiMarkedFiles.csv` - grading manual. 
Add line in /Results/Results.csv with actual filenames and scores before step 7 

8e. Check `outputs/Manual/ErrorFiles` for any page that has not been processed


#### Grades with names
9. To add the grades to the test images: `python3 add_grade.py outputs/Results/Results*.csv | tee ./scoring.log`
9a. check add_grade.py for posible grade adjustment/weighting

10. You will find the processed images with grades in `res/`


