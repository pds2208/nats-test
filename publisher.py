import asyncio

import nats


async def main():
    nc = await nats.connect("localhost")
    js = nc.jetstream()

    print(await js.streams_info(),"\n")

    for i in range(0, 10):
        ack = await js.publish("test", f"hello world: {i}".encode())
        print(ack)

    await nc.close()


if __name__ == '__main__':
    asyncio.run(main())
