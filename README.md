# Twisted Chat

Twisted based chat server using websocket protocol.
It became to live during few hours of STX Next internal hackathon.
Server stores chat history in memory, so it is gone when you restart server.

## How to run

1. `pip install -r requirements.txt`
2. `python server.py`

Server will listen on port 9000.

## Chat protocol

1. Sever accepts message: `<message>` - server will broadcast it to all the chat users (including sender)
2. Server accepts username change: `/username <new username>` - this will set username of the message sender and automatically broadcast list of chat users to all of them
3. Server sends out list of chat users: `/users user1,user2,...
4. Server sends out message in the JSON format:
```json
{
    "message": "test",
    "sender": "test_user",
    "timestamp": "2016-02-05T12:00:00.00000"
}
```
