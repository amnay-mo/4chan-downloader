#!/usr/bin/env python3
import urllib3
import asyncio
import aiohttp
import shutil
import json
import sys
import os
import argparse
import re
from tqdm import tqdm

async def download_post(board, post, output_dir, http, pbar):
    url = 'http://i.4cdn.org/%s/%s%s' % (board, post['tim'], post['ext'])
    async with http.get(url) as r:     
        with open('%s/%s%s' % (output_dir, post['tim'], post['ext']), 'wb') as f:
            data = await r.content.read()
            f.write(data)
            pbar.update(1)
        await r.release()


def create_output_dir(output_dir):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)


def get_posts(url, board, thrd):
    http = urllib3.PoolManager(num_pools=1)

    r = http.request(
        'GET',
        'http://a.4cdn.org/' + board + '/thread/' + thrd + '.json'
    )    
    posts_list = json.loads(r.data)['posts']
    return [p for p in posts_list if 'tim' in p and 'ext' in p]


async def download_posts(url, output_dir, loop):
    board = re.findall(r'\.org?/.*?/', url)[0][5:-1]
    thrd = re.findall(r'/thread/[0-9]*/', url)[0][8:-1]
    posts = get_posts(url, board, thrd)   
    pbar = tqdm(total=len(posts))
    async with aiohttp.ClientSession(loop=loop) as http:
        tasks = [download_post(board, post, output_dir, http, pbar) for post in posts]
        await asyncio.gather(*tasks)        


def thread_name(url):
    s = url.split('/')
    if len(s) > 1:
        return s[-1]
    else:
        raise ValueError('invalid url')


def main():
    parser = argparse.ArgumentParser(
        prog='4chan_dl',
        description='downloads all images from a 4chan thread'
    )
    parser.add_argument('url', nargs=1, help='Thread URL')
    url = parser.parse_args().url[0]
    output_dir = thread_name(url)
    create_output_dir(output_dir)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_posts(url, output_dir, loop))


if __name__ == '__main__':
    main()
