# VLCControl

small Utility to control VLC-PLayer via its HTTP-Server

## Install

### Requirements

	- Python 3+
	- VLC-Player

### Setup

	1.

	2. in VLC do the following:

		- Tools > Preferences:
	   select Show Settings: All

		 - Interface > Main interfaces:
	   enable "Web"

		 - Interface > Main interface > Lua:
	   LuaInterface: http
		 Lua-HTTP > Password: abcde
		 (or something else, we need it later)


   2. now open the config.json in the VLCControl folder and change

	  > "password":"abcde"

   to the password which we set in advance (if the password was different from abcde)

###
