### Chinese Checkers: An Exploration

# Introduction

I've liked this game since I was a kid and recently rediscovered an interest in it. It's simple to understand but complex to play well. I love the simplicity of the star shaped, hexagonal grid-based board, the pieces that move across it, and the rules. The geometric patterns that emerge during play are aesthetically pleasing, and the goal is simple: move all of your pieces into the opposing triangle from your own starting triangle before your opponents. Incidentially, I've just last semester taken an introductory artificial intelligence course, and a portion of it was devoted to game-playing agents, search trees, and related algorithms. I've also harbored a casual interest in reinforcement learning since DeepMind revealed AlphaStar in 2019, but never gotten the chance to engage with it hands-on. 

# Technical Introduction

At the end of the day, turn-based board games are just state space graphs (all possible board states are represented by nodes and all the moves that take your between board states are represented by edges). Certain nodes correspond to goal states, and these nodes are different for each player.

to be continued
