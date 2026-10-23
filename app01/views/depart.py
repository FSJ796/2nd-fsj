from django.shortcuts import render, redirect     # render：渲染模板返回页面；redirect：重定向，让浏览器跳转到另一个网址

from app01.models import Department, UserInfo     # 部门表模型、员工表模型


# ==================== 部门管理 ====================

# 部门列表页
def depart_list(request):                           # request：Django 封装好的请求对象，包含用户发来的所有信息
    depart_data = Department.objects.all()          # 查询部门表所有数据，返回 QuerySet（类似列表的对象）
    user_data = UserInfo.objects.all()              # 查询员工表所有数据（供页面下方"员工信息"面板使用）
    return render(request, "depart_list.html", {"depart_list": depart_data, "user_data": user_data})  # 把两组数据交给模板渲染成 HTML 返回给浏览器


# 新建部门
def depart_add(request):
    if request.method == "GET":                     # 判断请求方式：GET 表示第一次打开页面（不是提交表单）
        # GET 请求：只返回空的表单页面
        return render(request, "depart_add.html")   # 渲染新建部门的空白表单页

    # POST 请求：走到这里说明用户点了"提交"，开始接收表单数据
    title = request.POST.get("title", "").strip()   # 从提交数据中取 title 字段（取不到给空字符串），并去掉首尾空格
    errors = {}                                     # 定义空字典，收集校验不通过时的错误信息

    # 验证规则 1：标题不能为空
    if not title:                                   # 空字符串在 Python 中为假，说明用户没填标题
        errors["title"] = "标题不能为空"
    # 验证规则 2：长度限制
    elif len(title) > 32:                           # elif：上面的条件不成立时才检查这里
        errors["title"] = "标题长度不能超过32个字符"
    # 验证规则 3：标题不能重复
    elif Department.objects.filter(title=title).exists():  # filter 按条件查库，exists() 判断数据库里是否已存在同名部门
        errors["title"] = "该标题已存在"

    if errors:                                      # errors 字典非空，说明至少有一条校验没通过
        # 有错误：返回表单页，带上错误信息并保留已输入的内容（回显）
        return render(request, "depart_add.html", {"errors": errors, "title": title})

    Department.objects.create(title=title)  # 校验全部通过：执行 INSERT，往部门表写入一条新记录
    return redirect("/depart/list/")        # 重定向跳回部门列表页（地址栏会变成 /depart/list/）


# 编辑部门
def depart_edit(request, nid):                      # nid：从网址中捕获的部门 id（urls.py 里配置的动态参数）
    row = Department.objects.filter(id=nid).first()  # 按 id 查询要编辑的那一行，first() 取第一条（查不到返回 None）
    if not row:                                     # 查不到说明该部门不存在（或已被删除）
        return redirect("/depart/list/")            # 找不到该行就回列表页

    if request.method == "GET":
        # GET：显示编辑页，并把该行数据传入用于回显（输入框里显示原值）
        return render(request, "depart_edit.html", {"row": row})

    # POST：接收修改后的数据
    title = request.POST.get("title", "").strip()   # 取新标题并去掉首尾空格
    errors = {}                                     # 收集校验错误的字典

    # 验证：标题不能为空
    if not title:                                   # 没填标题
        errors["title"] = "标题不能为空"
    # 验证：长度限制
    elif len(title) > 32:                           # 超过 32 个字符
        errors["title"] = "标题长度不能超过32个字符"
    # 验证：标题不能重复（排除自身）
    elif Department.objects.filter(title=title).exclude(id=nid).exists():  # exclude 排除自己这条，剩下的里若还有同名就算重复
        errors["title"] = "该标题已存在"

    if errors:                                      # 校验没通过
        # 有错误：回到编辑页并保留已输入内容
        row_dict = {"id": nid, "title": title}      # 手工拼一个字典代替 row，让页面能回显用户刚输入的值
        return render(request, "depart_edit.html", {"row": row_dict, "errors": errors})

    Department.objects.filter(id=nid).update(title=title)  # 校验通过：执行 UPDATE，只更新这一行的 title 字段
    return redirect("/depart/list/")                # 跳回列表页


# 删除部门
def depart_delete(request, nid):                    # nid：要删除的部门 id
    Department.objects.filter(id=nid).delete()      # 按 id 定位该行并执行 DELETE 删除
    return redirect("/depart/list/")                # 跳回列表页
