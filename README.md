# autobleemer
binds bleem to a burned cd-r automagically

## how do i use?
clone this repo (use the code dropdown and click `download ZIP` or with `git clone`)

go to the ASPI folder

click on the `1` folder

copy `wnaspi32.dll` to `WINDOWS/SysWOW64`, if this worked, you can run `aspichk.exe` where `WNASPI32.DLL` should be listed. (screenshot pending)

if it did not work, repeat the process with each folder until it does

if it did, you can now exit that program

now go to the `XDuplicator` folder and run the program of the same name

in the `settings` tab, select your reader/writer. click the following checkbox: `leave session open`

go to the `write` tab, and select a `.cue` file where the audio tracks have been removed, for example:
```
FILE "Clock Tower - The First Fear (Track 1).bin" BINARY
  TRACK 01 MODE2/2352
    INDEX 01 00:00:00
FILE "Clock Tower - The First Fear (Track 2).bin" BINARY
  TRACK 02 AUDIO
    INDEX 00 00:00:00
    INDEX 01 00:02:00
```
becomes
```
FILE "Clock Tower - The First Fear (Track 1).bin" BINARY
  TRACK 01 MODE2/2352
    INDEX 01 00:00:00
```
you can edit this in notepad.

write this `.cue` file to your disc, then after successful competion, exit the program.

after this, navigate to the folder root and run `python autobleemer.py`. the program will tell you if anything fails, but if nothing does; then 

you'll see a success message:

(screenshot here)

## thanks
OVERRIDE (for the original bleemcast selfboot bash script)
burner0 (for ippatch.exe)
Jorg Schilling and others (for cdrtools)
Andreas Mueller and others (for cdrdao)
Mariposa (for cdrdao interface `XDuplicator`)
SMiTH (for updating the bleemcast selfboot script and methods, and the version of the bash script this python script is based on)
