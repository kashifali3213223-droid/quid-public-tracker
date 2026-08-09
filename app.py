import os
import threading
from flask import Flask, jsonify, request, render_template

from tracker import (
    wallet_volume,
    wallet_swap_count,
    data_lock,
    tracker_status,
    start_tracker,
)

app = Flask(__name__)


def snapshot():
    with data_lock:
        ranked = sorted(
            wallet_volume.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        total_volume = sum(wallet_volume.values())
        rows = [
            {
                "rank": i + 1,
                "wallet": address,
                "swaps": wallet_swap_count.get(address, 0),
                "volume_usd": round(volume, 2),
            }
            for i, (address, volume) in enumerate(ranked)
        ]
        return {
            "total_wallets": len(wallet_volume),
            "total_volume_usd": round(total_volume, 2),
            "wallets": rows,
            "tracker_running": tracker_status["running"],
            "last_error": tracker_status["last_error"],
            "last_swap_time": tracker_status["last_swap_time"],
        }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/stats")
def stats():
    return jsonify(snapshot())


@app.get("/api/wallet")
def wallet():
    address = request.args.get("address", "").strip().lower()
    if not address:
        return jsonify({"error": "address is required"}), 400

    with data_lock:
        volume = wallet_volume.get(address)
        swaps = wallet_swap_count.get(address, 0)

    if volume is None:
        return jsonify({
            "found": False,
            "wallet": address,
            "swaps": 0,
            "volume_usd": 0,
        })

    return jsonify({
        "found": True,
        "wallet": address,
        "swaps": swaps,
        "volume_usd": round(volume, 2),
    })


if __name__ == "__main__":
    start_tracker()
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, threaded=True)
