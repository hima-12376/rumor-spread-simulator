import cv2
import numpy as np

def detect_ai_video(uploaded_video):

    with open("uploaded_video.mp4", "wb") as f:
        f.write(uploaded_video.read())

    cap = cv2.VideoCapture("uploaded_video.mp4")

    prev_gray = None
    motion_vals = []
    texture_vals = []
    edge_vals = []

    frame_count = 0

    while frame_count < 30:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # -------- TEXTURE --------
        texture_vals.append(np.var(gray))

        # -------- EDGES --------
        edges = cv2.Canny(gray,100,200)
        edge_vals.append(np.mean(edges))

        # -------- MOTION --------
        if prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                prev_gray, gray,
                None,
                0.5,3,15,3,5,1.2,0
            )
            mag,_ = cv2.cartToPolar(flow[...,0],flow[...,1])
            motion_vals.append(np.mean(mag))

        prev_gray = gray
        frame_count += 1

    cap.release()

    motion_std = np.std(motion_vals)
    texture_mean = np.mean(texture_vals)
    edge_mean = np.mean(edge_vals)

    ai_score = 0

    if motion_std < 0.15:
        ai_score += 1
    if texture_mean < 400:
        ai_score += 1
    if edge_mean < 15:
        ai_score += 1

    if ai_score >= 2:
        return "❌ Likely AI Generated"
    else:
        return "✅ Likely Real"