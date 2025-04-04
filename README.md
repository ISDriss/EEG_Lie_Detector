# EEG Lie Detector

This project is an EEG-based lie detection system. It streams EEG data, allows users to record sessions, and predicts whether a statement is a truth or a lie based on EEG data.

## Features

- **Real-time EEG Data Streaming**: Streams EEG data from a connected device.
- **Recording**: Allows users to record EEG data for a specified duration.
- **Interactive Menu**: Provides options to start recording or stop streaming during the session.
- **Lie Detection**: Uses a trained model to predict whether the EEG data corresponds to a truth or a lie.

## Requirements

- Python 3.8+
- Required Python libraries (install via `pip`):
    - `pip install -r requirements.txt`

## Usage

1. Start the program by running the `setup()` function.
2. Use the interactive menu to:
   - Start a recording by specifying the duration.
   - Stop the streaming process.
3. Use the `predict.py` script to analyze recorded EEG data and predict whether it corresponds to a truth or a lie.

## File Structure

- **data/**: Contains recorded EEG data files (ignored by version control).
- **stream()**: Handles real-time EEG data streaming.
- **record()**: Records EEG data to a file.
- **view()**: Displays EEG data in real-time.
- **predict.py**: Processes EEG data and predicts truth or lie using a trained model.

## Notes

- Recorded files are saved in the `data/` folder and are ignored by Git.
- Ensure your EEG device is properly connected before starting the program.
- Replace the placeholder file path in `predict.py` with the actual path to your EEG data file.

## License

This project is for educational purposes and is not intended for medical or legal use.