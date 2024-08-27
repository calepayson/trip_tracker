import cv2
import sys
from mouse import MouseMetadata
from variables import BODY_PART_LABELS, CENTER_RECT, FRAMES_PER_SECOND

'''
Updates global variables pertaining to the video
'''
def update_video_variables(video_file_name):
    # Open the source file
    source = cv2.VideoCapture(video_file_name)
    # If the file was not opened...
    if not source.isOpened():
        # Print an error
        print(f"Error opening video file: {video_file_name}")
        # And exit the program
        sys.exit(1)
    # Update frames per second
    FRAMES_PER_SECOND = int(source.get(cv2.CAP_PROP_FPS))
    # Close the source file
    source.release()

def test_program_with_video(video_file_name: str, mouse: MouseMetadata):
    # Open the source file
    source = cv2.VideoCapture(video_file_name)
    # If the file was not opened...
    if not source.isOpened():
        # Print an error
        print(f"Error opening video file: {video_file_name}")
        # And exit the program
        sys.exit(1)

    # Read metadata from the video
    frame_height = int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(source.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(source.get(cv2.CAP_PROP_FPS))

    # Get the name for an output file
    output_file_name = f"{video_file_name[:-4]}_annotated.avi"
    # Initialize an output file using the metadata
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
            output_file_name, 
            fourcc, 
            fps, 
            (frame_width, frame_height))
    
    # Initialize a counter to keep track of the frame index
    frame_index = 0

    # For each frame in the file...
    while source.isOpened():
        ret, frame = source.read()
        if not ret:
            break

        # Draw the center rectangle onto the video
        cv2.rectangle(
                frame,
                (CENTER_RECT.x_min, CENTER_RECT.y_min),
                (CENTER_RECT.x_max, CENTER_RECT.y_max),
                (0, 255, 0),
                2)

        # For each body part...
        for part in BODY_PART_LABELS:
            # Get coordinates
            x_coord = int(mouse.data[part].iloc[frame_index]['x'])
            y_coord = int(mouse.data[part].iloc[frame_index]['y'])
            # Draw a dot on the current frame at those coordinates
            cv2.circle(
                    frame,
                    (x_coord, y_coord),
                    3,
                    (0, 0, 255), 
                    -1)

        # Increment the frame index
        frame_index += 1

        # Comment/uncomment to display the frame with the annotations
        cv2.imshow('Video with tracking', frame)

        # Write the frame to the output video file
        out.write(frame)

        # If you delete this line the program will crash. I have no idea why.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    source.release()
    out.release()
    cv2.destroyAllWindows()

