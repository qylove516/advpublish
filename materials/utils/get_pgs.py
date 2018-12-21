from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_pg(request, obj, page_num):
    # 生成paginator对象，定义每页10条数据
    paginator = Paginator(obj, page_num)
    # 从前端获取当前的页码数,默认1
    page = request.GET.get("page", 1)
    # 把页码数转换成整数型
    current_page = int(page)
    try:
        machines = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        machines = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        machines = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return machines, current_page
