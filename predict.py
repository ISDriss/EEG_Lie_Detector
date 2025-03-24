import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
from scipy.signal import spectrogram
from sklearn.preprocessing import StandardScaler

# 🔹 Constants
EEG_CHANNELS = ["TP9", "AF7", "AF8", "TP10"]
MODEL_PATH = "models\eeg_lie_detector2025-03-15.23.15.keras"  # Make sure this file exists
IMG_SIZE = (224, 224)  # Match model input size

# 🔹 Load trained Keras model
def load_model(model_path):
    return tf.keras.models.load_model(model_path)

model = load_model(MODEL_PATH)

# 🔹 Convert EEG to Spectrogram Image
def eeg_to_spectrogram(eeg_data, fs=256):
    """Convert EEG signals to a spectrogram image."""
    fig, axes = plt.subplots(1, len(EEG_CHANNELS), figsize=(10, 3))

    for i, channel in enumerate(EEG_CHANNELS):
        f, t, Sxx = spectrogram(eeg_data[:, i], fs=fs, nperseg=128, noverlap=64)
        axes[i].imshow(10 * np.log10(Sxx + 1e-10), aspect='auto', cmap='jet')
        axes[i].axis('off')

    # Save as image
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())  # Convert to numpy
    plt.close(fig)

    # Resize to 224x224 and convert to 3-channel format
    img = cv2.resize(img, IMG_SIZE)  # Resize to match model input size
    img = img[:, :, :3]  # Ensure 3 channels
    return img

# 🔹 Preprocess EEG data
def preprocess_eeg(csv_file):
    """Load EEG CSV, standardize, and convert to spectrogram image."""
    df = pd.read_csv(csv_file)

    # Ensure required EEG channels exist
    if not all(ch in df.columns for ch in EEG_CHANNELS):
        raise ValueError(f"Missing EEG channels in {csv_file}")

    eeg_data = df[EEG_CHANNELS].values  # Extract EEG values

    # Standardize using current sample (since no training sample)
    scaler = StandardScaler()
    eeg_data = scaler.fit_transform(eeg_data)

    # Convert to spectrogram image
    spectrogram_img = eeg_to_spectrogram(eeg_data)

    # Reshape for model input (1, 224, 224, 3)
    spectrogram_img = np.expand_dims(spectrogram_img, axis=0)  # Add batch dimension

    return spectrogram_img

# 🔹 Load EEG sample and predict
csv_file = "data/false/1_coeur_oui.csv"  # Replace with your actual EEG file
eeg_input = preprocess_eeg(csv_file)

# 🔹 Predict truth or lie
prediction = model.predict(eeg_input, verbose=0)
lie_prob = prediction[0][0]  # Assuming binary classification

if lie_prob > 0.5:
    print("🟥 Lie detected! ({:.2f} confidence)".format(lie_prob))
else:
    print("🟩 Truth detected! ({:.2f} confidence)".format(1 - lie_prob))
