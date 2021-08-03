import cv2
import os
import os.path as osp


def img2video(img_dir, img_size, video_dir, fps):
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')  # opencv3.0
    videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)

    for idx in sorted(os.listdir(img_dir)):
        img = osp.join(img_dir, idx)
        frame = cv2.imread(img)
        # print(frame.shape)  # h, w, c (480, 640, 3)
        videoWriter.write(frame)
        print('从文件中加载图片：' + idx)

    videoWriter.release()
    print('转换完成！')


if __name__ == '__main__':
    img_dir = 'C:\\Users\\22276\\Downloads\\mot_images\\mot_images\\0'
    # par_dir = osp.dirname(img_dir)
    video_path = osp.join('./', 'output.mp4')

    fps = 25  # 帧率为25帧，一秒读入25张图片
    img_size = (1920, 1080)  # w, h
    img2video(img_dir=img_dir, img_size=img_size, video_dir=video_path, fps=fps)
