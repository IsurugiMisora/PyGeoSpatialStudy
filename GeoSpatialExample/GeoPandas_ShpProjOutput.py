# _*_ coding: cp936 _*_
# ����geopandas
import geopandas,os
from fiona.crs import from_epsg
from geopandas import GeoSeries
import matplotlib.pyplot as plt

#��EPSG����תͶӰ
def TransferProjByEPSG(strVectorFile,code):
    vector = geopandas.read_file(strVectorFile)
    result = vector.to_crs(from_epsg(code))
    print('תͶӰ���ͶӰ��Ϣ��'+str(result.crs))
    return result

#���ʸ���ļ�
def OutputShp(vector,strVectorFile):

    #�������ļ����ָ���ļ���
    vector.to_file(strVectorFile,'ESRI Shapefile',encoding ="GB2312")
    #ԭʼ�����ʸ���ļ���ͼ����ɫ
    vector.plot(color='green')
    #��������ͼ��ͳһ��ͼ���ԱȻ���ǰ����
    plt.show()

#������
if __name__ == '__main__':

    #��ȡ���̸�Ŀ¼��·��
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #print('rootPath:'+rootPath)
    #�����ļ�·��
    dataPath = os.path.abspath(rootPath + r'\ShpData')
    #print('dataPath:'+dataPath)
    #�л�Ŀ¼
    os.chdir(dataPath)
    strVectorFile ="GIAHS.shp"
    result=TransferProjByEPSG(strVectorFile,3857)
    strVectorFile_3857="GIAHS3857.shp"
    OutputShp(result,strVectorFile_3857)
    strVectorFile_4326="GIAHS4326.shp"
    result_4326=TransferProjByEPSG(strVectorFile_3857,4326)
    OutputShp(result_4326,strVectorFile_4326)
