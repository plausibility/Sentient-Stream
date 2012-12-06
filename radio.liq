#!/usr/bin/liquidsoap
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Christopher Carter <chris@gibsonsec.org>
# Available under the MIT License.
#

base_dir = "."
sentience_dir = "./sentience"
source_pass = "hackme"

#--------------
#  Config
#--------------

set("init.daemon.pidfile.path", base_dir ^ "/radio.pid")
set("log.file", true)
set("log.file.append", true)
set("log.file.path", base_dir ^ "/radio.log")
set("log.file.perms", 644)
set("log.level", 4)
set("log.stdout", true)

#--------------
#  Functions
#--------------

def sentience()
	result = list.hd(get_process_lines(sentience_dir ^ "/build_playlist.py"))
	request.create(result)
end

# Not implemented yet.
def do_skip(s)
	source.skip(s)
	"Skipped!"
end

#--------------
#  Sources
#--------------

# If something cocks up, just play white-noise.
s_noise = amplify(0.0001, noise())
s_noise = rewrite_metadata([("artists", "Sentient Stream"), ("title", "Stream Offline")], s_noise)
s_noise = mksafe(s_noise)

# This will just re-request the song file every time. Yay!
s_sentience = request.dynamic(id="playlist", {sentience()})

# Crossfade, since it makes everything smoother.
s_sentience = crossfade(start_next=5., fade_out=1.5, fade_in=3., s_sentience)
# Skip -28dB blank if found for 3 seconds.
s_sentience = skip_blank(threshold=-28., length=3., s_sentience)

s_primary = fallback(track_sensitive=false, [s_sentience, s_noise])

output.icecast(%vorbis,
	host="localhost",
	port=8000,
	password=source_pass,
	mount="/sentience.ogg",
	url="http://change.me/sentience.ogg",
	name="CHANGEME Radio",
	genre="CHANGEME",
	description="CHANGEME!",
	public=true,
	s_primary
)