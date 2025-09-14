import asyncio

# List of connected clients
client_connection = []

async def handle_client(reader, writer):
    location = writer.get_extra_info("colleague")
    print(f"Clients have been connected: {location}")
    client_connection.append(writer)

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode.strip()
            print(f"Data gotten from {location} is {message}.")

            for client_writer in client_connection:
                if client_writer != writer:
                    client_writer.write(f"[{location[0]}:{location[1]}] {message}\n".encode())
                    await client_writer.drain()

    except asyncio.CancelledError:
        pass
    finally:
        print(f"Client has disconnected: {location}")
        client_connection.remove(writer)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888
    )

    server_address = server.sockets[0].getsockname()
    print(f"Serving on {server_address}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shutting down.")