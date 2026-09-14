from flask import Flask, request, make_response

app = Flask(__name__)

FLAG = open("/flag.txt").read().strip()

REQUIRED_IP = "127.0.0.1"
REQUIRED_UA = "Mozilla/5.0 (compatible; ImpostorBot/1.0)"
REQUIRED_REFERER = "https://admin.internal.ctf/login"


@app.route("/", methods=["GET", "POST", "OPTIONS"])
def index():
    if request.method == "OPTIONS":
        resp = make_response(
            "\U0001f50d \u68c0\u6d4b\u5230\u63a2\u6d4b\u8bf7\u6c42... \u8ba9\u6211\u770b\u770b\u4f60\u7684\u4f2a\u88c5\u80fd\u529b\u3002\n\n"
            "\u4f60\u9700\u8981\u6ee1\u8db3\u4ee5\u4e0b\u6761\u4ef6\uff1a\n"
            "1. \u4ece\u5185\u90e8\u7f51\u7edc\u8bbf\u95ee (X-Forwarded-For)\n"
            "2. \u4f7f\u7528\u6b63\u786e\u7684\u5ba2\u6237\u7aef\u6807\u8bc6 (User-Agent)\n"
            "3. \u4ece\u7ba1\u7406\u540e\u53f0\u8df3\u8f6c\u8fc7\u6765 (Referer)\n\n"
            "\u4f7f\u7528 POST \u65b9\u6cd5\u5e26\u4e0a\u6b63\u786e\u7684 Headers \u6765\u83b7\u53d6 flag\u3002\n"
        )
        resp.headers["X-Hint-IP"] = REQUIRED_IP
        resp.headers["X-Hint-UA"] = REQUIRED_UA
        resp.headers["X-Hint-Referer"] = REQUIRED_REFERER
        resp.headers["Allow"] = "GET, POST, OPTIONS"
        return resp

    if request.method == "POST":
        xff = request.headers.get("X-Forwarded-For", "")
        ua = request.headers.get("User-Agent", "")
        referer = request.headers.get("Referer", "")

        if xff != REQUIRED_IP:
            return "IP \u9a8c\u8bc1\u5931\u8d25\uff01\u4f60\u4e0d\u662f\u6765\u81ea\u5185\u90e8\u7f51\u7edc\u3002", 403
        if ua != REQUIRED_UA:
            return "User-Agent \u9a8c\u8bc1\u5931\u8d25\uff01\u4f60\u4e0d\u662f\u6307\u5b9a\u7684\u5ba2\u6237\u7aef\u3002", 403
        if referer != REQUIRED_REFERER:
            return "Referer \u9a8c\u8bc1\u5931\u8d25\uff01\u4f60\u4e0d\u662f\u4ece\u7ba1\u7406\u540e\u53f0\u8df3\u8f6c\u8fc7\u6765\u7684\u3002", 403

        return "\U0001f389 \u4f2a\u88c5\u6210\u529f\uff01\u6b22\u8fce\u8fdb\u5165\u5185\u90e8\u7cfb\u7edf\u3002\n\nFlag: " + FLAG

    resp = make_response(
        "<!DOCTYPE html>\n<html>\n"
        "<head><title>\u5185\u90e8\u7ba1\u7406\u7cfb\u7edf v3.2</title></head>\n"
        '<body style="background:#1a1a2e;color:#eee;font-family:monospace;padding:40px;">\n'
        "<h1>\U0001f510 \u5185\u90e8\u7ba1\u7406\u7cfb\u7edf v3.2</h1>\n<hr>\n"
        "<p>\u6b22\u8fce\u8bbf\u95ee\u5185\u90e8\u7ba1\u7406\u7cfb\u7edf\u3002"
        "\u4f60\u7684\u8bf7\u6c42\u770b\u8d77\u6765\u5b8c\u5168\u6b63\u5e38\u2014\u2014\u4e5f\u592a\u6b63\u5e38\u4e86\u3002</p>\n"
        '<p style="color:#ff6b6b;">\u63d0\u793a\uff1a\u771f\u6b63\u7684\u7ba1\u7406\u5458\u4e0d\u4f1a'
        "\u7528\u666e\u901a\u7684 GET \u8bf7\u6c42\u8bbf\u95ee\u8fd9\u4e2a\u9875\u9762...</p>\n"
        "<!-- \u63d0\u793a\uff1a\u8bd5\u8bd5 HTTP \u7684 OPTIONS \u65b9\u6cd5 -->\n"
        "</body>\n</html>"
    )
    resp.headers["X-Backend-Version"] = "3.2"
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
