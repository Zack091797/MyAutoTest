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
    渲染模板字符串, 改写默认的引用变量语法{{var}}, 换成${var}

    模板中引用变量语法 ${var},

    调用函数${fun()}
    :param t_str: 模板字符串
    :param args:
    :param kwargs:
    :return:
    """
    t = Template(t_str, variable_start_string='${', variable_end_string='}')
    result = t.render(*args, **kwargs)
    if t_str.startswith("${") and t_str.endswith("}"):
        try:
            # 检索字符串开头结尾是${ }, 则try执行内部表达式或函数
            # eval函数执行字符串中有效的表达式，并返回结果；
            # 将字符串转换成相应的对象(list、tuple、dict和string之间)；
            # 将利用反引号转换的字符串再反转回对象
            # 传入的 str必须是完全的表达式或函数，否则报错
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
