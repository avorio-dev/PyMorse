####################################################################################################################
# IMPORTS
import json
import os
import subprocess
import time

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile


####################################################################################################################
# CORE
class MorseConverter:
    # ---> CONSTANTS
    FREQUENCY = 800  # Frequency of the beep in Hz
    SAMPLING_RATE = 44100  # Sample rate for the audio (CD quality)

    # ---> ATTRIBUTES
    duration_dot = 100 / 1000  # Duration of the beep in milliseconds
    duration_dash = duration_dot * 3  # Duration of the beep in milliseconds
    duration_pause = duration_dot * 7

    # ---> CONSTRUCTOR
    def __init__(self):
        with open("res/morse_alphabet.json", "r") as file:
            json_content = json.load(file)

            self._ddic_str_to_morse = json_content['morse_code']['str_to_morse']
            self._ddic_morse_to_str = json_content['morse_code']['morse_to_str']

    # ---> FUNCTIONS
    def get_ddic_str_to_morse(self):
        return self._ddic_str_to_morse

    def get_ddic_morse_to_str(self):
        return self._ddic_morse_to_str

    def string_to_morse(self, input_string):

        string_to_morse = input_string
        string_to_morse = string_to_morse.upper()
        string_to_morse = string_to_morse.strip()

        # TODO implement special chars
        morse_text = ""
        for char in string_to_morse.upper():
            if char == ' ':
                morse_text += '|'
            else:
                if char in self._ddic_str_to_morse['chars']:
                    morse_text += self._ddic_str_to_morse['chars'][char]

                elif char in self._ddic_str_to_morse['digits']:
                    morse_text += self._ddic_str_to_morse['digits'][char]

                elif char in self._ddic_str_to_morse['punctuation_marks']:
                    morse_text += self._ddic_str_to_morse['punctuation_marks'][char]

                else:
                    morse_text += ' '

            morse_text += ' '

        return morse_text.strip()

    def morse_to_string(self, input_morse):
        # TODO morse to string
        pass

    def play_sound(self, all_notes):
        if len(all_notes) > 0:
            sd.play(all_notes, self.SAMPLING_RATE)
            sd.wait()

    @staticmethod
    def print_plot(all_notes):
        if len(all_notes) > 0:
            plt.plot(all_notes)
            plt.xlabel('Sample')
            plt.ylabel('Amplitude')
            plt.title('Audio Waveform')
            plt.show()

    def export_file(self, all_notes):
        if all_notes:
            sound_name = f'morse_{time.time()}.wav'

            out_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            out_folder = out_folder + '\\MorseAudio\\'
            if not os.path.isdir(out_folder):
                os.makedirs(out_folder)

            out_path = out_folder + sound_name
            wavfile.write(out_path, self.SAMPLING_RATE, all_notes)

            subprocess.Popen(f'explorer {out_folder}"')

    def _get_signal_wave(self, duration):
        # Generate time for temporal axis of signal
        t = np.linspace(0, duration, int(self.SAMPLING_RATE * duration), endpoint=False)

        # Generate sine wave for signal
        signal_wave = 0.5 * np.sin(2 * np.pi * self.FREQUENCY * t)
        return signal_wave

    def _get_silence_wave(self, duration):
        # Generate time for temporal axis of signal
        t_silence = np.linspace(0, duration, int(self.SAMPLING_RATE * duration), endpoint=False)

        # Generate sine wave for signal
        silence_wave = np.zeros_like(t_silence)  # Silence Wave
        return silence_wave

    def morse_process(self, morse_text, play_sound=False, print_plot=False, export_file=False):

        morse_audio = np.array([])

        # Start the signal with a Silence Wave
        silence_wave = self._get_silence_wave(self.duration_dash)
        morse_audio = np.concatenate((morse_audio, silence_wave))

        for char in morse_text:
            match char:
                case ".":
                    duration = self.duration_dot
                    signal_wave = self._get_signal_wave(duration)
                    morse_audio = np.concatenate((morse_audio, signal_wave))

                case "-":
                    duration = self.duration_dash
                    signal_wave = self._get_signal_wave(duration)
                    morse_audio = np.concatenate((morse_audio, signal_wave))

                case " ":
                    duration = self.duration_dash
                    silence_wave = self._get_silence_wave(duration)
                    morse_audio = np.concatenate((morse_audio, silence_wave))

                case "|":
                    duration = self.duration_pause
                    silence_wave = self._get_silence_wave(duration)
                    morse_audio = np.concatenate((morse_audio, silence_wave))

            silence_wave = self._get_silence_wave(self.duration_dot)
            morse_audio = np.concatenate((morse_audio, silence_wave))

        # End the signal with a Silence Wave
        silence_wave = self._get_silence_wave(self.duration_dash)
        morse_audio = np.concatenate((morse_audio, silence_wave))

        all_notes = np.int16(morse_audio * 32767)

        if play_sound:
            self.play_sound(all_notes)

        if print_plot:
            self.print_plot(all_notes)

        if export_file:
            self.export_file(all_notes)

        return morse_audio


if __name__ == "__main__":
    mc = MorseConverter()
    sos = mc.string_to_morse("SOS")
    print(sos)

    mc.morse_process(sos, True, True, True)
