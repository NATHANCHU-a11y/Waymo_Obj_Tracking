import cv2
import numpy as np
from sort.sort import Sort

tracker = Sort()


def track_and_visualize(video_path, results, output_path='output_images/tracked_output.mp4'):
    # Initialize SORT object
    tracker = Sort()

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the video dimensions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Check if there are detections for the current frame
        current_detections = []
        if frame_index < len(results):
            for box in results[frame_index].boxes.xyxy:
                x1, y1, x2, y2 = box
                current_detections.append([x1, y1, x2, y2, 1.0])  # Assume confidence is 1.0
        current_detections = np.array(current_detections)

        # Use SORT to track objects
        track_bbs_ids = tracker.update(current_detections)

        # Draw the tracked objects on the frame
        for track in track_bbs_ids:
            x1, y1, x2, y2, track_id = map(int, track)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, str(track_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        # Write the frame to the video
        out.write(frame)

        # Increment the frame index
        frame_index += 1

    # Release the VideoWriter and VideoCapture
    cap.release()
    out.release()


video_path = "/Users/tianlezhu/Waymo_Obj_Tracking/output_images/output.mp4"
track_and_visualize(video_path, camera1_results)