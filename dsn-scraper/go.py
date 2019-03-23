from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import re
from db.db_handler import db
from db.models import Word, Form


categories = [
    'sb.',
    'vb.',
    'fork.',
    'fork. for',
    'adj.',
    'præp.',
    'prop.',
    'sb. pl.',
    'adv.',
    'ubøj. adj.',
    'i sms.',
    'pl.',
    'pron.',
    'itk.',
    'konj.',
    'pron. sg.',
    'artikel',
    'adj. pl.',
    'ubøj. pron.',
    'pron. pl.',
    'itk. og bf. d.s.'
]


def url(letter, iteration, include_max=True):
    components = [
        "https://dsn.dk/?retskriv=",
        quote(letter),
        "&p=",
        str(iteration*100),
    ]
    
    if include_max:
        components.append("&resultsperpage=100")

    return "".join(components)


def init_letter(letter):
    '''
        makes a first request to determine number of words beginning
        with that letter
    '''
    u = url(letter, 0, False)
    html = str(urlopen(u).read())
    m = re.search(r'af i alt (\d+) artikler', html)

    if m:
        return int(m.group(1))

    raise Exception("the search gave no results")


def do_scrape(base_url):
    html = urlopen(base_url)
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find("div", {"id": "articles"}).find_all("div")

    for div in articles:
        tag = div.find("b")
        if tag.span:
            word = tag.span.decompose()
        word = tag.text

        categories = div.find_all('abbr')
        if len(categories) == 0:
            categories = ['']

        for ic, category in enumerate(categories):
            w = Word()
            if ic == 0:
                w.word = word
            else:

                try:
                    if str(category.previous_sibling).strip() == '(':
                        continue

                    sibling_word = category.parent.next_sibling
                    sibling_word = sibling_word.split(";")[0].replace(',','').strip()
                    if '-' in sibling_word:
                        continue

                    w.word = sibling_word
                except Exception as e:
                    w.word = ''

                if len(w.word) == 0:
                    continue

            desc = ""
            m = re.search(r'\((.*)\)', div.text)
            if m:
                desc = m.group(1)
                if len(desc) <= 5:
                    desc = ''

            w.description = desc

            ends = []

            # -er, -et style endings
            m = re.findall(r', -([a-zæøå]+)', div.text)
            for end in m:
                ends.append(word + end)

            # A'erne ... style
            m = re.findall(', '+word+'’([a-zæøå]+)', div.text)
            for i, end in enumerate(m):
                ends.append(word + "'" + end)

            if len(ends) == 0:
                # irregular, e.g., 'adfærdsmønster'; 'adfærdsmønst(e)ret'
                remainder = div.text.replace('('+desc+')', '')
                m = re.findall(r'([a-zæøå\(\)]+)(,|$)', remainder)
                for end in m:
                    end = end[0]
                    if '(' in end:
                        ends.append(end.replace('(', '').replace(')', ''))  # with
                        ends.append(end.replace(r"\(.*\)", ""))  # without
                    else:
                        ends.append(end)

            for i, end in enumerate(ends):
                f = Form()
                f.index = i
                f.form = end
                print("->", f.form)
                db.add(f)
                w.forms.append(f)

            try:
                w.category = category.text
            except AttributeError:
                w.category = ''

            print("saved", w.word)

            db.add(w)
        db.commit()


if __name__ == "__main__":

    letters = list('abcdefghijklmnopqrstuvwxyzæøå')

    for letter in letters:
        try:
            num_words = init_letter(letter)
        except:
            # no more words
            continue

        iterations = num_words // 100 + 1
        for i in range(0, iterations):
            print("ITERATION", i)
            do_scrape(url(letter, i))

#do_scrape("https://dsn.dk/?retskriv=g%C3%B8re&ae=0")
# do_scrape(url('g', 0))
#do_scrape("https://dsn.dk/?retskriv=ampere&ae=0")
