The goal of this project is to get more experience with the following:  
* Pygame
* Writing documentation
* Mypy
* Black (formatting)
* Testing
* GitHub Actions
* General code structure

This being my first pygame project. I followed this [youtube video](https://www.youtube.com/watch?v=Qf3-aDXG8q4)
to get a baseline project started.

Planned:
* [x] Class-ify the ball, player, and opponent code.
* [x] Randomize ball start direction on reset
* [x] Build out file structure
* [x] Scoreboard
  * [x] Code cleanup/class-ify code.
* [ ] Sounds
  * [ ] Ball bounce sound
  * [ ] Ball duplicate sound?
  * [ ] Player score sound
  * [ ] Opponent score sound is different?
  * [ ] Background music. Change/scale with player score?
  * [ ] Certain environmental hazards
    * [ ] On arrival
    * [ ] While they're in play
    * [ ] On dissipation
  * [ ] Powerup/Abilities
    * [ ] On arrival/Cool down complete
    * [ ] On use
* [x] Scaling opponent difficulty
  * [x] Scales with score (1 extra ball per 10 player points. 1% movement speed per player point)
  * [x] Speed up movement (to a max)
  * [x] Duplicates n number of balls based on player score (1 extra ball for every 10 points)
    * [x] Duplicated balls have non-default speeds. (Can have slow or fast balls)
* [ ] Startup Screen
  * [ ] Play - Just start the default game
  * [ ] Maybe a couple of options for game mode? Endless, Standard (200 pts), Crazytime?
  * [ ] Settings - To adjust the initial ball, opponent, player, environment settings
  * [ ] Instructions - To explain difficulty settings, powerups/abilities, and terrain hazards.
* Environmental Hazards, based on difficulty, affects both sides.
  * [ ] Obstacles might be generated that either persist for n seconds, or require being hit n times to dissipate
    * Different shapes (square, circle, triangle) to cause the ball to bounce less predictably.
  * [ ] Speed/Slow zones for the ball. 
  * [ ] Portals that teleport the ball, either from portal to portal, or an entrance and the exit is random (within reason)
  * [ ] Stationary Gravity Sphere
    * A sphere or point that pulls on the ball
    * Not strong enough to hold the ball
* [ ] 2 player mode
* Abilities
  * [ ] Random powerups on the field,
  * [ ] A popup appears and the user can select a power, every so many points.
    * [ ] Popup selections might include downside to selecting certain ability?
      * Ie: While having access to (but not using) the sticky paddle, your paddle speed is reduced by 10%. Speed reduction is reset when you use the sticky paddle ability (which either goes on cooldown or goes away.)
  * [ ] Abilities might go on cooldown, 
  * [ ] or be one time uses.
  * [ ] Reverse Paddle
    * Invert the interactive zone of the player's paddle, giving an advantage, if used correctly.
  * [ ] Multi-Ball
    * Generate additional balls, either all at once, or per bounce for a set number of bounces?
  * [ ] Sticky Paddle
    * Allow the player to catch the ball, releasing it at their leisure. (random direction?)
  * [ ] Stop/Slow Time [Ball/Opponent]
    * Stop/Slows the ball or opponent, but leaving the player unaffected.
  * [ ] Speed Boost
    * Give the player's paddle a speed boost for n seconds.
  * [ ] Shield Wall
    * Throw up a wall of tiles at the center line, trapping the ball on the respective side. Each tile requires n hits to dissipate.
    * The whole wall may only last 30 seconds or so.
  * [ ] Swarm Mode
    * Instead of having one 140px long paddle, break up into 14 10px long paddles.
    * The user controls one of the micro-paddles, and the other paddles trail after. Staying relatively spread out.
    * The further a swarm paddle is from the main paddle, the faster it moves with a set acceleration (speed up and down). So that if it's far enough away, could appear to slingshot past the main temporarily.
    * Main paddle moves faster in this mode? With the swarm speed relative to it's distance from the main.
    * Swarm slowly spreads to either side of the main paddle when stationary?
  * [ ] Path Prediction
    * Simply show a dotted/dashed line for where the ball is going.
* Testing
* [ ] Write tests
  

#### Known Bugs:
* [x] If the ball hits the top or bottom of the paddle in just the right spot, it will bounce inside the paddle, for the length of the paddle.
* [x] If the ball spawns on the top or bottom pixel, it becomes stuck at that y level.