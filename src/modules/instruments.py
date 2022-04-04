#TODO: structure needs more work
from types import new_class
import numpy as np
from numpy.core.fromnumeric import size
from numpy.core.function_base import linspace
import sounddevice as sd
import scipy

import wave
from collections import defaultdict
from numpy import random
class Instrument():
    # super class of all instruments
    # should contain the common general functions
    def __init__(self):
        pass
    # Functions;
    # play notes
    # import base sample/tone
    # set and get the following
    # Variables
    # current tone
    # instrument name

# ahlan bel inhertiance

class Drums(Instrument): 

    def __init__(self):
        super().__init__()
        self.drum_sampling_rate=44100        
        self.drum_kit_tones={
                        'snare':['snare1.wav','snare2.wav','snare3.wav','snare4.wav']
                        ,'hat':['hat1.wav','hat2.wav','hat3.wav','hat4.wav']
                        ,'kick':['kick1.wav','kick2.wav','kick3.wav','kick4.wav']
                        ,'FLoor_tom':['Floor_tom1.wav','Floor_tom2.wav','Floor_tom3.wav','Floor_tom4.wav']
                        ,'H_tom':['H_tom1.wav','H_tom2.wav','H_tom3.wav','H_tom4.wav']
                        ,'ride_cymbal':['ride_cymbal1.wav','ride_cymbal2.wav','ride_cymbal3.wav','ride_cymbal4.wav']
                        ,'crash_cymbal':['crash_cymbal1.wav','crash_cymbal2.wav','crash_cymbal3.wav','crash_cymbal4.wav']}
        self.read_drum_tones={
                        'snare':[]
                        ,'hat':[]
                        ,'kick':[]
                        ,'FLoor_tom':[]
                        ,'H_tom':[]
                        ,'ride_cymbal':[]
                        ,'crash_cymbal':[]}
        self.read_all_samples()
    
    def read_all_samples(self):
        for key in self.drum_kit_tones:
            for index in self.drum_kit_tones[key]:
                tone=wave.open('resources\drum_tones\\' + str(index))
                signal = tone.readframes(-1) 
                signal = np.frombuffer(signal, dtype =np.int16)
                
                self.read_drum_tones[key].append(signal)
   

    def play_drums(self,tone):
        play_tone= random.choice(self.read_drum_tones[tone])
        sd.play(play_tone, self.drum_sampling_rate)

    def selecting_drum_kit(self,index):  
       self.play_drums(index)
        
    


class Piano(Instrument):
    def __init__(self):
        super().__init__()
        self.BASE_FREQ = 440
        self.PIANO_SAMPLING_RATE=44100
        self.octave_number =1  #default

    def key_freq(self,key_index,octave_number):

        n= self.n_jumps(key_index,octave_number)
        print('number of jumps:')
        print(n)
        print('octave:')
        print(octave_number)
        note_freq=self.BASE_FREQ*pow(2,n/12)
        print('freq:')
        print(note_freq)
        return note_freq

    def generating_wave(self,freq,duration=2.5):
        time = np.linspace(0, duration, int(self.PIANO_SAMPLING_RATE * duration))
        piano_wave = 0.6*np.sin(2 * np.pi * freq * time) * np.exp(-0.0015 * 2 * np.pi * freq * time)
        #overtones 
        piano_wave += 0.4*np.sin(2 * 2 * np.pi * freq * time) * np.exp(-0.0015 * 2 * np.pi * freq * time) / 2
       
        piano_wave += piano_wave * piano_wave * piano_wave
        #piano_wave *= 1 + 16 * time * np.exp(-6 * time)
        return  piano_wave
    
    def play_note(self,input_note):
         sd.play(input_note, self.PIANO_SAMPLING_RATE)
    def dial_value(self,dial_number):
        #TODO:LIMIT DIAL 1-7
        self.octave_number= dial_number
        print('HERE DIAL')
        print(self.octave_number)
    def n_jumps(self,key_index,octave_number):
        OCTAVE_LENGTH = 12
        A4_INDEX = 10

        if octave_number==0 :
            n= OCTAVE_LENGTH - key_index +12*3+9
            return -n
        elif octave_number==1:
            n= OCTAVE_LENGTH - key_index+12*2+9
            return -n
        elif octave_number==2:
            n= OCTAVE_LENGTH - key_index+12+9
            return -n
        elif octave_number==3:
            n= OCTAVE_LENGTH - key_index+9
            return -n
        elif octave_number== 4:
            n= key_index-A4_INDEX +1
            return n

        elif octave_number== 5:
            n=key_index+3
            return n
        elif octave_number== 6:
            n=key_index+12+3
            return n
        elif octave_number== 7:
            n=key_index+12*2+3
            return n
        elif octave_number== 8:
            n=key_index+12*3+3
            return n
    def generating_note(self,key_index):
        if key_index <12:
            octave_number= self.octave_number
        else:
            key_index= key_index - 12
            octave_number= self.octave_number+1
            
        freq= self.key_freq(key_index,octave_number)
        wave= self.generating_wave(freq,duration=1.7)
        self.play_note(wave)

    
class Guitar(Instrument):
    def __init__(self):
        super().__init__()
        self.GUITAR_SAMPLING_RATE=44100
        self.guitar_chords={
                        'G_major':[98,123,147,196,247,392]
                        ,'D_major':[82,110,147,220,294,370]
                        ,'C_major':[82,131,165,196,262,329]
                        ,'E_major':[82,123,165,208,247,329]
                        ,'A_major':[82,110,165,220,277,329]}
        self.chord=self.guitar_chords['G_major'] #default
        self.samples = []
    def wavetable_initiator(self,string_pitch):
        """Generates a new wavetable for the string."""
        print('WAVETABLE_INIT')
        print('pitch:')
        print(string_pitch)
        wavetable_size = self.GUITAR_SAMPLING_RATE // int(string_pitch)
        print('wavetable_size:')
        print(wavetable_size)
        wavetable = (2 * np.random.randint(0, 2, wavetable_size) - 1).astype(np.float)
        print('wavetable:')
        print(wavetable)
        return wavetable
      
    def get_sample(self,wavetable, n_samples):
        """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging."""
        current_sample = 0
        previous_value = 0
        samples = []
        while len(samples) < n_samples:
            wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size
        return np.array(samples)

    def guitar_chord_selection(self,dial_number):
        if dial_number ==1:
            self.chord=self.guitar_chords['G_major']
        elif dial_number ==2:
            self.chord=self.guitar_chords['D_major']
        elif dial_number ==3:
            self.chord=self.guitar_chords['C_major']
        elif dial_number ==4:
            self.chord=self.guitar_chords['E_major']
        elif dial_number ==5:
            self.chord=self.guitar_chords['D_major']

    def play_string(self,sound):
         sd.play(sound, self.GUITAR_SAMPLING_RATE)

    def guitar_string_sound(self,string_num):
        print('chord:')
        print(self.chord)
        pitchs = self.chord
        print('freq:')
        print(pitchs[string_num])
        #frequancy is the frequancy of string in the chosen chord
        frequancy=pitchs[string_num]
        print('freq entering the equation:')
        print(frequancy)
        wave = self.wavetable_initiator(frequancy)
        guitar_sound=self.get_sample(wave,self.GUITAR_SAMPLING_RATE * 5)
        self.play_string(guitar_sound)





    #def ks(self, f=220, length = np.linspace(0, np.fix(44100/220), int(44100*(np.fix(44100/220))))):
        #fs = 44100
        #f = 220
       # n = np.fix(fs/f)
        #x = np.zeros((1, len(length)))
        #b1 = [np.zeros(1, n), 1]
        #a1 = [1, np.zeros(1, n-1), -0.5, -0.5]
       # zi = np.random.uniform(1, max(max(size(a1)), max(size(b1))) -1)
       
      #y = lfilter(b1,a1,x,zi)
       # play_string(y)




#TODO: make this adaptable to the 3 instrument types
#TODO: connect in interface
def keyboard_pressed(key, instrument_index):
    # match key: match case needs python 3.10...
    #     case 'a':
    #         pass
    #     case  #TODO: do this in the future :(

    if key == 'a':
        pass
    elif key == 's':
        pass
    elif key == 'd':
        pass
    elif key == 'f':
        pass
    elif key == 'g':
        pass
    elif key == 'h':
        pass
