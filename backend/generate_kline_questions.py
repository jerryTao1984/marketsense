"""
从 StockPillar API 拉取真实 K 线数据，生成 100 道 K 线实盘题目
"""
import sqlite3
import json
import os
import sys
import ssl
import urllib.request
import urllib.parse
import random
from datetime import datetime, timedelta

# 跳过 SSL 验证
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = os.environ.get("STOCKPILLAR_API_KEY", "sk_2645c49d31e6769badc17b20758c91d506d0e532dba00ac8475a0364eb541d2a")
API_URL = "https://layercake.com.cn/stockpillar/api/skill/v1"
# Docker 容器用 /data，本地开发用当前目录
DB_PATH = os.environ.get("DB_PATH", "shipanya.db")
# 输出图片路径：Docker 容器内 backend 下的 public 目录，本地开发用上层 public
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'public', 'assets', 'kline')
if not os.path.isdir(OUTPUT_DIR):
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'assets', 'kline')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 选取多行业、不同发展阶段的 A 股
STOCKS = [
    # 消费
    ("600519.SH", "贵州茅台"),     # 白酒龙头，成熟期
    ("000858.SZ", "五粮液"),        # 白酒，成熟期
    ("000651.SZ", "格力电器"),      # 家电，成熟期
    ("000333.SZ", "美的集团"),      # 家电，成熟期
    ("601888.SH", "中国中免"),      # 免税消费，成长期
    ("603288.SH", "海天味业"),      # 调味品，成熟期
    ("002714.SZ", "牧原股份"),      # 养猪，周期股
    # 科技
    ("300750.SZ", "宁德时代"),      # 锂电池龙头，成长期
    ("688981.SH", "中芯国际"),      # 芯片代工，成长期
    ("002415.SZ", "海康威视"),      # 安防，成熟期
    ("300059.SZ", "东方财富"),      # 互联网金融，成长期
    ("002230.SZ", "科大讯飞"),      # AI，成长期
    # 金融
    ("601318.SH", "中国平安"),      # 保险龙头，成熟期
    ("600036.SH", "招商银行"),      # 银行龙头，成熟期
    ("601398.SH", "工商银行"),      # 大行，成熟期
    ("601166.SH", "兴业银行"),      # 股份行，成熟期
    ("000001.SZ", "平安银行"),      # 股份行，成熟期
    # 医药
    ("600276.SH", "恒瑞医药"),      # 创新药龙头，成熟期
    ("603259.SH", "药明康德"),      # CXO，成长期
    ("300760.SZ", "迈瑞医疗"),      # 医疗器械，成熟期
    # 新能源
    ("601012.SH", "隆基绿能"),      # 光伏，成长期
    ("002594.SZ", "比亚迪"),        # 新能源车龙头，成长期
    # 周期/制造
    ("600900.SH", "长江电力"),      # 水电，成熟防御
    ("601857.SH", "中国石油"),      # 石油，周期股
    ("600028.SH", "中国石化"),      # 石化，周期股
    # 基建/地产
    ("601668.SH", "中国建筑"),      # 建筑龙头，成熟期
    ("000002.SZ", "万科A"),         # 地产，成熟期
    # 军工
    ("601989.SH", "中国重工"),      # 军工船舶，周期
    ("600760.SH", "中航沈飞"),      # 军工航空，成长期
    # 通信
    ("600941.SH", "中国移动"),      # 运营商，成熟期
    ("002456.SZ", "欧菲光"),        # 光学，成长期
]


def api_get(path, params=None):
    if not API_KEY:
        print("API error: STOCKPILLAR_API_KEY is not set")
        return None
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


def kline_image_url(code, recent=False):
    filename = f"kline_{code.replace('.', '_')}{'_20d' if recent else ''}.png"
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.isfile(file_path):
        return f"/assets/kline/{filename}"
    print(f"⚠️  Missing generated image for {code}: {filename}")
    return None


def calc_ma(prices, period):
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def calc_rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        gains.append(max(0, diff))
        losses.append(max(0, -diff))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def is_yang(open_p, close_p):
    return close_p > open_p


def is_yin(open_p, close_p):
    return close_p < open_p


def classify_kline(open_p, high, low, close_p):
    """简单判断K线类型"""
    body = abs(close_p - open_p)
    range_hl = high - low
    if range_hl == 0:
        return "十字星"
    body_ratio = body / range_hl if range_hl > 0 else 0
    upper_shadow = high - max(open_p, close_p)
    lower_shadow = min(open_p, close_p) - low

    if body_ratio < 0.1:
        return "十字星"
    if close_p > open_p:
        if lower_shadow > body * 2 and upper_shadow < body:
            return "锤子线"
        if upper_shadow > body * 2 and lower_shadow < body:
            return "射击之星"
        if body_ratio > 0.7:
            return "大阳线"
        return "阳线"
    else:
        if upper_shadow > body * 2 and lower_shadow < body:
            return "倒锤子线"
        if lower_shadow > body * 2 and upper_shadow < body:
            return "T字线"
        if body_ratio > 0.7:
            return "大阴线"
        return "阴线"


def generate_questions():
    """生成 100 道 K 线题目"""
    questions = []
    q_id = 0

    # 随机选择 15 只股票
    selected = random.sample(STOCKS, min(15, len(STOCKS)))

    for idx, (code, name) in enumerate(selected):
        # 获取最近 120 天 K 线
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=150)).strftime("%Y%m%d")

        data = api_get("prices/kline", {
            "ts_code": code,
            "start_date": start_date,
            "end_date": end_date,
        })

        if not data or "data" not in data or not data["data"]:
            print(f"跳过 {name}({code}) - 无数据")
            continue

        rows = data["data"]
        if len(rows) < 20:
            print(f"跳过 {name}({code}) - 数据不足 {len(rows)} 条")
            continue

        closes = [r["close"] for r in rows]
        opens = [r["open"] for r in rows]
        highs = [r["high"] for r in rows]
        lows = [r["low"] for r in rows]
        volumes = [r.get("vol", 0) for r in rows]
        dates = [r.get("trade_date", "") for r in rows]

        latest = rows[-1]
        recent_5 = rows[-5:]
        recent_10 = rows[-10:]
        recent_20 = rows[-20:]

        latest_close = closes[-1]
        latest_open = opens[-1]
        ma5 = calc_ma(closes, 5)
        ma10 = calc_ma(closes, 10)
        ma20 = calc_ma(closes, 20)
        ma60 = calc_ma(closes, min(60, len(closes)))
        rsi_val = calc_rsi(closes)

        # 最近 5 天涨跌
        change_5d = (closes[-1] - closes[-5]) / closes[-5] * 100 if len(closes) >= 5 else 0
        # 最近 20 天涨跌
        change_20d = (closes[-1] - closes[-20]) / closes[-20] * 100 if len(closes) >= 20 else 0

        # 最近 5 天成交量均值 vs 前 15 天
        vol_recent = sum(volumes[-5:]) / 5 if len(volumes) >= 5 else 0
        vol_prev = sum(volumes[-20:-5]) / 15 if len(volumes) >= 20 else 0
        vol_trend = "放量" if vol_recent > vol_prev * 1.2 else ("缩量" if vol_recent < vol_prev * 0.8 else "平量")

        # === 生成题目 ===

        # 类型1: 单根K线识别（最近一根K线）
        ktype = classify_kline(latest_open, latest["high"], latest["low"], latest_close)
        q_id += 1
        date_str = dates[-1] if dates[-1] else "最近"
        questions.append((
            f"kg_q{q_id}", "K1", "text",
            f"{name}（{code}）{date_str}的K线特征：开盘{latest_open:.2f}，最高{latest['high']:.2f}，"
            f"最低{latest['low']:.2f}，收盘{latest_close:.2f}，这根K线属于什么类型？",
            None,
            json.dumps([
                {"label": "阳线（收盘高于开盘）", "value": "A"},
                {"label": "阴线（收盘低于开盘）", "value": "B"},
                {"label": "十字星（开盘≈收盘）", "value": "C"},
                {"label": "一字线", "value": "D"},
            ]),
            "A" if is_yang(latest_open, latest_close) else ("B" if is_yin(latest_open, latest_close) else "C"),
            f"{name}当日{'收盘高于开盘为阳线' if is_yang(latest_open, latest_close) else '收盘低于开盘为阴线' if is_yin(latest_open, latest_close) else '开盘≈收盘为十字星'}，"
            f"实体{abs(latest_close - latest_open):.2f}元。"
        ))

        # 类型2: 价格与均线关系
        if ma5 and ma20:
            q_id += 1
            ma_relation = "高于" if latest_close > ma5 else "低于"
            questions.append((
                f"kg_q{q_id}", "K1", "text",
                f"{name}（{code}）当前收盘价 {latest_close:.2f} 元，MA5={ma5:.2f} 元，"
                f"价格相对 MA5 的位置是？",
                None,
                json.dumps([
                    {"label": "价格在 MA5 上方", "value": "A"},
                    {"label": "价格在 MA5 下方", "value": "B"},
                    {"label": "价格等于 MA5", "value": "C"},
                    {"label": "无法判断", "value": "D"},
                ]),
                "A" if ma_relation == "高于" else "B",
                f"{name}收盘价 {latest_close:.2f} {'>' if ma_relation == '高于' else '<'} MA5({ma5:.2f})，"
                f"价格{ma_relation}5日均线。"
            ))

        # 类型3: 短期趋势判断
        if ma10 and ma20:
            q_id += 1
            short_trend = "多头" if ma5 > ma10 > ma20 else ("空头" if ma5 < ma10 < ma20 else "混合")
            questions.append((
                f"kg_q{q_id}", "K2", "text",
                f"{name}（{code}）当前 MA5={ma5:.2f}，MA10={ma10:.2f}，MA20={ma20:.2f}，"
                f"均线排列状态是？",
                None,
                json.dumps([
                    {"label": "多头排列（MA5>MA10>MA20）", "value": "A"},
                    {"label": "空头排列（MA5<MA10<MA20）", "value": "B"},
                    {"label": "均线交叉缠绕", "value": "C"},
                    {"label": "全部均线平行向上", "value": "D"},
                ]),
                "A" if short_trend == "多头" else ("B" if short_trend == "空头" else "C"),
                f"MA5({ma5:.2f}) {'>' if ma5>ma10 else '<'} MA10({ma10:.2f}) {'>' if ma10>ma20 else '<'} MA20({ma20:.2f})，"
                f"属于{short_trend}排列。"
            ))

        # 类型4: 近N日涨跌判断
        q_id += 1
        trend_dir = "上涨" if change_5d > 0 else "下跌" if change_5d < 0 else "持平"
        questions.append((
            f"kg_q{q_id}", "P1", "text",
            f"{name}（{code}）最近 5 个交易日从 {closes[-5]:.2f} 元到 {latest_close:.2f} 元，"
            f"涨跌幅 {change_5d:+.1f}%，这期间走势是？",
            None,
            json.dumps([
                {"label": f"📈 上涨（{abs(change_5d):.1f}%）", "value": "A"},
                {"label": f"📉 下跌（{abs(change_5d):.1f}%）", "value": "B"},
                {"label": "➡️ 横盘（变化不大）", "value": "C"},
            ]),
            "A" if change_5d > 1 else ("B" if change_5d < -1 else "C"),
            f"{name}近5日{'上涨' if change_5d>1 else '下跌' if change_5d<-1 else '横盘'}{abs(change_5d):.1f}%，"
            f"从{closes[-5]:.2f}元到{latest_close:.2f}元。"
        ))

        # 类型5: 量价关系
        q_id += 1
        price_up = closes[-1] > closes[-2]
        vol_up = volumes[-1] > sum(volumes[-6:-1]) / 5 if len(volumes) >= 6 else False
        if price_up and vol_up:
            correct = "A"
            expl = f"价涨量增：当日收阳且成交量大于近5日均量，量价配合良好。"
        elif price_up and not vol_up:
            correct = "B"
            expl = f"价涨量缩：当日收阳但成交量萎缩，上涨动能可能不足。"
        elif not price_up and vol_up:
            correct = "C"
            expl = f"价跌量增：当日收阴且放量，卖压较重。"
        else:
            correct = "D"
            expl = f"价跌量缩：当日收阴且缩量，抛压在减少。"

        questions.append((
            f"kg_q{q_id}", "K4", "text",
            f"{name}（{code}）当日收盘{'上涨' if price_up else '下跌'}，"
            f"成交量{'放大' if vol_up else '萎缩'}（相比近5日均量），"
            f"量价关系属于？",
            None,
            json.dumps([
                {"label": "量价配合（价涨量增）", "value": "A"},
                {"label": "量价背离（价涨量缩）", "value": "B"},
                {"label": "放量下跌", "value": "C"},
                {"label": "缩量下跌", "value": "D"},
            ]),
            correct, expl
        ))

        # 类型6: RSI 超买超卖
        if rsi_val is not None:
            q_id += 1
            if rsi_val > 70:
                correct = "A"
                expl = f"RSI={rsi_val:.1f} > 70，处于超买区域，短期可能回调。"
            elif rsi_val < 30:
                correct = "B"
                expl = f"RSI={rsi_val:.1f} < 30，处于超卖区域，短期可能反弹。"
            else:
                correct = "C"
                expl = f"RSI={rsi_val:.1f} 在 30-70 之间，处于正常区间，无明显超买超卖信号。"

            questions.append((
                f"kg_q{q_id}", "K1", "text",
                f"{name}（{code}）当前 RSI(14) = {rsi_val:.1f}，技术面状态是？",
                None,
                json.dumps([
                    {"label": "超买区域（RSI>70）", "value": "A"},
                    {"label": "超卖区域（RSI<30）", "value": "B"},
                    {"label": "正常区域（30<RSI<70）", "value": "C"},
                    {"label": "RSI 无法计算", "value": "D"},
                ]),
                correct, expl
            ))

        # 类型7: 预测类 - 下周走势判断
        q_id += 1
        # 基于多项指标综合判断
        bullish_signals = 0
        if ma5 and ma20 and ma5 > ma20:
            bullish_signals += 1
        if rsi_val and 40 < rsi_val < 70:
            bullish_signals += 1
        if change_5d > 0:
            bullish_signals += 1
        if vol_trend == "放量" and change_5d > 0:
            bullish_signals += 1

        bearish_signals = 0
        if ma5 and ma20 and ma5 < ma20:
            bearish_signals += 1
        if rsi_val and rsi_val > 70:
            bearish_signals += 1
        if change_5d < 0:
            bearish_signals += 1
        if vol_trend == "放量" and change_5d < 0:
            bearish_signals += 1

        rsi_str = f"{rsi_val:.1f}" if rsi_val is not None else "N/A"

        if bullish_signals >= 3:
            predict_answer = "A"
            predict_expl = (f"多头信号占优：{bullish_signals}个看涨信号，"
                           f"5日涨幅{change_5d:+.1f}%，{vol_trend}，RSI={rsi_str}，"
                           f"短期偏强。")
        elif bearish_signals >= 3:
            predict_answer = "B"
            predict_expl = (f"空头信号占优：{bearish_signals}个看跌信号，"
                           f"5日跌幅{change_5d:+.1f}%，{vol_trend}，RSI={rsi_str}，"
                           f"短期偏弱。")
        else:
            predict_answer = "C"
            predict_expl = (f"多空信号均衡：5日变动{change_5d:+.1f}%，{vol_trend}，"
                           f"RSI={rsi_str}，"
                           f"短期方向不明确。")

        # 20日K线图作为题目配图
        img_url = kline_image_url(code, recent=True)

        questions.append((
            f"kg_q{q_id}", "P1", "image",
            f"{name}（{code}）基于近期数据：5日{vol_trend}{change_5d:+.1f}%，"
            f"RSI={rsi_str}，"
            f"请判断下周可能走势？",
            img_url,
            json.dumps([
                {"label": "📈 偏强看涨", "value": "A"},
                {"label": "📉 偏弱看跌", "value": "B"},
                {"label": "➡️ 横盘震荡", "value": "C"},
            ]),
            predict_answer, predict_expl
        ))

        # 类型8: 支撑压力位
        if len(recent_20) >= 10:
            q_id += 1
            high_20 = max(r["high"] for r in recent_20)
            low_20 = min(r["low"] for r in recent_20)
            dist_to_high = (high_20 - latest_close) / latest_close * 100
            dist_to_low = (latest_close - low_20) / latest_close * 100

            img_url = kline_image_url(code, recent=True)

            if dist_to_high < 3:
                correct = "A"
                expl = f"当前价{latest_close:.2f}距20日高点{high_20:.2f}仅{dist_to_high:.1f}%，接近前期压力位。"
            elif dist_to_low < 3:
                correct = "B"
                expl = f"当前价{latest_close:.2f}距20日低点{low_20:.2f}仅{dist_to_low:.1f}%，接近前期支撑位。"
            else:
                correct = "C"
                expl = f"当前价{latest_close:.2f}在20日区间[{low_20:.2f}, {high_20:.2f}]中间位置，" \
                       f"距高点{dist_to_high:.1f}%，距低点{dist_to_low:.1f}%。"

            questions.append((
                f"kg_q{q_id}", "P3", "image",
                f"{name}（{code}）当前价 {latest_close:.2f} 元，"
                f"20日最高 {high_20:.2f} 元，最低 {low_20:.2f} 元，"
                f"价格当前位置？",
                img_url,
                json.dumps([
                    {"label": "接近压力位（距20日高点<3%）", "value": "A"},
                    {"label": "接近支撑位（距20日低点<3%）", "value": "B"},
                    {"label": "区间中部（上下都有空间）", "value": "C"},
                    {"label": "无法判断", "value": "D"},
                ]),
                correct, expl
            ))

        # 类型9: 中长期趋势
        if ma20 and ma60:
            q_id += 1
            mid_trend = "MA20>MA60，中期偏多" if ma20 > ma60 else "MA20<MA60，中期偏空"
            img_url = kline_image_url(code, recent=True)

            questions.append((
                f"kg_q{q_id}", "P2", "image",
                f"{name}（{code}）MA20={ma20:.2f}，MA60={ma60:.2f}，中期趋势判断？",
                img_url,
                json.dumps([
                    {"label": "中期偏多（MA20在MA60上方）", "value": "A"},
                    {"label": "中期偏空（MA20在MA60下方）", "value": "B"},
                    {"label": "趋势不明（均线接近）", "value": "C"},
                ]),
                "A" if ma20 > ma60 else "B" if (ma60 - ma20) / ma60 > 0.02 else "C",
                f"MA20({ma20:.2f}) {'>' if ma20>ma60 else '<'} MA60({ma60:.2f})，"
                f"{mid_trend}。"
            ))

        print(f"✅ {name}({code}) 生成 {q_id} 题")

        if q_id >= 100:
            break

    return questions


def save_to_db(questions):
    """写入 SQLite"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    count = 0
    for q in questions:
        q_id, level_id, q_type, title, image_url, options_json, answer, explanation = q
        cursor.execute(
            "INSERT OR REPLACE INTO questions (id, level_id, type, title, image_url, options_json, answer, explanation) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (q_id, level_id, q_type, title, image_url, options_json, answer, explanation)
        )
        count += 1

    conn.commit()
    conn.close()
    print(f"\n✅ 写入 {count} 道题目到 {DB_PATH}")


if __name__ == "__main__":
    import traceback
    try:
        print("开始从 StockPillar API 拉取真实 K 线数据...")
        questions = generate_questions()
        print(f"\n共生成 {len(questions)} 道题目")
        if len(questions) == 0:
            print("⚠️  没有生成任何题目，可能是 API 不可达或数据不足")
            print("   跳过题目生成，系统将使用 init_db 中的基础题目")
            sys.exit(2)
        else:
            save_to_db(questions)
    except Exception as e:
        print(f"❌ 生成题目失败: {e}")
        traceback.print_exc()
        print("   跳过题目生成，系统将使用 init_db 中的基础题目")
        sys.exit(1)
