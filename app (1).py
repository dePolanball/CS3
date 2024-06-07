
import streamlit as st
import os
import time
from datetime import date

# Define analysis data with placeholder timings for when emotions and scripts should pop up
analysis_data = {
    "audio_0.wav": {
        "Duration": 1 * 60 + 39,  # Duration in seconds (1:39)
        "Events": [
            {"time": 15, "alert": "Green", "script_var": "Script A"},
            {"time": 60, "alert": "Light Green", "script_var": "Script B"},
            {"time": 90, "alert": "Light Green", "script_var": "Script B"},
            {"time": 120, "alert": "Light Green", "script_var": "Script B"},
            {"time": 135, "alert": "Light Green", "script_var": "Script B"}
        ],
        "Scripts": {
            "Script A": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Script B": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Script C": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
            "Script D": "Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor.",
            "Script E": "In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        }
    },
    "audio_1.wav": {
        "Duration": 8 * 60 + 37,  # Duration in seconds (8:37)
        "Events": [
            {"time": 15, "alert": "Red", "script_var": "Script E"},
            {"time": 42, "alert": "Yellow", "script_var": "Script C"},
            {"time": 186.6, "alert": "Light Green", "script_var": "Script B"},
            {"time": 425.4, "alert": "Green", "script_var": "Script A"},
            {"time": 600, "alert": "Green", "script_var": "Script A"}
        ],
        "Scripts": {
            "Script A": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Script B": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Script C": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
            "Script D": "Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor.",
            "Script E": "In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        }
    },
    "audio_2.wav": {
        "Duration": 4 * 60 + 22,  # Duration in seconds (4:22)
        "Events": [
            {"time": 30, "alert": "Green", "script_var": "Script A"},
            {"time": 90, "alert": "Light Green", "script_var": "Script B"},
            {"time": 150, "alert": "Yellow", "script_var": "Script C"},
            {"time": 210, "alert": "Orange", "script_var": "Script D"},
            {"time": 250, "alert": "Red", "script_var": "Script E"}
        ],
        "Scripts": {
            "Script A": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Script B": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Script C": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
            "Script D": "Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor.",
            "Script E": "In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        }
    },
    "audio_3.wav": {
        "Duration": 2 * 60 + 45,  # Duration in seconds (2:45)
        "Events": [
            {"time": 25, "alert": "Green", "script_var": "Script A"},
            {"time": 60, "alert": "Light Green", "script_var": "Script B"},
            {"time": 90, "alert": "Yellow", "script_var": "Script C"},
            {"time": 120, "alert": "Orange", "script_var": "Script D"},
            {"time": 150, "alert": "Red", "script_var": "Script E"}
        ],
        "Scripts": {
            "Script A": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Script B": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Script C": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
            "Script D": "Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor.",
            "Script E": "In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
        }
    }
}

# Function to create lights
def create_lights(alert_type):
    colors = {"Green": "#00FF00", "Light Green": "#ADFF2F", "Yellow": "#FFFF00", "Orange": "#FFA500", "Red": "#FF0000"}
    light_colors = ["#D3D3D3"] * 5
    if alert_type == "Green":
        light_colors[0] = colors[alert_type]
    elif alert_type == "Light Green":
        light_colors[1] = colors[alert_type]
    elif alert_type == "Yellow":
        light_colors[2] = colors[alert_type]
    elif alert_type == "Orange":
        light_colors[3] = colors[alert_type]
    elif alert_type == "Red":
        light_colors[4] = colors[alert_type]
    return light_colors

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

    duration = analysis_data[selected_audio]["Duration"]
    events = analysis_data[selected_audio]["Events"]
    scripts = analysis_data[selected_audio]["Scripts"]

    # Initialize dynamic lights
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
        st.session_state.current_event_index = 0
        st.session_state.visible_table_data = []

    elapsed_time = time.time() - st.session_state.start_time

    if st.session_state.current_event_index < len(events) and elapsed_time >= events[st.session_state.current_event_index]["time"]:
        event = events[st.session_state.current_event_index]
        light_colors = create_lights(event["alert"])
        st.session_state.light_colors = light_colors

        # Update table with the current event
        st.session_state.visible_table_data.append([time.strftime("%M:%S", time.gmtime(event["time"])), event["alert"], event["script_var"]])
        st.session_state.current_event_index += 1

    if "light_colors" in st.session_state:
        st.markdown(f"<div style='text-align: center;'>"
                    f"<span style='background-color: {st.session_state.light_colors[0]}; padding: 15px 30px; margin: 5px;'></span>"
                    f"<span style='background-color: {st.session_state.light_colors[1]}; padding: 15px 30px; margin: 5px;'></span>"
                    f"<span style='background-color: {st.session_state.light_colors[2]}; padding: 15px 30px; margin: 5px;'></span>"
                    f"<span style='background-color: {st.session_state.light_colors[3]}; padding: 15px 30px; margin: 5px;'></span>"
                    f"<span style='background-color: {st.session_state.light_colors[4]}; padding: 15px 30px; margin: 5px;'></span>"
                    f"</div>", unsafe_allow_html=True)

    st.table(st.session_state.visible_table_data)

    if st.session_state.current_event_index > 0:
        current_event = events[st.session_state.current_event_index - 1]
        st.markdown(f"### {current_event['script_var']}

{scripts[current_event['script_var']]}")

    # After audio ends, show a selection box for the user
    if elapsed_time >= duration:
        st.write("### Select the outcome of this audio:")
        outcome = st.selectbox("Outcome", ["Resolved", "Unresolved", "Revert by"])

        if outcome == "Revert by":
            revert_date = st.date_input("Select a date to revert by", min_value=date.today())
            st.write("Revert by date:", revert_date)

else:
    st.error(f"File {audio_file_path} not found.")
