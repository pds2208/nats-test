import asyncio

import nats

    
async def main():
    nc = await nats.connect("localhost")
    js = nc.jetstream()

    sub = await js.subscribe(subject="test", durable="psub", stream="test-stream", manual_ack=True)

    async for msg in sub.messages:
        print("Received", msg)
        await msg.ack()

    await nc.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
