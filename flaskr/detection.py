import os

import numpy
import paddle.inference as paddle_infer
import cv2


def predict(image):
    # 创建 config，并设置预测模型路径
    config = paddle_infer.Config("static/model/faster_rcnn_r50_vd_fpn_ssld_2x_coco/model.pdmodel","static/model/faster_rcnn_r50_vd_fpn_ssld_2x_coco/model.pdiparams")

    # 根据 config 创建 predictor
    predictor = paddle_infer.create_predictor(config)
    # 获取输入 Tensor
    input_names = predictor.get_input_names()
    input_tensor = predictor.get_input_handle(input_names[0])

    # 从 CPU 获取数据，设置到 Tensor 内部
    input_tensor.copy_from_cpu(image)

    # 执行预测
    predictor.run()

    # 获取输出 Tensor
    output_names = predictor.get_output_names()
    output_tensor = predictor.get_output_handle(output_names[0])
    output_data = output_tensor.copy_to_cpu()  # numpy.ndarray类型

    # 释放中间Tensor
    predictor.clear_intermediate_tensor()

    # 释放内存池中的所有临时 Tensor
    predictor.try_shrink_memory()


if __name__ == '__main__':
    model_cfg = "./model/faster_rcnn_r50_vd_fpn_ssld_2x_coco"
    image = "./static/img/people/00002.jpg"
    use_gpu = False
    os.system("python infer.py --model_dir={} --image_file={} --use_gpu={} --threshold=0".format(model_cfg, image, use_gpu))
