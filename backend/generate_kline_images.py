"""
用 matplotlib 生成真实 K 线图，保存到前端静态目录
"""
import sqlite3
import ssl
import urllib.request
import urllib.parse
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

# 设置中文字体（Docker 用 Noto，本地用 PingFang）
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'PingFang SC', 'Arial Unicode MS', 'STHeiti', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = "sk_2645c49d31e6769badc17b20758c91d506d0e532dba00ac8475a0364eb541d2a"
API_URL = "https://layercake.com.cn/stockpillar/api/skill/v1"
# Docker 容器用 /data，本地开发用当前目录
DB_PATH = os.environ.get("DB_PATH", "shipanya.db")
# 输出到 backend/public/assets/kline（Docker 和 本地都兼容）
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'public', 'assets', 'kline')
if not os.path.isdir(OUTPUT_DIR):
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'assets', 'kline')

STOCKS = [
    ("600519.SH", "贵州茅台"), ("000858.SZ", "五粮液"),
    ("601318.SH", "中国平安"), ("000333.SZ", "美的集团"),
    ("300750.SZ", "宁德时代"), ("601012.SH", "隆基绿能"),
    ("002594.SZ", "比亚迪"), ("600036.SH", "招商银行"),
    ("000001.SZ", "平安银行"), ("601888.SH", "中国中免"),
    ("600900.SH", "长江电力"), ("002714.SZ", "牧原股份"),
    ("601166.SH", "兴业银行"), ("000651.SZ", "格力电器"),
    ("603259.SH", "药明康德"), ("300059.SZ", "东方财富"),
    ("600276.SH", "恒瑞医药"), ("601398.SH", "工商银行"),
    ("002415.SZ", "海康威视"), ("688981.SH", "中芯国际"),
    ("601989.SH", "中国重工"), ("600760.SH", "中航沈飞"),
    ("600941.SH", "中国移动"), ("002230.SZ", "科大讯飞"),
    ("600028.SH", "中国石化"),
]


def api_get(path, params=None):
    url = f"{API_URL}/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"API error {path}: {e}")
        return None


def plot_kline(rows, filename, title="", show_ma=True, highlight_last=5):
    """绘制 K 线图"""
    if not rows or len(rows) < 10:
        return False

    dates = []
    opens, highs, lows, closes, volumes = [], [], [], [], []

    for r in rows:
        try:
            dt = datetime.strptime(str(r["trade_date"]), "%Y%m%d")
        except:
            dt = datetime.now()
        dates.append(dt)
        opens.append(r["open"])
        highs.append(r["high"])
        lows.append(r["low"])
        closes.append(r["close"])
        volumes.append(r.get("vol", 0))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    fig.suptitle(title, fontsize=12, fontweight='bold')

    # K线图
    x = np.arange(len(dates))
    width = 0.6

    for i in range(len(dates)):
        color = '#ef4444' if closes[i] >= opens[i] else '#22c55e'
        # K线实体
        ax1.bar(x[i], abs(closes[i] - opens[i]), bottom=min(opens[i], closes[i]),
                width=width, color=color, edgecolor=color, zorder=3)
        # 上下影线
        ax1.plot([x[i], x[i]], [lows[i], highs[i]], color=color, linewidth=1, zorder=3)

    # 均线
    if show_ma:
        for period, color_line, label in [(5, '#f59e0b', 'MA5'), (10, '#3b82f6', 'MA10'), (20, '#8b5cf6', 'MA20')]:
            if len(closes) >= period:
                ma = np.convolve(closes, np.ones(period)/period, mode='valid')
                ax1.plot(x[period-1:], ma, color=color_line, linewidth=1, label=label, alpha=0.8)
        ax1.legend(loc='upper left', fontsize=8)

    ax1.set_ylabel('价格', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # 成交量
    colors = ['#ef4444' if closes[i] >= opens[i] else '#22c55e' for i in range(len(dates))]
    ax2.bar(x, volumes, color=colors, width=width, alpha=0.7, zorder=3)
    ax2.set_ylabel('成交量', fontsize=9)
    ax2.set_xlabel('日期', fontsize=9)

    # x轴日期标签
    step = max(1, len(dates) // 8)
    ax2.set_xticks(x[::step])
    ax2.set_xticklabels([d.strftime('%m/%d') for d in dates[::step]], rotation=30, fontsize=8)

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=120, bbox_inches='tight')
    plt.close()
    return True


def generate_all_kline_images():
    """为所有股票生成K线图"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    count = 0

    for code, name in STOCKS:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=120)).strftime("%Y%m%d")

        data = api_get("prices/kline", {
            "ts_code": code,
            "start_date": start_date,
            "end_date": end_date,
        })

        if not data or "data" not in data or not data["data"]:
            print(f"跳过 {name}({code})")
            continue

        rows = data["data"]
        if len(rows) < 20:
            print(f"跳过 {name}({code}) - 数据不足")
            continue

        # 完整K线图
        filename = f"kline_{code.replace('.', '_')}.png"
        if plot_kline(rows, filename, f"{name}（{code}）近120日K线图"):
            count += 1
            print(f"✅ {name}: {filename}")

        # 最近20日K线图（用于预测题）
        recent = rows[-20:]
        filename_recent = f"kline_{code.replace('.', '_')}_20d.png"
        if plot_kline(recent, filename_recent, f"{name}（{code}）近20日K线图", highlight_last=5):
            count += 1
            print(f"✅ {name} 20日: {filename_recent}")

    print(f"\n共生成 {count} 张K线图")


def update_db_image_urls():
    """更新数据库中K线题目的 image_url"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 为 K1/K2 题目设置图片URL
    cursor.execute("SELECT id, title FROM questions WHERE level_id IN ('K1', 'K2', 'K3', 'K4')")
    kline_questions = cursor.fetchall()

    # 为 P1/P2/P3 预测题设置图片URL
    cursor.execute("SELECT id, title FROM questions WHERE level_id IN ('P1', 'P2', 'P3')")
    predict_questions = cursor.fetchall()

    all_questions = kline_questions + predict_questions

    import re
    updated = 0
    for q_id, title in all_questions:
        # 从题目中提取股票代码
        match = re.search(r'（(\d+\.\w+)）', title)
        if match:
            code = match.group(1)
            if level_in_predict(q_id):
                img_url = f"/assets/kline/kline_{code.replace('.', '_')}_20d.png"
            else:
                img_url = f"/assets/kline/kline_{code.replace('.', '_')}.png"
            cursor.execute("UPDATE questions SET image_url = ? WHERE id = ?", (img_url, q_id))
            updated += 1

    conn.commit()
    conn.close()
    print(f"更新了 {updated} 道题目的 image_url")


def level_in_predict(q_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT level_id FROM questions WHERE id = ?", (q_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0] in ('P1', 'P2', 'P3')
    return False


if __name__ == "__main__":
    import traceback
    try:
        print("生成 K 线图...")
        generate_all_kline_images()
        print("\n更新数据库图片链接...")
        update_db_image_urls()
    except Exception as e:
        print(f"❌ 生成 K 线图失败: {e}")
        traceback.print_exc()
        exit(1)
