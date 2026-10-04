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

if __name__ == "__main__":
    print("Starting server...")
    asyncio.run(main())
