import netifaces as ni
import asyncio as aio

async def main():
    reader, writer = await aio.open_connection('127.0.0.1', 8899)

    writer.write(b"Hello stranger")
    await writer.drain()

    writer.close()
    await writer.wait_closed()

aio.run(main())

