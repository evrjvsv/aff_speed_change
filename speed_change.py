#from ffmpeg import audio
import os
import re
import sys

from arcfutil import aff

# supported file types
audiosuffix = ['.mp3', '.ogg']
beatmapsuffix = '.aff'


def change_audio_rate(rate: float, audio_file):
    for i, audio1 in enumerate(audio_file):
        is_audio = False
        for suf in audiosuffix:
            if(audio1.endswith(suf)):
                is_audio = True
                break
        if(is_audio):
            cmd = "ffmpeg -n -i "+audio1 + \
                " -filter:a \"atempo=%f\" " % rate + \
                ".\\speed_change\\"+audio1
            os.system(cmd)


def change_note_rate(rate: float, note):
    if(isinstance(note, aff.AudioOffset)):
        note.offset = int(note.offset/rate)
    elif(isinstance(note, aff.Timing)):
        note.time = int(note.time/rate)
        note.bpm = note.bpm*rate
    elif(isinstance(note, aff.Tap)):
        note.time = int(note.time/rate)
        if(isinstance(note, aff.Hold)):
            note.totime = int(note.totime/rate)
    elif(isinstance(note, aff.Arc)):
        note.time = int(note.time/rate)
        note.totime = int(note.totime/rate)
        for k, n in enumerate(note.skynote):
            note.skynote[k] = int(int(n)/rate)
    elif(note != None):
        print('Type \'{}\' is not supported for the moment'.format(type(note)))
        return None
    return note


def change_beatmap_rate(rate: float, beatmap_file):
    for i, beatmap1 in enumerate(beatmap_file):
        is_beatmap = False
        for suf in beatmapsuffix:
            if(beatmap1.endswith(suf)):
                is_beatmap = True
        if(is_beatmap):
            notelist = aff.loads(beatmap1)
            for j, note in enumerate(notelist):
                if(isinstance(note, aff.TimingGroup)):
                    for k, n in enumerate(note):
                        note[k] = change_note_rate(rate, n)
                else:
                    note = change_note_rate(rate, note)
                if(note != None):
                    notelist[j] = note
            os.chdir(".\\speed_change")
            aff.dumps(notelist, os.getcwd()+'\\'+beatmap1)
            os.chdir("..\\")


def main():
    rate = round(float(input("input rate:")), 2)
    if rate < 0.1:
        print("illegal value!The rate value must ")
    else:
        path = input("input path of audio(not include the file name):")
        os.chdir(path)
        file = os.listdir()
        if not os.path.exists('.\\speed_change'):
            os.mkdir('.\\speed_change')
        change_audio_rate(rate, file)
        change_beatmap_rate(rate, file)


main()
