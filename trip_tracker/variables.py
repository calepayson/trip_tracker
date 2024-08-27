from rectangle import Rectangle

# The name of the h5 file containing the mouse tracking coordinates
DATA_FILE_NAME = 'mouse_trip.h5'

# The name of video-file with the recording of the mouse trip
VIDEO_FILE_NAME = 'mouse_trip.avi'

# The fps of the video (and data)
FRAMES_PER_SECOND = 30

# The minimum viable likelihood for coordinates (any coordinates with a
# probability less than this will be interpolated)
LIKELIHOOD_THRESHOLD = 0.95

# The dimensions of the center rectangle
CENTER_RECT = Rectangle(
        x_min=475,
        y_min=305,
        x_max=845,
        y_max=680,)

# The labels for each body part in the data set (NOTE: order matters!)
BODY_PART_LABELS = [
        'nose', 
        'head', 
        'neck', 
        'leftear', 
        'rightear', 
        'body', 
        'tailbase']

# The labels for each coordinate column in the data set (NOTE: order matters!)
COORDINATE_LABELS = [
        'x', 
        'y', 
        'likelihood']
