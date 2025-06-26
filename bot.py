import os
from discord_interactions import InteractionType, InteractionResponseType, verify_key_decorator
from flask import Flask, request, jsonify

PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
app = Flask(__name__)

@app.route("/", methods=["POST"])
@verify_key_decorator(PUBLIC_KEY)
def interactions():
    data = request.json
    if data["type"] == InteractionType.PING:
        return jsonify({"type": InteractionResponseType.PONG})

    if data["type"] == InteractionType.APPLICATION_COMMAND:
        if data["data"]["name"] == "order":
            order_text = data["data"]["options"][0]["value"]
            user_id = data["member"]["user"]["id"]

            # เก็บลง SQLite
            import sqlite3
            conn = sqlite3.connect("orders.db")
            conn.execute("INSERT INTO orders (user_id, order_text, status, notified) VALUES (?, ?, ?, ?)",
                         (user_id, order_text, "รอดำเนินการ", 0))
            conn.commit()
            conn.close()

            return jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": f"✅ รับออเดอร์แล้ว: `{order_text}`"
                }
            })

    return "bad request", 400
