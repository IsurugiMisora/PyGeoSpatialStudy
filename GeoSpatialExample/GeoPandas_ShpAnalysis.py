# _*_ coding: cp936 _*_
# ����geopandas
import geopandas,os
from geopandas import GeoSeries
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

#����ʸ������
#�뾶
def ShpBuffer(strVectorFile,radius):
    #geopandas������
    vector = geopandas.read_file(strVectorFile)
    #��ӡ�������������
    print(vector.head())
    #��ӡ�������ͶӰ��Ϣ
    #print(vector.crs)
    #��ӡ�������ͶӰ��Ϣ��init:  һ��Ϊ'ESPG:����'
    print(vector.crs['init'])
    #��ȡ����ʸ�����ݵļ�����Ϣ
    g = GeoSeries(vector['geometry'])

    print('----------------------buffer-------------------------------')
    #�������������뾶Ϊ�������������radius
    buffer=g.buffer(radius)
    #��ͼ�ĵ�ͼ���ã���ɫ��򣬰�ɫ�ڲ�
    base = buffer.plot(color='white',edgecolor='black')
    #ԭʼ�����ʸ���ļ���ͼ����ɫ
    vector.plot(ax=base, color='green')
    #��������ͼ��ͳһ��ͼ���ԱȻ���ǰ����
    plt.show()

    #�������������û����ļ�����Ϣ
    vector_buffer = vector.set_geometry(buffer)
    print(vector_buffer.head())
    #�����������ʸ�����ݶ���ͶӰ=����ʸ���ļ�ͶӰ
    vector_buffer.crs=vector.crs['init']
    #��ȡ�ļ�������������׺����
    shorFilename = strVectorFile.split('.')[0]
    #�����������ʸ���ļ���
    bufferVectorFile= shorFilename+"_buffer_"+str(radius)+"km.shp"
    #�������ļ����ָ���ļ���
    vector_buffer.to_file(bufferVectorFile,'ESRI Shapefile')

def overlay():
    polys1 = geopandas.GeoSeries([Polygon([(0,0), (2,0), (2,2), (0,2)]),
                                  Polygon([(2,2), (4,2), (4,4), (2,4)])])
    polys2 = geopandas.GeoSeries([Polygon([(1,1), (3,1), (3,3), (1,3)]),
                                  Polygon([(3,3), (5,3), (5,5), (3,5)])])
    df1 = geopandas.GeoDataFrame({'geometry': polys1, 'df1':[1,2]})
    df2 = geopandas.GeoDataFrame({'geometry': polys2, 'df2':[1,2]})

    #ԭʼ������ʾ
    ax = df1.plot(color='red')
    df2.plot(ax=ax, color='green', alpha=0.5)
    plt.title('data')

    #����
    res_union = geopandas.overlay(df1, df2, how='union')

    ax = res_union.plot(alpha=0.5, cmap='tab10')
    df1.plot(ax=ax, facecolor='none', edgecolor='k')
    df2.plot(ax=ax, facecolor='none', edgecolor='k')
    plt.title('union')

    #�ཻ
    res_intersection = geopandas.overlay(df1, df2, how='intersection')

    ax = res_intersection.plot(alpha=0.5, cmap='tab10')
    df1.plot(ax=ax, facecolor='none', edgecolor='k')
    df2.plot(ax=ax, facecolor='none', edgecolor='k')
    plt.title('intersection')

    #����ȡ��
    res_symdiff = geopandas.overlay(df1, df2, how='symmetric_difference')

    ax = res_symdiff.plot(alpha=0.5, cmap='tab10')
    df1.plot(ax=ax, facecolor='none', edgecolor='k')
    df2.plot(ax=ax, facecolor='none', edgecolor='k')
    plt.title('symmetric_difference')
    plt.show()



#���ӷ���
def interacte(shp_a,shp_b):
    df_a = geopandas.read_file(shp_a,encoding ="gb18030")
    print(df_a)
    df_b = geopandas.read_file(shp_b,encoding ="gb18030")
    print(df_b)
    ax = df_a.plot(color='white', edgecolor='black')
    df_b.plot(ax=ax, color='green',edgecolor='red', alpha=0.5)
    #plt.show()
    #������B����һ���ֶ�same����������ͬ������ֵdissolveall��Ϊ�ں�ȫ��Ҫ����׼��
    df_b['same'] = 'dissolveall'
    #��ȫ��Ҫ���ں�
    df_b_dissolve = df_b.dissolve(by='same')
    df_b_dissolve.plot(alpha=0.5, cmap='tab10')
    # plt.show()
    print('------------dissolve���---------')
    print(df_b_dissolve.head())

    res_intersection = geopandas.overlay(df_a, df_b_dissolve, how='intersection')
    print('-----------------------�ཻ���----------------------------')
    print(res_intersection)
    ax = res_intersection.plot(alpha=0.5, cmap='tab10')

    df_b_dissolve.plot(ax=ax, alpha=0.5,facecolor='green')
    df_a.plot(ax=ax, facecolor='red',alpha=0.7 )
    plt.title('intersection')
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

    #ShpBuffer(strVectorFile,0.1)
    shp_a='GIAHS_buffer_0.1km.shp'
    shp_b='SpecialTown_buffer_1km.shp'
    interacte(shp_a,shp_b)
    #overlay()