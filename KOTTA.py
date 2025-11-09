from music21 import stream,note,chord,meter,key,tempo,harmony,metadata,duration,expressions
import re
import os

def text_to_musicxml(txt_path,musicxml_path):

 with open(txt_path,'r',encoding='utf-8') as f:
  lines=[line.rstrip('\n') for line in f]

 # Parse header
 i=0
 title=lines[i].strip();i+=1
 capo=lines[i].strip();i+=1
 key_name=lines[i].strip();key_name="C"if key_name=="C major" else key_name;i+=1
 mtr=lines[i].strip();i+=1
 bpm=lines[i].strip();i+=1
 # After reading them in, omit the header lines: title, capo, beats-per-minute and empty line
 n_header_lines=i+1
 lines=lines[n_header_lines:]

 sections=[]

 i_line=0
 while i_line<len(lines):
  line=lines[i_line].strip()

  section_name=lines[i_line].strip();i_line+=1

  # Section lines
  i_section=0
  b_new_section=False
  section_lines=[]
  while b_new_section==False and i_line<len(lines) and lines[i_line].strip():

   # Process one line of the song
   chords=lines[i_line];i_line+=1
   durations=lines[i_line];i_line+=1
   notes=lines[i_line];i_line+=1

   # Collect all lyrics lines until an empty line
   lyrics=[]
   n_lyrics=0
   while i_line<len(lines) and lines[i_line].strip():
    lyrics.append(lines[i_line]);i_line+=1
    n_lyrics+=1

   # Build section line and append to section_lines array
   section_lines.append({
    'chords': chords,
    'durations': durations,
    'notes': notes,
    'lyrics': lyrics
   })

   # Check if end of section (either there is no more line, or the next line is a new section)
   if i_line+1>=len(lines) or lines[i_line+1][0]!=' ':
    i_section+=1
    b_new_section=True
    sections.append({
     'name': section_name,
     'lines': section_lines,
    })
   i_line+=1

 # Map of durations 
 note_durations_map={
  # Note durations
  'lo.': 3.0 , # 3.00 / 4   12 / 16   6 / 8
  'lo':  2.0 , # 2.00 / 4   8 / 16   4 / 8
  'l.':  1.5 , # 1.50 / 4   6 / 16   3 / 8
  'l' :  1.0 , # 1.00 / 4   4 / 16   2 / 8   ta
  '.' :  0.5 , # 0.50 / 4   2 / 16   1 / 8   ti
  ':' :  0.25, # 0.25 / 4   1 / 16
 }
 rest_durations_map={
  # Rest durations
  '_' : 4.0, # 4.0 / 4   16 / 16   8 / 8
  '-' : 2.0, # 2.0 / 4    8 / 16   4 / 8
  'z' : 1.0, # 1.0 / 4    4 / 16   2 / 8
  'p' : 0.5, # 0.5 / 4    2 / 16   1 / 8
 }

 # Build song structure in MusicXML
 score=stream.Score()
 score.metadata=metadata.Metadata()
 score.metadata.title=f"{title}\n{capo}"
 part=stream.Part()
 part.append(meter.TimeSignature(mtr))
 measure=stream.Measure()
 measure.append(key.KeySignature(0)) # C major is 0, it is the default
 measure.append(tempo.MetronomeMark(number=(int)(bpm.split('=',1)[1])))
 part.append(measure)

 num,denom=mtr.split('/')
 const_measure_length=float(num)/float(denom) # in quarters (x * 1/4)

 # Set the sections and the lines of the song
 for i_section in range(len(sections)):
  section_name=sections[i_section]['name']
  print(section_name)
  for i_line in range(len(sections[i_section]["lines"])):

   # Chords - line, tokens, positions
   chords_line=sections[i_section]['lines'][i_line]['chords']
   print(chords_line)
   chord_tokens=chords_line.split()
   chord_positions=[]
   for match in re.finditer(r'\S+',chords_line):
    chord_positions.append((match.group(),match.start()))

   # Durations - line, tokens, positions
   durations_line=sections[i_section]['lines'][i_line]['durations']
   print(durations_line)
   duration_tokens=durations_line.split()
   duration_positions=[]
   for match in re.finditer(r'\S+',durations_line):
    duration_positions.append((match.group(),match.start()))

   # Notes - line, tokens, positions
   notes_line=sections[i_section]['lines'][i_line]['notes']
   print(notes_line)
   notes_tokens=notes_line.split()
   note_positions=[]
   for match in re.finditer(r'\S+',notes_line):
    note_positions.append((match.group(),match.start()))

   for i_lyric in range(len(sections[i_section]['lines'][i_line]['lyrics'])):

    #Lyrics - line, tokens, positions
    lyrics_line=sections[i_section]['lines'][i_line]['lyrics'][i_lyric]
    print(lyrics_line)
    lyrics_tokens=lyrics_line.split()
    lyric_positions=[]
    for match in re.finditer(r'\S+',lyrics_line):
     lyric_positions.append((match.group(),match.start()))

 # Process the sections of the song (Prelude, Verse, Refrain, Interlude, Postlude)
 for i_section in range(len(sections)):
  section_name=sections[i_section]['name']
  print(section_name)
  for i_line in range(len(sections[i_section]["lines"])):
   chords_line=sections[i_section]['lines'][i_line]['chords']
   durations_line=sections[i_section]['lines'][i_line]['durations']
   notes_line=sections[i_section]['lines'][i_line]['notes']
   lyrics_lines=sections[i_section]['lines'][i_line]['lyrics']  # This is a list of lyric lines

   # Find all duration matches
   duration_matches=list(re.finditer(r'\S+',durations_line))
   if False:
    print(duration_matches)
   # Duration start positions (bar lines filtered)
   duration_positions=[m.start() for m in duration_matches if m.group() != '|']
   if False:
    print("duration_positions:\n",duration_positions)
   # Duration tokens
   duration_tokens=[m.group() for m in duration_matches if m.group() != '|']
   if False:
    print("duration_tokens:\n",duration_tokens)
   # Create a dictionary mapping the duration position to duration tokens - dictionary item can be referenced later by key
   duration_dict=dict(zip(duration_positions,duration_tokens))
   if True:
    print("duration_dict:\n",duration_dict)
   
   # Find all chord matches
   chord_matches=list(re.finditer(r'\S+',chords_line))
   if False:
    print(chord_matches)
   # Chord start positions
   chord_positions=[m.start() for m in chord_matches]
   if False:
    print("chord_positions:\n",chord_positions)
   # Chord tokens
   chord_tokens=[m.group() for m in chord_matches]
   if False:
    print("chord_tokens:\n",chord_tokens)
   # Create a dictionary mapping the chord position to chord tokens
   chord_dict=dict(zip(chord_positions,chord_tokens))
   if True:
    print("chord_dict:\n",chord_dict)

   # Find all note matches and store them in a dictionary
   note_matches=list(re.finditer(r'\S+',notes_line))
   if False:
    print(note_matches)
   # Note start positions
   note_positions=[m.start() for m in note_matches]
   if False:
    print("note_positions:\n",note_positions)
   # Note tokens
   note_tokens=[m.group() for m in note_matches]
   if False:
    print(note_tokens)
   # Create a dictionary mapping the note position to note tokens
   note_dict=dict(zip(note_positions,note_tokens))
   if True:
    print("note_dict:\n",note_dict)

   # Find all lyric matches and store them in an array of dictionaries by lyric lines
   lyric_dicts=[]
   for i_lyrics_line in range(len(lyrics_lines)):
    lyrics_line=lyrics_lines[i_lyrics_line]
    # Find all lyric matches (non-whitespace tokens)
    lyric_matches=list(re.finditer(r'\S+',lyrics_line))
    if False:
     print("lyric_matches:\n",lyric_matches)
    # Find lyric tokens and their ranges
    lyric_ranges=[(m.start(),m.end()-1,m.group()) for m in lyric_matches]
    # Lyric positions
    lyric_positions=[]
    lyric_tokens=[]
    for pos in duration_positions:
     # Find the token whose range contains pos
     for start,end,lyric_token in lyric_ranges:
      if start<=pos<=end:
       lyric_positions.append(pos)
       lyric_tokens.append(lyric_token)
       break
    if False:
     print("lyric_positions:\n",lyric_positions)
    if False:
     print("lyric_tokens:\n",lyric_tokens)
    # Create a dictionary mapping the closest duration position to the lyric tokens
    lyric_dict=dict(zip(lyric_positions,lyric_tokens))
    if True:
     print("lyric_dict:\n",lyric_dict)
    lyric_dicts.append(lyric_dict)

   # Add the measures of a line of a section to the part
   act_measure_length=0.0
   measure=stream.Measure()
   if i_line==0:
    measure.append(expressions.RehearsalMark(section_name))
   # Duration position is the base for all other elements, like chords, notes, rests and lyrics
   for position in duration_positions:
    dur=duration_dict[position]
    if dur in note_durations_map:
     dur_val=note_durations_map.get(dur,1.0)
    if dur in rest_durations_map:
     dur_val=rest_durations_map.get(dur,1.0)
    if False:
     print(dur,dur_val)

    # Append chord to the measure, if there is any at this position
    if position in chord_dict:
     chord_str=chord_dict[position]
     if False:
      print("chord: ",chord_str)
     chord_obj=harmony.ChordSymbol(chord_str)
     measure.append(chord_obj)

    # Append notes/rests to the measure (either a note or a rest must be at each duration position)
    dur=duration_dict[position]
    if dur in note_durations_map:
     # Note
     note_str=note_dict[position]
     if False:
      print("note: ",note_str)
     note_obj=note.Note(note_str)
     note_obj.quarterLength=dur_val
     # Attach all lyric syllables from all lyric lines to this note using the lyric_dicts array
     for i_lyric,lyric_dict in enumerate(lyric_dicts):
      lyric=lyric_dicts[i_lyric][position]
      note_obj.addLyric(lyric)
     measure.append(note_obj)
    if dur in rest_durations_map:
     # Rest
     rest_str=duration_dict[position]
     print("rest: ",rest_str)
     rest_obj=note.Rest()
     rest_obj.quarterLength=dur_val
     measure.append(rest_obj)

    # Check if it is already the end of the measure or not
    act_measure_length+=dur_val
    print(act_measure_length)
    if act_measure_length>const_measure_length*4:
     print("Error: measure length")
     exit()
    if act_measure_length==const_measure_length*4:
     print("measure complete")
     part.append(measure)
     act_measure_length=0.0
     measure=stream.Measure()

 # Complete the song and export to MusicXML
 score.append(part)

 score.write('musicxml',fp=musicxml_path)
 print(f"Exported to {musicxml_path}")

 # Copy to .xml - for easier sharing and displaying in an XML viewer
 import shutil
 xml_copy_path = musicxml_path + ".xml"
 shutil.copyfile(musicxml_path, xml_copy_path)
 print(f"Copied to {xml_copy_path}")
 return

import subprocess

musescore_path=r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"

def musicxml_to_mscz(musicxml_path,mscz_path):
 subprocess.run([musescore_path,musicxml_path,'-o',mscz_path],check=True)
 return

def musicxml_to_pngs(musicxml_path,png_path):
 subprocess.run([musescore_path,musicxml_path,'-o',png_path],check=True)
 return

mspaint_path=r"mspaint.exe"

def open_png_in_paint(png_path):
 subprocess.run([mspaint_path,png_path],check=True)
 return

def musicxml_to_pdf(musicxml_path,pdf_path):
 subprocess.run([musescore_path,musicxml_path,'-o',pdf_path],check=True)
 return

from PIL import Image,ImageOps
import glob

def del_pngs(png_base_path):
 for f in glob.glob(png_base_path + "-*.png"):
  try:
   os.remove(f)
   print(f"Deleted {f}")
  except Exception as e:
   print(f"Could not delete {f}: {e}")
 return

def merge_pngs_to_pdf(png_base_path,pdf_path,b_invert):
 png_files = sorted(glob.glob(png_base_path + "-*.png"))
 images = []
 for f in png_files:
  try:
   im = Image.open(f)
   if im.mode == 'RGBA':
    # Flatten transparency onto white background
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3])  # 3 is the alpha channel
    im = bg
   else:
    im = im.convert('RGB')
   if b_invert:
    im=ImageOps.invert(im)
   images.append(im)
  except Exception as e:
   print(f"Error: Processing {f}: {e}")
 if images:
  images[0].save("test_single.pdf")  # For testing
  images[0].save(pdf_path, save_all=True, append_images=images[1:])
  print("PDF created successfully!")
 else:
  print("No PNG files found.")
 return

def open_pdf_in_viewer(pdf_path):
 subprocess.run(['cmd', '/c', 'start', '', pdf_path], check=True)
 return

if __name__ == "__main__":

 # MUSICXML
 txt_path="tu-te-reconnaitras.txt"
 musicxml_path="tu-te-reconnaitras.musicxml"
 text_to_musicxml(txt_path,musicxml_path)
 
 # MSCZ
 #mscz_path="tu-te-reconnaitras.mscz"
 #musicxml_to_mscz(musicxml_path,mscz_path)

 # PDF
 #pdf_path="tu-te-reconnaitras.pdf"
 #musicxml_to_pdf(musicxml_path,pdf_path) # creates only as many pages PDF as many mesures are in the song

 # PNG
 png_base_path="tu-te-reconnaitras"
 png_path="tu-te-reconnaitras.png"
 del_pngs(png_base_path)
 musicxml_to_pngs(musicxml_path,png_path)

 # if b_invert is True, then white on black music sheet will be created, if False, then black on white
 b_invert=False
 pdf_path="tu-te-reconnaitras_BoW.pdf"
 merge_pngs_to_pdf(png_base_path,pdf_path,b_invert) # for printing
 b_invert=True
 pdf_path="tu-te-reconnaitras_WoB.pdf"
 merge_pngs_to_pdf(png_base_path,pdf_path,b_invert) # for viewing in dark mode
 open_pdf_in_viewer(pdf_path)
