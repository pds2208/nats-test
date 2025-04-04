import asyncio

import nats
from nats.js.errors import NotFoundError


async def main():
    nc = await nats.connect("localhost")
    js = nc.jetstream()

    try:
        await js.delete_stream("test-stream")
    except NotFoundError:
        pass
    
    await js.add_stream(name="test-stream", subjects=["test"])

    await nc.close()


if __name__ == '__main__':
    asyncio.run(main())
