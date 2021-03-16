This is the README file for A0228402N's submission

== Python Version ==

	I'm using Python Version 3.8.5 in an Anaconda environment for this assignment

	Other packages imported that were not in the boilerplate code are as follows:
		nltk 3.5
		pandas 1.2.1
		numpy 1.19.2


== Specific Notes about this assignment ==
	In build_test_LM.py, line 170, I have set a threshold of 0.4. This threshold acts as a bar to clear. 
	For a given string, at least 40% of its 4-grams must be found in the language model in order to be considered a valid string in the predicted language
	The rationale is to try and capture the strings that do not belong to any of ["malaysian", "indonesian", "tamil"] and classify them as "others"	

	This works for the provided train/test sets. However it might result in some misclassifications for the actual test set used by evaluators. 
	Please amend this threshold accordingly if performance seems worse than expected! 

	Advised to lower the threshold if facing poor evaluation results 

	
	This assignment was executed through console, with the following commands as provided in the assignment brief
		python build_test_LM.py -b input.train.txt -t input.test.txt -o input.predict.txt
		python eval.py input.predict.txt input.correct.txt	
	Please adapt to your environment accordingly
	

== General Notes about this assignment ==

	The entirety of my work and my program can be found in the build_test_LM.py file.
	There are two main parts to the code: the build_LM() and test_LM() functions

	build_LM() function takes in an input file name and creates a language model based on the input file.
	The pseudocode is as such:
		1. Open input file
		2. Process contents - split label and string, then clean the string rudimentarily
			2a. Perform simple conversion to lowercase to standardize input
			2b. Strip terminal end-line marker ("\n")
		3. Create a vocabulary and a language model 
		For every string:
			3a. nltk.ngrams() function is used to split input strings into character level 4-grams
				4-grams generated will not have padding for start and stop. Given that we are doing character level 4-grams, 
				it is not very meaningful to discover which sets of characters tend to start the string. It might be 
				more meaningful if it was at a word level instead
			3b. Every 4-gram generated will be added to the vocabulary. The count does not matter here, only the existence
			3c. Every 4-gram generated will also be added to the respective languages' language_model. the count matters
		
		Once every string has been processed:
			3d. Perform add-one smoothing on the language_model using the vocabulary
			3e. Perform conversion from count to probability for the language model
		4. Return the language model

	test_LM() function takes in an input file, output file, and the language model generated from build_LM(). 
	The input file in this case is a test file. The output file will be generated 
	The pseudocode is as such:
		1. Open input file
		2. Process contents - clean the string rudimentarily
			2a. Perform simple conversion to lowercase to standardize input
			2b. Strip terminal end-line marker ("\n")
		3. Perform 4-gram conversion on the strings
		4. Match the 4-grams against the language_model from build_LM()
		For each 4-gram in the string:
			For each of the languages in the language_model:
				4a. Check if the 4-gram exists in the language model. 
					If exists, pull out the associated probability 
					If not exists, set probability to 1
				4b. Sum up the log-probability with the probability that we obtain in 4a. 
					Note that log(1) = 0, hence this is why if we cannot find an associated probability, we set it as 1 so it does not affect our sum
			
		For each string: 
			4c. Select the maximum log-probability obtained from 4b for each of the three languages for a given string's 4-grams
				Set the corresponding language as the predicted language for the string
			4d. Perform sanity checks to see if there is cause to reject the prediction. If rejected, set the prediction to "other"
				If the log-probability is too positive (close to zero), then we reject because it likely means that there are no matches 
				If there are fewer than 40% matches of the 4-grams in the string are found in the language model then we also reject
				because this indicates low confidence

		5. Generate the output file in the same format as input.train.txt, with a space separating the prediction from the string
		

== Files included with this submission ==

	Amended files from boilerplate code
		build_test_LM.py	included three new library imports, and filled in working code for the build_LM() and test_LM() functions
		README.txt		amended README 
	New files generated
		input.predict.txt	contains predictions after running build_test_LM.py and eval.py
	Untouched files from boilerplate code
		CS3245-hw1-check	
		eval.py			
		input.correct.txt
		input.test.txt
		input.train.txt



== Statement of individual work ==

	Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

	[x] I, A0228402N certify that I have followed the CS 3245 Information
	Retrieval class guidelines for homework assignments.  In particular, I
	expressly vow that I have followed the Facebook rule in discussing
	with others in doing the assignment and did not take notes (digital or
	printed) from the discussions.  

	[ ] I, A0228402N did not follow the class rules regarding homework
	assignment, because of the following reason:

	NA

	I suggest that I should be graded as follows:

	As per normal

== References ==
	
	NTU CZ4045 lecture slides	referenced for a refresher on Natural Language Processing, specifically on Language Models
					unable to share this because of school confidentiality policy
	https://stackoverflow.com/ 	referenced for some syntax 
	http://www.nltk.org/index.html	to understand how nltk works

	There was no collaboration with other students
