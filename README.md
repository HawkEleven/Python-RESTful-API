> 初学Python，以此项目来练手，欢迎点赞、留言、交流

### 文件概述
文件 | 说明
---- | ----
pymysql01.py | pymysql数据库处理逻辑
pymysql01.py | 数据爬虫
pymysql01.py | RESTful API
NewBaseModel | 数据模型(供SqlalchemyCommand使用)

### 一、数据库

1、MySQLCommand类涉及到数据库操作，有三个函数:


* **insertData()**：将爬到的数据存入数据库
* **selectAllData()**：通过api接口调用，查询所有列表数据
* **getLastId()**：根据api接口传入的id，返回相应的数据

2、SqlalchemyCommand类：把关系数据库的表结构映射到对象上（ORM）

**MySQLCommand和SqlalchemyCommand，任选其一即可。**

### 二、爬虫
利用BeautifulSoup库爬取“hot-article-img”里面的title，href，img src；并转换为字典存入数据库

	target_url = 'https://www.huxiu.com'
	head = {}
	head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
	target_req = request.Request(url=target_url, headers=head)
	target_response = request.urlopen(target_req)
	target_html = target_response.read().decode('utf-8','ignore')
	
	hot_article_soup = BeautifulSoup(target_html, 'lxml')
	chapters = hot_article_soup.find_all('div', class_='box-moder hot-article hp-hot-article')
	download_soup = BeautifulSoup(str(chapters), 'lxml')
	hot_list = download_soup.select('.hot-article-img')

![image.png](https://upload-images.jianshu.io/upload_images/1338824-815e53c4c584f182.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![image.png](https://upload-images.jianshu.io/upload_images/1338824-5365d8bc06375040.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 三、API

	mysqlCommand = MySQLCommand()
	mysqlCommand.connectMysql()
	news = mysqlCommand.selectAllData()
	
	@app.route('/news/api/v1.0/list', methods=['GET'])
	def get_news():
	    return jsonify({'news': news})

### 使用方法
依次运行三个文件

### 效果
在浏览器输入地址

![image.png](https://upload-images.jianshu.io/upload_images/1338824-db301c5329573ffb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/1338824-fff72eb6251ebf89.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image.png](https://upload-images.jianshu.io/upload_images/1338824-e14d0069560e7b71.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
