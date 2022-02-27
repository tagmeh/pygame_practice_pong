The goal of this project is to get more experience with the following:  
* Pygame
* Writing documentation
* Mypy
* Black (formatting)
* Testing
* GitHub Actions
* General code structure

Initially, I'm following a [youtube video](https://www.youtube.com/watch?v=Qf3-aDXG8q4), 
but beyond that, it's all custom code.

Planned:
* [ ] Sounds
* [ ] Scoreboard
* [ ] Scaling opponent difficulty
  * [ ] Scales with score
  * [ ] Speed up movement (to a max)
  * [ ] randomly generate n number of balls
    * [ ] Balls might be varied in their speed
* Environmental Hazards, based on difficulty, affects both sides.
  * [ ] Obstacles might be generated that either persist for n seconds, or require being hit n times to dissipate
  * [ ] Speed/Slow zones for the ball. 
  * [ ] Portals that teleport the ball, either from portal to portal, or an entrance and the exit is random (within reason)
* [ ] 2 player mode
* Triggerable Abilities
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