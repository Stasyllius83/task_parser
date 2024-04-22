from bs4 import BeautifulSoup
import requests



TASK_TOPIC = ['brute', 'math','strings', 'greedy', \
              'implementation', 'sortings', 'constructive', \
                'algorithms', 'graph', 'matchings', 'shortest', 'paths', \
                    'Function', 'Problem', 'structures', 'hashing', 'search', \
                        'binary', 'number', 'theory', 'dp', 'pointers', \
                            'parsing', 'expression', 'two', '*special', 'data', 'bitmasks']

def task_parser():
    """

    """
    num_of_page = 95
    for i in range(num_of_page):
        url = 'https://codeforces.com/problemset/page/' + str(i) + '?order=BY_SOLVED_DESC'
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page, 'lxml')

        all_tasks = []

        for a in soup.find_all('tr')[1:-1]:

            task_items = []

            line = ' '.join(a.text.split())
            line_words = line.split(' ', 1)
            words_in_line = line_words[1].split()

            list_word = []

            for word in words_in_line:
                res_word = word.replace(",","")
                if res_word not in TASK_TOPIC:
                    list_word.append(res_word)
                else:
                    break

            name = ' '.join(list_word)
            task_items.append(f'{name} № {line_words[0]}')

            for word in words_in_line:
                res_word = word.replace(",","")
                if res_word in TASK_TOPIC:
                    topic = res_word
                    break

            for word in words_in_line[-2:-1]:
                difficulty = word
                break

            for word in words_in_line[-1:]:
                quantity_solved = word[1:]
                break

            task_items.append(topic)
            task_items.append(difficulty)
            task_items.append(quantity_solved)
            all_tasks.append(task_items)

        return all_tasks
