from django import forms                          # 导入 forms：给字段指定 placeholder 等额外属性时使用
from django.shortcuts import render, redirect     # render：渲染模板返回页面；redirect：重定向跳转

from app01.models import PrettyNum                # 靓号表模型
from app01.utils.bootstrap import BootStrapModelForm  # 自动给所有字段加 form-control 样式的表单基类
from app01.utils.pagination import paginate       # 通用分页组件


# ========== 靓号管理：列表 / 搜索 / 编辑 / 删除 ==========

class PrettyModelForm(BootStrapModelForm):          # 继承 BootStrapModelForm，样式自动生成
    class Meta:                                     # 声明对应的模型和字段
        model = PrettyNum                           # 绑定靓号模型
        fields = ["mobile", "price", "level", "status"]  # 表单包含的字段
        widgets = {                                 # form-control 由基类统一添加，这里只写额外属性
            "mobile": forms.TextInput(attrs={"placeholder": "请输入号码"}),  # 号码框，placeholder 是灰色提示文字
            "price": forms.TextInput(attrs={"placeholder": "请输入价格"}),   # 价格框
        }


# 靓号列表（含号码搜索 + 分页）
def pretty_list(request):
    # ===== 1. 搜索：先按条件把数据查出来 =====
    q = request.GET.get("q", "").strip()            # 从网址 ?q=xxx 中取搜索词，取不到给空串，并去掉首尾空格
    data_dict = {}                                  # 存放查询条件的字典（先为空 = 不筛选）
    if q:                                           # 搜索词非空时才加条件，避免空值影响查询
        # 号码包含该词（mobile__contains 相当于 SQL 的 LIKE '%q%'）
        data_dict["mobile__contains"] = q           # 双下划线语法：字段名__contains 表示模糊匹配
    queryset = PrettyNum.objects.filter(**data_dict).order_by("id")  # 条件为空时相当于查询全部；按 id 排序保证每页数据稳定

    # ===== 2. 分页：调用通用分页组件（每页 10 条） =====
    page_obj, pager = paginate(request, queryset)   # 返回当前页数据 + 分页条上下文（prefix/页码/总页数等）

    return render(request, "pretty_list.html", {
        "queryset": page_obj,                       # 当前页的数据（模板里的 for 循环写法不用变）
        "q": q,                                     # 搜索词回填到搜索框
        **pager,                                    # 展开分页上下文：prefix / current_page / prev_page / next_page / total_pages / page_range
    })


# 编辑靓号
def pretty_edit(request, nid):                      # nid：要编辑的靓号 id
    row_object = PrettyNum.objects.filter(id=nid).first()  # 按 id 取要编辑的那一行
    if not row_object:                              # 该靓号不存在
        return redirect("/pretty/list/")            # 回靓号列表页
    if request.method == "GET":
        # GET：把该行数据交给表单回显
        form = PrettyModelForm(instance=row_object)  # instance：用这条记录的值填充表单
        return render(request, "pretty_edit.html", {"form": form})
    # POST：用提交的数据 + instance 更新该行
    form = PrettyModelForm(data=request.POST, instance=row_object)  # 绑定新数据并指明更新目标
    if form.is_valid():                             # 校验通过
        form.save()                                 # 执行 UPDATE 更新这条靓号
        return redirect("/pretty/list/")            # 成功后跳回列表页
    return render(request, "pretty_edit.html", {"form": form})  # 校验失败：带错误回到编辑页


# 删除靓号
def pretty_delete(request, nid):                    # nid：要删除的靓号 id
    PrettyNum.objects.filter(id=nid).delete()       # 按 id 定位并删除该行
    return redirect("/pretty/list/")                # 跳回靓号列表页


# 新建靓号
def pretty_add(request):
    if request.method == "GET":                     # 第一次打开页面
        form = PrettyModelForm()                    # 生成一张空表单
        return render(request, "pretty_add.html", {"form": form})  # 交给模板渲染

    form = PrettyModelForm(data=request.POST)       # 用提交的数据实例化表单
    if form.is_valid():                             # 全部字段校验通过
        form.save()                                 # 执行 INSERT 写入一条新靓号
        return redirect("/pretty/list/")            # 成功后跳回靓号列表页
    return render(request, "pretty_add.html", {"form": form})  # 校验失败则回显错误
