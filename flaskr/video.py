import math
import os
import time

import cv2
import numpy as np
from flask import (
    Blueprint, render_template, request, session,
    Response)

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.model.detection import create_detection, predict_video

bp = Blueprint('video', __name__, url_prefix='/video')

BASE = 'flaskr/static/'
UPLOAD_FOLDER = 'upload/'


@bp.route('/video/<int:page>', methods=('GET', 'POST'))
@login_required
def video(page=0):
    db = get_db()
    total_count = db.execute("select count(video_id) from video where create_user = '{}'".format(
        session.get('user_id'))).fetchone()[0]
    pages = math.ceil(total_count / 6)
    if page == -1:
        page = pages - 1

    sql = "select * from video where create_user = '{}'  order by video_id limit 6 offset {};".format(
        session.get('user_id'), page)
    video_list = db.execute(sql).fetchall()

    pages = math.ceil(total_count / 6)
    return render_template('video/video.html', video_list=video_list, total_count=total_count, pages=pages,
                           now_page=page)


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    return render_template('video/upload.html')


@bp.route('/delete/<int:video_id>', methods=('GET', 'POST'))
@login_required
def remove(video_id=None):
    if video_id is not None:
        # 先验证
        db = get_db()
        sql = "select * from video where video_id = {} and create_user= {}".format(video_id, session.get('user_id'))
        videos = db.execute(sql).fetchone()
        if videos is not None:
            try:
                # 先删文件
                file_dir = os.path.join(os.getcwd(), BASE + videos[2])
                os.remove(file_dir)
            except OSError:
                print("文件被占用")
            # 删数据库
            sql_1 = "delete from video where video_id = {} and create_user= {}".format(video_id, session.get('user_id'))
            db.execute(sql_1)
            db.commit()
    return {
        'delete': True
    }


@bp.route('/realtimeVideo', methods=('GET', 'POST'))
@login_required
def realtimeVideo():
    db = get_db()
    video_id = request.args.get("video_id")
    sql = "select * from video where video_id = {} and create_user= {}".format(video_id, session.get('user_id'))
    videos = db.execute(sql).fetchone()

    return render_template('video/realtimeVideo.html',video=videos)


@bp.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    # 获取数据库最后一个视频id
    db = get_db()
    sql = "select video_id from video ORDER BY video_id DESC "
    pre = db.execute(sql).fetchone()
    if pre is None:
        pre = 0
    else:
        pre = pre[0]
        print(pre)
        pre += 1
    f = request.files['file']
    print(f)
    # 保存文件
    new_f = f.filename.split('.')[-1]

    file_dir = os.path.join(os.getcwd(), BASE + UPLOAD_FOLDER)
    if not os.path.exists(file_dir):
        print("创建文件:{}".format(file_dir))
        os.makedirs(file_dir)
    file_path = os.path.join(file_dir, str(pre) + '.' + new_f)

    # 保存数据库
    error = None

    if error is None:
        db.execute(
            'INSERT INTO video (name, url,create_user,create_date) VALUES (?, ?,?,?)',
            (f.filename, UPLOAD_FOLDER + str(pre) + '.' + new_f, session.get('user_id'),
             time.strftime("%Y-%m-%d", time.localtime()))
        )
        db.commit()
    f.save(file_path)
    return render_template('video/upload.html')

# detector = create_detection()


class VideoCamera(object):
    def __init__(self,video_url):
        # 打开视频
        print(video_url)
        self.cap = cv2.VideoCapture(video_url)

    # 退出程序释放摄像头
    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        else:
            return None


def gen(camera):
    while True:
        frame = camera.get_frame()
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg

        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

draw = True


@bp.route('/video_feed')
def video_feed():
    url = str(request.args.get("url"))
    return Response(gen(VideoCamera(video_url="flaskr/static/"+url)), mimetype='multipart/x-mixed-replace; boundary=frame')

