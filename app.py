# Install necessary packages
!pip install streamlit requests plotly

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Create the Streamlit app script
app_code = """
import streamlit as st
import time
import plotly.graph_objects as go
from datetime import date
import os

# Define analysis data with placeholder timings for when emotions and scripts should pop up
analysis_data = {
    "audio_0.wav": {
        "Duration": 1 * 60 + 39,  # Duration in seconds (1:39)
        "Events": [
            {"time": 15, "alert": "Green", "script_var": "Script A"},
            {"time": 60, "alert": "Light Green", "script_var": "Script B"},
            {"time": 90, "alert": "Yellow", "script_var": "Script C"},
            {"time": 120, "alert": "Orange", "script_var": "Script D"},
            {"time": 135, "alert": "Red", "script_var": "Script E"}
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
            {"time": 10, "alert": "Red", "script_var": "Script E"},
            {"time": 58, "alert": "Orange", "script_var": "Script D"},
            {"time": 190.8, "alert": "Yellow", "script_var": "Script C"},
            {"time": 206.4, "alert": "Light Green", "script_var": "Script B"},
            {"time": 426.6, "alert": "Green", "script_var": "Script A"}
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

# Function to create a dynamic semicircle gauge using Plotly
def create_gauge(alert_type):
    gauge_value = {
        "Green": 1,
        "Light Green": 2,
        "Yellow": 3,
        "Orange": 4,
        "Red": 5
    }[alert_type]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        gauge={
            "axis": {"range": [0, 5]},
            "bar": {"color": "black"},
            "steps": [
                {"range": [0, 1], "color": "#00FF00"},
                {"range": [1, 2], "color": "#ADFF2F"},
                {"range": [2, 3], "color": "#FFFF00"},
                {"range": [3, 4], "color": "#FFA500"},
                {"range": [4, 5], "color": "#FF0000"}
            ]
        }
    ))

    return fig

# Streamlit app
st.title("Customer Service Audio Analysis")

# Dropdown menu for audio selection
audio_files = list(analysis_data.keys())
selected_audio = st.selectbox("Select an audio file", audio_files)

# Path to the voices folder in Google Drive
voices_dir = "/content/drive/MyDrive/Voices/"
audio_file_path = os.path.join(voices_dir, selected_audio)

# Check if file exists and play audio
if os.path.exists(audio_file_path):
    st.audio(audio_file_path)
else:
    st.error(f"Audio file {selected_audio} not found in Google Drive.")

duration = analysis_data[selected_audio]["Duration"]
events = analysis_data[selected_audio]["Events"]
scripts = analysis_data[selected_audio]["Scripts"]

start_time = time.time()
current_event_index = 0

# Initialize dynamic gauge
gauge_placeholder = st.empty()
table_placeholder = st.empty()
script_placeholder = st.empty()

# Initialize table data
table_data = []
visible_table_data = []

for event in events:
    table_data.append([time.strftime("%M:%S", time.gmtime(event["time"])), event["alert"], event["script_var"]])

# Display table and gauge immediately after loading
if events:
    current_event_index = 0
    event = events[current_event_index]
    gauge_fig = create_gauge(event["alert"])
    gauge_placeholder.plotly_chart(gauge_fig, use_container_width=True)

    # Update table with the current event
    visible_table_data.append([time.strftime("%M:%S", time.gmtime(event["time"])), event["alert"], event["script_var"]])
    table_placeholder.table(visible_table_data)
    script_placeholder.markdown(f"### {event['script_var']}\n\n{scripts[event['script_var']]}")

# After audio ends, show a selection box for the user
st.write("### Select the outcome of this audio:")
outcome = st.selectbox("Outcome", ["Resolved", "Unresolved", "Revert by"])

if outcome == "Revert by":
    revert_date = st.date_input("Select a date to revert by", min_value=date.today())
    st.write("Revert by date:", revert_date)
"""

# Write the app code to a file
with open("app.py", "w") as f:
    f.write(app_code)

# Run the Streamlit app
!streamlit run app.py --server.port 8501 --server.enableCORS false
