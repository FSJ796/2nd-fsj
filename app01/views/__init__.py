# views 包（相当于以前的 views.py 本体）：把三个子文件导入进来，它们正式成为 views 的子模块
# 导入后既可以用 views.depart.depart_list 访问，也可以单独 from app01.views import depart
from . import depart, pretty, user
