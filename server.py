from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from tiktok_listener import TikTokListener

SERVER = FastAPI()

@SERVER.websocket('/live')
async def get_live_events(websocket: WebSocket):
    # later on pass in dynamic user names??? so long as they do not conflict
    await websocket.accept()
    print('good!')
    try:
        listener_ref: TikTokListener
        while True:
            payload_if_any = await websocket.receive_json()
            username = payload_if_any.get('username')
            print('username', username)
            action = payload_if_any.get('action')
            if action == 'connect':
                listener_ref = TikTokListener(websocket, f'{username}')
                await listener_ref.start_client()
            elif action == 'disconnect':
                await listener_ref.close_client()
    except Exception as e:
        print('e', e)
        pass

