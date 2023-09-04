import asyncio
import websockets
import sys


async def producer(host: str, port: int):
    async with websockets.connect(f'ws://{host}:{port}') as ws:
        while True:
            message = input('>>> ')
            await ws.send(message)


if __name__ == '__main__':
    # asyncio.run(producer(message=sys.argv[1], host='localhost', port=4000))
    try:
        asyncio.run(producer(host='localhost', port=4000))
    except KeyboardInterrupt:
        print('Connection is closed.')