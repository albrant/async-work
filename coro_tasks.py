import random
from time import sleep, time
import asyncio


SEC = [9, 5, 7, 6, 5, 4, 3, 2, 1, 5]


def task(pid):
    """Synchronous non-deterministic task.
    """
    start = time()
    sleep(random.randint(0, 2) * 0.001)
    print(f'Задача {pid} выполнена за {(time()-start)}')


async def task_coro(pid):
    """Coroutine non-deterministic task
    """
    start = time()
    # await asyncio.sleep(random.randint(0, 2) * 0.001)
    await asyncio.sleep(SEC[pid])
    print(f'Задача {pid} выполнена за {(time()-start)}')


def synchronous():
    for i in range(1, 10):
        task(i)


async def asynchronous():
    tasks = [asyncio.ensure_future(task_coro(i)) for i in range(1, 10)]
    await asyncio.wait(tasks)


print('Синхронные задачи:')
synchronous()
print('='*50)

print('Асинхронные задачи:')
ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous())
ioloop.close()