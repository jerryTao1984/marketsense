"""
增强版 K 线题目：整合真实 K 线 + 资金流 + 基本面数据
"""
import sqlite3
import ssl
import urllib.request
import urllib.parse
import json
import os
from datetime import datetime, timedelta

ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = "sk_2645c49d31e6769badc17b20758c91d506d0e532dba00ac8475a0364eb541d2a"
API_URL = "https://layercake.com.cn/stockpillar/api/skill/v1"
DB_PATH = os.path.join(os.path.dirname(__file__), 'shipanya.db')

# 股票基本面数据（手动整理）
STOCK_INFO = {
    "600519.SH": {"name": "贵州茅台", "industry": "白酒", "pe": 28.5, "pb": 9.2, "eps": 51.5, "market_cap": "1.85万亿"},
    "000858.SZ": {"name": "五粮液", "industry": "白酒", "pe": 18.3, "pb": 5.1, "eps": 8.2, "market_cap": "5800亿"},
    "601318.SH": {"name": "中国平安", "industry": "保险", "pe": 9.8, "pb": 1.2, "eps": 6.5, "market_cap": "8900亿"},
    "000333.SZ": {"name": "美的集团", "industry": "家电", "pe": 13.5, "pb": 4.8, "eps": 5.1, "market_cap": "4800亿"},
    "300750.SZ": {"name": "宁德时代", "industry": "锂电池", "pe": 22.1, "pb": 5.6, "eps": 9.8, "market_cap": "8200亿"},
    "601012.SH": {"name": "隆基绿能", "industry": "光伏", "pe": 35.2, "pb": 3.1, "eps": 0.52, "market_cap": "1500亿"},
    "002594.SZ": {"name": "比亚迪", "industry": "新能源车", "pe": 25.8, "pb": 6.2, "eps": 11.2, "market_cap": "8600亿"},
    "600036.SH": {"name": "招商银行", "industry": "银行", "pe": 6.5, "pb": 0.95, "eps": 5.8, "market_cap": "8800亿"},
    "000001.SZ": {"name": "平安银行", "industry": "银行", "pe": 5.2, "pb": 0.58, "eps": 2.1, "market_cap": "2200亿"},
    "601888.SH": {"name": "中国中免", "industry": "免税消费", "pe": 32.1, "pb": 4.5, "eps": 2.3, "market_cap": "1200亿"},
    "600900.SH": {"name": "长江电力", "industry": "水电", "pe": 20.5, "pb": 3.8, "eps": 1.35, "market_cap": "6800亿"},
    "002714.SZ": {"name": "牧原股份", "industry": "养猪", "pe": 18.6, "pb": 3.2, "eps": 2.1, "market_cap": "2000亿"},
    "601166.SH": {"name": "兴业银行", "industry": "银行", "pe": 5.0, "pb": 0.52, "eps": 3.5, "market_cap": "3600亿"},
    "000651.SZ": {"name": "格力电器", "industry": "家电", "pe": 8.5, "pb": 2.8, "eps": 5.2, "market_cap": "2400亿"},
    "603259.SH": {"name": "药明康德", "industry": "CXO", "pe": 28.3, "pb": 4.2, "eps": 1.9, "market_cap": "1500亿"},
    "300059.SZ": {"name": "东方财富", "industry": "互联网金融", "pe": 45.2, "pb": 6.8, "eps": 0.52, "market_cap": "2800亿"},
    "600276.SH": {"name": "恒瑞医药", "industry": "创新药", "pe": 55.8, "pb": 8.5, "eps": 0.85, "market_cap": "3000亿"},
    "601398.SH": {"name": "工商银行", "industry": "银行", "pe": 5.8, "pb": 0.55, "eps": 0.92, "market_cap": "1.8万亿"},
    "002415.SZ": {"name": "海康威视", "industry": "安防", "pe": 22.5, "pb": 5.2, "eps": 1.5, "market_cap": "2800亿"},
    "688981.SH": {"name": "中芯国际", "industry": "芯片代工", "pe": 85.2, "pb": 3.5, "eps": 0.65, "market_cap": "4200亿"},
    "601989.SH": {"name": "中国重工", "industry": "军工船舶", "pe": 45.5, "pb": 1.8, "eps": 0.12, "market_cap": "1200亿"},
    "600760.SH": {"name": "中航沈飞", "industry": "军工航空", "pe": 65.2, "pb": 8.5, "eps": 0.68, "market_cap": "900亿"},
    "600941.SH": {"name": "中国移动", "industry": "运营商", "pe": 15.2, "pb": 1.5, "eps": 6.5, "market_cap": "2.1万亿"},
    "002230.SZ": {"name": "科大讯飞", "industry": "AI", "pe": 120.5, "pb": 8.2, "eps": 0.42, "market_cap": "1200亿"},
    "600028.SH": {"name": "中国石化", "industry": "石化", "pe": 12.5, "pb": 0.85, "eps": 0.52, "market_cap": "6800亿"},
}


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


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def insert_q(cursor, q_id, level_id, q_type, title, options, answer, explanation, image_url=None, sort_order=0):
    options_json = json.dumps(options, ensure_ascii=False)
    cursor.execute(
        "INSERT OR REPLACE INTO questions (id, level_id, type, title, image_url, options_json, answer, explanation, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (q_id, level_id, q_type, title, image_url, options_json, answer, explanation, sort_order)
    )


def analyze_moneyflow(mf_data):
    """分析资金流数据"""
    if not mf_data or len(mf_data) < 2:
        return {}

    latest = mf_data[0]
    prev = mf_data[1] if len(mf_data) > 1 else None

    # 主力资金净流入（超大单+大单）
    net_main = latest.get('net_mf_amount', 0)

    # 3日资金趋势
    net_3d = 0
    for d in mf_data[:3]:
        net_3d += d.get('net_mf_amount', 0)

    # 5日资金趋势
    net_5d = 0
    for d in mf_data[:5]:
        net_5d += d.get('net_mf_amount', 0)

    # 超大单方向
    net_elg = latest.get('buy_elg_amount', 0) - latest.get('sell_elg_amount', 0)

    result = {
        'net_main': net_main,
        'net_3d': net_3d,
        'net_5d': net_5d,
        'net_elg': net_elg,
        'trade_count': latest.get('trade_count', 0),
    }

    # 判断资金面状态
    if net_main > 50000:
        result['signal'] = '主力大幅流入'
    elif net_main > 0:
        result['signal'] = '主力小幅流入'
    elif net_main > -50000:
        result['signal'] = '主力小幅流出'
    else:
        result['signal'] = '主力大幅流出'

    return result


def generate_enhanced_questions():
    """生成增强版题目：K线+资金流+基本面"""
    conn = get_db()
    cursor = conn.cursor()

    selected_codes = [
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
        ("600941.SH", "中国移动"), ("002230.SZ", "科大讯飞"),
    ]

    qid_num = 1
    count = 0

    for code, name in selected_codes:
        info = STOCK_INFO.get(code, {})

        # 获取K线数据
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=60)).strftime("%Y%m%d")

        kline_data = api_get("prices/kline", {
            "ts_code": code,
            "start_date": start_date,
            "end_date": end_date,
        })

        # 获取资金流数据
        mf_data = api_get("moneyflow", {
            "ts_code": code,
            "start_date": start_date,
            "end_date": end_date,
        })

        if not kline_data or not mf_data or "data" not in kline_data or "data" not in mf_data:
            print(f"跳过 {name}({code}) - 数据不足")
            continue

        rows = kline_data["data"]
        mf_rows = mf_data["data"]

        if len(rows) < 10 or len(mf_rows) < 2:
            print(f"跳过 {name}({code}) - 数据量不够")
            continue

        latest = rows[-1]
        latest_close = latest["close"]
        latest_vol = latest.get("vol", 0)
        latest_amount = latest.get("amount", 0)
        latest_pct = latest.get("pct_chg", 0)

        # 资金流分析
        mf_analysis = analyze_moneyflow(mf_rows)

        # 基本面信息字符串
        pe_str = f"{info.get('pe', 'N/A')}" if info.get('pe') else 'N/A'
        pb_str = f"{info.get('pb', 'N/A')}" if info.get('pb') else 'N/A'
        eps_str = f"{info.get('eps', 'N/A')}" if info.get('eps') else 'N/A'
        industry = info.get('industry', '未知')
        market_cap = info.get('market_cap', '未知')

        fund_info = f"{mf_analysis.get('signal', '未知')}"
        if mf_analysis.get('net_main'):
            fund_info += f"（当日净流{mf_analysis['net_main']/10000:.0f}万）"

        # === 生成增强版题目 ===

        # 类型1: 综合基本面+资金流判断
        qid = f"enh_{qid_num}"
        qid_num += 1
        count += 1

        # 判断估值高低
        if isinstance(info.get('pe'), (int, float)):
            if info['pe'] < 10:
                val_desc = "低估值"
            elif info['pe'] < 30:
                val_desc = "合理估值"
            else:
                val_desc = "高估值"
        else:
            val_desc = "估值未知"

        # 判断趋势
        closes = [r["close"] for r in rows[-10:]]
        if len(closes) >= 5:
            trend_5d = (closes[-1] - closes[-5]) / closes[-5] * 100
        else:
            trend_5d = 0

        title = (f"{name}（{code}）{industry} | PE:{pe_str} PB:{pb_str} | "
                 f"收盘{latest_close:.2f} 涨跌{latest_pct:+.2f}% | "
                 f"资金面: {fund_info}")

        # 判断正确答案
        bullish = 0
        bearish = 0

        if mf_analysis.get('net_main', 0) > 0:
            bullish += 1
        else:
            bearish += 1

        if mf_analysis.get('net_3d', 0) > 0:
            bullish += 1
        else:
            bearish += 1

        if trend_5d > 0:
            bullish += 1
        else:
            bearish += 1

        if bullish >= 2:
            correct = "A"
            expl = (f"资金面：主力{mf_analysis.get('signal', '未知')}，3日净流{mf_analysis.get('net_3d', 0)/10000:.0f}万；"
                   f"技术面：5日{trend_5d:+.1f}%。综合判断偏多。")
        elif bearish >= 2:
            correct = "B"
            expl = (f"资金面：主力{mf_analysis.get('signal', '未知')}，3日净流{mf_analysis.get('net_3d', 0)/10000:.0f}万；"
                   f"技术面：5日{trend_5d:+.1f}%。综合判断偏空。")
        else:
            correct = "C"
            expl = (f"资金面和技术面信号矛盾，多空力量均衡，方向不明确。")

        insert_q(cursor, qid, 'K1', 'text', title, [
            {"label": f"📈 偏强看涨（{val_desc}+资金面配合）", "value": "A"},
            {"label": f"📉 偏弱看跌（资金流出+趋势走弱）", "value": "B"},
            {"label": "➡️ 方向不明（多空信号矛盾）", "value": "C"},
        ], correct, expl,
        image_url=f"/assets/kline/kline_{code.replace('.', '_')}.png",
        sort_order=count)

        # 类型2: 量价与资金流关系
        qid = f"enh_{qid_num}"
        qid_num += 1
        count += 1

        vol_avg_5d = sum(r.get('vol', 0) for r in rows[-5:]) / 5
        vol_trend = "放量" if latest_vol > vol_avg_5d * 1.2 else ("缩量" if latest_vol < vol_avg_5d * 0.8 else "平量")

        price_up = latest_pct > 0
        main_in = mf_analysis.get('net_main', 0) > 0

        if price_up and main_in:
            correct = "A"
            expl = f"价涨+主力流入+{vol_trend}，量价资金三维度配合良好，健康上涨。"
        elif price_up and not main_in:
            correct = "B"
            expl = f"价涨但主力流出+{vol_trend}，散户推涨机构派发，警惕假突破。"
        elif not price_up and main_in:
            correct = "C"
            expl = f"价跌但主力流入，机构逢低吸筹，可能是洗盘。"
        else:
            correct = "D"
            expl = f"价跌+主力流出+{vol_trend}，量价资金三维度均偏空。"

        title2 = (f"{name}（{code}）{industry} | 当日涨跌{latest_pct:+.2f}% 成交量{vol_trend} | "
                  f"资金{mf_analysis.get('signal', '未知')}（{mf_analysis.get('net_main', 0)/10000:.0f}万）| "
                  f"PE:{pe_str} PB:{pb_str}")

        insert_q(cursor, qid, 'K4', 'text', title2, [
            {"label": "量价资金配合良好（价涨+主力流入）", "value": "A"},
            {"label": "量价背离（价涨但主力流出，散户推涨）", "value": "B"},
            {"label": "洗盘吸筹（价跌但主力流入）", "value": "C"},
            {"label": "量价资金均偏空（价跌+主力流出）", "value": "D"},
        ], correct, expl,
        image_url=f"/assets/kline/kline_{code.replace('.', '_')}.png",
        sort_order=count)

        # 类型3: 资金趋势与K线共振
        qid = f"enh_{qid_num}"
        qid_num += 1
        count += 1

        net_5d = mf_analysis.get('net_5d', 0)
        fund_trend = "持续流入" if net_5d > 0 else "持续流出"

        # 均线判断
        ma5 = sum(closes[-5:]) / 5 if len(closes) >= 5 else 0
        ma_signal = "站上MA5" if latest_close > ma5 else "跌破MA5"

        if latest_close > ma5 and net_5d > 0:
            correct = "A"
            expl = f"价格{ma_signal}+5日资金{fund_trend}，K线与资金流共振看多。"
        elif latest_close < ma5 and net_5d < 0:
            correct = "B"
            expl = f"价格{ma_signal}+5日资金{fund_trend}，K线与资金流共振看空。"
        elif latest_close > ma5 and net_5d < 0:
            correct = "C"
            expl = f"价格{ma_signal}但5日资金{fund_trend}，资金面不支持上涨。"
        else:
            correct = "D"
            expl = f"价格{ma_signal}但5日资金{fund_trend}，可能底部吸筹。"

        title3 = (f"{name}（{code}）{industry} | 收盘{latest_close:.2f} MA5:{ma5:.2f} | "
                  f"5日资金净流{net_5d/10000:.0f}万（{fund_trend}）| "
                  f"PE:{pe_str} PB:{pb_str}")

        insert_q(cursor, qid, 'K2', 'text', title3, [
            {"label": "K线与资金共振看多（站稳均线+资金流入）", "value": "A"},
            {"label": "K线与资金共振看空（跌破均线+资金流出）", "value": "B"},
            {"label": "背离看空（站稳均线但资金流出）", "value": "C"},
            {"label": "背离看多（跌破均线但资金流入，可能底部吸筹）", "value": "D"},
        ], correct, expl,
        image_url=f"/assets/kline/kline_{code.replace('.', '_')}.png",
        sort_order=count)

        # 类型4: 预测类 - 下周走势
        qid = f"enh_{qid_num}"
        qid_num += 1
        count += 1

        signals_bull = 0
        signals_bear = 0

        if mf_analysis.get('net_main', 0) > 0:
            signals_bull += 1
        else:
            signals_bear += 1

        if mf_analysis.get('net_5d', 0) > 0:
            signals_bull += 1
        else:
            signals_bear += 1

        if trend_5d > 0:
            signals_bull += 1
        else:
            signals_bear += 1

        if mf_analysis.get('net_elg', 0) > 0:
            signals_bull += 1
        else:
            signals_bear += 1

        if signals_bull >= 3:
            correct = "A"
            predict_expl = (f"4项指标中{signals_bull}项看多：主力当日净流入、5日趋势、价格趋势、超大单方向。"
                          f"{industry}{val_desc}，资金面和技术面共振看多。")
        elif signals_bear >= 3:
            correct = "B"
            predict_expl = (f"4项指标中{signals_bear}项看空：主力资金流出、5日趋势、价格趋势。"
                          f"资金面和技术面共振看空。")
        else:
            correct = "C"
            predict_expl = (f"多空信号均衡：{signals_bull}项看多 vs {signals_bear}项看空。"
                          f"需要等待更多确认信号。")

        title4 = (f"{name}（{code}）{industry} | PE:{pe_str} PB:{pb_str} EPS:{eps_str} | "
                  f"5日{trend_5d:+.1f}% | 资金{mf_analysis.get('signal', '未知')} | "
                  f"5日净流{mf_analysis.get('net_5d', 0)/10000:.0f}万 | "
                  f"超大单{'流入' if mf_analysis.get('net_elg', 0) > 0 else '流出'}")

        insert_q(cursor, qid, 'P1', 'text', title4, [
            {"label": "📈 偏强看涨", "value": "A"},
            {"label": "📉 偏弱看跌", "value": "B"},
            {"label": "➡️ 横盘震荡", "value": "C"},
        ], correct, predict_expl,
        image_url=f"/assets/kline/kline_{code.replace('.', '_')}_20d.png",
        sort_order=count)

        if count % 10 == 0:
            print(f"✅ 已生成 {count} 道增强题目")

    conn.commit()
    conn.close()
    print(f"\n共生成 {count} 道增强版题目（K线+资金流+基本面）")


if __name__ == "__main__":
    print("生成增强版 K 线题目（整合真实资金流和基本面数据）...")
    generate_enhanced_questions()
