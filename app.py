
import streamlit as st
import time
import os
import matplotlib.pyplot as plt
from io import BytesIO

# Define analysis data with placeholder timings for when emotions and scripts should pop up
analysis_data = {
    'audio_0.wav': {
        'Duration': 1 * 60 + 39,  # Duration in seconds (1:39)
        'Events': [
            {'time': 15, 'alert': 'Green', 'script_var': 'Script A'},
            {'time': 60, 'alert': 'Light Green', 'script_var': 'Script B'},
            {'time': 90, 'alert': 'Yellow', 'script_var': 'Script C'},
            {'time': 120, 'alert': 'Orange', 'script_var': 'Script D'},
            {'time': 135, 'alert': 'Red', 'script_var': 'Script E'}
        ],
        'Scripts': {
            'Script A': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'Script B': 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            'Script C': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
            'Script D': 'Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor.',
            'Script E': 'In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
        }
    },
    'audio_1.wav': {
        'Duration': 8 * 60 + 37,  # Duration in seconds (8:37)
        'Events': [
            {'time': 21, 'alert': 'Green', 'script_var': 'Script A'},
            {'time': 120, 'alert': 'Light Green', 'script_var': 'Script B'},
            {'time': 300, 'alert': 'Yellow', 'script_var': 'Script C'},
            {'time': 480, 'alert': 'Orange', 'script_var': 'Script D'},
            {'time': 600, 'alert': 'Red', 'script_var': 'Script E'}
        ],
        'Scripts': {
            'Script A': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'Script B': 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            'Script C': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
            'Script D': 'Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor.',
            'Script E': 'In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
        }
    },
    'audio_2.wav': {
        'Duration': 4 * 60 + 22,  # Duration in seconds (4:22)
        'Events': [
            {'time': 30, 'alert': 'Green', 'script_var': 'Script A'},
            {'time': 90, 'alert': 'Light Green', 'script_var': 'Script B'},
            {'time': 150, 'alert': 'Yellow', 'script_var': 'Script C'},
            {'time': 210, 'alert': 'Orange', 'script_var': 'Script D'},
            {'time': 250, 'alert': 'Red', 'script_var': 'Script E'}
        ],
        'Scripts': {
            'Script A': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'Script B': 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            'Script C': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
            'Script D': 'Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor.',
            'Script E': 'In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
        }
    },
    'audio_3.wav': {
        'Duration': 2 * 60 + 45,  # Duration in seconds (2:45)
        'Events': [
            {'time': 25, 'alert': 'Green', 'script_var': 'Script A'},
            {'time': 60, 'alert': 'Light Green', 'script_var': 'Script B'},
            {'time': 90, 'alert': 'Yellow', 'script_var': 'Script C'},
            {'time': 120, 'alert': 'Orange', 'script_var': 'Script D'},
            {'time': 150, 'alert': 'Red', 'script_var': 'Script E'}
        ],
        'Scripts': {
            'Script A': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'Script B': 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
            'Script C': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
            'Script D': 'Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor.',
            'Script E': 'In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
        }
    }
}

# Function to create a dynamic gauge
def create_gauge(alert_type):
    fig, ax = plt.subplots()

    labels = ['Green', 'Light Green', 'Yellow', 'Orange', 'Red']
    colors = ['#00FF00', '#ADFF2F', '#FFFF00', '#FFA500', '#FF0000']
    ranges = [1, 1, 1, 1, 1]
    start = 0

    for label, color, r in zip(labels, colors, ranges):
        ax.barh(0, r, left=start, color=color)
        start += r

    needle_pos = labels.index(alert_type) + 0.5
    ax.barh(0, 0.05, left=needle_pos, color='black')

    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xlim(0, sum(ranges))
    ax.set_frame_on(False)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

# Streamlit app
st.title("Customer Service Audio Analysis")

# Dropdown menu for audio selection
audio_files = list(analysis_data.keys())
selected_audio = st.selectbox("Select an audio file", audio_files)

# Define the path to the audio files in the local environment
audio_path = "/content/voices/"  # Update this path as necessary

# Check if file exists
audio_file_path = os.path.join(audio_path, selected_audio)
if os.path.exists(audio_file_path):
    st.audio(audio_file_path)

    if st.button('Start Audio and Show Events'):
        duration = analysis_data[selected_audio]['Duration']
        events = analysis_data[selected_audio]['Events']
        scripts = analysis_data[selected_audio]['Scripts']

        start_time = time.time()
        current_event_index = 0

        # Initialize dynamic gauge
        gauge_placeholder = st.empty()
        table_placeholder = st.empty()
        script_placeholder = st.empty()

        # Table of timestamps, alert types, and script variables
        table_data = []
        for event in events:
            table_data.append((time.strftime("%M:%S", time.gmtime(event['time'])), event['alert'], event['script_var']))

        table_placeholder.table(table_data)

        while time.time() - start_time < duration:
            elapsed_time = time.time() - start_time
            if current_event_index < len(events) and elapsed_time >= events[current_event_index]['time']:
                event = events[current_event_index]
                gauge_img = create_gauge(event['alert'])
                gauge_placeholder.image(gauge_img, caption='Conversation Dynamic')

                table_data[current_event_index] = (
                    time.strftime("%M:%S", time.gmtime(event['time'])),
                    f"**{event['alert']}**",
                    f"[{event['script_var']}]({event['script_var']})"
                )

                table_placeholder.table(table_data)
                script_placeholder.markdown(f"### {event['script_var']}

{scripts[event['script_var']]}")

                current_event_index += 1
            time.sleep(1)
else:
    st.error(f"File {audio_file_path} not found.")
