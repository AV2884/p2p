# p2p_chat.py
import asyncio
import libp2p
from libp2p import new_host
from libp2p.peer.peerinfo import PeerInfo
from libp2p.discovery.dht import DHTPeerRouting
from libp2p.stream.stream import NetStream
from libp2p.crypto.keys import KeyPair

async def handle_stream(stream: NetStream):
    while True:
        try:
            message = await stream.read()
            print(f"📶 📶 📶 {message.decode('utf-8')}")
        except Exception as e:
            print(f"Error: {e}")
            break

async def send_message(stream : NetStream, message :str):
    await stream.write(message.encode('utf-8'))

async def connect_to_peer(host, peer_info):
    #host.new_stream defines a stream between 2 peers
    #["/chat/1.0.0"] is a chatting protocol
    try:
        stream = await host.new_stream(peer_info.peer_id, ["/chat/1.0.0"])
        print(f"⛓️ ⛓️ ⛓️ Successfully connected to peer: {peer_info.peer_id}")
        asyncio.ensure_future(handle_stream(stream))
        return stream
    except Exception as e:
        print(f"Failed to connect to peer {peer_info.peer_id}: {e}")
        return None


async def discover_peers(host):
    """Discover other peers using DHT."""
    routing = DHTPeerRouting(host.get_network())
    peers = await routing.find_peers(1)  
    return [PeerInfo(peer_id) for peer_id in peers]


async def main():
    key_pair = KeyPair.generate()
    host = await new_host(key_pair=key_pair)

    discovered_peers = await discover_peers(host)
    if discovered_peers:
        print(f"🛜 🛜 🛜 Discovered peers: {discovered_peers}")
        stream = await connect_to_peer(host, discovered_peers[0])

        while True:
                message = input("Enter message: ")
                await send_message(stream, message)
    
    else:
        print("No peers discovered.")

    await asyncio.Event().wait() 


if __name__ == "__main__":
    asyncio.run(main())