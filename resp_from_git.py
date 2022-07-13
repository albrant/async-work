import time
import urllib.request
import asyncio
import aiohttp

URL = 'https://api.github.com/events'
MAX_CLIENTS = 3


def fetch_sync(pid):
    print('Запуск синхронного процесса {} - СТАРТ!'.format(pid))
    start = time.time()
    response = urllib.request.urlopen(URL)
    datetime = response.getheader('Date')

    print('Процесс {}: {} занял: {:.2f} секунд'.format(
        pid, datetime, time.time() - start))

    return datetime


async def fetch_async(pid):
    print('Запуск процесса {} - СТАРТ!'.format(pid))
    start = time.time()
    async with aiohttp.request('GET', URL) as response:
        datetime = response.headers.get('Date')
        print('Процесс {}: {}, занял: {:.2f} секунд'.format(
            pid, datetime, time.time() - start))
        return datetime


def synchronous():
    start = time.time()
    for i in range(1, MAX_CLIENTS + 1):
        fetch_sync(i)
    print("Процессы заняли: {:.2f} секунд".format(time.time() - start))


async def asynchronous():
    start = time.time()
    tasks = [asyncio.ensure_future(
        fetch_async(i)) for i in range(1, MAX_CLIENTS + 1)]
    await asyncio.wait(tasks)
    print("Процессы заняли: {:.2f} секунд".format(time.time() - start))


print('Синхронная часть:')
synchronous()
print('='*50)
print('Асинхронная часть:')
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()
