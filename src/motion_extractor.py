import cv2
import numpy as np
import queue

class MotionExtractor:
    """
    Extracts motion from a video stream by comparing the current frame
    with a frame from the past (delayed by a queue).
    """

    def __init__(self, source=0, queue_size=1, gain=10):
        """
        Initialize the MotionExtractor.

        Args:
            source (str or int): Video source. Can be an integer (camera index), 
                                 a string representing a file path, or a URL.
            queue_size (int): Number of frames to delay for comparison.
            gain (float): Multiplier for the difference to make motion more visible.
        """
        self.source = source
        self.queue_size = queue_size
        self.gain = gain
        self.frame_queue = queue.Queue()
        
        # Determine if source is an integer (camera index)
        if isinstance(source, str) and source.isdigit():
            self.source = int(source)

        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open video source '{self.source}'.")

        # Window setup
        self.window_name = 'Motion Extraction'
        cv2.namedWindow(self.window_name)
        
        # Trackbar callback (does nothing but required)
        def nothing(x):
            pass

        # Interactive trackbars
        cv2.createTrackbar('Queue Size', self.window_name, self.queue_size, 100, nothing)
        cv2.createTrackbar('Gain', self.window_name, self.gain, 50, nothing)

    def run(self):
        """
        Main loop to process frames.
        """
        print(f"Starting motion extraction on source: {self.source}")
        print("Press 'q' to quit.")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("End of stream or error reading frame.")
                break

            # Update parameters from trackbars
            current_queue_size = cv2.getTrackbarPos('Queue Size', self.window_name)
            current_gain = cv2.getTrackbarPos('Gain', self.window_name)
            
            # Use at least 1 for valid trackbar values
            self.queue_size = max(0, current_queue_size)
            self.gain = max(1, current_gain)

            # Process frame
            processed_frame = self.process_frame(frame)

            # Display
            cv2.imshow(self.window_name, processed_frame)

            # Enqueue current frame
            self.frame_queue.put(frame)

            # Maintain queue size: Remove old frames if queue is too big
            while self.frame_queue.qsize() > self.queue_size:
                self.frame_queue.get()

            # Exit condition
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        self.cleanup()

    def process_frame(self, frame):
        """
        Calculates the absolute difference between the current frame and the
        oldest frame in the queue.
        """
        if not self.frame_queue.empty():
            # Compare with the oldest frame in the queue (the one about to be popped if full)
            # Actually, `queue.queue[0]` gives the head of the queue (oldest item).
            old_frame = self.frame_queue.queue[0]
            
            abs_diff = cv2.absdiff(frame, old_frame)
            
            # Apply gain and normalize
            abs_diff = abs_diff.astype(np.float32) * self.gain
            abs_diff = np.clip(abs_diff, 0, 255)
            abs_diff = abs_diff.astype(np.uint8)
            
            return abs_diff
        else:
            # If queue is empty, just return the original frame (or black)
            return frame

    def cleanup(self):
        """
        Release resources.
        """
        self.cap.release()
        cv2.destroyAllWindows()
