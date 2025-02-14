import os

from os import makedirs
from os.path import exists

from PIL import Image


def crop(input_img_path, output_img_path, crop_w, crop_h):
    """指定宽高从中心裁剪图片

    Args:
        input_img_path (_type_): _description_
        output_img_path (_type_): _description_
        crop_w (_type_): _description_
        crop_h (_type_): _description_
    """
    image = Image.open(input_img_path)
    x_max = image.size[0]
    y_max = image.size[1]
    mid_point_x = int(x_max / 2)
    mid_point_y = int(y_max / 2)
    right = mid_point_x + int(crop_w / 2)
    left = mid_point_x - int(crop_w / 2)
    down = mid_point_y + int(crop_h / 2)
    up = mid_point_y - int(crop_h / 2)
    BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN = left, up, right, down
    box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
    crop_img = image.crop(box)
    crop_img.save(output_img_path)

    
def crop1(input_img_path, output_img_path, crop_l, crop_r, crop_u, crop_d):
    """指定上下左右需裁剪的图片宽度

    Args:
        input_img_path (_type_): _description_
        output_img_path (_type_): _description_
        crop_l (_type_): _description_
        crop_r (_type_): _description_
        crop_u (_type_): _description_
        crop_d (_type_): _description_
    """
    image = Image.open(input_img_path)
    x_max = image.size[0]
    y_max = image.size[1]
    left = crop_l
    right = x_max - crop_r
    up = crop_u
    down = y_max-crop_d
    BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN = left, up, right, down
    box = (BOX_LEFT, BOX_UP, BOX_RIGHT, BOX_DOWN)
    crop_img = image.crop(box)
    crop_img.save(output_img_path)

def create_directory(directory):
    if not exists(directory):
        makedirs(directory)
        print(f"创建目录: {directory}")

if __name__ == '__main__':
    dataset_dir = "TSMaster开发从入门到精通webp/"  # 图片路径
    output_dir = 'out/'  # 输出路径
    crop_left = 70
    crop_right = 70
    crop_up = 100
    crop_down = 100
    # crop_w = 300  # 裁剪图片宽
    # crop_h = 300  # 裁剪图片高
    # 获得需要转化的图片路径并生成目标路径
    image_filenames = [(os.path.join(dataset_dir, x), os.path.join(output_dir, x))
                       for x in os.listdir(dataset_dir)]
    create_directory(output_dir)
    # 转化所有图片
    for path in image_filenames:
        # crop(path[0], path[1], crop_w, crop_h)
        print(path)
        crop1(path[0], path[1], crop_left, crop_right, crop_up, crop_down)