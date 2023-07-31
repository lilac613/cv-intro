from lane_detection import *
from lane_following import *

def render_frame(frame):
    sliced = frame[ int(frame.shape[0] / 2) : frame.shape[0]]
    height = sliced.shape[0]
    width = sliced.shape[1]
    gray = cv2.cvtColor(sliced, cv2.COLOR_BGR2GRAY)
    blurredimg = cv2.GaussianBlur(gray,(9,9),0)
    ret,bw_image = cv2.threshold(blurredimg, 140, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(bw_image,50, 200, apertureSize=3)
    lines = detect_lines(frame,edges,50,200, 3, 100, 10)

    if len(lines)>1:
        lanes = detect_lanes(lines)
        center_lane = get_lane_center(lanes)
        center_line = get_center_line(center_lane[0])
        (strafe_direction,turn_direction,turn_in_degrees,direction) = recommend_direction(center_line.get_x_intercept(),center_line.get_slope(),center_line,width)
        text = f"The AUV should move {strafe_direction} and {turn_direction} by {turn_in_degrees} {direction}"

        frame = draw_lines(frame, [center_line], (0,0,255), offset = True)
        frame = cv2.putText(frame, text, (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
    return frame

if __name__ == "__main__":
    cap = cv2.VideoCapture('AUV_Vid.mkv')
    ret, frame1 = cap.read()
    height, width, layers = frame1.shape
    size = (width, height)
    out = cv2.VideoWriter("rendered_video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, size)

    count = 0 # the number of frames since the last    
    while ret:
        ret, frame = cap.read()
        if not ret:
            break

        print(f"now on frame {count}...")
        frame = render_frame(frame)
            
        out.write(frame)

        count += 1

    cap.release()
    out.release()
    print("Finished rendering the video.")