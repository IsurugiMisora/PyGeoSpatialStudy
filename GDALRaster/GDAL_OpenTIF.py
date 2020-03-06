from osgeo import gdal
import os

#读图像文件函数
#输入参数：文件名
#返回参数im_data
def read_img(filename):
    #打开文件
    dataset=gdal.Open(filename)
    #栅格矩阵的列数
    im_width = dataset.RasterXSize
    print('-------栅格矩阵的列数---------')
    print (im_width)
    #栅格矩阵的行数
    im_height = dataset.RasterYSize
    print('-------栅格矩阵的行数---------')
    print (im_height)
    #地图投影信息
    im_proj = dataset.GetProjection()
    print('-------地图投影信息---------')
    print (im_proj)
    #将数据写成数组，对应栅格矩阵
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)
    print('-------影像属性---波段数，行数，列数------')
    print (im_data.shape)
    print('-------栅格矩阵信息---------')
    print (im_data)
    #清除数据集缓存
    del im_data
    #返回获取的参数
    return dataset

#主函数
if __name__ == '__main__':
    #获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(__file__))
    #print('rootPath:'+rootPath)
    #数据文件路径
    dataPath = os.path.abspath(rootPath + r'\data')
    #print('dataPath:'+dataPath)
    #切换目录
    os.chdir(dataPath)
    #读数据并获取影像信息
    data = read_img('S2_20190727San.tif')
