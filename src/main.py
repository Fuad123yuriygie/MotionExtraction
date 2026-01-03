import argparse
from motion_extractor import MotionExtractor

def main():
    parser = argparse.ArgumentParser(description="Motion Extraction Tool")
    parser.add_argument('--source', type=str, default='0', 
                        help='Video source: Camera index (e.g., 0), file path, or URL.')
    parser.add_argument('--queue-size', type=int, default=5, 
                        help='Initial size of the frame delay queue.')
    parser.add_argument('--gain', type=int, default=10, 
                        help='Initial gain multiplier for difference visibility.')
    
    args = parser.parse_args()

    try:
        extractor = MotionExtractor(source=args.source, queue_size=args.queue_size, gain=args.gain)
        extractor.run()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
