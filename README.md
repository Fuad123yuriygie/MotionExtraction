# Motion Extraction

A Python-based tool for extracting and visualizing motion from video sources (live camera or video files) using temporal frame differencing.

## Features

- **Real-time Motion Detection**: Highlights changes between the current frame and previous frames.
- **Adjustable Sensitivity**:
  - **Queue Size**: Control the time delay for comparison (adjustable via slider).
  - **Gain**: Control the visual amplification of motion (adjustable via slider).
- **Flexible Source**: Supports webcams, IP cameras, and video files.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Fuad123yuriygie/MotionExtraction.git
    cd MotionExtraction
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    
    pip install -r requirements.txt
    ```

## Usage

Run the main script from the terminal:

```bash
python src/main.py
```

### Command Line Arguments

- `--source`: Specify the video source.
    - Webcam (default): `0`
    - Video File: `path/to/video.mp4`
    - IP Camera: `http://192.168.1.x:8080/video`
- `--queue-size`: Initial frame delay (default: 5).
- `--gain`: Initial contrast gain (default: 10).

### Examples

**Use default webcam:**
```bash
python src/main.py
```

**Use a video file:**
```bash
python src/main.py --source "path/to/my_video.mp4"
```

**Use an IP camera URL:**
```bash
python src/main.py --source "http://192.168.0.101:8080/video"
```

## How It Works

The tool maintains a queue of past frames. It calculates the absolute generated difference between the current live frame and the oldest frame in the queue. This difference is then amplified by a gain factor to make the motion clearly visible.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
