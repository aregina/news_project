import html
import re


# TODO все переделать нах

def tags_filter_head_and_script(txt):
    # срезаем  head инорируя регистр(на некоторых сайтах HEAD in Upper case)
    head_match = re.search("</\s*?head\s*?>", txt, re.IGNORECASE)
    text = txt[head_match.end():]
    text = html.unescape(text)
    tag = "script"
    return re.sub("<\s*?{0}.*?>(.|\s)*?</\s*?{0}\s*?>".format(tag), " ", text)


def tags_filter(txt):
    t = tags_filter_head_and_script(txt)
    # TODO должна быть независима от регистра
    tags = ["header", "svg", "noscript", "form",
            "nav", "iframe", "footer", "time", "noindex", "style", "abbr", "select", "aside", "figure"]
    for tag in tags:
        t = re.sub("<\s*?{0}.*?>(.|\s)*?</\s*?{0}\s*?>".format(tag), " ", t)

    t = re.sub("style.?=.?\"(.|\s)*?\"", " ", t)
    t = re.sub("class.?=.?\"(.|\s)*?\"", " ", t)
    t = re.sub("id.?=.?\"(.|\s)*?\"", " ", t)
    t = re.sub("<\s*?/?(body|html|br|hr)(.|\s)*?>", " ", t)
    t = re.sub("<!--(.|\s)*?-->", " ", t)
    t = re.sub("<img(.|\s)*?>", " ", t)
    t = re.sub("<meta(.|\s)*?>", " ", t)
    t = re.sub("<input(.|\s)*?>", " ", t)
    t = re.sub("</?p(.|\s)*?>", "<p>", t)
    t = re.sub("<\s*?/?(article|font|table|tr|td|div|h1|h2|h3|h4|span|ul|li|ol|label|section)(.|\s)*?>",
               "<p>", t)
    t = re.sub("</?(i|u|b|strong|em)(.|\s)*?>", " ", t)

    return t


def count_chars(text_line):
    d, c = 0, 0
    in_tag_brackets = False
    left_bracket = False
    in_a_tag = False
    for char in text_line:
        if left_bracket:
            if char == "a":
                left_bracket = False
                in_a_tag = True
            elif char == "/":
                left_bracket = False
                in_a_tag = False
        elif char == '<':
            left_bracket = True
            in_tag_brackets = True
        elif char == '>':
            in_tag_brackets = False
        elif char == ' ':
            continue
        elif in_tag_brackets:
            continue
        elif not in_tag_brackets and not in_a_tag:
            c += 1
        elif not in_tag_brackets and in_a_tag:
            d += 1
    return d, c


def get_list_of_lines(text):
    cnt = []
    lines = text.split("<p>")
    maximum, minimum = 0, 100000
    for line in lines:
        line = line.strip()
        if not line:
            continue
        inTagChars, outTagChars = count_chars(line)
        if outTagChars > maximum:
            maximum = outTagChars
        elif 0 < outTagChars < minimum:
            minimum = outTagChars
        cnt.append([outTagChars, inTagChars, line])
    return maximum, minimum, cnt


def delete_bad_links(text):
    """
    Метод удаляет ссылки с большим количеством тегов <p> внутри текста ссылки
    Если количество больше 2 - ссылка удаляется.
    Два и меньше - теги <p> заменяются на пробелы
    <a>
        <p>
        <p>
        ...
        <p>
    </a>
    :param text:
    :return:
    """
    end = 0
    result = ""
    while end < len(text):
        y = re.search("<a(.|\s)*?</a>", text[end:])
        if not y:
            result += text[end:]
            break
        else:
            result += text[end:end + y.start()]
            sub = text[end + y.start():end + y.end()]
            i = sub.count("<p>")
            if i == 0:
                end += y.end()
                result += sub
            elif i < 3:
                end += y.end()
                sub = re.sub("<p>", " ", sub)
                result += sub
            else:
                end += y.end()
    return result


def get_text_from_html(text):
    text = tags_filter(text)
    text = delete_bad_links(text)
    max_char, min_char, line_list = get_list_of_lines(text)
    text = ""
    '''
    for i, j in enumerate(line_list):
        level = max_char * 0.3
        if j[0] >= level and not j[2].startswith("Copyright"):
            text += j[2] + " "
            '''
    max_index = 0
    for i, l in enumerate(line_list):
        if l[0] * 2 >= max_char:
            max_index = i
            break

    hop = 2
    start = max_index
    while start > 0 and (line_list[start - 1][0] > 40 or hop):
        if line_list[start - 1][0] <= 40:
            hop -= 1
        start -= 1

    hop = 2
    end = max_index
    while end < len(line_list) - 1 and (line_list[end + 1][0] > 40 or hop):
        if line_list[end + 1][0] <= 40:
            hop -= 1
        end += 1

    i = start
    while i <= end:
        if line_list[i][0] > 40:
            text += line_list[i][2] + " "
        i += 1
    return text


def main():
    import urlOpen

    text = urlOpen.get_html("http://www.interfax.ru/world/502926")
    text = tags_filter(text)

    with open("parsed3.html", mode='w', encoding='utf-8') as file:
        file.write(text)
    max_char, min_char, line_list = get_list_of_lines(text)

    for i, c in enumerate(line_list):
        level = max_char * 0.4
        if c[0] >= level and not c[2].startswith("Copyright"):
            print(i, c[0], c[1], c[2])

    print("Max chars in line: {}\n"
          "Min chars in line {}\n"
          "Num of lines {}".format(max_char, min_char, len(line_list)))


if __name__ == "__main__":
    main()
