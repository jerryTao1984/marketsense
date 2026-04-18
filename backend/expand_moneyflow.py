"""
扩充K线实盘和预测题目，增加资金流维度（主力资金、北向资金、融资融券等）
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'shipanya.db')

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

def gen_moneyflow_questions(cursor):
    """生成资金流相关题目，分配到K1-K4和P1-P3"""
    questions = {
        'K1': [
            {
                "title": "某股票当日收阳线且主力资金净流入5000万元，量价关系属于？",
                "options": [
                    {"label": "价涨量增，主力资金推动的健康上涨", "value": "A"},
                    {"label": "价涨量缩，上涨动能不足", "value": "B"},
                    {"label": "放量下跌，卖压沉重", "value": "C"},
                    {"label": "缩量下跌，抛压减少", "value": "D"},
                ],
                "answer": "A",
                "explanation": "收阳线（价涨）且主力资金大幅净流入，说明机构资金在积极买入，属于量价配合的健康上涨。"
            },
            {
                "title": "某股票当日股价上涨，但主力资金净流出2亿元，说明？",
                "options": [
                    {"label": "机构在持续加仓", "value": "A"},
                    {"label": "散户推动上涨，机构在逢高减仓派发", "value": "B"},
                    {"label": "北向资金在买入", "value": "C"},
                    {"label": "量价配合良好", "value": "D"},
                ],
                "answer": "B",
                "explanation": "股价上涨但主力资金净流出，说明散户推动的上涨，而机构大户在逢高减仓派发，这是一个危险的背离信号。"
            },
            {
                "title": "什么是主力资金？",
                "options": [
                    {"label": "散户的小额资金", "value": "A"},
                    {"label": "由特大单和大单构成的机构或大户资金", "value": "B"},
                    {"label": "公司的注册资本", "value": "C"},
                    {"label": "银行贷款资金", "value": "D"},
                ],
                "answer": "B",
                "explanation": "主力资金通常由特大单（≥100万元）和大单（20-100万元）构成，反映机构或大户的买卖动向。"
            },
            {
                "title": "北向资金通常被称为A股的什么？",
                "options": [
                    {"label": "热钱", "value": "A"},
                    {"label": "聪明钱和风向标", "value": "B"},
                    {"label": "散户资金", "value": "C"},
                    {"label": "游资", "value": "D"},
                ],
                "answer": "B",
                "explanation": "北向资金（沪深港通外资）被视为A股的聪明钱和风向标，具有中长线资金配置意义。"
            },
            {
                "title": "DDX指标反映什么？",
                "options": [
                    {"label": "RSI超买超卖", "value": "A"},
                    {"label": "大单动向，反映主力买入意愿", "value": "B"},
                    {"label": "MACD金叉死叉", "value": "C"},
                    {"label": "布林带宽度", "value": "D"},
                ],
                "answer": "B",
                "explanation": "DDX（大单动向指标）反映主力买入意愿，是衡量主力资金流向的重要指标。"
            },
        ],
        'K2': [
            {
                "title": "某股票连续3日股价下跌，但主力资金持续净流入，这属于什么信号？",
                "options": [
                    {"label": "机构在逢低吸筹，可能即将反转", "value": "A"},
                    {"label": "主力在出逃", "value": "B"},
                    {"label": "量价配合良好", "value": "C"},
                    {"label": "趋势将加速下跌", "value": "D"},
                ],
                "answer": "A",
                "explanation": "股价下跌但主力资金持续净流入，说明机构在逢低悄悄吸筹，通常是底部反转的前兆。"
            },
            {
                "title": "融资余额连续增加，同时股价持续上涨，说明？",
                "options": [
                    {"label": "做空力量强大", "value": "A"},
                    {"label": "杠杆资金看多情绪浓厚，趋势可能延续", "value": "B"},
                    {"label": "市场极度悲观", "value": "C"},
                    {"label": "机构在抛售", "value": "D"},
                ],
                "answer": "B",
                "explanation": "融资余额增加说明借钱买入的杠杆资金增多，看多情绪浓厚，趋势可能延续。但需警惕融资盘过度拥挤。"
            },
            {
                "title": "某股票当日放巨量但K线实体极小（十字星），同时主力资金净流出，说明？",
                "options": [
                    {"label": "机构在悄悄加仓", "value": "A"},
                    {"label": "高位放量滞涨，机构可能在派发出货", "value": "B"},
                    {"label": "量价配合良好", "value": "C"},
                    {"label": "底部反转信号", "value": "D"},
                ],
                "answer": "B",
                "explanation": "放巨量但K线实体极小（高努力低结果），配合主力资金净流出，说明散户买入的热情被机构限价卖单吸收，是派发出货信号。"
            },
            {
                "title": "北向资金连续5日净流入某股票，但股价横盘不动，说明？",
                "options": [
                    {"label": "外资在逢低布局，后续可能突破", "value": "A"},
                    {"label": "外资在出逃", "value": "B"},
                    {"label": "股价会暴跌", "value": "C"},
                    {"label": "没有意义", "value": "D"},
                ],
                "answer": "A",
                "explanation": "外资持续流入但股价不动，说明有大资金在低位吸纳筹码，这通常是蓄势待发的信号。"
            },
            {
                "title": "融券余额创历史新高，同时股价在高位震荡，说明？",
                "options": [
                    {"label": "看空情绪积累，下跌风险加大", "value": "A"},
                    {"label": "市场看多", "value": "B"},
                    {"label": "没有风险", "value": "C"},
                    {"label": "应该加仓", "value": "D"},
                ],
                "answer": "A",
                "explanation": "融券余额高说明做空力量在积累，同时股价在高位震荡显示上涨动能不足，下跌风险加大。"
            },
        ],
        'K3': [
            {
                "title": "主力资金流向与股价短期表现出现背离时，应该优先考虑哪个信号？",
                "options": [
                    {"label": "股价走势", "value": "A"},
                    {"label": "主力资金流向，因为机构信息更充分", "value": "B"},
                    {"label": "RSI指标", "value": "C"},
                    {"label": "布林带", "value": "D"},
                ],
                "answer": "B",
                "explanation": "主力资金流向与股价出现背离时，应重视资金信号。机构拥有更充分的信息和研究能力，资金流向往往领先于价格变化。"
            },
            {
                "title": "某股票突破20日新高，但主力资金净流入很少，成交量萎缩，这属于？",
                "options": [
                    {"label": "健康突破", "value": "A"},
                    {"label": "假突破（海龟汤信号），缺乏资金支持", "value": "B"},
                    {"label": "趋势极强", "value": "C"},
                    {"label": "应该追涨", "value": "D"},
                ],
                "answer": "B",
                "explanation": "突破新高但缺乏资金支持和成交量配合，属于无量突破，极大概率是假突破。这是海龟汤策略的典型做空场景。"
            },
            {
                "title": "融资买入额占当日成交额比例超过15%，同时股价处于高位，说明？",
                "options": [
                    {"label": "市场极度理性", "value": "A"},
                    {"label": "杠杆资金过度拥挤，一旦回调将加速下跌", "value": "B"},
                    {"label": "趋势将继续", "value": "C"},
                    {"label": "没有风险", "value": "D"},
                ],
                "answer": "B",
                "explanation": "融资盘占比过高说明杠杆资金过度拥挤。一旦股价回调，融资盘被迫平仓将形成踩踏效应，加速下跌。"
            },
            {
                "title": "北向资金当日大幅净流出100亿元，同时大盘K线收长阴线，说明？",
                "options": [
                    {"label": "外资在抄底", "value": "A"},
                    {"label": "外资看空A股，市场可能面临调整", "value": "B"},
                    {"label": "市场极度乐观", "value": "C"},
                    {"label": "应该加仓", "value": "D"},
                ],
                "answer": "B",
                "explanation": "北向资金大幅净流出配合大盘长阴线，说明外资在撤离，市场可能面临调整风险。"
            },
            {
                "title": "某股票底部缩量横盘20日，某日突然放量长阳突破，主力资金大幅净流入，同时北向资金同步加仓，这是？",
                "options": [
                    {"label": "假突破信号", "value": "A"},
                    {"label": "多重资金共振确认的真突破", "value": "B"},
                    {"label": "应该做空", "value": "C"},
                    {"label": "震荡信号", "value": "D"},
                ],
                "answer": "B",
                "explanation": "底部横盘后放量长阳+主力净流入+北向加仓，三重资金共振确认，这是高确信度的真突破信号。"
            },
        ],
        'K4': [
            {
                "title": "如何综合判断一只股票的资金面健康程度？",
                "options": [
                    {"label": "只看北向资金", "value": "A"},
                    {"label": "结合主力资金、北向资金、融资余额和量价关系综合判断", "value": "B"},
                    {"label": "只看成交量", "value": "C"},
                    {"label": "只看K线形态", "value": "D"},
                ],
                "answer": "B",
                "explanation": "健康的资金面需要多维验证：主力资金净流入、北向资金态度、融资余额变化与量价关系相互印证。"
            },
            {
                "title": "某股票股价创新高，但主力资金连续5日净流出，同时RSI出现顶背离，这是？",
                "options": [
                    {"label": "趋势极强的信号", "value": "A"},
                    {"label": "典型的顶部信号，应警惕反转", "value": "B"},
                    {"label": "应该追涨", "value": "C"},
                    {"label": "正常现象", "value": "D"},
                ],
                "answer": "B",
                "explanation": "股价新高但主力持续流出+RSI顶背离，这是经典的三重顶部确认信号，趋势反转概率极高。"
            },
            {
                "title": "融资余额下降但股价上涨，这属于什么情况？",
                "options": [
                    {"label": "杠杆资金看空但散户推动上涨", "value": "A"},
                    {"label": "去杠杆式上涨，更加健康", "value": "B"},
                    {"label": "趋势即将结束", "value": "C"},
                    {"label": "没有意义", "value": "D"},
                ],
                "answer": "B",
                "explanation": "融资余额下降说明激进杠杆资金在退出，但股价仍在上涨，说明上涨由中长期资金而非杠杆资金推动，这种上涨更可持续。"
            },
            {
                "title": "主力净流入占比超过流通市值的5%，通常意味着？",
                "options": [
                    {"label": "资金关注度低", "value": "A"},
                    {"label": "主力高度关注，可能出现趋势性行情", "value": "B"},
                    {"label": "散户行为", "value": "C"},
                    {"label": "量价背离", "value": "D"},
                ],
                "answer": "B",
                "explanation": "主力净流入占比超过流通市值5%属于极高比例，说明主力资金高度关注并大举介入，可能推动趋势性行情。"
            },
            {
                "title": "当某股票出现量价齐升、主力净流入、北向加仓、融资余额适度增长四重共振时，说明？",
                "options": [
                    {"label": "应该立即做空", "value": "A"},
                    {"label": "多方资金高度一致看多，趋势极可能延续", "value": "B"},
                    {"label": "趋势即将结束", "value": "C"},
                    {"label": "震荡信号", "value": "D"},
                ],
                "answer": "B",
                "explanation": "量价+主力+北向+融资四重共振表明市场多方资金高度一致看多，这是最强的做多信号组合，趋势极可能延续。"
            },
        ],
        'P1': [
            {
                "title": "某股票近期K线横盘震荡，但主力资金持续净流入10日，北向资金同步加仓，预测下周走势？",
                "options": [
                    {"label": "偏强看涨，机构暗中吸筹即将突破", "value": "A"},
                    {"label": "偏弱看跌，横盘后大概率下跌", "value": "B"},
                    {"label": "横盘震荡，无明显方向", "value": "C"},
                ],
                "answer": "A",
                "explanation": "K线横盘但主力和北向资金持续流入，说明机构在悄悄吸筹布局，属于蓄势待发形态，偏强看涨。"
            },
            {
                "title": "某股票连续上涨，K线多头排列，但主力连续3日净流出，融资余额暴增，预测下周走势？",
                "options": [
                    {"label": "偏强看涨，趋势极强", "value": "A"},
                    {"label": "偏弱看跌，机构派发+杠杆过度拥挤", "value": "B"},
                    {"label": "横盘震荡", "value": "C"},
                ],
                "answer": "B",
                "explanation": "虽然K线多头排列，但主力在派发+融资暴增，说明上涨由散户杠杆推动，机构在撤退，反转风险极大。"
            },
            {
                "title": "某股票底部放量长阳，主力净流入3亿，北向加仓，融资余额温和增长，RSI从超卖区回升，预测下周？",
                "options": [
                    {"label": "偏强看涨，多重资金共振确认底部", "value": "A"},
                    {"label": "偏弱看跌，反弹即做空机会", "value": "B"},
                    {"label": "横盘震荡", "value": "C"},
                ],
                "answer": "A",
                "explanation": "底部放量长阳+主力大幅流入+北向加仓+融资温和+RSI回升，五重共振确认底部反转，偏强看涨。"
            },
        ],
        'P2': [
            {
                "title": "某股票经历大幅下跌后K线出现锤子线，主力资金由连续流出转为小幅净流入，但北向资金仍在流出，预测中期趋势？",
                "options": [
                    {"label": "中期偏多，底部初现但外资仍有分歧", "value": "A"},
                    {"label": "中期偏空，外资仍在撤离", "value": "B"},
                    {"label": "趋势不明，需观察", "value": "C"},
                ],
                "answer": "C",
                "explanation": "锤子线和主力流入转正显示底部可能形成，但北向资金仍在流出表明外资仍有分歧，多空信号不统一，需继续观察确认。"
            },
            {
                "title": "某股票高位K线射击之星，主力大幅净流出8000万，融资余额处于历史90%分位，RSI顶背离，预测中期走势？",
                "options": [
                    {"label": "中期偏多", "value": "A"},
                    {"label": "中期偏空，多重顶部信号共振", "value": "B"},
                    {"label": "趋势不明", "value": "C"},
                ],
                "answer": "B",
                "explanation": "射击之星+主力大幅流出+融资拥挤+RSI顶背离，四重顶部信号共振，中期偏空概率极高。"
            },
            {
                "title": "某股票K线MA20>MA60中期偏多，主力资金小幅净流入，北向资金连续5日加仓，但IVP处于极低水平，预测中期走势？",
                "options": [
                    {"label": "中期偏多，波动率挤压后可能出现突破", "value": "A"},
                    {"label": "中期偏空", "value": "B"},
                    {"label": "横盘震荡", "value": "C"},
                ],
                "answer": "A",
                "explanation": "中期均线多头+主力流入+北向加仓，叠加IVP极低（波动率挤压），预示可能出现方向性突破，偏强看涨。"
            },
        ],
        'P3': [
            {
                "title": "某股票K线在20日区间中位运行，主力资金连续流出但北向资金持续加仓，融资余额下降，当前位置判断？",
                "options": [
                    {"label": "接近压力位", "value": "A"},
                    {"label": "接近支撑位", "value": "B"},
                    {"label": "区间中部，内资外资分歧，需等待方向确认", "value": "C"},
                ],
                "answer": "C",
                "explanation": "价格在区间中部运行，内资（主力）流出但外资（北向）流入，融资在降温，信号矛盾，需等待资金面统一后再判断方向。"
            },
            {
                "title": "某股票K线接近20日高点，主力资金大幅净流入，北向加仓，融资余额适度增长，当前位置判断？",
                "options": [
                    {"label": "接近压力位，但资金面配合良好，突破概率高", "value": "A"},
                    {"label": "接近支撑位", "value": "B"},
                    {"label": "区间中部", "value": "C"},
                ],
                "answer": "A",
                "explanation": "虽然接近压力位，但主力资金大幅流入+北向加仓+融资适度增长，资金面全面配合，突破压力位的概率很高。"
            },
            {
                "title": "某股票K线距20日低点仅2%，主力净流出但缩量，北向资金由流出转为流入，融资余额下降，当前位置判断？",
                "options": [
                    {"label": "接近压力位", "value": "A"},
                    {"label": "接近支撑位，卖压衰竭+外资抄底，反弹概率大", "value": "B"},
                    {"label": "区间中部", "value": "C"},
                ],
                "answer": "B",
                "explanation": "距20日低点仅2%且主力缩量流出（卖压减弱）+北向转流入（外资抄底），支撑位附近的反弹概率较高。"
            },
        ],
    }

    count = 0
    for level_id, qs in questions.items():
        for i, q in enumerate(qs):
            qid = f"moneyflow_{count + 1}"
            count += 1
            insert_q(cursor, qid, level_id, 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=i+1)
    return count

if __name__ == "__main__":
    conn = get_db()
    cursor = conn.cursor()

    print("生成资金流相关题目...")
    mf_count = gen_moneyflow_questions(cursor)
    print(f"OK 资金流题目: {mf_count} 题")

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM questions")
    total = cursor.fetchone()[0]
    print(f"\nTotal: {total} 题")

    cursor.execute("SELECT level_id, COUNT(*) FROM questions GROUP BY level_id ORDER BY level_id")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} 题")

    conn.close()
