from jinja2 import Template


def render_template_by_jinja2(any_obj, *args, **kwargs):
    """

    :param any_obj:
    :param args:
    :param kwargs:
    :return:
    """
    if isinstance(any_obj, str):
        return render_template_str_by_jinja2(any_obj, *args, **kwargs)
    elif isinstance(any_obj, list):
        return render_template_list_by_jinja2(any_obj, *args, **kwargs)
    elif isinstance(any_obj, dict):
        return rend_template_dict_by_jinja2(any_obj, *args, **kwargs)
    else:
        return any_obj


def render_template_str_by_jinja2(t_str, *args, **kwargs):
    """
    整体模板替换思路：
        1.把替换的实际值，方法对象传入
        2.修改模板对象的检索字符串为 ${}
        3.先进行模板替换
        4.再判断如果 被替换字符串是以${}开头结尾，则对替换之后的字符串尝试执行表达式并返回，报错则直接返回替换后的字符串
    :param t_str: 模板字符串
    :param args:
    :param kwargs:
    :return:
    """
    t = Template(t_str, variable_start_string='${', variable_end_string='}')
    result = t.render(*args, **kwargs)
    if t_str.startswith("${") and t_str.endswith("}"):
        try:
            return eval(result)
        except Exception:
            return result
    else:
        return result


def rend_template_dict_by_jinja2(t_dict: dict, *args, **kwargs):
    """

    :param t_dict:
    :param args:
    :param kwargs:
    :return:
    """
    if isinstance(t_dict, dict):
        for key, value in t_dict.items():
            if isinstance(value, str):
                t_dict[key] = render_template_str_by_jinja2(value, *args, **kwargs)
            elif isinstance(value, dict):
                rend_template_dict_by_jinja2(value, *args, **kwargs)
            elif isinstance(value, list):
                render_template_list_by_jinja2(value, *args, **kwargs)
            else:
                pass
        return t_dict


def render_template_list_by_jinja2(t_list, *args, **kwargs):
    """

    :param t_list:
    :param args:
    :param kwargs:
    :return:
    """
    if isinstance(t_list, list):
        new_list = []
        for index, item in enumerate(t_list):
            if isinstance(item, str):
                new_list.append(render_template_str_by_jinja2(item, *args, **kwargs))
            elif isinstance(item, list):
                new_list.append(render_template_list_by_jinja2(item, *args, **kwargs))
            elif isinstance(item, dict):
                new_list.append(rend_template_dict_by_jinja2(item, *args, **kwargs))
            else:
                new_list.append(item)
        return new_list
