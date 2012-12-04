Sentient-Stream
===============

A semi-sentient AutoDJ like streaming system for IceCast and the likes.  
Sentient Stream uses liquidsoap (1.0.1 for testing) and Python (2.7 for testing), so you'll need those installed.

Setup
---
There are some small steps to getting Sentient Stream setup.
+ Git clone Sentient Stream somewhere.
+ Gather up all your music, sort it into genre. You want this sort of layout:

```
genres
- jazz
  - Glenn Miller
  - Fats Waller
- rock
  - Led Zeppelin
  - Dire Straights
- alt rock
  - Muse
  - Nirvana
```

+ Give build_playlist.py an __absolute__ link to that folder. (The string is called "_genre")
+ Change anything applicable in radio.liq and build_playlist.py.
	+ The source_pass, + connection variables in radio.liq
	+ The genre directory + song count in build_playlist.py
+ Make sure nothing messed up horribly. `liquidsoap --check radio.liq`
+ Run it! `liquidsoap -d radio.liq`

What's it do?
---
The idea behind Sentient Stream is this:  
When you can't man your station, what do you do? Maybe you have some sort of AutoDJ, and for those lucky few who do, that's probably sufficient.  
The power of Sentient Stream, however, is that it:
+ Will pick a random genre from your listed genre directory
+ Then from that genre, it will find all of your applicable song files, and append those to a pool.
+ It will then pick X random songs (default: 10) from that song pool.
+ Write these songs to a playlist.
+ Pop the first song from this playlist.
+ Get liquidsoap to play it.
+ liquidsoap will then request another, and python pops the next file. (This is repeated until the playlist is empty)
+ If the playlist is empty, it will be repopulated and liquidsoap will play the jingle file (if applicable).
+ Rinse and repeat.

License
---
Sentient Stream is licensed under the MIT License, so you're basically free to do whatever you like with it. Sell it, modify it, distribute it however you please!