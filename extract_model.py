import bz2
import os

# Path to the compressed file
compressed_file = "shape_predictor_model/shape_predictor_68_face_landmarks.dat.bz2"
output_file = "shape_predictor_model/shape_predictor_68_face_landmarks.dat"

# Extract the file
with bz2.open(compressed_file, 'rb') as source, open(output_file, 'wb') as dest:
    dest.write(source.read())

# Remove the compressed file
os.remove(compressed_file)

print("Model file extracted successfully!") 