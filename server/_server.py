import asyncio
from websockets.asyncio.server import serve
import functools

async def handler(websocket, server_queue) -> None:
    async for message in websocket:
        print(f"< Received: {message}")
        # print(f"> Sending: {message}")
        # await websocket.send(message)

        while True:
            try:
                rate, data = server_queue.get()
                data = data.tolist()
                if data:
                    # print(f">>> Sending: voice data")
                    for i in data:
                        await websocket.send(str(i))
                        await asyncio.sleep(1/rate)
                server_queue.task_done()
            except Exception as e:
                print(e)

async def main(server_queue) -> None:
    bound_handler = functools.partial(handler, server_queue=server_queue)
    server = await serve(bound_handler, "localhost", 8000)
    await server.serve_forever()

def run(server_queue) -> None:
    """
    Starts the server
    """

    print("starting server...")
    asyncio.run(main(server_queue))

if __name__ == "__main__":
    run()
