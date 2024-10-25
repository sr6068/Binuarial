import pyaudio
import numpy as np

# Initialize PyAudio
p = pyaudio.PyAudio()

def generate_tone(frequency, volume, duration, rate):
    """Generate a sine wave tone for a given frequency, volume, duration, and rate."""
    t = np.linspace(0, duration, int(rate * duration), False)
    tone = volume * np.sin(frequency * t * 2 * np.pi)
    return tone

def interleave_channels(channel1, channel2):
    """Interleave two mono channels into a stereo signal."""
    interleaved = np.empty((channel1.size + channel2.size,), dtype=channel1.dtype)
    interleaved[0::2] = channel1
    interleaved[1::2] = channel2
    return interleaved

def play_tone(frequency1, volume1, frequency2, volume2, duration, rate, channels=2):
    """Generate and play a stereo tone using two frequencies and volumes for left and right channels."""
    # Generate tones for each channel
    tone1 = generate_tone(frequency1, volume1, duration, rate)
    tone2 = generate_tone(frequency2, volume2, duration, rate)
    
    # Interleave to create stereo sound
    stereo_tone = interleave_channels(tone1, tone2)
    
    # Open audio stream
    stream = p.open(format=pyaudio.paFloat32,
                    channels=channels,
                    rate=rate,
                    output=True)
    
    # Play sound
    stream.write(stereo_tone.astype(np.float32).tostring())
    
    # Close the stream
    stream.stop_stream()
    stream.close()

# Emotional state presets for binaural beats
emotional_states = {
    "sleeping": {"frec1": 80, "vol1": 0.5, "frec2": 85, "vol2": 0.5, "duration": 30.0},   # Low, relaxing frequencies
    "angry": {"frec1": 400, "vol1": 0.9, "frec2": 405, "vol2": 0.9, "duration": 10.0},    # Sharp, intense frequencies
    "emotional": {"frec1": 220, "vol1": 0.7, "frec2": 225, "vol2": 0.7, "duration": 15.0}, # Warm, middle frequencies
    "focused": {"frec1": 350, "vol1": 0.8, "frec2": 355, "vol2": 0.8, "duration": 20.0}   # Higher, focus-driven frequencies
}

# Sample rate
rate = 44100

# Get user input for emotional state
state = input("Enter the emotional state (sleeping, angry, emotional, focused): ").lower()

# Get parameters based on the emotional state
if state in emotional_states:
    params = emotional_states[state]
    frec1 = params["frec1"]
    vol1 = params["vol1"]
    frec2 = params["frec2"]
    vol2 = params["vol2"]
    duration = params["duration"]
else:
    print("Invalid state! Defaulting to 'sleeping' preset.")
    params = emotional_states["sleeping"]
    frec1 = params["frec1"]
    vol1 = params["vol1"]
    frec2 = params["frec2"]
    vol2 = params["vol2"]
    duration = params["duration"]

# Play the tone with preset parameters
play_tone(frec1, vol1, frec2, vol2, duration, rate)

# Terminate PyAudio
p.terminate()
