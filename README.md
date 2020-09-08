# Breakout
My own implementation of Breakout using Numpy, PyGame and PyOpenGL. 
You'll probally need to `pip install` those 3 libraries in order for it to work. 

You'll probally need to `pip install` those 3 libraris in order for it to work. 

Once everything is set up, just run: 

      python3 Breakout
  
This will start the game on "pause".

- To pause/play, just hit the left-click. 
- Press R do start a new game
- Press Q to quit the game
- Press the right-click to pause the game, and press the right-click again to advance the game on 1 frame. Notice that for every click there will be a terminal output with some stats of the game. 

Extra features: 
      - At the bottom of the screen, you can see three stats
            - The first one shows the ammount of bricks already broken, and the goal ammount of bricks to be broken. 
            - The second stat is the ball speed, it goes from 1 to 100. 
            - The third stat is the ammount of lives you have, you'll always start with 3
      - The paddle speed will increase with the distance between the paddle and the mouse pointer. This is done in such a way that the paddle will "chase" your pointer on the x axis.
      - The ball speed will increase with each broken brick.
