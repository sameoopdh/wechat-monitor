import requests
import feedparser
import os

# ============= 你只需要改这里 =============
# 公众号 RSS 链接（可添加多个）
RSS_URLS = [
    "https://rsshub.app/wechat/gh_b8f5b6d69123",
	"https://rsshub.app/wechat/gh_7e5b213d574a",
	"https://rsshub.app/wechat/gh_635855300233",
    # "https://rsshub.app/wechat/gh_yyyyyyy",
]

# 关键词列表
KEYWORDS = ["停水通知", "葛店开发区"]
# ========================================

def get_access_token():
    """获取微信接口调用凭证"""
    appid = os.getenv("WX_APPID")
    secret = os.getenv("WX_APPSECRET")
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    res = requests.get(url).json()
    return res.get("access_token")

def send_wechat(title, content):
    """发送消息到微信"""
    try:
        token = get_access_token()
        openid = os.getenv("WX_OPENID")
        template_id = os.getenv("WX_TEMPLATE_ID")

        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"

        data = {
            "touser": openid,
            "template_id": template_id,
            "data": {
                "title": {"value": f"【监控提醒】{title}"},
                "content": {"value": content}
            }
        }
        requests.post(url, json=data)
        print("推送成功：" + title)
    except Exception as e:
        print("推送失败：", e)

def monitor():
    print("开始监控...")
    for rss_url in RSS_URLS:
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                content = entry.get("summary", "")[:200]  # 取摘要

                # 匹配关键词
                for kw in KEYWORDS:
                    if kw in title or kw in content:
                        msg = f"关键词：{kw}\n文章标题：{title}\n链接：{link}"
                        print("发现：" + msg)
                        send_wechat(title, msg)
                        return  # 找到即推送，避免重复
        except Exception as e:
            print("出错：", e)

if __name__ == "__main__":
    monitor()
































