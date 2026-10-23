from django import forms                          # 导入 forms：给个别字段指定特殊控件、追加自定义字段时使用
from django.shortcuts import render, redirect     # render：渲染模板返回页面；redirect：重定向跳转

from app01.models import UserInfo                 # 员工表模型
from app01.utils.bootstrap import BootStrapModelForm  # 自动给所有字段加 form-control 样式的表单基类


# ========== 员工（用户）管理：ModelForm 方式 ==========

class UserModelForm(BootStrapModelForm):            # 继承 BootStrapModelForm，样式自动生成，无需逐个写字段控件
    # 自定义字段（不属于 UserInfo 模型，仅用于演示 ModelForm 可追加自定义字段）
    xx = forms.CharField(label="自定义字段", required=False)  # label 是页面上显示的名称；required=False 表示可以不填

    class Meta:                                     # Meta 里声明"这个表单对应哪个模型、包含哪些字段"
        model = UserInfo                            # 绑定员工模型，表单字段从它自动生成
        # 表单包含的字段（关联字段 depart 会自动生成下拉框，无需手动写循环）
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart", "xx"]  # 前几个来自模型，xx 是上面自定义的
        widgets = {                                 # widgets：只需声明有特殊需求的控件；form-control 样式由基类统一添加
            "create_time": forms.DateInput(attrs={"type": "date"}),  # 入职时间：日期选择器
        }


# 新建员工
def user_add(request):
    if request.method == "GET":                     # 第一次打开页面
        form = UserModelForm()                      # 生成一张空表单（不带任何数据）
        return render(request, "user_add.html", {"form": form})  # 把表单对象交给模板，模板里循环渲染出输入框

    form = UserModelForm(data=request.POST)         # 用提交的数据实例化表单（data 参数表示绑定用户输入）
    if form.is_valid():                             # is_valid()：触发全部字段的校验，全部通过返回 True
        form.save()                                 # 校验通过，保存到数据库（自动执行 INSERT 新增一条）
        # 保存成功后重新给一张空表单，并提示成功
        return render(request, "user_add.html", {"form": UserModelForm(), "success": "添加成功"})  # 不跳转，方便连续录入
    return render(request, "user_add.html", {"form": form})  # 校验失败则回显错误：模板会自动显示每个字段的错误提示


# 员工列表
def user_list(request):
    queryset = UserInfo.objects.all()               # 查询员工表所有数据
    return render(request, "user_list.html", {"queryset": queryset})  # 数据交给列表页模板渲染


# 编辑员工
def user_edit(request, nid):                        # nid：网址中捕获的员工 id
    """ 编辑用户 """
    # 根据id获取某一行对象
    row_object = UserInfo.objects.filter(id=nid).first()  # 按 id 查出要编辑的员工对象，查不到为 None
    if not row_object:                              # 该员工不存在
        return redirect("/user/list/")              # 直接回员工列表页

    if request.method == "GET":
        # GET：把该行对象交给表单（instance），字段自动回显在输入框中
        form = UserModelForm(instance=row_object)   # instance 参数：告诉表单"用这条记录的值来填充"
        return render(request, "user_edit.html", {"form": form})

    # instance=row_object 表示更新到某一行，否则 form.save() 会新增一条数据
    form = UserModelForm(data=request.POST, instance=row_object)  # data 是新输入，instance 指明更新哪条记录
    if form.is_valid():                             # 校验提交的数据
        # 默认保存用户输入的所有数据；如需在用户输入以外增加值：form.instance.字段名 = 值
        form.save()                                 # 自动执行 UPDATE 更新该行
        return redirect("/user/list/")              # 保存成功，跳回员工列表页
    return render(request, "user_edit.html", {"form": form})  # 校验失败：带错误信息回到编辑页
