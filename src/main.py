#!/usr/bin/env python

import alsaaudio
import wave
import simplejson as json
import subprocess
import httplib
import os
import atexit

import Loader
import ProcessText

CHUNK = 1024
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
SLEEP_TIME = 15
WAVE_OUTPUT_FILENAME = 'recording.wav'
FLAC_OUTPUT_FILENAME = 'recording.flac'
HTTP_API_BASE = 'google.com'
HTTP_API_CALL = '/speech-api/v1/recognize?lang=en-us&client=chromium'

def clean_up():
    ''' Clean up, clean up, everybody do your share '''
    os.remove(FLAC_OUTPUT_FILENAME)

def send_recv():
    ''' Encode, send, and receive FLAC file '''
    body = open(FLAC_OUTPUT_FILENAME, 'rb').read()
    h = httplib.HTTP(HTTP_API_BASE)
    h.putrequest('POST', HTTP_API_CALL)
    h.putheader('content-type', 'audio/x-flac; rate=16000')
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, _, _ = h.getreply()
    return errcode, h.file.read()

def capture_audio(loader):
    ''' Set up mic, capture audio, and return string of the result '''
    def setup_mic():
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        inp.setchannels(CHANNELS)
        inp.setrate(RATE)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(CHUNK)
        return inp

    inp = setup_mic()
    sound = []

    print "* recording\n"
    for i in xrange(0, RATE / CHUNK * RECORD_SECONDS):
        loader(i)
        _, data = inp.read()
        sound.append(data)
    print "* done recording\n"

    return ''.join(sound)

def write_wav(data):
    ''' Write string of data to WAV file of specified name '''
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def main():
    ''' Run through process of getting, converting, sending/receiving, and 
        processing data '''

    # First capture audio and write to WAV file
    write_wav(capture_audio(Loader.Loader(SLEEP_TIME * RECORD_SECONDS, 2)))
   
    # Then convert to FLAC
    subprocess.call(['flac', '-f', '-s', '--sample-rate=' + str(RATE), 
                    '--delete-input-file', WAVE_OUTPUT_FILENAME])
    
    # Send and receive translation
    err, resp = send_recv()

    # Analyze results
    if err is not 200:
        print 'No results.'
        import time
        time.sleep(2)
    else:
        ProcessText.process_text(json.loads(resp)['hypotheses'][0].values())

if __name__ == '__main__':
    atexit.register(clean_up)
    main()
