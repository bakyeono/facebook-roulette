ABOUT  = 'Collect likers or commentors for a post, using Facebook Graph API.'
AUTHOR = 'Bak Yeon O (bakyeono@gmail.com)'
SITE   = 'https://bakyeono.net'

import requests
import argparse
from sys import stderr

base_url = 'https://graph.facebook.com/v2.11'


def query_raw(url):
    """페이스북 그래프 API에 질의한다. (수동 URL)"""
    response = requests.get(url)
    if response.status_code != 200:
        print(f'[WARN] API response code: {response.status_code}', file=stderr)
    return response.json()


def query(token, endpoint, options='metadata=1'):
    """페이스북 그래프 API에 질의한다. (자동 URL)"""
    url = f'{base_url}{endpoint}?{options}'
    url += '&' if options else ''
    url += f'access_token={token}'
    return query_raw(url)


def flatten(seq):
    """중첩 시퀀스를 한 층위 평평하게 한다."""
    return [e for subseq in seq for e in subseq]


def collect_pages(first_page):
    """pagenated 된 데이터를 반복하여 읽어들인다."""
    pages = [first_page]
    next_page = first_page.get('paging', {}).get('next')
    while next_page:
        new_page = query_raw(next_page)
        pages.append(new_page)
        next_page = new_page.get('paging', {}).get('next')
    return pages


def get_likers(token, post_id, validator=lambda x: True):
    """포스트에 좋아요를 누른 사람의 명단을 구한다."""
    endpoint    = f'/{post_id}'
    fields      = 'likes{name}'
    options     = f'fields={fields}&limit=1000'
    first_page  = query(token, endpoint, options).get('likes', {})
    pages       = collect_pages(first_page)
    likes       = flatten([e.get('data') for e in pages])
    filtered    = [e for e in likes if validator(e)]
    candidates  = [e.get('name', '') for e in filtered]
    return list(sorted(candidates))


def get_commentors(token, post_id, validator=lambda x: True):
    """포스트에 댓글을 단 사람의 명단을 구한다."""
    endpoint    = f'/{post_id}'
    fields      = 'comments'
    options     = f'fields={fields}&limit=1000'
    first_page  = query(token, endpoint, options).get('comments', {})
    pages       = collect_pages(first_page)
    comments    = flatten([e.get('data') for e in pages])
    filtered    = [e for e in comments if validator(e)]
    candidates  = [e.get('from') for e in filtered]
    candidates  = [(e.get('id'), e.get('name')) for e in candidates]
    return list(sorted(candidates, key=lambda x: x[1]))


def test_api_access(token):
    """API 접근 가능여부를 확인한다."""
    return bool(query(token, '/me', '').get('id'))


def test_post_fetch(token, post_id):
    """포스트 조회 가능여부를 확인한다."""
    return bool(query(token, f'/{post_id}', '').get('id'))


def parse_args():
    """실행 인자를 해석한다."""
    parser = argparse.ArgumentParser(description=ABOUT)
    parser.add_argument(dest='edge', help='likers or commentors')
    parser.add_argument(dest='post_id', help='target post ID')
    parser.add_argument(dest='token', help='access token for API')
    parser.add_argument('--duedate', dest='duedate', metavar='YYYY-MM-DD',
                        help='example: 2017-12-05')
    args = parser.parse_args()

    if not (args.edge == 'likers' or args.edge == 'commentors'):
        print(f'[ERROR] unsupported edge: {args.edge}', file=stderr)
        exit(-1)

    return args


def print_candidates(candidates):
    """후보자 명단을 출력한다."""
    for candidate in candidates:
        print(candidate)


if __name__ == '__main__':
    args = parse_args()

    if not test_api_access(args.token):
        print('[ERROR] Cannot access to the API: wrong token?', file=stderr)
        exit(-1)

    if not test_post_fetch(args.token, args.post_id):
        print('[ERROR] Cannot fetch the post: wrong post ID?', file=stderr)
        exit(-1)

    if args.edge == 'likers':
        candidates = get_likers(args.token, args.post_id)

    if args.edge == 'commentors':
        if args.duedate:
            validator  = lambda x: x.get('created_time', 'a') < args.duedate
            candidates = get_commentors(args.token, args.post_id, validator)
        else:
            candidates = get_commentors(args.token, args.post_id)

    print_candidates(candidates)
    exit(0)

