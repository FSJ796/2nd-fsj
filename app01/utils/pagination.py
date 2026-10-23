from django.core.paginator import Paginator       # Django 自带分页器：自动切分每页数据、计算总页数


def paginate(request, queryset, page_size=10):
    """通用分页组件：任何列表页都可以复用（靓号列表、员工列表……）

    参数:
        request:   请求对象（从中取 ?page= 页码，并保留除 page 外的其他参数如搜索词）
        queryset:  要分页的数据
        page_size: 每页条数，默认 10 条
    返回:
        page_obj: 当前页的数据（可直接被模板 for 循环遍历）
        pager:    分页条需要的上下文字典（当前页、上一页、下一页、总页数、链接前缀等）
    """
    paginator = Paginator(queryset, page_size)      # 把查询集交给分页器，自动算出总页数 paginator.num_pages

    page = request.GET.get("page", "1")             # 从网址 ?page= 取当前页码，默认第 1 页
    try:
        page_num = int(page)                        # 页码转成数字；用户乱输入非数字时走 except
    except ValueError:
        page_num = 1                                # 非法页码统一回第 1 页
    if page_num < 1:                                # 页码不能小于 1
        page_num = 1
    elif page_num > paginator.num_pages:            # 页码不能超过总页数
        page_num = max(paginator.num_pages, 1)      # 回到最后一页（表里没数据时至少保持在第 1 页）
    page_obj = paginator.page(page_num)             # 取出当前页的数据

    # 链接前缀：把当前网址里除 page 以外的参数（如搜索词 q）原样保留，翻页时不会丢失
    params = request.GET.copy()                     # 复制一份查询参数，避免改动原始 request.GET
    params.pop("page", None)                        # 去掉 page，其余参数（q=xxx）拼进前缀
    prefix = f"{params.urlencode()}&" if params else ""  # 有参数时链接形如 ?q=138&page=2，没有时是 ?page=2

    pager = {
        "prefix": prefix,                           # 翻页链接的公共前缀
        "current_page": page_obj.number,            # 当前页码（模板里用来高亮页码）
        "prev_page": page_num - 1 if page_num > 1 else 1,          # 上一页页码（已在第 1 页时仍指向第 1 页）
        "next_page": page_num + 1 if page_num < paginator.num_pages else paginator.num_pages,  # 下一页页码（已在最后一页时仍指向最后一页）
        "total_pages": paginator.num_pages,         # 总页数（尾页链接、边界判断用）
        "page_range": paginator.page_range,         # 所有页码，如共 3 页就是 [1, 2, 3]
    }
    return page_obj, pager
