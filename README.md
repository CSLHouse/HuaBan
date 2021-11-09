1.首先需要下载Chromedriver，地址：http://npm.taobao.org/mirrors/chromedriver/，下载后得到的是一个chromedriver.exe文件。

2.将chromedriver.exe拷贝至谷歌浏览器目录（如 C:\Program Files(x86)\Google\Chrome\Application）以及python根目录（C:\Python27）。

3.将谷歌浏览器环境变量添加到PATH中（C:\Program Files(x86)\Google\Chrome\Application）。



然后好像这样就解决了，但是我试了N遍，好像都不可以，结果有个学员找到了答案：还需要在Python的根目录下将这个文件拷贝进去(如 D:\Python37)。


参考文档：https://akynazh.top/2021/07/29/python%E7%88%AC%E5%8F%96%E8%8A%B1%E7%93%A3%E7%BD%91%E4%BB%BB%E6%84%8F%E9%9D%A2%E6%9D%BF%E5%9B%BE%E7%89%87/