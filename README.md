# autobleemer
binds bleem to a burned cd-r automagically

## how to use
1. clone this repo (use the code dropdown and click `download ZIP` or with `git clone` using [git](https://git-scm.com/))
2. [install python and add to PATH](https://www.python.org/downloads/)
3. go to the `ASPI` folder
4. click on the `1` folder
5. copy `wnaspi32.dll` to `WINDOWS/SysWOW64`, if this worked, you can run `aspichk.exe` where `WNASPI32.DLL` should be listed. if it did not work, repeat the process with each folder until it does. if it did, you can now exit that program
6. now go to the `XDuplicator` folder and run the program of the same name
7. in the `settings` tab, select your reader/writer. click the following checkbox: `leave session open`
8. go to the `write` tab, and select a `.cue` file where the audio tracks have been removed, for example:
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

9. write this `.cue` file to your disc, then after successful competion, exit the program.
10. after this, navigate to the folder root and run `python autobleemer.py`. the program will tell you if anything fails, but if nothing does; you'll see the program do it's thing. a successful bleem is noted with `"successfully bleemed!you're all done! happy bleem!castin'.."`

## why use this instead of the original bash script?
in the original scripts, you had to use a separate bash script to find what drive to use, and then edit the main script with that. in this python script, we do that all of that for you.

really, the thing that takes up the most amount of steps/manual time is the initial dll tomfoolery. if there was a way to avoid that altogether, then that + this script would be the ideal way to do things.. but for now, this is the fastest/most reliable way to create bleemed games.

eventually, there will be support for automatically making cdi files... we'll see.

## thanks
- OVERRIDE (for the original bleemcast selfboot bash script)
- burner0 (for ippatch.exe)
- Jorg Schilling and others (for cdrtools)
- Andreas Mueller and others (for cdrdao)
- Mariposa (for cdrdao interface `XDuplicator`)
- SMiTH (for updating the bleemcast selfboot script and methods, and the version of the bash script this python script is based on)

