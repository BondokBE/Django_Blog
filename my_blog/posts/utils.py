import re, math, datetime, string, random

from django.utils.text import slugify
from django.utils.html import strip_tags

# words = """
# In previous parts of the tutorial, the templates have been provided with a context that contains the question and latest_question_list context variables. For DetailView the question variable is provided automatically – since we’re using a Django model (Question), Django is able to determine an appropriate name for the context variable. However, for ListView, the automatically generated context variable is question_list. To override this we provide the context_object_name attribute, specifying that we want to use latest_question_list instead. As an alternative approach, you could change your templates to match the new default context variables – but it’s a lot easier to just tell Django to use the variable you want.
# """

def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    if count < 200:
        read_time_min = 0
    else:
        read_time_min = math.ceil(count/200)  # assuming the average time 200 w/s
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    read_time = datetime.datetime.strptime('{}'.format(read_time_min), '%M')
    return read_time.minute
    # print(read_time.minute)


# get_read_time(words)


'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

