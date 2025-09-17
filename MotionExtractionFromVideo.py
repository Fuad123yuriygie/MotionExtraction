import queue
import cv2
import numpy as np

# Replace with your video file path
video_path = 'Mountains.mp4'

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open IP webcam stream.")
    exit()

queueFrame = queue.Queue()
queueSize = 5

while True:
    ret, frame = cap.read()
    if not ret:
        break


    # Calculate absolute color difference from first element of the queue
    if not queueFrame.empty():
        abs_diff_frame = cv2.absdiff(frame, queueFrame.queue[0])
        # Multiply by 10 and normalize to 0-255
        abs_diff_frame = abs_diff_frame.astype(np.float32) * 1
        abs_diff_frame = np.clip(abs_diff_frame, 0, 255)
        abs_diff_frame = abs_diff_frame.astype(np.uint8)
    
    else:
        abs_diff_frame = frame

    # Display the absolute difference frame
    cv2.imshow('Absolute Color Difference (2 frames ago)', abs_diff_frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    
    queueFrame.put(frame)

    # Update previous frames
    while queueFrame.qsize() > queueSize:
        queueFrame.get()    

cap.release()
cv2.destroyAllWindows()