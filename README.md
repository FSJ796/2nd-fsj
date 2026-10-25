# 联通用户管理系统（ems）

基于 Django 4.2 的员工管理练手项目，包含部门管理、员工管理、靓号管理三大模块。

## 技术栈

- Python 3.9
- Django 4.2
- SQLite
- Bootstrap 3.4.1 + jQuery 3.6.0

## 项目结构

```
ems/
├── manage.py
├── ems/                  # 项目配置
│   ├── settings.py
│   └── urls.py
└── app01/                # 业务应用
    ├── models.py         # Department / UserInfo / PrettyNum
    ├── utils/            # 通用组件（分页、表单基类）
    └── views/            # 视图包（depart / user / pretty）
```

## 功能模块

| 模块 | 路由 | 说明 |
|------|------|------|
| 部门管理 | /depart/list/ 等 | 原生 request.POST 手写校验（非空、长度、查重） |
| 员工管理 | /user/list/ 等 | ModelForm 方式，BootStrapModelForm 统一样式 |
| 靓号管理 | /pretty/list/ 等 | 搜索 + 分页（每页 10 条）+ ModelForm |

## 运行方式

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

访问 http://127.0.0.1:8000/depart/list/

详细说明见 [项目总结.md](项目总结.md)
