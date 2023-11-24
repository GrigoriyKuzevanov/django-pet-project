from blog.utils import menu

def get_blog_context(request):  # переменные из словаря будут доступны во всех шаблонах
    return {'mainmenu': menu}
