1.startapp keepblog
2.setting.py add keepblog
3.url.py add keepblog.url
4.staic 在全局static下自定义keepblog文件夹存放static(html加载href="{% static 'keepblog/css/base.css' %}">)
5.template 在全局templates目录下新建keepblog （views返回'keepblog/index.html'）