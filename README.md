
Tetris Game using Expectimax and Neural Networks.


1. Installation/Dependencies

        pip3 install pandas  
        pip3 install numpy  
        pip3 install matplotlib  
        pip3 install torch  
        pip3 install scipy  

2.  To run the interactive domain :

        Run python3 play.py on terminal.
        Select problem size.
        Select the player type: 1. Baseline AI  2. Expectimax (Heuristic)  3. NN  
        While playing baseline and expectimax AI please press enter since the code pauses every move and waits for input.

        Heuristic Tree Experiments:  
        We have also included the experiment files that we used to test the types with different shape probabilities.  
        To run these experiments we have put the test experiment data for different experiments in experiment_test_data.txt and please replace the self.shapeProb with the test data values of the respective                  experiment and run by experimentN.py where N is from 1 tp 4.


3.  References :

        https://web.stanford.edu/class/archive/cs/cs221/cs221.1192/2018/restricted/posters/thawsitt/poster.pdf  
        We took the shapes for the Tetris game from  #Definition for Tetris shapes:https://en.wikipedia.org/wiki/Tetromino  
        https://inst.eecs.berkeley.edu/~cs188/sp22/assets/slides/Lecture6.pdf#page=13  
        https://inst.eecs.berkeley.edu/~cs188/fa19/assets/slides/archive/SP18-CS188%20Lecture%207%20--%20Expectimax%20Search%20and%20Utilities.pdf  
