import alsaaudio
import wave
import os
import simplejson as json
import subprocess
import httplib

from Loader import Loader

CHUNK = 1024
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
SLEEP_TIME = 15
WAVE_OUTPUT_FILENAME = 'recording.wav'
FLAC_OUTPUT_FILENAME = 'recording.flac'
HTTP_API_BASE = 'google.com'
HTTP_API_CALL = '/speech-api/v1/recognize?lang=en-us&client=chromium'

def send_recv(host, selector, filename):
    body = open(filename, 'rb').read()
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', 'audio/x-flac; rate=16000')
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return errcode, h.file.read()

def setup_mic():
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
    inp.setchannels(1)
    inp.setrate(16000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(CHUNK)
    return inp

def capture_audio(inp, loader):
    sound = []
    print "* recording\n"
    for i in xrange(0, RATE / CHUNK * RECORD_SECONDS):
        loader(i)
        _, data = inp.read()
        sound.append(data)
    print "* done recording"
    return sound

def write_wav(data):
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def process_text(values):
    confidence, text = values
    print 'result is: \'', text, '\' with confidence', confidence

    # Open a process 
    if text.startswith('open'):
        os.system(text[text.index('open ')+5:])
    # Compute a product or sum
    elif text.startswith('calculate '):
        os.system('echo \"' + text[text.index('calculate ')+10:] + '\" | bc')
    # Lock the screen
    elif text == 'lock screen':
        subprocess.call(['rm', FLAC_OUTPUT_FILENAME])
        os.system('gnome-screensaver-command -l')
        exit()

def main():
    loader = Loader(SLEEP_TIME * RECORD_SECONDS, 2)
    
    write_wav(''.join(capture_audio(setup_mic(), loader)))
   
    # Convert to FLAC
    subprocess.call(['flac', '-f', '-s', '--sample-rate=' + str(RATE), 
                    '--delete-input-file', WAVE_OUTPUT_FILENAME])
    
    # Send and receive translation
    err, resp = send_recv(HTTP_API_BASE, HTTP_API_CALL, FLAC_OUTPUT_FILENAME)

    # Could not find any match
    if err is not 200:
        print 'No results.'
        exit()
        
    process_text(json.loads(resp)['hypotheses'][0].values())

    subprocess.call(['rm', FLAC_OUTPUT_FILENAME])

if __name__ == '__main__':
    main()

