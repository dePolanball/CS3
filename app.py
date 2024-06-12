# Install necessary packages
!pip install streamlit requests plotly pyngrok

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Create the Streamlit app script
app_code = '''
import streamlit as st
import plotly.graph_objects as go
from datetime import date
import time
import os

# Define analysis data with placeholder timings for when emotions and scripts should pop up
analysis_data = {
    "audio_1.wav": {
        "Duration": 8 * 60 + 37,  # Duration in seconds (8:37)
        "Events": [
            {"time": 13, "alert": "Red", "script_var": "Script E"},
            {"time": 92, "alert": "Orange", "script_var": "Script D"},
            {"time": 196, "alert": "Yellow", "script_var": "Script C"},
            {"time": 217, "alert": "Light Green", "script_var": "Script B"},
            {"time": 323, "alert": "Green", "script_var": "Script A"}
        ],
        "Scripts": {
            "Script A": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.",
            "Script B": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Nam nec ante. Sed lacinia, urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante quis turpis.",
            "Script C": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Nulla facilisi. Integer lacinia sollicitudin massa. Cras metus. Sed aliquet risus a tortor. Integer id quam.",
            "Script D": "Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Maecenas malesuada. Praesent congue erat at massa. Sed cursus turpis vitae tortor. Donec posuere vulputate arcu. Phasellus accumsan cursus velit.",
            "Script E": "In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium. Curabitur at lacus ac velit ornare lobortis. Curabitur a felis in nunc fringilla tristique. Morbi mollis tellus ac sapien."
        }
    },
    "audio_2.wav": {
        "Duration": 2 * 60 + 36,  # Duration in seconds (2:36)
        "Events": [
            {"time": 9, "alert": "Yellow", "script_var": "Script C"},
            {"time": 113, "alert": "Green", "script_var": "Script A"}
        ],
        "Scripts": {
            "Script A": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.",
            "Script B": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Nam nec ante. Sed lacinia, urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante quis turpis.",
            "Script C": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Nulla facilisi. Integer lacinia sollicitudin massa. Cras metus. Sed aliquet risus a tortor. Integer id quam." 
        }
    },
    "audio_3.wav": {
        "Duration": 1 * 60 + 38,  # Duration in seconds (1:38)
        "Events": [
            {"time": 12, "alert": "Orange", "script_var": "Script D"},
            {"time": 53, "alert": "Red", "script_var": "Script E"}
        ],
        "Scripts": {
            "Script B": "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Nam nec ante. Sed lacinia, urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante quis turpis.",
            "Script D": "Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Maecenas malesuada. Praesent congue erat at massa. Sed cursus turpis vitae tortor. Donec posuere vulputate arcu. Phasellus accumsan cursus velit.",
            "Script E": "In reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium. Curabitur at lacus ac velit ornare lobortis. Curabitur a felis in nunc fringilla tristique. Morbi mollis tellus ac sapien."
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
voices_dir = "/content/drive/MyDrive/Voices "
audio_file_path = os.path.join(voices_dir, selected_audio)

# Check if file exists and play audio
if os.path.exists(audio_file_path):
    st.audio(audio_file_path)
else:
    st.error("Audio file {} not found in Google Drive.".format(selected_audio))

duration = analysis_data[selected_audio]["Duration"]
events = analysis_data[selected_audio]["Events"]
scripts = analysis_data[selected_audio]["Scripts"]

# Initialize table data
table_data = []
visible_table_data = []

for event in events:
    table_data.append([time.strftime("%M:%S", time.gmtime(event["time"])), event["alert"], event["script_var"]])

# Initialize dynamic gauge
gauge_placeholder = st.empty()
table_placeholder = st.empty()
script_placeholder = st.empty()

# Display initial table and gauge
table_placeholder.table(visible_table_data)
gauge_placeholder.plotly_chart(create_gauge("Green"), use_container_width=True)

start_time = time.time()
current_event_index = 0

# Main loop to update gauge and table
while time.time() - start_time < duration:
    elapsed_time = time.time() - start_time
    if current_event_index < len(events) and elapsed_time >= events[current_event_index]["time"]:
        event = events[current_event_index]
        gauge_fig = create_gauge(event["alert"])
        gauge_placeholder.plotly_chart(gauge_fig, use_container_width=True)

        # Update table with the current event
        visible_table_data.append([time.strftime("%M:%S", time.gmtime(event["time"])), event["alert"], event["script_var"]])
        table_placeholder.table(visible_table_data)
        script_placeholder.markdown("### {}\\n\\n{}".format(event["script_var"], scripts[event["script_var"]]))

        current_event_index += 1
    time.sleep(1)

# After audio ends, show a selection box for the user
st.write("### Select the outcome of this audio:")
outcome = st.selectbox("Outcome", ["Resolved", "Unresolved", "Revert by"])

if outcome == "Revert by":
    revert_date = st.date_input("Select a date to revert by", min_value=date.today(), format="YYYY/MM/DD", disabled=False, label_visibility="visible")
    st.write("Revert by date:", revert_date)
'''

# Write the app code to a file
with open("app.py", "w") as f:
    f.write(app_code)
