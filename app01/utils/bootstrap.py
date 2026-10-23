from django.forms import ModelForm                # 导入 ModelForm 基类


class BootStrapModelForm(ModelForm):
    """让所有 ModelForm 自动套上 Bootstrap 样式的基类

    用法：自己写的表单类改为继承本类，就不必在 Meta.widgets 里
    一个字段一个字段地写 attrs={"class": "form-control"} 了
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)           # 先按 ModelForm 的原逻辑把所有字段生成好
        # 循环每个字段，给控件统一加上 form-control 样式（已有的其他属性如 placeholder 不受影响）
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
