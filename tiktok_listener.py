from TikTokLive import TikTokLiveClient
from TikTokLive.client.web.web_settings import WebDefaults
from TikTokLive.events import ConnectEvent, FollowEvent, GiftEvent, LikeEvent, CommentEvent
from fastapi import WebSocket

WebDefaults.tiktok_sign_api_key = 'euler_YzA0MzlkNGEwYTlhODgxMzVjZDk4MmNjY2QzMDE5YWE1OWQ5MmQzZGVkMDNkOWNlODk5Y2M3'

class TikTokListener:
    def __init__(self, websocket: WebSocket, username: str):
        self.client: TikTokLiveClient = TikTokLiveClient(unique_id=username)
        self.socket_ref: WebSocket = websocket
        self.username: str = username

    async def start_client(self):
        await self.client.start()

        # trigger event listeners
        # self.client.add_listener(ConnectEvent, self.on_connect)
        self.client.add_listener(LikeEvent, self.on_like_event)
        # self.client.add_listener(GiftEvent, self.on_gift_event)
        self.client.add_listener(FollowEvent, self.on_follow_event)
        # self.client.add_listener(CommentEvent, self.on_comment_event)

    async def close_client(self):
        await self.client.disconnect()

    async def on_connect(self, event: ConnectEvent):
        await self.send_event({
            'unique_id': event.unique_id,
            'room_id': event.room_id,
            'event_type': 'connect'
        })

    async def on_like_event(self, event: LikeEvent):
        await self.send_event({
            'name': event.user.nick_name,
            'username': event.user.username,
            'avatar': event.user.avatar_thumb.m_urls[0],
            'event_type': 'like',
            'likes_increment': event.count
        })

    async def on_gift_event(self, event: GiftEvent):
        await self.send_event({
            'name': event.user.nick_name,
            'username': event.user.username,
            'avatar': event.user.avatar_thumb.m_urls[0],
            'event_type': 'gift',
            'gift': {
                'repeat': event.repeat_count,
                'name': event.gift.name,
            }
        })

    async def on_follow_event(self, event: FollowEvent):
        await self.send_event({
            'name': event.user.nick_name,
            'username': event.user.username,
            'avatar': event.user.avatar_thumb.m_urls[0],
            'event_type': 'follow'
        })

    async def on_comment_event(self, event: CommentEvent):
        await self.send_event({
            'name': event.user_info.nick_name,
            'username': event.user_info.username,
            'avatar': event.user_info.avatar_thumb.m_urls[0],
            'event_type': 'comment',
            'comment': event.comment
        })

    async def send_event(self, event):
        await self.socket_ref.send_json(event)