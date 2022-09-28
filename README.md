# Viterbi_Algorithm_NLP
In this project, I construct the Viterbi Algorithm used to identify the POS tags for input documents using Python

## Environment Requirements Set Up:
Prior to running the program **lz2278_hw3.py**, users need to make sure to have the packages ***pandas, numpy*** successfully set up on their computer.

## Files Paths:
In order to apply the programming models to the file, kindly noted to replace the training file path with the **file_path** variable in line 3, and the test file path with the **test_corpora** in line 4. To run the file, just type "python lz2278_hw3.py" in your terminal, and the results will be automatically saved into a file named "submission.pos".

## Training File & Test File:
Training file consists both words and identified POS tags. Each line consists of a token, a single blank, and the part-of-speech of that token using the Penn Treebank tag set. Sentence boundaries are marked by an empty line.
Test File only consist the words whose POS tags need to be predicted. We need to implement the Viterbi Model trained from the Test File to predict the POS Tags for the test file.

## Viterbi Algorithm Implementation Logic:
a. Construct the emission hash table and transition hash table used to calculate emission & transmission probability
b. Used transition hash table to construct transmission matrix that stores the probability of one tag followed by another tag
c. Construct Viterbi Algorithm function to calculate the probability for each tag being the authentic tag of each word. Take the maximum probability out, and the matched tag for this probability is our predicted tag for this word.
d. Construct a new empty file and write the predicted answers into this file and name this file "submission.pos".

## How to handle OOV words:
	a. If the OOV contains any digit, treat it as 1 CD.
	b. If the OOV ends with 's', treat it as 0.5 NNS.
	c. If the OOV begins with capital letter, treat it as 0.5 NNP
	d. If the OOV has neither digits nor letters, treat it as 0.5 ".", punctuation.
	e. Otherwise 0.0001


