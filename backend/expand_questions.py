"""
扩充题库到 300+ 题
1. 基于海龟交易法则生成交易法则题目
2. 补充基础概念题目
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'shipanya.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_next_qid(cursor):
    cursor.execute("SELECT MAX(id) FROM questions")
    row = cursor.fetchone()
    if row and row[0]:
        prefix = 'expand_'
        nums = []
        cursor.execute("SELECT id FROM questions WHERE id LIKE 'exp%'", )
        for r in cursor.fetchall():
            try:
                nums.append(int(r['id'].split('_')[1]))
            except:
                pass
        if nums:
            return f"exp_{max(nums) + 1}"
    return "exp_1"


def insert_q(cursor, q_id, level_id, q_type, title, options, answer, explanation, image_url=None, sort_order=0):
    options_json = json.dumps(options, ensure_ascii=False)
    cursor.execute(
        "INSERT OR REPLACE INTO questions (id, level_id, type, title, image_url, options_json, answer, explanation, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (q_id, level_id, q_type, title, image_url, options_json, answer, explanation, sort_order)
    )


def gen_turtle_questions(cursor):
    """基于海龟交易法则生成题目 - T1~T4"""
    qid_num = 1

    def next_id():
        nonlocal qid_num
        qid = f"turtle_{qid_num}"
        qid_num += 1
        return qid

    # ===== T1: 海龟交易法基础 =====
    t1_questions = [
        {
            "title": "海龟交易法的创始人理查德·丹尼斯通过实验证明了什么？",
            "options": [
                {"label": "伟大交易员可以通过后天规则培养", "value": "A"},
                {"label": "交易员必须是天生有直觉的", "value": "B"},
                {"label": "只有华尔街精英才能成功", "value": "C"},
                {"label": "交易完全靠运气", "value": "D"},
            ],
            "answer": "A",
            "explanation": "丹尼斯招募并培训了一批毫无交易经验的普通人（海龟），他们用严格的机械化系统创造了年均80%的复合收益率，证明了交易员可以后天培养。"
        },
        {
            "title": "海龟交易法的胜率通常在什么范围？",
            "options": [
                {"label": "70%-80%", "value": "A"},
                {"label": "50%-60%", "value": "B"},
                {"label": "30%-40%", "value": "C"},
                {"label": "90%以上", "value": "D"},
            ],
            "answer": "C",
            "explanation": "海龟交易法的历史胜率通常仅徘徊在30%至40%之间，系统的正向期望完全依赖于非对称的盈亏比——在大量假突破中承受小额亏损，在少数史诗级趋势中攫取巨额利润。"
        },
        {
            "title": "海龟交易法的核心N值（ATR）计算的是什么？",
            "options": [
                {"label": "市场的成交量变化", "value": "A"},
                {"label": "真实波动幅度的20日EMA", "value": "B"},
                {"label": "价格的移动平均线", "value": "C"},
                {"label": "RSI超买超卖指标", "value": "D"},
            ],
            "answer": "B",
            "explanation": "N值是真实波动幅度（TR）的20日指数移动平均值（EMA）。TR取当日最高减最低、最高减前日收盘、最低减前日收盘三者中的最大值。"
        },
        {
            "title": "海龟交易法规定，单一头寸单位（Unit）的风险不能超过账户总资金的多少？",
            "options": [
                {"label": "5%", "value": "A"},
                {"label": "10%", "value": "B"},
                {"label": "1%", "value": "C"},
                {"label": "2%", "value": "D"},
            ],
            "answer": "C",
            "explanation": "海龟法则规定单一头寸单位（Unit）所承担的风险绝不能超过账户总权益的1%，这样理论上需要连续亏损100次才会爆仓。"
        },
        {
            "title": "海龟交易系统一（System 1）的入场触发基准是什么？",
            "options": [
                {"label": "55日最高价突破", "value": "A"},
                {"label": "10日最高价突破", "value": "B"},
                {"label": "20日最高价突破", "value": "C"},
                {"label": "100日最高价突破", "value": "D"},
            ],
            "answer": "C",
            "explanation": "系统一是激进的中短期突破系统，当价格突破过去20天的最高点时做多，跌破过去20天的最低点时做空。"
        },
        {
            "title": "海龟交易系统二（System 2）的入场触发基准是什么？",
            "options": [
                {"label": "20日最高价突破", "value": "A"},
                {"label": "55日最高价突破", "value": "B"},
                {"label": "10日最高价突破", "value": "C"},
                {"label": "100日最高价突破", "value": "D"},
            ],
            "answer": "B",
            "explanation": "系统二基于55日高低点突破，作为防止错失大趋势的故障保险机制，没有任何过滤规则，必须无条件执行。"
        },
        {
            "title": "海龟交易法的金字塔加仓步长是多少？",
            "options": [
                {"label": "1N", "value": "A"},
                {"label": "2N", "value": "B"},
                {"label": "0.5N", "value": "C"},
                {"label": "0.25N", "value": "D"},
            ],
            "answer": "C",
            "explanation": "一旦触发突破信号建立底仓，只要市场价格向有利方向移动0.5N（即半个N值），就增加1个Unit，直至达到4个Unit上限。"
        },
        {
            "title": "海龟交易法的初始止损设置在入场点反向多少距离？",
            "options": [
                {"label": "1N", "value": "A"},
                {"label": "0.5N", "value": "B"},
                {"label": "3N", "value": "C"},
                {"label": "2N", "value": "D"},
            ],
            "answer": "D",
            "explanation": "在建立任何Unit时，系统会在入场点反向2N的位置设置硬止损，这刚好等同于账户总权益2%的极限损失。"
        },
        {
            "title": "海龟系统一的退出离场基准是什么？",
            "options": [
                {"label": "跌破20日最低点", "value": "A"},
                {"label": "跌破10日最低点", "value": "B"},
                {"label": "跌破55日最低点", "value": "C"},
                {"label": "跌破5日最低点", "value": "D"},
            ],
            "answer": "B",
            "explanation": "系统一的退出基准是跌破过去10日的最低点（多头时）或突破过去10日的最高点（空头时）。"
        },
        {
            "title": "海龟系统二的退出离场基准是什么？",
            "options": [
                {"label": "跌破5日最低点", "value": "A"},
                {"label": "跌破10日最低点", "value": "B"},
                {"label": "跌破20日最低点", "value": "C"},
                {"label": "跌破55日最低点", "value": "D"},
            ],
            "answer": "C",
            "explanation": "系统二的退出基准是跌破过去20日的最低点（多头时）或突破过去20日的最高点（空头时）。"
        },
        {
            "title": "海龟法则中，单一市场最多可以累积多少个头寸单位（Units）？",
            "options": [
                {"label": "2个", "value": "A"},
                {"label": "4个", "value": "B"},
                {"label": "6个", "value": "C"},
                {"label": "12个", "value": "D"},
            ],
            "answer": "B",
            "explanation": "海龟规定单一市场（如仅限黄金）最高累积4个Units，防止在单一标的遭遇黑天鹅时造成毁灭性打击。"
        },
        {
            "title": "海龟法则中，高度相关市场同一方向上最多累积多少Units？",
            "options": [
                {"label": "4个", "value": "A"},
                {"label": "6个", "value": "B"},
                {"label": "10个", "value": "C"},
                {"label": "12个", "value": "D"},
            ],
            "answer": "B",
            "explanation": "高度相关市场（如原油与取暖油、黄金与白银）同一方向上最高累积6个Units，防止资金在同一宏观因子上暴露过度。"
        },
        {
            "title": "海龟交易中，TR（真实波动幅度）取以下哪项的最大值？",
            "options": [
                {"label": "当日收盘价减前日收盘价", "value": "A"},
                {"label": "当日最高减最低、最高减前日收盘、最低减前日收盘三者", "value": "B"},
                {"label": "当日成交量变化", "value": "C"},
                {"label": "当日开盘价减收盘价", "value": "D"},
            ],
            "answer": "B",
            "explanation": "TR取三者中的最大值：当日最高减最低、当日最高减前日收盘、当日最低减前日收盘，以全面衡量日内绝对变动。"
        },
        {
            "title": "海龟交易法中，账户从最高峰回撤达到10%时，应该怎么做？",
            "options": [
                {"label": "加大仓位快速回本", "value": "A"},
                {"label": "停止交易", "value": "B"},
                {"label": "将后续交易Unit规模削减20%", "value": "C"},
                {"label": "不变，继续正常交易", "value": "D"},
            ],
            "answer": "C",
            "explanation": "回撤达到10%时，必须强行将后续所有交易的Unit规模硬性削减20%，通过缩小头寸熬过震荡市。"
        },
        {
            "title": "海龟交易法中，如果上一次系统一突破是理论盈利信号，下一次信号应该如何处理？",
            "options": [
                {"label": "立即执行", "value": "A"},
                {"label": "加倍执行", "value": "B"},
                {"label": "强制忽略", "value": "C"},
                {"label": "减半执行", "value": "D"},
            ],
            "answer": "C",
            "explanation": "系统一内置过滤器：如果上一次突破是理论盈利信号，则当前突破信号被强制忽略，以规避震荡市的假突破磨损。"
        },
        {
            "title": "海龟交易中，Unit的计算公式是什么？",
            "options": [
                {"label": "Unit = 账户总资金 / N值", "value": "A"},
                {"label": "Unit = (账户总资金 × 1%) / (N × 合约乘数)", "value": "B"},
                {"label": "Unit = 账户总资金 × N值", "value": "C"},
                {"label": "Unit = N值 / 账户总资金", "value": "D"},
            ],
            "answer": "B",
            "explanation": "Unit = (账户总资金 × 1%) / Dollar_N，其中Dollar_N = N值 × 合约乘数。确保每笔交易风险为账户的1%。"
        },
    ]

    # ===== T2: 海龟进阶规则 =====
    t2_questions = [
        {
            "title": "海龟实验发生在哪个年代？",
            "options": [
                {"label": "1970年代初", "value": "A"},
                {"label": "1980年代初", "value": "B"},
                {"label": "1990年代初", "value": "C"},
                {"label": "2000年代初", "value": "D"},
            ],
            "answer": "B",
            "explanation": "海龟实验发生在20世纪80年代初（1983-1987），丹尼斯与埃克哈特围绕交易员是天生还是后天培养展开了著名争论。"
        },
        {
            "title": "海龟实验中，丹尼斯为什么禁止交易肉类期货？",
            "options": [
                {"label": "肉类没有趋势", "value": "A"},
                {"label": "当时肉类交易池存在严重价格操纵", "value": "B"},
                {"label": "肉类波动太小", "value": "C"},
                {"label": "没有足够流动性", "value": "D"},
            ],
            "answer": "B",
            "explanation": "当时芝加哥肉类交易池中存在严重的场内交易员价格操纵问题。后来FBI确实开展了针对肉类交易池的诱捕行动，起诉了大量涉嫌操纵的交易员。"
        },
        {
            "title": "海龟交易法中，单向总敞口（做多或做空）最高累积多少Units？",
            "options": [
                {"label": "4个", "value": "A"},
                {"label": "6个", "value": "B"},
                {"label": "10个", "value": "C"},
                {"label": "12个", "value": "D"},
            ],
            "answer": "D",
            "explanation": "整个投资组合中单向最高累积12个Units，防止组合处于100%净多头或净空头的裸露风险状态。"
        },
        {
            "title": "海龟交易法的N值计算使用什么类型的移动平均？",
            "options": [
                {"label": "简单移动平均（SMA）", "value": "A"},
                {"label": "指数移动平均（EMA）", "value": "B"},
                {"label": "加权移动平均（WMA）", "value": "C"},
                {"label": "几何移动平均", "value": "D"},
            ],
            "answer": "B",
            "explanation": "N值使用20日指数移动平均（EMA），EMA赋予近期数据更高权重，使N值在市场突然从平静转为剧烈震荡时能迅速反应。"
        },
        {
            "title": "海龟交易法中，加仓过程中每增加一个Unit，所有前期头寸的止损点要上移多少？",
            "options": [
                {"label": "1N", "value": "A"},
                {"label": "2N", "value": "B"},
                {"label": "0.5N", "value": "C"},
                {"label": "0.25N", "value": "D"},
            ],
            "answer": "C",
            "explanation": "每增加一个Unit，所有前期已建仓头寸的止损线也要上移0.5N，极大程度上锁定了早期底仓的利润。"
        },
        {
            "title": "海龟交易法累计获利超过多少美元？",
            "options": [
                {"label": "5000万美元", "value": "A"},
                {"label": "1亿美元", "value": "B"},
                {"label": "1.75亿美元", "value": "C"},
                {"label": "3亿美元", "value": "D"},
            ],
            "answer": "C",
            "explanation": "海龟们在数年间运用严格机械化趋势跟踪系统，创造了年均80%的复合收益率，累计获利超过1.75亿美元。"
        },
        {
            "title": "海龟选拔中，丹尼斯设计的心理测试包含多少道是非题？",
            "options": [
                {"label": "23道", "value": "A"},
                {"label": "43道", "value": "B"},
                {"label": "63道", "value": "C"},
                {"label": "83道", "value": "D"},
            ],
            "answer": "C",
            "explanation": "丹尼斯设计了63道是非题（True/False Test），旨在揭示候选人对风险、概率及市场行为的底层认知。"
        },
        {
            "title": "海龟交易中，如果当天盈亏对净资产产生重大影响，说明什么？",
            "options": [
                {"label": "说明行情很好", "value": "A"},
                {"label": "说明交易过度，头寸规模失控", "value": "B"},
                {"label": "说明市场波动正常", "value": "C"},
                {"label": "说明策略有效", "value": "D"},
            ],
            "answer": "B",
            "explanation": "严格的风险平价控制是生存前提，单日过度波动意味着头寸规模失控，违反了1%风险控制原则。"
        },
        {
            "title": "海龟交易法为什么不建议设定固定止盈？",
            "options": [
                {"label": "固定止盈会导致亏损", "value": "A"},
                {"label": "固定止盈会截断利润，无法让利润无限奔跑", "value": "B"},
                {"label": "固定止盈违反法规", "value": "C"},
                {"label": "固定止盈计算太复杂", "value": "D"},
            ],
            "answer": "B",
            "explanation": "设定固定止盈会截断利润。海龟通过追踪止损让利润无限奔跑，在低胜率系统中依赖少数大趋势的肥尾利润来弥补大量小额止损。"
        },
        {
            "title": "海龟交易中，向下摊平（Averaging Down）为什么是错误的？",
            "options": [
                {"label": "因为会增加收益", "value": "A"},
                {"label": "因为违背截断亏损的铁律，加速破产", "value": "B"},
                {"label": "因为会增加手续费", "value": "C"},
                {"label": "因为需要更多资金", "value": "D"},
            ],
            "answer": "B",
            "explanation": "向下摊平违背了截断亏损的铁律，只会加速破产。海龟只在盈利头寸上金字塔加仓，绝不逆势摊平。"
        },
    ]

    # ===== T3: 海龟现代应用 =====
    t3_questions = [
        {
            "title": "现代市场（2007-2026）中，原版海龟交易法的收益率如何变化？",
            "options": [
                {"label": "大幅提升", "value": "A"},
                {"label": "基本不变", "value": "B"},
                {"label": "灾难性崩塌，CAGR仅0.5%-3.5%", "value": "C"},
                {"label": "翻倍增长", "value": "D"},
            ],
            "answer": "C",
            "explanation": "自2007年以来，原版海龟法则收益率出现灾难性崩塌，现代动量策略CAGR仅3.5%，双移动平均线跌至0.5%，被描述为已死亡多年。"
        },
        {
            "title": "导致海龟交易法在现代市场失效的主要原因是什么？",
            "options": [
                {"label": "全球央行政策变化", "value": "A"},
                {"label": "量化宽松和算法主导市场", "value": "B"},
                {"label": "散户数量减少", "value": "C"},
                {"label": "交易量下降", "value": "D"},
            ],
            "answer": "B",
            "explanation": "量化宽松压平了波动率，高频算法精确制造假突破猎杀海龟止损线，20日和55日高点成为算法的流动性提款机。"
        },
        {
            "title": "现代优化海龟策略中，推荐将突破周期延长到多少日？",
            "options": [
                {"label": "30-50日", "value": "A"},
                {"label": "55-100日", "value": "B"},
                {"label": "150-200日", "value": "C"},
                {"label": "10-20日", "value": "D"},
            ],
            "answer": "B",
            "explanation": "将通道参数扩展至55日至100日甚至更长，能极大提高突破有效性，成功过滤掉虚假的算法波动。"
        },
        {
            "title": "海龟汤（Turtle Soup）策略是什么？",
            "options": [
                {"label": "原版海龟策略的优化版", "value": "A"},
                {"label": "在突破后重回通道内时反向开仓", "value": "B"},
                {"label": "一种新的入场策略", "value": "C"},
                {"label": "一种加仓策略", "value": "D"},
            ],
            "answer": "B",
            "explanation": "海龟汤专盯突破后无力延续的价格区间，在价格重回20日通道内部时瞬间反向开仓，以收割海龟交易员的2N止损盘为利润。"
        },
        {
            "title": "现代海龟策略中，推荐用什么均线作为牛熊分界过滤器？",
            "options": [
                {"label": "50日均线", "value": "A"},
                {"label": "100日均线", "value": "B"},
                {"label": "200日均线", "value": "C"},
                {"label": "20日均线", "value": "D"},
            ],
            "answer": "C",
            "explanation": "200日均线作为牛熊分界：只有当收盘价高于200日均线时方可执行多头突破信号，低于200日均线时仅执行空头信号。"
        },
        {
            "title": "ADX指标在海龟策略中用于什么目的？",
            "options": [
                {"label": "计算波动率", "value": "A"},
                {"label": "确认趋势强度", "value": "B"},
                {"label": "计算止损点", "value": "C"},
                {"label": "确定仓位大小", "value": "D"},
            ],
            "answer": "B",
            "explanation": "引入ADX作为趋势强度确认器，只有当ADX值跃升至20或25以上（表明存在真实动能）时，才认定突破有效。"
        },
        {
            "title": "哪位海龟成员自1988年创立切萨皮克资本以来持续活跃35年以上？",
            "options": [
                {"label": "理查德·丹尼斯", "value": "A"},
                {"label": "威廉·埃克哈特", "value": "B"},
                {"label": "杰瑞·帕克", "value": "C"},
                {"label": "柯蒂斯·费思", "value": "D"},
            ],
            "answer": "C",
            "explanation": "杰瑞·帕克自1988年创立切萨皮克资本以来持续活跃在华尔街逾35年，资管规模一度突破十亿美元，源于对海龟哲学宗教般的恪守。"
        },
        {
            "title": "柯蒂斯·费思溃败的核心原因是什么？",
            "options": [
                {"label": "市场太不公平", "value": "A"},
                {"label": "缺乏资金", "value": "B"},
                {"label": "知行鸿沟与赌徒心理，放弃N值风控", "value": "C"},
                {"label": "技术太落后", "value": "D"},
            ],
            "answer": "C",
            "explanation": "面临回撤压力时，验证自我的需求压倒了系统逻辑。他放弃N值仓位约束，在不具备概率优势的震荡市强行主观开仓，最终走向崩溃。"
        },
        {
            "title": "对于加密货币市场，海龟策略建议将单笔风险压缩到多少？",
            "options": [
                {"label": "1%", "value": "A"},
                {"label": "2%", "value": "B"},
                {"label": "0.5%或更低", "value": "C"},
                {"label": "5%", "value": "D"},
            ],
            "answer": "C",
            "explanation": "对于加密资产的极端波动性，现代优化建议将N值计算基准与单笔风险进一步压缩至0.5%甚至更低，以抵御瞬间暴跌插针。"
        },
        {
            "title": "海龟交易法中，为什么交易者永远不可能在趋势最巅峰逃顶？",
            "options": [
                {"label": "因为技术做不到", "value": "A"},
                {"label": "因为系统规定跌破10/20日低点才退出，意味着必须回撤部分利润", "value": "B"},
                {"label": "因为交易所不允许", "value": "C"},
                {"label": "因为资金不够", "value": "D"},
            ],
            "answer": "B",
            "explanation": "基于周期低点/高点的追踪退出意味着在趋势末期，跌破10/20日低点通常意味着账面未实现利润将出现20%-30%甚至更多的剧烈回撤。"
        },
    ]

    # ===== T4: 海龟实战综合 =====
    t4_questions = [
        {
            "title": "黄金触发55日突破，N=2.50，第一笔在310.00建仓，第二笔加仓价格是多少？",
            "options": [
                {"label": "310.50", "value": "A"},
                {"label": "311.25", "value": "B"},
                {"label": "312.50", "value": "C"},
                {"label": "315.00", "value": "D"},
            ],
            "answer": "B",
            "explanation": "加仓步长为0.5N=1.25，第二笔=310.00+1.25=311.25。"
        },
        {
            "title": "接上题，当满仓第四个Unit（313.75）时，所有四个Unit的止损线在什么位置？",
            "options": [
                {"label": "308.75", "value": "A"},
                {"label": "309.75", "value": "B"},
                {"label": "310.75", "value": "C"},
                {"label": "311.75", "value": "D"},
            ],
            "answer": "A",
            "explanation": "所有四个Unit的止损线=313.75-2N(5.00)=308.75。每增加一个Unit，止损线随之上移0.5N。"
        },
        {
            "title": "账户10万美元，某股票N=5美元，可以买多少股？",
            "options": [
                {"label": "100股", "value": "A"},
                {"label": "200股", "value": "B"},
                {"label": "500股", "value": "C"},
                {"label": "1000股", "value": "D"},
            ],
            "answer": "B",
            "explanation": "1%风险=100000×1%=1000美元，Unit=1000/5=200股。"
        },
        {
            "title": "账户10万美元，原油期货N=1.20，合约乘数1000美元，能买几手标准合约？",
            "options": [
                {"label": "0.83手（向下取整为0，无法交易标准合约）", "value": "A"},
                {"label": "1手", "value": "B"},
                {"label": "2手", "value": "C"},
                {"label": "3手", "value": "D"},
            ],
            "answer": "A",
            "explanation": "Dollar_N=1.20×1000=1200美元，Unit=1000/1200≈0.83手。期货不能交易小数，向下取整后无法交易标准合约，只能交易微型合约。"
        },
        {
            "title": "海龟交易法中，1996-2006年回测经典唐奇安趋势的CAGR是多少？",
            "options": [
                {"label": "10.2%", "value": "A"},
                {"label": "29.4%", "value": "B"},
                {"label": "49.5%", "value": "C"},
                {"label": "57.8%", "value": "D"},
            ],
            "answer": "B",
            "explanation": "1996-2006年回测中，经典唐奇安趋势的CAGR为29.4%，双移动平均线高达57.8%。"
        },
        {
            "title": "海龟交易法中，哪个市场组合被描述为最适合趋势跟踪的天然温床？",
            "options": [
                {"label": "传统大宗商品", "value": "A"},
                {"label": "外汇市场", "value": "B"},
                {"label": "加密货币和高散户参与的宽基ETF", "value": "C"},
                {"label": "国债市场", "value": "D"},
            ],
            "answer": "C",
            "explanation": "尽管大宗商品趋势红利减弱，但高流动性、高散户参与度且具有极强羊群效应的加密货币市场和宏观宽基ETF成为海龟策略的完美天然温床。"
        },
        {
            "title": "海龟交易法中，低度相关市场同一方向最高累积多少Units？",
            "options": [
                {"label": "4个", "value": "A"},
                {"label": "6个", "value": "B"},
                {"label": "10个", "value": "C"},
                {"label": "12个", "value": "D"},
            ],
            "answer": "C",
            "explanation": "低度相关市场（如黄金与玉米属于不同板块）同一方向上最高累积10个Units，实现跨板块风险分散。"
        },
        {
            "title": "海龟交易法中，N值公式中TR的EMA计算权重是？",
            "options": [
                {"label": "N_t = (18×N_{t-1} + TR_t) / 19", "value": "A"},
                {"label": "N_t = (19×N_{t-1} + TR_t) / 20", "value": "B"},
                {"label": "N_t = (20×N_{t-1} + TR_t) / 21", "value": "C"},
                {"label": "N_t = (TR_t) / 20", "value": "D"},
            ],
            "answer": "B",
            "explanation": "N_t = (19×N_{t-1} + TR_t) / 20，EMA赋予近期数据更高权重。"
        },
        {
            "title": "海龟交易中，如果账户回撤22%（在前一基础上再跌10%），头寸规模要再削减多少？",
            "options": [
                {"label": "10%", "value": "A"},
                {"label": "15%", "value": "B"},
                {"label": "20%", "value": "C"},
                {"label": "30%", "value": "D"},
            ],
            "answer": "C",
            "explanation": "回撤进一步达到22%时，头寸规模将再次削减20%。每个Unit所代表的风险已大幅降低。"
        },
        {
            "title": "海龟交易法中，唐奇安通道在Python中如何构建上轨？",
            "options": [
                {"label": "rolling(window=55).mean()", "value": "A"},
                {"label": "rolling(window=55).max()", "value": "B"},
                {"label": "rolling(window=55).min()", "value": "C"},
                {"label": "rolling(window=55).std()", "value": "D"},
            ],
            "answer": "B",
            "explanation": "唐奇安通道上轨使用rolling(window=55).max()，下轨使用rolling(window=20).min()。"
        },
    ]

    sort_order = 0
    for i, q in enumerate(t1_questions):
        qid = f"t_{qid_num}"
        qid_num += 1
        sort_order += 1
        insert_q(cursor, qid, 'T1', 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=sort_order)

    for i, q in enumerate(t2_questions):
        qid = f"t_{qid_num}"
        qid_num += 1
        sort_order += 1
        insert_q(cursor, qid, 'T2', 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=sort_order)

    for i, q in enumerate(t3_questions):
        qid = f"t_{qid_num}"
        qid_num += 1
        sort_order += 1
        insert_q(cursor, qid, 'T3', 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=sort_order)

    for i, q in enumerate(t4_questions):
        qid = f"t_{qid_num}"
        qid_num += 1
        sort_order += 1
        insert_q(cursor, qid, 'T4', 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=sort_order)

    return len(t1_questions) + len(t2_questions) + len(t3_questions) + len(t4_questions)


def gen_basics_questions(cursor):
    """生成基础概念题 - 股票、市场、财务基础"""
    qid_num = 1

    def next_id():
        nonlocal qid_num
        qid = f"basics_{qid_num}"
        qid_num += 1
        return qid

    questions = []

    # === 市场基础 ===
    market_basics = [
        {
            "title": "股票的本质是什么？",
            "options": [
                {"label": "公司向投资者借款的凭证", "value": "A"},
                {"label": "公司所有权的一部分（股权）", "value": "B"},
                {"label": "政府发行的债券", "value": "C"},
                {"label": "银行存款证明", "value": "D"},
            ],
            "answer": "B",
            "explanation": "股票代表公司所有权的一部分，持有股票即持有该公司的部分股权，享有分红权和投票权。"
        },
        {
            "title": "A股市场中，红色K线代表什么？",
            "options": [
                {"label": "当日下跌", "value": "A"},
                {"label": "当日上涨（收盘高于开盘）", "value": "B"},
                {"label": "成交量放大", "value": "C"},
                {"label": "停牌", "value": "D"},
            ],
            "answer": "B",
            "explanation": "A股市场中红色代表上涨（收盘高于开盘），绿色代表下跌（收盘低于开盘）。"
        },
        {
            "title": "股票交易的最小单位是？",
            "options": [
                {"label": "1股", "value": "A"},
                {"label": "10股", "value": "B"},
                {"label": "100股（1手）", "value": "C"},
                {"label": "1000股", "value": "D"},
            ],
            "answer": "C",
            "explanation": "A股交易中最小单位为1手，1手=100股。买入时必须是100股的整数倍。"
        },
        {
            "title": "A股的涨跌幅限制是多少？",
            "options": [
                {"label": "5%", "value": "A"},
                {"label": "10%", "value": "B"},
                {"label": "20%", "value": "C"},
                {"label": "没有涨跌停限制", "value": "D"},
            ],
            "answer": "B",
            "explanation": "主板股票涨跌幅限制为10%，科创板和创业板为20%，北交所为30%。"
        },
        {
            "title": "以下哪个交易所是A股的主板市场？",
            "options": [
                {"label": "纽约证券交易所", "value": "A"},
                {"label": "上海证券交易所", "value": "B"},
                {"label": "伦敦证券交易所", "value": "C"},
                {"label": "东京证券交易所", "value": "D"},
            ],
            "answer": "B",
            "explanation": "A股主板包括上海证券交易所（沪市）和深圳证券交易所（深市）。"
        },
        {
            "title": "市盈率（P/E）的计算公式是？",
            "options": [
                {"label": "股价÷每股收益", "value": "A"},
                {"label": "总市值÷总资产", "value": "B"},
                {"label": "净利润÷总营收", "value": "C"},
                {"label": "股价÷每股净资产", "value": "D"},
            ],
            "answer": "A",
            "explanation": "市盈率=股价÷每股收益（EPS），反映投资者为每1元盈利愿意支付的价格。"
        },
        {
            "title": "市净率（P/B）是什么？",
            "options": [
                {"label": "股价÷每股收益", "value": "A"},
                {"label": "股价÷每股净资产", "value": "B"},
                {"label": "总市值÷净利润", "value": "C"},
                {"label": "总营收÷总资产", "value": "D"},
            ],
            "answer": "B",
            "explanation": "市净率=股价÷每股净资产，衡量股票相对其账面价值的高低。"
        },
        {
            "title": "ROE（净资产收益率）衡量什么？",
            "options": [
                {"label": "公司总资产规模", "value": "A"},
                {"label": "公司利用股东权益创造利润的效率", "value": "B"},
                {"label": "公司的负债率", "value": "C"},
                {"label": "公司的现金流", "value": "D"},
            ],
            "answer": "B",
            "explanation": "ROE=净利润÷净资产，反映公司利用股东资金赚钱的效率，ROE越高说明盈利能力越强。"
        },
        {
            "title": "分红（派息）是指？",
            "options": [
                {"label": "公司增发新股", "value": "A"},
                {"label": "公司将部分利润以现金或股份形式分配给股东", "value": "B"},
                {"label": "公司发行债券", "value": "C"},
                {"label": "公司回购股票", "value": "D"},
            ],
            "answer": "B",
            "explanation": "分红是公司将部分利润以现金或股份形式分配给股东的行为，是股东获得投资回报的重要方式。"
        },
        {
            "title": "什么是除权除息？",
            "options": [
                {"label": "股票停牌", "value": "A"},
                {"label": "分红或送股后股价相应下调", "value": "B"},
                {"label": "公司破产", "value": "C"},
                {"label": "股票退市", "value": "D"},
            ],
            "answer": "B",
            "explanation": "除权除息是指分红或送股后，公司每股净资产减少，股价相应下调以保持总价值不变。"
        },
        {
            "title": "A股T+1交易制度意味着？",
            "options": [
                {"label": "当天买入可以当天卖出", "value": "A"},
                {"label": "当天买入的股票下一个交易日才能卖出", "value": "B"},
                {"label": "买入后锁定7天", "value": "C"},
                {"label": "没有交易限制", "value": "D"},
            ],
            "answer": "B",
            "explanation": "A股实行T+1制度，当天买入的股票必须到下一个交易日才能卖出，防止日内过度投机。"
        },
        {
            "title": "成交量（Volume）代表什么？",
            "options": [
                {"label": "股票的总数量", "value": "A"},
                {"label": "某段时间内股票交易的总手数", "value": "B"},
                {"label": "公司的总资产", "value": "C"},
                {"label": "公司的员工数量", "value": "D"},
            ],
            "answer": "B",
            "explanation": "成交量指某段时间内该股票交易的总手数，反映市场活跃度和资金参与程度。"
        },
        {
            "title": "什么是蓝筹股？",
            "options": [
                {"label": "股价很低的小盘股", "value": "A"},
                {"label": "业绩稳定、规模大的成熟公司股票", "value": "B"},
                {"label": "刚上市的新股", "value": "C"},
                {"label": "亏损公司的股票", "value": "D"},
            ],
            "answer": "B",
            "explanation": "蓝筹股指业绩稳定、规模大、分红稳定的成熟公司股票，如茅台、招行等。"
        },
        {
            "title": "什么是ST股票？",
            "options": [
                {"label": "特别好的股票", "value": "A"},
                {"label": "连续亏损被特别处理的股票", "value": "B"},
                {"label": "停牌中的股票", "value": "C"},
                {"label": "新上市的股票", "value": "D"},
            ],
            "answer": "B",
            "explanation": "ST（Special Treatment）表示公司连续亏损，被交易所特别处理，涨跌幅限制为5%。"
        },
        {
            "title": "什么是IPO？",
            "options": [
                {"label": "公司退市", "value": "A"},
                {"label": "公司首次公开发行并上市", "value": "B"},
                {"label": "公司被收购", "value": "C"},
                {"label": "公司分红", "value": "D"},
            ],
            "answer": "B",
            "explanation": "IPO（Initial Public Offering）指公司首次向公众公开发行股票并上市交易。"
        },
        {
            "title": "什么是融资融券？",
            "options": [
                {"label": "公司发行债券", "value": "A"},
                {"label": "向券商借钱买入或借股票卖出", "value": "B"},
                {"label": "公司增发新股", "value": "C"},
                {"label": "银行存款业务", "value": "D"},
            ],
            "answer": "B",
            "explanation": "融资是向券商借钱买入股票（加杠杆做多），融券是向券商借股票卖出（做空）。"
        },
    ]

    # === 财务基础 ===
    financial_basics = [
        {
            "title": "资产负债表反映什么信息？",
            "options": [
                {"label": "公司在某一时点的资产、负债和所有者权益", "value": "A"},
                {"label": "公司一年的收入支出", "value": "B"},
                {"label": "公司的现金流情况", "value": "C"},
                {"label": "公司的股价变动", "value": "D"},
            ],
            "answer": "A",
            "explanation": "资产负债表反映公司在某一时点的财务状况，即资产=负债+所有者权益。"
        },
        {
            "title": "利润表（损益表）反映什么？",
            "options": [
                {"label": "公司的总资产", "value": "A"},
                {"label": "某一段时期的收入、费用和利润", "value": "B"},
                {"label": "公司的现金流动", "value": "C"},
                {"label": "公司的股东结构", "value": "D"},
            ],
            "answer": "B",
            "explanation": "利润表反映公司一段时间内的经营成果，包括营业收入、成本费用和净利润。"
        },
        {
            "title": "现金流量表反映什么？",
            "options": [
                {"label": "公司的利润情况", "value": "A"},
                {"label": "公司的资产变化", "value": "B"},
                {"label": "公司经营活动、投资和筹资的现金流入流出", "value": "C"},
                {"label": "公司的负债结构", "value": "D"},
            ],
            "answer": "C",
            "explanation": "现金流量表反映公司经营、投资和筹资三大活动产生的现金流入和流出。"
        },
        {
            "title": "毛利率的计算公式是？",
            "options": [
                {"label": "（营业收入-营业成本）÷营业收入", "value": "A"},
                {"label": "净利润÷营业收入", "value": "B"},
                {"label": "营业成本÷营业收入", "value": "C"},
                {"label": "营业收入÷总资产", "value": "D"},
            ],
            "answer": "A",
            "explanation": "毛利率=（营业收入-营业成本）÷营业收入，反映产品或服务的盈利能力。"
        },
        {
            "title": "净利率的计算公式是？",
            "options": [
                {"label": "（收入-成本）÷收入", "value": "A"},
                {"label": "净利润÷营业收入", "value": "B"},
                {"label": "净利润÷总资产", "value": "C"},
                {"label": "营业成本÷营业收入", "value": "D"},
            ],
            "answer": "B",
            "explanation": "净利率=净利润÷营业收入，反映公司最终盈利占收入的比例。"
        },
        {
            "title": "每股收益（EPS）如何计算？",
            "options": [
                {"label": "净利润÷总股数", "value": "A"},
                {"label": "总营收÷总股数", "value": "B"},
                {"label": "总资产÷总股数", "value": "C"},
                {"label": "现金流÷总股数", "value": "D"},
            ],
            "answer": "A",
            "explanation": "EPS=净利润÷总股本，代表每股所对应的公司盈利。"
        },
        {
            "title": "负债率（资产负债率）过高意味着？",
            "options": [
                {"label": "公司盈利能力很强", "value": "A"},
                {"label": "公司偿债风险较大", "value": "B"},
                {"label": "公司现金流充裕", "value": "C"},
                {"label": "公司股价会上涨", "value": "D"},
            ],
            "answer": "B",
            "explanation": "负债率=总负债÷总资产，过高说明公司依赖大量借款经营，偿债风险较大。"
        },
        {
            "title": "经营性现金流为正，说明？",
            "options": [
                {"label": "公司投资赚了钱", "value": "A"},
                {"label": "公司主营业务产生了净现金流入", "value": "B"},
                {"label": "公司在大量借债", "value": "C"},
                {"label": "公司在分红", "value": "D"},
            ],
            "answer": "B",
            "explanation": "经营性现金流为正，说明公司主营业务产生的现金流入大于流出，经营健康。"
        },
        {
            "title": "什么是净利润？",
            "options": [
                {"label": "总收入减去所有成本、税费后的最终利润", "value": "A"},
                {"label": "总收入减去营业成本", "value": "B"},
                {"label": "总现金收入", "value": "C"},
                {"label": "总资产减总负债", "value": "D"},
            ],
            "answer": "A",
            "explanation": "净利润=营业收入-营业成本-各项费用-税费，是公司最终赚到的钱。"
        },
        {
            "title": "什么是营业收入？",
            "options": [
                {"label": "公司扣除成本后的利润", "value": "A"},
                {"label": "公司销售商品或提供服务获得的总收入", "value": "B"},
                {"label": "公司持有的现金", "value": "C"},
                {"label": "公司的总负债", "value": "D"},
            ],
            "answer": "B",
            "explanation": "营业收入是公司通过销售商品或提供服务所获得的总收入，尚未扣除任何成本和费用。"
        },
    ]

    # === 技术分析基础 ===
    technical_basics = [
        {
            "title": "MA5代表什么？",
            "options": [
                {"label": "5日成交量均线", "value": "A"},
                {"label": "5日收盘价移动平均线", "value": "B"},
                {"label": "5日最高价均线", "value": "C"},
                {"label": "5日涨跌幅", "value": "D"},
            ],
            "answer": "B",
            "explanation": "MA5是5日移动平均线（Moving Average），由最近5个交易日的收盘价平均值得到。"
        },
        {
            "title": "多头排列指什么？",
            "options": [
                {"label": "短期均线在长期均线下方", "value": "A"},
                {"label": "短期均线在长期均线上方", "value": "B"},
                {"label": "均线交叉缠绕", "value": "C"},
                {"label": "成交量持续萎缩", "value": "D"},
            ],
            "answer": "B",
            "explanation": "多头排列指短期均线（如MA5）在长期均线（如MA20）上方，表明短期趋势偏强。"
        },
        {
            "title": "空头排列指什么？",
            "options": [
                {"label": "短期均线在长期均线上方", "value": "A"},
                {"label": "短期均线在长期均线下方", "value": "B"},
                {"label": "均线交叉缠绕", "value": "C"},
                {"label": "价格横盘", "value": "D"},
            ],
            "answer": "B",
            "explanation": "空头排列指短期均线在长期均线下方，表明短期趋势偏弱。"
        },
        {
            "title": "什么是支撑位？",
            "options": [
                {"label": "价格很难跌破的价位区域", "value": "A"},
                {"label": "价格很难突破的价位区域", "value": "B"},
                {"label": "成交量最大的价位", "value": "C"},
                {"label": "开盘价", "value": "D"},
            ],
            "answer": "A",
            "explanation": "支撑位是买方力量较强、价格较难跌破的价位区域，通常由前期低点或均线构成。"
        },
        {
            "title": "什么是压力位（阻力位）？",
            "options": [
                {"label": "价格很难跌破的价位", "value": "A"},
                {"label": "价格很难突破的价位区域", "value": "B"},
                {"label": "最低价格", "value": "C"},
                {"label": "平均价格", "value": "D"},
            ],
            "answer": "B",
            "explanation": "压力位是卖方力量较强、价格较难突破的价位区域，通常由前期高点或均线构成。"
        },
        {
            "title": "什么是放量？",
            "options": [
                {"label": "成交量比之前明显增加", "value": "A"},
                {"label": "成交量比之前明显减少", "value": "B"},
                {"label": "成交量不变", "value": "C"},
                {"label": "股价上涨", "value": "D"},
            ],
            "answer": "A",
            "explanation": "放量指成交量比前期明显增加，通常表示市场参与度提高，趋势可能加速。"
        },
        {
            "title": "什么是缩量？",
            "options": [
                {"label": "成交量明显增加", "value": "A"},
                {"label": "成交量比之前明显减少", "value": "B"},
                {"label": "股价大幅波动", "value": "C"},
                {"label": "涨停板", "value": "D"},
            ],
            "answer": "B",
            "explanation": "缩量指成交量比前期明显减少，可能表示市场观望情绪浓厚，趋势动能减弱。"
        },
        {
            "title": "什么是量价背离？",
            "options": [
                {"label": "价格上涨同时成交量放大", "value": "A"},
                {"label": "价格上涨但成交量萎缩", "value": "B"},
                {"label": "价格下跌同时成交量放大", "value": "C"},
                {"label": "价格和成交量无关", "value": "D"},
            ],
            "answer": "B",
            "explanation": "量价背离指价格上涨但成交量萎缩，说明上涨动能不足，趋势可能反转。"
        },
        {
            "title": "RSI指标超过70意味着？",
            "options": [
                {"label": "处于超买区域，可能回调", "value": "A"},
                {"label": "处于超卖区域，可能反弹", "value": "B"},
                {"label": "价格一定上涨", "value": "C"},
                {"label": "一定下跌", "value": "D"},
            ],
            "answer": "A",
            "explanation": "RSI>70表示处于超买区域，短期内买盘力量过强，可能出现回调。"
        },
        {
            "title": "RSI指标低于30意味着？",
            "options": [
                {"label": "超买", "value": "A"},
                {"label": "超卖，可能反弹", "value": "B"},
                {"label": "价格横盘", "value": "C"},
                {"label": "趋势不明", "value": "D"},
            ],
            "answer": "B",
            "explanation": "RSI<30表示处于超卖区域，短期内卖盘力量过强，可能出现反弹。"
        },
        {
            "title": "什么是十字星K线？",
            "options": [
                {"label": "收盘价远高于开盘价", "value": "A"},
                {"label": "开盘价等于或接近收盘价，几乎无实体", "value": "B"},
                {"label": "收盘价远低于开盘价", "value": "C"},
                {"label": "开盘价等于最高价", "value": "D"},
            ],
            "answer": "B",
            "explanation": "十字星是开盘价等于或接近收盘价的K线，几乎没有实体，上下影线较长。"
        },
        {
            "title": "锤子线通常暗示什么？",
            "options": [
                {"label": "即将下跌", "value": "A"},
                {"label": "可能出现底部反转上涨", "value": "B"},
                {"label": "价格横盘", "value": "C"},
                {"label": "趋势不变", "value": "D"},
            ],
            "answer": "B",
            "explanation": "锤子线是下影线很长、实体很小的K线，通常出现在下跌末期，暗示可能见底反转。"
        },
        {
            "title": "射击之星通常暗示什么？",
            "options": [
                {"label": "即将大涨", "value": "A"},
                {"label": "可能出现顶部反转下跌", "value": "B"},
                {"label": "价格横盘", "value": "C"},
                {"label": "趋势不变", "value": "D"},
            ],
            "answer": "B",
            "explanation": "射击之星是上影线很长、实体很小的K线，通常出现在上涨末期，暗示可能见顶反转。"
        },
        {
            "title": "什么是唐奇安通道？",
            "options": [
                {"label": "由N日最高价和最低价构成的通道", "value": "A"},
                {"label": "一种均线指标", "value": "B"},
                {"label": "一种成交量指标", "value": "C"},
                {"label": "一种RSI变体", "value": "D"},
            ],
            "answer": "A",
            "explanation": "唐奇安通道由一段时间（如20日或55日）的最高价和最低价构成，用于捕捉突破信号。"
        },
        {
            "title": "什么是ATR（真实波动幅度）？",
            "options": [
                {"label": "最高价减最低价的差值", "value": "A"},
                {"label": "衡量价格波动率的指标", "value": "B"},
                {"label": "收盘价的变化", "value": "C"},
                {"label": "成交量的变化", "value": "D"},
            ],
            "answer": "B",
            "explanation": "ATR（Average True Range）是衡量价格波动率的指标，取真实波动幅度的平均值。"
        },
        {
            "title": "趋势跟踪策略的核心思想是？",
            "options": [
                {"label": "预测市场高低点", "value": "A"},
                {"label": "跟随趋势，截断亏损，让利润奔跑", "value": "B"},
                {"label": "频繁短线交易", "value": "C"},
                {"label": "持有不动", "value": "D"},
            ],
            "answer": "B",
            "explanation": "趋势跟踪策略不预测市场，而是等待趋势确立后跟随，通过止损控制风险，通过追踪止盈让利润奔跑。"
        },
    ]

    # === 投资策略基础 ===
    strategy_basics = [
        {
            "title": "什么是价值投资？",
            "options": [
                {"label": "追涨杀跌", "value": "A"},
                {"label": "买入被低估的股票并长期持有", "value": "B"},
                {"label": "频繁短线交易", "value": "C"},
                {"label": "只买高价股", "value": "D"},
            ],
            "answer": "B",
            "explanation": "价值投资是寻找市场价格低于内在价值的股票，买入并长期持有，等待价值回归。"
        },
        {
            "title": "什么是趋势投资？",
            "options": [
                {"label": "买入后永不卖出", "value": "A"},
                {"label": "跟随市场趋势，上涨做多、下跌做空或空仓", "value": "B"},
                {"label": "只买大盘股", "value": "C"},
                {"label": "只看基本面不看技术面", "value": "D"},
            ],
            "answer": "B",
            "explanation": "趋势投资是跟随市场趋势方向操作，上涨趋势中做多，下跌趋势中空仓或做空。"
        },
        {
            "title": "什么是止损？",
            "options": [
                {"label": "亏损后继续加仓摊平", "value": "A"},
                {"label": "在预定亏损幅度时卖出离场", "value": "B"},
                {"label": "等待股价回升", "value": "C"},
                {"label": "卖出盈利的股票", "value": "D"},
            ],
            "answer": "B",
            "explanation": "止损是在价格下跌到预定幅度时主动卖出离场，防止亏损进一步扩大。"
        },
        {
            "title": "什么是止盈？",
            "options": [
                {"label": "亏损时卖出", "value": "A"},
                {"label": "达到预期盈利目标后卖出锁定利润", "value": "B"},
                {"label": "继续持有不动", "value": "C"},
                {"label": "加仓买入", "value": "D"},
            ],
            "answer": "B",
            "explanation": "止盈是当盈利达到预期目标后卖出锁定利润，防止利润回吐。"
        },
        {
            "title": "什么是分散投资？",
            "options": [
                {"label": "把所有资金投入一只股票", "value": "A"},
                {"label": "将资金分配到不同行业或资产以降低风险", "value": "B"},
                {"label": "只买同行业股票", "value": "C"},
                {"label": "频繁换股", "value": "D"},
            ],
            "answer": "B",
            "explanation": "分散投资是将资金分配到不同行业、不同资产上，降低单一标的暴雷带来的风险。"
        },
        {
            "title": "什么是左侧交易？",
            "options": [
                {"label": "在下跌过程中逢低买入（抄底）", "value": "A"},
                {"label": "在上涨趋势确立后买入", "value": "B"},
                {"label": "只买不卖", "value": "C"},
                {"label": "追涨杀跌", "value": "D"},
            ],
            "answer": "A",
            "explanation": "左侧交易是在下跌过程中逢低买入（抄底），试图在底部区域建仓。"
        },
        {
            "title": "什么是右侧交易？",
            "options": [
                {"label": "在下跌过程中抄底", "value": "A"},
                {"label": "在趋势确立（底部形成后）买入", "value": "B"},
                {"label": "只买高价股", "value": "C"},
                {"label": "追涨杀跌", "value": "D"},
            ],
            "answer": "B",
            "explanation": "右侧交易是等待趋势确立（如底部形态完成、突破关键阻力）后才买入，不抄底。"
        },
        {
            "title": "什么是仓位管理？",
            "options": [
                {"label": "随意买卖，不考虑比例", "value": "A"},
                {"label": "根据风险和市场状况控制持有头寸的比例", "value": "B"},
                {"label": "全部资金买入", "value": "C"},
                {"label": "只买1股", "value": "D"},
            ],
            "answer": "B",
            "explanation": "仓位管理是根据风险承受能力和市场状况，合理分配资金在不同头寸中的比例。"
        },
        {
            "title": "为什么不建议向下摊平（亏损后加仓）？",
            "options": [
                {"label": "因为会增加收益", "value": "A"},
                {"label": "因为可能越亏越多，违背止损原则", "value": "B"},
                {"label": "因为手续费太贵", "value": "C"},
                {"label": "因为会增加交易量", "value": "D"},
            ],
            "answer": "B",
            "explanation": "向下摊平可能导致亏损无限扩大，违背截断亏损的原则，是导致重大亏损的常见原因。"
        },
        {
            "title": "什么是动量效应？",
            "options": [
                {"label": "过去涨的股票未来更可能继续涨", "value": "A"},
                {"label": "过去涨的股票未来一定跌", "value": "B"},
                {"label": "股票不会有趋势", "value": "C"},
                {"label": "价格完全随机", "value": "D"},
            ],
            "answer": "A",
            "explanation": "动量效应指过去表现好的股票在未来一段时间更可能继续上涨，是趋势跟踪的理论基础之一。"
        },
    ]

    all_questions = market_basics + financial_basics + technical_basics + strategy_basics

    # Distribute across L1-L4 levels
    sort_orders = {'L1': 0, 'L2': 0, 'L3': 0, 'L4': 0}
    level_map = {}

    # Market basics -> L1
    for q in market_basics:
        sort_orders['L1'] += 1
        qid = f"basics_{qid_num}"
        qid_num += 1
        insert_q(cursor, qid, 'L1', 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=sort_orders['L1'])

    # Financial basics -> L2
    for q in financial_basics:
        sort_orders['L2'] += 1
        qid = f"basics_{qid_num}"
        qid_num += 1
        insert_q(cursor, qid, 'L2', 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=sort_orders['L2'])

    # Technical basics -> L3
    for q in technical_basics:
        sort_orders['L3'] += 1
        qid = f"basics_{qid_num}"
        qid_num += 1
        insert_q(cursor, qid, 'L3', 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=sort_orders['L3'])

    # Strategy basics -> L4
    for q in strategy_basics:
        sort_orders['L4'] += 1
        qid = f"basics_{qid_num}"
        qid_num += 1
        insert_q(cursor, qid, 'L4', 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=sort_orders['L4'])

    return len(all_questions)


if __name__ == "__main__":
    conn = get_db()
    cursor = conn.cursor()

    print("生成海龟交易法题目...")
    turtle_count = gen_turtle_questions(cursor)
    print(f"✅ 海龟交易法: {turtle_count} 题")

    print("\n生成基础概念题目...")
    basics_count = gen_basics_questions(cursor)
    print(f"✅ 基础概念: {basics_count} 题")

    conn.commit()

    # 统计总数
    cursor.execute("SELECT COUNT(*) FROM questions")
    total = cursor.fetchone()[0]
    print(f"\n📊 数据库总计: {total} 题")

    cursor.execute("SELECT level_id, COUNT(*) FROM questions GROUP BY level_id ORDER BY level_id")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} 题")

    conn.close()
