Task 2: Learning With Support Vector Machines

Grid search was run to find the best C and Gamma parameters for all three representations, the graphs can be found in the 'graphs' subfolder along with an image represnting the accuracy vs bins used for all 3 representations. 

Best values obtained along with Accuracy :

RAD : C - 0.03125 , Gamma - 1.0 , Accuracy - 56.3%

HJPD : C - 2.0 , Gamma - 0.125 , Accuracy - 72.9%

HOD : C - 8 , Gamma - 0.125 , Accuracy - 58.4% 

__________________________________________________________________________


The highest accuray obtained was using HJPD , which used 10 bins. RAD used 10 bins as well and HOD used 8 bins.
The data for HOD which used a different number of bins from RAD and HJPD needed to be scaled before training.

After installing Lib SVM using the same instructions from the website , the code can be run from the command line

The data for all 3 representaions are converted into the format for libsvm , the code is reformat_data.py and the files can be found under the 'formatted' subfolder

The code for the C-SVM can be found in learning.py 

The prediction files can also be found under 'formatted'
_________________________________________________________________________

To run the code from command line specifying which representaion to use:

python part2_main.py [rad/hjpd/hod]

Example format running with RAD :

python part2_main.py rad



