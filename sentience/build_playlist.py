#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Christopher Carter <chris@gibsonsec.org>
# Available under the MIT License.
#
import os
import sys
import re
import random

"""
The idea here is that:
+ This will recurse the "genre dir", finding all genres (folders), and picking a random one.
+ It will then find all music files in that genre, and return a random selection.
+ The script will generate a "playlist" file with the songs in it.
+ It will pop the first out of this list, and print that.
+ When the playlist is empty, it will generate a new playlist, and print the jingle file.
+ This means if the song count is 10, it will play ten songs, then a jingle, followed by ten new songs.
"""

# We'll play .mp3, .m4a, .ogg, .flac (change if you have more/less liquidsoap plugins)
_reg_file = re.compile("\\.(?:mp3|m4a|ogg|flac)$", re.I)
_genre = "/path/to/genre/folder"
_playlist = "./playlist.pls" # Relative to script calling dir, since it doesn't matter.
_jingle = "/path/to/jingle.ogg" # Doesn't have to be an ogg!
_song_count = 10

def genre_pool_():
	pool = []
	for genre in os.listdir(_genre):
		if not os.path.isdir(os.path.join(_genre, genre)):
			continue
		pool.append(genre)
	return pool

def song_pool_(genre):
	genre = os.path.join(_genre, genre)
	songs = []
	pool = []
	for root, dirs, files in os.walk(genre):
		for file_ in files:
			if _reg_file.search(file_):
				songs.append(os.path.join(root, file_))
	random.shuffle(songs)
	if len(songs) < _song_count:
		return songs
	while len(pool) < _song_count:
		song = random.choice(songs)
		if song in pool:
			continue
		pool.append(song)
	random.shuffle(pool)
	return pool[:_song_count]

def make_playlist():
	genre_pool = genre_pool_()
	genre = os.path.join(_genre, random.choice(genre_pool))
	song_pool = song_pool_(genre)
	try:
		with open(_playlist, 'wb') as f:
			f.write("\n".join(song_pool))
	except IOError as e:
		raise

def fetch_next():
	if not os.path.isfile(_playlist):
		make_playlist()
		return fetch_next()

	try:
		lines = []
		with open(_playlist, 'rb') as f:
			lines = [line.strip() for line in f.readlines()]
		
		if len(lines) == 0:
			make_playlist()
			return _jingle
		
		song = lines.pop(0)
		with open(_playlist, 'wb') as f:
			f.write("\n".join(lines))
		return song

	except IOError as e:
		raise

print fetch_next()