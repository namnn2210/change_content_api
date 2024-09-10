from bs4 import BeautifulSoup
from rewrite_enum import RewriteConstants


def rewrite_api(api_obj, input_config, option):
    return api_obj.rewrite(input_string=input_config, option=option)


def do_rewrite(api_obj, title, content, option):
    title_options = title.get('config', {})
    content_options = content.get('config', {})
    title_text = title.get('text', '')
    content_text = content.get('text', '')
    description = ''
    if title_options:
        rewrite_title = title_options.get('rewrite_title')
        message = f'{rewrite_title}: {title_text}'
        title_text = rewrite_api(api_obj=api_obj, input_config=message, option=option)
    if content_options:
        if RewriteConstants.REWRITE_HEADING.value in content_options.keys():
            content_text = rewrite_heading(api_obj=api_obj, content_text=content_text,
                                           list_change=['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
                                           input_config=content_options.get(RewriteConstants.REWRITE_HEADING.value),
                                           option=option)
        if RewriteConstants.REWRITE_CONTENT.value in content_options.keys():
            content_text = rewrite_content(api_obj=api_obj, content_text=content_text,
                                           input_config=content_options.get(RewriteConstants.REWRITE_CONTENT.value),
                                           option=option)
        if RewriteConstants.REWRITE_DESCRIPTION.value in content_options.keys():
            description = generate_description(api_obj=api_obj, title_text=title_text, input_config=content_options.get(
                RewriteConstants.REWRITE_DESCRIPTION.value), option=option)
    return {
        "title": title_text.strip('\n'),
        "content": content_text.strip('\n'),
        "description": description.strip('\n')
    }


def rewrite_heading(api_obj, content_text, list_change, input_config, option):
    soup = BeautifulSoup(content_text, "html.parser")
    tags = soup.find_all(list_change)
    for tag in tags:
        message = f'{input_config}: {tag.text}'
        new_text = rewrite_api(api_obj=api_obj, input_config=message, option=option)
        tag.string = new_text
    return str(soup)


def rewrite_content(api_obj, content_text, input_config, option):
    content_text = rewrite_api(api_obj=api_obj, input_config=f'{input_config} this content and keep HTML tags (just render the result only without any other text): {content_text}',option=option)
    return content_text


def generate_description(api_obj, title_text, input_config, option):
    message = f'Write a description {input_config} about the title: {title_text}'
    description = rewrite_api(api_obj=api_obj, input_config=message, option=option)
    return description
