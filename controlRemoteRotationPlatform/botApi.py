import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from switchbot_api import VirtualSwitchBot
from switchbot_api.bot_types import SwitchBotAction

MAC_ADRESS = 'Put your Switch Bot Mac address'

class SwitchBotServer(BaseHTTPRequestHandler):
    bot = None
    loop = None

    def do_GET(self):
        path = self.path
        cls = type(self)

        if path == "/connect":
            print("Connect")
            fut = asyncio.run_coroutine_threadsafe(connect(), cls.loop)
            cls.bot = fut.result()
            self.respond("✅ Connected")

        elif path == "/press":
            print("Press")
            if cls.bot is None:
                self.respond("❌ Not connected")
                return
            asyncio.run_coroutine_threadsafe(press(cls.bot), cls.loop)
            self.respond("✅ Pressed")

        elif path == "/disconnect":
            print("Disconnect")
            if cls.bot:
                asyncio.run_coroutine_threadsafe(disconnect(cls.bot), cls.loop)
                cls.bot = None
            self.respond("✅ Disconnected")

        else:
            self.respond("❌ Unknown command", 404)

    def respond(self, msg, code=200):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(msg.encode("utf-8"))


# Async bot functions
async def connect():
    bot = VirtualSwitchBot(mac_address=MAC_ADRESS)
    bot.info.password_str = "0000"
    print("🔵 Connecting...")
    await bot.connect()
    print("✅ Connected")
    return bot

async def press(bot):
    print("▶️ Pressing...")
    await bot.set_bot_state(SwitchBotAction.PRESS)
    print("✅ Done")

async def disconnect(bot):
    print("🔴 Disconnecting...")
    await bot.disconnect()
    print("✅ Disconnected")

# Entry point
if __name__ == "__main__":
    # Set up persistent loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    SwitchBotServer.loop = loop

    # Start loop in background thread
    t = Thread(target=loop.run_forever, daemon=True)
    t.start()

    # Start HTTP server
    server = HTTPServer(('', 8000), SwitchBotServer)
    print("🌐 Server running at http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        server.shutdown()
        loop.call_soon_threadsafe(loop.stop)
        t.join()
