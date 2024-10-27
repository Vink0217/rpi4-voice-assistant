# rpi4-voice-assistant
> Streamlit based webapp for voice based interaction with Gemini 1.5 Flash model.

### Requirements

- Python 3.11+
- USB audio device with a built-in microphone
- Docker installed and setup

### Libraries Used
- `google.generativeai` - LLM for prompt-response
- `sounddevice`, `wavio` - Manipulating voice recording
- `streamlit` - UI

## Setup for Local Development

- Clone the repository and change to project directory.
  ```bash
  $ git clone https://github.com/SourasishBasu/rpi4-voice-assistant.git
  $ cd rpi4-voice-assistant/
  ```
- Create a virtual environment and install the necessary packages.
  ```bash
  $ python -m venv venv
  
  # For Windows
  $ ./venv/Scripts/activate
  # For Linux
  $ source venv/bin/activate
  
  $ pip install -r requirements.txt
  ```
- Make changes in `main.py` and launch the webapp UI
  ```bash
  streamlit run main.py
  ```
- Visit http://localhost:8501.

## Usage (with Docker)

- Pull the app image and run with `Docker`.
  ```bash
  # Docker run
  $ docker run --rm --device /dev/snd -p 8501:8501 -e GEMINI_API_KEY=<insert-api-key-here> sasquatch06/vink_project:latest  
  ```

### Docker Compose

- The `Docker Compose` config enables a `Watchtower` container to monitor for new images for the app container every 60 minutes.
- In case a new image is detected it is pulled, the old container and image is removed and the app container is updated automatically.

  ```bash
  $ docker compose up -d
  ```

#### Expected Result

  ```bash
  $ docker compose ps
  NAME         IMAGE                             COMMAND                  SERVICE      CREATED          STATUS                            PORTS
  app          sasquatch06/vink_project:latest   "streamlit run main.…"   app          14 seconds ago   Up 4 seconds (health: starting)   0.0.0.0:8501->8501/tcp, :::8501->8501/tcp
  watchtower   containrrr/watchtower:latest      "/watchtower --inter…"   watchtower   14 seconds ago   Up 5 seconds (health: starting)   8080/tcp
  ```

- Visit http://localhost:8501 to view the Streamlit Dashboard for interacting with the webapp.