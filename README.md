# VLCControl

small Utility to control VLC-PLayer via its HTTP-Server

---
## Features

- Simple Player Controls

  (play, pause, next, previous)

- Title and Artist lookup

	(with simple substitution for files with no artist tag but **"artist - title"** in the filename)

- Volume control and display

<img src="https://github.com/acereca/VLCControl/raw/master/res/example.PNG"></img>

---
## Install

### Requirements

	- Python 3+
	- VLC-Player

### Setup

1. in VLC do the following:

 - Tools > Preferences:

    select Show Settings: **All**

 - Interface > Main interfaces:

	  enable **Web**

 - Interface > Main interface > Lua:

	- LuaInterface: **http**

	- Lua-HTTP > Password: **abcde**

	  (or something else, we need it later)


2. now open the **config.json** in the VLCControl folder and change

	 ```json
   "password": "abcde"
   ```

   to the password which we set in advance (if the password was different from abcde)

---
## Usage

1. Run **vlcc.pyw**
