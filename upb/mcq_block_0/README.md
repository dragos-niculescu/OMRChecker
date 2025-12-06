
This configuration only looks for the Cassette labeled with 'Nr' and extracts the actual variant A..F marked.

template.json should be properly set so that the cassette is parsed correctly. Only
block "MCQ_Block_0" is used to read the multiple choice field Nr. 

It is used internally by run_upb.py to classify files into directories based on their
variant/Nr

