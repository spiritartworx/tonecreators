import numpy as np
import pyaudio
import time
import wave
import soundfile as sf  # For saving WAV files with sf.write
import sounddevice as sd  # For playing audio (if needed)

# Audio Constants
SAMPLE_RATE = 44100
VOLUME = 0.1  # Lower volume for complex sounds

# --- Audio Generation Functions (Tony Kujo Inspired) ---
def generate_complex_sound(duration, theta_freq, gamma_freq, wobble_freq, modulation_depth, fm_depth):
    """Generates a complex soundscape with Theta/Gamma waves, modulation, and panning."""

    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)

    # --- Generate Theta Wave (Left Channel) ---
    fm_wave = np.sin(2 * np.pi * wobble_freq * t) * fm_depth
    theta_wave = np.sin(2 * np.pi * (theta_freq + fm_wave) * t)
    wobble_am = 1 - modulation_depth + modulation_depth * np.sin(2 * np.pi * wobble_freq * t)
    theta_wave_modulated = theta_wave * wobble_am

    # --- Generate Gamma Wave (Right Channel) ---
    gamma_wave = np.sin(2 * np.pi * gamma_freq * t)

    # --- Add Panning Effect (Gamma Wave Dynamic Stereo) ---
    pan_speed = 0.05
    pan_wave = np.sin(2 * np.pi * pan_speed * t)
    gamma_left = (1 + pan_wave) / 2 * gamma_wave
    gamma_right = (1 - pan_wave) / 2 * gamma_wave

    # --- Combine Waves into Stereo Channels ---
    left_channel = theta_wave_modulated + gamma_left
    right_channel = gamma_right

    stereo_sound = np.column_stack((left_channel, right_channel))
    stereo_sound *= VOLUME / np.max(np.abs(stereo_sound))  # Normalize

    return stereo_sound.astype(np.float32)

def play_audio(samples):  #Using PyAudio
    """Plays the generated audio samples."""

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=2, rate=SAMPLE_RATE, output=True) # Stereo
    stream.write(samples.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

def save_wave(filename, samples):
    """Saves the audio samples as a WAV file."""

    sf.write(filename, samples, SAMPLE_RATE) # Using soundfile

# --- Presentation Logic ---
def present_to_investor(investor_name, investor_focus, investor_preferences, tonecreators_data, save_audio=False):
    """Presents Tonecreators information to a single investor (with Tony Kujo vibes!)."""

    print("\n--- Get Ready for the Tonecreators Sonic Experience, {}! ---".format(investor_name))
    print("Your Focus: {}".format(investor_focus))
    print("Your Preferences: {}\n".format(investor_preferences))
    print("Prepare to be sonically amazed!\n")

    # Intro Soundscape
    intro_sound = generate_complex_sound(
        duration=5, theta_freq=7, gamma_freq=35, wobble_freq=2, modulation_depth=0.4, fm_depth=0.08
    )
    if save_audio:
        save_wave("01_intro.wav", intro_sound)
    play_audio(intro_sound)
    time.sleep(1)

    print("--- Tonecreators: Our Core Essence ---")
    print("Mission: {}".format(tonecreators_data['mission']))
    print("Vision: {}\n".format(tonecreators_data['vision']))
    time.sleep(2)

    # Products Soundscape
    products_sound = generate_complex_sound(
        duration=7, theta_freq=8, gamma_freq=45, wobble_freq=4, modulation_depth=0.3, fm_depth=0.1
    )
    if save_audio:
        save_wave("02_products.wav", products_sound)
    play_audio(products_sound)
    time.sleep(1)

    print("--- Core Products and Offerings ---")
    for i, product in enumerate(tonecreators_data['core_products']):
        print(f"{i + 1}. {product}")
        time.sleep(0.3)
    print()
    time.sleep(2)

    # Impact Soundscape
    impact_sound = generate_complex_sound(
        duration=6, theta_freq=6, gamma_freq=25, wobble_freq=1, modulation_depth=0.2, fm_depth=0.05
    )
    if save_audio:
        save_wave("03_impact.wav", impact_sound)
    play_audio(impact_sound)
    time.sleep(1)

    print("--- Social Impact Initiatives ---")
    for initiative in tonecreators_data['impact_initiatives']:
        print(f"- {initiative}")
        time.sleep(0.3)
    print()
    time.sleep(2)

    # Revenue Soundscape
    revenue_sound = generate_complex_sound(
        duration=5, theta_freq=9, gamma_freq=50, wobble_freq=5, modulation_depth=0.5, fm_depth=0.12
    )
    if save_audio:
        save_wave("04_revenue.wav", revenue_sound)
    play_audio(revenue_sound)
    time.sleep(1)

    print("--- Show Me the Money (and the Impact)! ---")
    print("Our revenue streams are designed for sustainable growth and maximum impact.")
    time.sleep(2)

    # Outro Soundscape
    outro_sound = generate_complex_sound(
        duration=4, theta_freq=5, gamma_freq=30, wobble_freq=1.5, modulation_depth=0.1, fm_depth=0.03
    )
    if save_audio:
        save_wave("05_outro.wav", outro_sound)
    play_audio(outro_sound)
    time.sleep(1)

    print("--- Invest in the Future of Creativity! ---")
    print("Let's build a sonic revolution together.")

def get_investor_input():
    """Gets investor information from the user."""

    investor_name = input("\nEnter Investor Name: ")
    investor_focus = input("Enter Investor Focus Areas (e.g., Tech, Impact): ")
    investor_preferences = input("Enter Investor Preferences (e.g., Sustainable, High-Growth): ")
    return investor_name, investor_focus, investor_preferences

def main():
    """Main function to run the investor presentation."""

    # Load Tonecreators data
    tonecreators_data = {
        'mission': 'To empower individuals and communities through the synergy of creative expression, technological innovation, and collaborative networks.',
        'vision': 'To forge a world where creativity and technology unite to break down barriers, ignite positive change, and enable every individual to reach their full potential.',
        'core_products': ['Day2Night Events', 'Ahyea Productions', 'Niteworx', 'Massive Mind App',
                          'Quantum Human Dynamics', 'LUCC', 'ArtAccess', 'From Shadow With Love'],
        'impact_initiatives': ['Operation Gimme Shelter', 'Area 520']
    }

    # Get investor input
    investor_name, investor_focus, investor_preferences = get_investor_input()

    # Present to the investor and save audio
    present_to_investor(investor_name, investor_focus, investor_preferences, tonecreators_data, save_audio=True)

    print("\nInvestor presentation completed. Sonic files created.\n")

if __name__ == "__main__":
    main()
