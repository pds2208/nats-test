import asyncio

import nats
from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.aio.subscription import Subscription

async def main():
    nc = await nats.connect("localhost")
    js = nc.jetstream()

    await js.add_stream(name="test-stream", subjects=["test"])

    print(await js.streams_info(),"\n")
    
    for i in range(0, 10):
        ack = await js.publish("test", f"hello world: {i}".encode())
        print(ack)

    psub = await js.pull_subscribe("test", "psub")
    for i in range(0, 10):
        msgs = await psub.fetch(1)
        for msg in msgs:
            await msg.ack()
            print(msg)

    # for i in range(0, 10):
    #     ack = await js.publish("test", f"hello world: {i}".encode())
    #     print(ack)
    #
    # # Create pull based consumer on 'foo'.
    # js.
    # psub = await js.pull_subscribe("foo", "psub")
    #
    # # Fetch and ack messagess from consumer.
    # for i in range(0, 10):
    #     msgs = await psub.fetch(1)
    #     for msg in msgs:
    #         await msg.ack()
    #         print(msg)
    #
    # # Create single ephemeral push based subscriber.
    # sub = await js.subscribe("foo")
    # msg = await sub.next_msg()
    # await msg.ack()
    #
    # # Create single push based subscriber that is durable across restarts.
    # sub = await js.subscribe("foo", durable="myapp")
    # msg = await sub.next_msg()
    # await msg.ack()
    #
    # # Create deliver group that will be have load balanced messages.
    # async def qsub_a(msg):
    #     print("QSUB A:", msg)
    #     await msg.ack()
    #
    # async def qsub_b(msg):
    #     print("QSUB B:", msg)
    #     await msg.ack()
    # await js.subscribe("foo", "workers", cb=qsub_a)
    # await js.subscribe("foo", "workers", cb=qsub_b)
    #
    # for i in range(0, 10):
    #     ack = await js.publish("foo", f"hello world: {i}".encode())
    #     print("\t", ack)
    #
    # # Create ordered consumer with flow control and heartbeats
    # # that auto resumes on failures.
    # osub = await js.subscribe("foo", ordered_consumer=True)
    # data = bytearray()
    #
    # while True:
    #     try:
    #         msg = await osub.next_msg()
    #         data.extend(msg.data)
    #     except TimeoutError:
    #         break
    # print("All data in stream:", len(data))

    await nc.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
