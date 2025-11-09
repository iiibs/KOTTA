# KOTTA

 A program that converts text file to music sheet.
  - KOTTA.py - program code that uses
    - text input file - with the sections, lines, chords, durations, notes, lyrics of a song
      input_structure_BNF.txt - BNF format for the text input
    - music21 library - to create MusicXml format output from text input
    - MuseScore3.exe - to create PNG outputs from the MusicXML
      https://musescore.org/en/handbook/4/command-line-usage
    - Pillow - to create a single PDF file from the individual PNG pages
  - input structure in Backhus-Naur format (BNF)
    - input_structure_BNF.txt
  - sample - a song from the EuroVision contest in 1973
    - https://www.youtube.com/watch?v=XtIm4nRWvO4 - 
      Anne-Marie David - Tu te reconnaîtras - Eurovision 1973 (HQ/HD)
      uploaded by Jack McHammer
    - tu-te-reconnaitras.txt - my interpretation of the song (may contain mistakes)
    - tu-te-reconnaitras.musicxml - Music XML format for MuseScore
    - tu-te-reconnaitras_WoB.pdf - white on black music sheet for viewing in dark mode
    - tu-te-reconnaitras_BoW.pdf - black on white music sheet for printing
