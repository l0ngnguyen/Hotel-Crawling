import re
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException


def get_element_by_selector(driver, selector, find_more=False, content='t'):
    """find the element by css selector and get the information that we need: WebElement, text or attribute

    Args:
        driver (WebDriver): WebDriver selenium that we want to extract
        selector (str): the css selector 
        find_more (bool, optional): find more elements or just one. Defaults to False.
        content (string, optional): 3 options: 't' - text => get text, 'e' - element => get selenium WebElement, 
                                    else get attribute that has name is content. Defaults to None.

    Returns:
        list, str or None: 
    """
    try:
        if find_more:
            elements = driver.find_elements_by_css_selector(selector)
            if len(elements) == 0:
                raise NoSuchElementException

            if content == 't':
                return [e.text for e in elements]
            elif content == 'e':
                return elements
            else:
                res = []
                for e in elements:
                    attr_content = e.get_attribute(content)
                    if attr_content is not None:
                        res.append(attr_content)
                    else:
                        raise NoSuchAttributeException
                return res
        else:
            element = driver.find_element_by_css_selector(selector)
            if not element:
                raise NoSuchElementException

            if content == 't':
                return element.text
            elif content == 'e':
                return element
            else:
                res = element.get_attribute(content)
                if res:
                    return res
                else:
                    raise NoSuchAttributeException

    except NoSuchElementException:
        print('No such element exception')
        return None
    except NoSuchAttributeException:
        print('No such attribute exception')
        return None
    except Exception:
        print('Exception when use selenium to find element by css selector')
        return None


def clean_text(s):
    if not s:
        return ''
    if len(s) > 0:
        return re.sub('\n', '', s).strip()
    else:
        return ''


def clean_text_list(text_list):
    if not text_list:
        return []
    if len(text_list) > 0:
        text_list = list(set(text_list))
        return [clean_text(text) for text in text_list if text != '\n']
    else:
        return []


def get_date_from_string(s):  # '... Ngay xx thang xx nam xx'
    if not s:
        return None
    idx = s.find('Ngày')
    if idx != -1:
        s = s[idx:].split()
        return s[1] + '/' + s[3] + '/' + s[5]
    else:
        return None
