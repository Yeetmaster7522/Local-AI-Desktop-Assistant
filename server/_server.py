import asyncio

from websockets.asyncio.server import serve

async def echo(websocket):
    async for message in websocket:
        print(f"< Received: {message}")
        print(f"> Sending: {message}")
        await websocket.send(message)

async def main():
    server = await serve(echo, "localhost", 8000)
    await server.serve_forever()

def run() -> None:
    """
    Starts the server
    """

    print("starting server...")
    asyncio.run(main())

if __name__ == "__main__":
    run()
