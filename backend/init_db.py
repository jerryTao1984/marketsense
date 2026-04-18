"""
识盘鸭 V1.0 后端 - FastAPI + SQLite
初始化数据库并写入所有题目数据
"""
import sqlite3
import json
import os

DB_PATH = os.environ.get('DB_PATH', os.path.join(os.path.dirname(__file__), 'shipanya.db'))


def init_db():
    """创建数据库表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            phone TEXT,
            nickname TEXT,
            hearts INTEGER DEFAULT 5,
            streak_days INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 关卡表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            id TEXT PRIMARY KEY,
            category_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            sort_order INTEGER DEFAULT 0
        )
    ''')

    # 题目表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id TEXT PRIMARY KEY,
            level_id TEXT NOT NULL,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            image_url TEXT,
            options_json TEXT NOT NULL,
            answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY (level_id) REFERENCES levels(id)
        )
    ''')

    # 用户进度表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            level_id TEXT NOT NULL,
            is_completed INTEGER DEFAULT 0,
            best_score INTEGER DEFAULT 0,
            completed_at TIMESTAMP DEFAULT NULL,
            UNIQUE(user_id, level_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (level_id) REFERENCES levels(id)
        )
    ''')

    # 答题记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answer_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question_id TEXT NOT NULL,
            level_id TEXT NOT NULL,
            category_id TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            is_correct INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 答题会话表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            level_id TEXT NOT NULL,
            correct_count INTEGER DEFAULT 0,
            total_count INTEGER DEFAULT 0,
            passed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


def seed_levels_and_questions():
    """写入关卡和题目数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ===== 关卡数据 =====
    levels = [
        # 基础概念
        ('L1', 'basics', '市场基础', 'A股市场基本规则与常识', 1),
        ('L2', 'basics', '财务报表', '读懂三大财务报表基础', 2),
        ('L3', 'basics', '交易术语', '掌握常见股市交易术语', 3),
        ('L4', 'basics', '估值与选股', '常见估值方法与选股指标', 4),
        # 交易法则
        ('T1', 'trading', '海豚交易法', '短线波段交易体系', 1),
        ('T2', 'trading', '海龟交易法', '经典趋势跟踪策略', 2),
        ('T3', 'trading', '均线策略', '移动平均线交易系统', 3),
        ('T4', 'trading', '定投与网格', '定投策略与网格交易法', 4),
        # K线实盘
        ('K1', 'kline', '单根K线', '识别常见单根K线形态', 1),
        ('K2', 'kline', 'K线组合', '识别经典K线组合形态', 2),
        ('K3', 'kline', '趋势形态', '识别经典趋势和整理形态', 3),
        ('K4', 'kline', '量价分析', '成交量与价格的关系分析', 4),
        # K线预测
        ('P1', 'predict', '下周涨跌预测', '根据本周K线预测下周走势', 1),
        ('P2', 'predict', '趋势转折预测', '判断趋势是否即将反转', 2),
        ('P3', 'predict', '支撑压力预测', '判断关键支撑位和压力位', 3),
    ]

    cursor.executemany(
        'INSERT OR IGNORE INTO levels (id, category_id, name, description, sort_order) VALUES (?, ?, ?, ?, ?)',
        levels
    )

    # ===== 题目数据 =====
    questions = []

    # ---- 基础概念 L1: 市场基础 ----
    for i, q in enumerate([
        ('b1_q1', 'L1', 'text', 'A股市场连续竞价的交易时间是？', None,
         '[{"label":"9:00-15:00","value":"A"},{"label":"9:30-11:30, 13:00-15:00","value":"B"},{"label":"9:00-11:30, 13:30-15:00","value":"C"},{"label":"10:00-15:00","value":"D"}]',
         'B', 'A股连续竞价时间为 9:30-11:30 和 13:00-15:00。9:15-9:25 为集合竞价。'),
        ('b1_q2', 'L1', 'text', '沪深主板非ST股票的日涨跌幅限制为？', None,
         '[{"label":"5%","value":"A"},{"label":"10%","value":"B"},{"label":"20%","value":"C"},{"label":"30%","value":"D"}]',
         'B', '主板非ST股票涨跌幅10%，ST为5%，创业板/科创板20%，北交所30%。'),
        ('b1_q3', 'L1', 'text', '以下哪个代码属于上交所主板？', None,
         '[{"label":"000001","value":"A"},{"label":"600519","value":"B"},{"label":"300750","value":"C"},{"label":"830946","value":"D"}]',
         'B', '600开头为沪市主板，000为深市主板，300为创业板，830为北交所。'),
        ('b1_q4', 'L1', 'text', 'T+1 交易制度意味着？', None,
         '[{"label":"当天买入当天可卖出","value":"A"},{"label":"当天买入次日才能卖出","value":"B"},{"label":"资金当天到账","value":"C"},{"label":"手续费隔天结算","value":"D"}]',
         'B', 'T+1 指当日买入的股票需到下一个交易日才能卖出，防止日内过度投机。'),
        ('b1_q5', 'L1', 'text', 'A股市场股票交易的最小单位"一手"等于？', None,
         '[{"label":"10股","value":"A"},{"label":"50股","value":"B"},{"label":"100股","value":"C"},{"label":"1000股","value":"D"}]',
         'C', 'A股主板1手=100股，买入须为100股整数倍。科创板200股起，以1股递增。'),
        ('b1_q6', 'L1', 'text', '科创板股票的涨跌幅限制为？', None,
         '[{"label":"5%","value":"A"},{"label":"10%","value":"B"},{"label":"20%","value":"C"},{"label":"30%","value":"D"}]',
         'C', '科创板涨跌幅限制为20%，上市前5个交易日不设涨跌幅限制。'),
        ('b1_q7', 'L1', 'text', '北交所股票的涨跌幅限制为？', None,
         '[{"label":"10%","value":"A"},{"label":"20%","value":"B"},{"label":"30%","value":"C"},{"label":"无限制","value":"D"}]',
         'C', '北交所涨跌幅限制为30%，是A股各板块中最大的。上市首日不设限制。'),
        ('b1_q8', 'L1', 'text', 'ST股票的日涨跌幅限制为？', None,
         '[{"label":"5%","value":"A"},{"label":"10%","value":"B"},{"label":"20%","value":"C"},{"label":"30%","value":"D"}]',
         'A', 'ST和*ST股票涨跌幅限制为5%，低于主板非ST的10%。'),
        ('b1_q9', 'L1', 'text', '集合竞价中不可撤单的时间段是？', None,
         '[{"label":"9:15-9:20","value":"A"},{"label":"9:20-9:25","value":"B"},{"label":"9:25-9:30","value":"C"},{"label":"全天可撤","value":"D"}]',
         'B', '9:15-9:20可申报和撤单，9:20-9:25可申报但不可撤单。'),
        ('b1_q10', 'L1', 'text', '个人投资者开通科创板需满足的条件是？', None,
         '[{"label":"日均资产20万+1年经验","value":"A"},{"label":"日均资产50万+2年经验","value":"B"},{"label":"日均资产100万+2年经验","value":"C"},{"label":"日均资产10万+1年经验","value":"D"}]',
         'B', '科创板要求前20个交易日日均资产≥50万，且证券交易经验≥24个月。'),
        ('b1_q11', 'L1', 'text', '创业板股票交易的资产门槛是？', None,
         '[{"label":"5万元","value":"A"},{"label":"10万元","value":"B"},{"label":"20万元","value":"C"},{"label":"50万元","value":"D"}]',
         'B', '创业板要求前20个交易日日均资产≥10万，且交易经验≥24个月。'),
        ('b1_q12', 'L1', 'text', '科创板股票代码以什么开头？', None,
         '[{"label":"300","value":"A"},{"label":"600","value":"B"},{"label":"688","value":"C"},{"label":"830","value":"D"}]',
         'C', '科创板代码688开头，创业板300开头，沪市主板600/601/603，深市主板000/001/002，北交所8开头。'),
        ('b1_q13', 'L1', 'text', 'IPO新股在科创板上市后前几个交易日不设涨跌幅限制？', None,
         '[{"label":"3个","value":"A"},{"label":"5个","value":"B"},{"label":"10个","value":"C"},{"label":"20个","value":"D"}]',
         'B', '全面注册制下，科创板和创业板新股上市前5个交易日不设涨跌幅限制。'),
        ('b1_q14', 'L1', 'text', '以下哪个板块主要服务"硬科技"企业？', None,
         '[{"label":"创业板","value":"A"},{"label":"科创板","value":"B"},{"label":"北交所","value":"C"},{"label":"主板","value":"D"}]',
         'B', '科创板面向世界科技前沿，服务突破关键核心技术的"硬科技"企业。'),
        ('b1_q15', 'L1', 'text', '关于A股和B股，说法正确的是？', None,
         '[{"label":"A股以美元认购","value":"A"},{"label":"B股以人民币标明面值，以外币交易","value":"B"},{"label":"B股只在上交所上市","value":"C"},{"label":"A股和B股交易币种相同","value":"D"}]',
         'B', 'B股以人民币标明面值，沪市B股以美元交易，深市B股以港币交易。'),
        ('b1_q16', 'L1', 'text', '投资者参与科创板需通过哪种证券账户？', None,
         '[{"label":"深圳A股账户","value":"A"},{"label":"上海A股账户","value":"B"},{"label":"上海B股账户","value":"C"},{"label":"深圳B股账户","value":"D"}]',
         'B', '科创板是上交所设立的板块，需通过上海A股账户参与。'),
        ('b1_q17', 'L1', 'text', '发行价格高于面值称为？', None,
         '[{"label":"平价发行","value":"A"},{"label":"折价发行","value":"B"},{"label":"溢价发行","value":"C"},{"label":"折价配售","value":"D"}]',
         'C', '溢价发行指发行价高于面值，溢价款列入资本公积金。我国不允许折价发行。'),
        ('b1_q18', 'L1', 'text', '深交所A股大宗交易单笔最低限额为？', None,
         '[{"label":"10万股或100万元","value":"A"},{"label":"30万股或200万元","value":"B"},{"label":"50万股或300万元","value":"C"},{"label":"100万股或500万元","value":"D"}]',
         'C', '深交所A股大宗交易标准：≥50万股或≥300万元。'),
    ]):
        questions.append((*q, i))

    # ---- 基础概念 L2: 财务报表 ----
    for i, q in enumerate([
        ('b2_q1', 'L2', 'text', '以下哪项不属于三大财务报表？', None,
         '[{"label":"资产负债表","value":"A"},{"label":"利润表","value":"B"},{"label":"现金流量表","value":"C"},{"label":"股东变动表","value":"D"}]',
         'D', '三大报表为资产负债表、利润表、现金流量表。股东变动表是附注内容。'),
        ('b2_q2', 'L2', 'text', 'ROE（净资产收益率）衡量的核心是？', None,
         '[{"label":"总资产周转速度","value":"A"},{"label":"股东投入资本的回报效率","value":"B"},{"label":"债务偿还能力","value":"C"},{"label":"营业收入增长率","value":"D"}]',
         'B', 'ROE = 净利润/净资产，衡量股东每一块钱投入能产生多少回报。'),
        ('b2_q3', 'L2', 'text', '经营性现金流为负说明什么？', None,
         '[{"label":"公司一定在亏损","value":"A"},{"label":"公司主业没收到足够现金","value":"B"},{"label":"公司正在大量投资","value":"C"},{"label":"公司借了很多钱","value":"D"}]',
         'B', '经营现金流为负意味着主业现金流入不足，即使利润表盈利也可能是"纸面富贵"。'),
        ('b2_q4', 'L2', 'text', '毛利率的计算公式是？', None,
         '[{"label":"净利润/营业收入","value":"A"},{"label":"（营业收入-营业成本）/营业收入","value":"B"},{"label":"营业利润/营业收入","value":"C"},{"label":"净利润/总资产","value":"D"}]',
         'B', '毛利率 =（营业收入-营业成本）/营业收入，反映产品核心盈利能力。'),
        ('b2_q5', 'L2', 'text', '资产负债率的合理范围通常是？', None,
         '[{"label":"越低越好","value":"A"},{"label":"40%-60% 较健康","value":"B"},{"label":"越高越好","value":"C"},{"label":"固定为50%","value":"D"}]',
         'B', '40%-60%通常较健康，过低没利用好杠杆，过高财务风险大，行业标准不同。'),
        ('b2_q6', 'L2', 'text', '市盈率（PE）的计算公式是？', None,
         '[{"label":"每股市价/每股净资产","value":"A"},{"label":"每股市价/每股收益","value":"B"},{"label":"每股收益/每股市价","value":"C"},{"label":"每股净资产/每股市价","value":"D"}]',
         'B', 'PE = 每股市价/每股收益，反映投资者为每元盈利愿意支付的价格。'),
        ('b2_q7', 'L2', 'text', '市净率（PB）最适合用于哪类企业估值？', None,
         '[{"label":"轻资产互联网公司","value":"A"},{"label":"金融机构（如银行）","value":"B"},{"label":"高速成长的生物医药","value":"C"},{"label":"持续亏损企业","value":"D"}]',
         'B', 'PB适用于资产密集型行业（银行、保险等），其净资产账面价值接近市场价值。'),
        ('b2_q8', 'L2', 'text', '某股票价格20元，每股收益10元，市盈率为？', None,
         '[{"label":"0.5倍","value":"A"},{"label":"1倍","value":"B"},{"label":"1.6倍","value":"C"},{"label":"2倍","value":"D"}]',
         'D', 'PE = 20/10 = 2倍，即投资者为每1元盈利支付2元。'),
        ('b2_q9', 'L2', 'text', '净利率（净利润率）的计算公式是？', None,
         '[{"label":"毛利润/营业收入","value":"A"},{"label":"营业利润/营业收入","value":"B"},{"label":"净利润/营业收入","value":"C"},{"label":"净利润/总资产","value":"D"}]',
         'C', '净利率 = 净利润/营业收入，反映扣除所有成本费用后的最终盈利水平。'),
        ('b2_q10', 'L2', 'text', '资产负债率的计算公式是？', None,
         '[{"label":"总资产/总负债","value":"A"},{"label":"总负债/总资产","value":"B"},{"label":"总负债/净资产","value":"C"},{"label":"净资产/总资产","value":"D"}]',
         'B', '资产负债率 = 总负债/总资产，反映资产中负债融资占比。'),
        ('b2_q11', 'L2', 'text', '市盈率的局限性在于？', None,
         '[{"label":"可用于所有企业","value":"A"},{"label":"越低说明盈利越差","value":"B"},{"label":"不能用于亏损企业","value":"C"},{"label":"与股价无关","value":"D"}]',
         'C', '亏损企业EPS为负，市盈率为负值或无意义，此时可考虑市销率PS等替代指标。'),
        ('b2_q12', 'L2', 'text', 'PEG小于1通常意味着？', None,
         '[{"label":"股票定价过高","value":"A"},{"label":"股票可能被低估","value":"B"},{"label":"股票已被高估","value":"C"},{"label":"企业盈利差","value":"D"}]',
         'B', 'PEG = PE/盈利增长率，PEG<1可能意味着股票被低估，或市场认为成长性不及预期。'),
        ('b2_q13', 'L2', 'text', '持续亏损、现金流为负、资产偏低的公司，哪种估值方法更合适？', None,
         '[{"label":"市盈率法","value":"A"},{"label":"市净率法","value":"B"},{"label":"市销率（PS）法","value":"C"},{"label":"股息折现法","value":"D"}]',
         'C', '亏损企业PE不可用，资产偏低PB也无法参考。PS = 股价/每股营收，只要有营业收入就可计算。'),
        ('b2_q14', 'L2', 'text', '以下关于财务指标的说法，错误的是？', None,
         '[{"label":"ROE越高股东盈利越强","value":"A"},{"label":"毛利率下降可能竞争加剧","value":"B"},{"label":"资产负债率越高财务风险越小","value":"C"},{"label":"经营现金流为正说明造血能力强","value":"D"}]',
         'C', '资产负债率越高，负债占总资产比重越大，偿债压力越高，财务风险越大。'),
        ('b2_q15', 'L2', 'text', '市销率（PS）反映的是股权价值与哪项指标的倍数关系？', None,
         '[{"label":"净利润","value":"A"},{"label":"总资产","value":"B"},{"label":"营业收入","value":"C"},{"label":"净资产","value":"D"}]',
         'C', 'PS = 每股市价/每股营业收入，常用于评估尚未盈利但有营收成长性的公司。'),
        ('b2_q16', 'L2', 'text', '以下哪组指标属于相对估值法？', None,
         '[{"label":"DCF、DDM","value":"A"},{"label":"PE、PB、PS","value":"B"},{"label":"WACC、IRR","value":"C"},{"label":"NPV、ROI","value":"D"}]',
         'B', 'PE、PB、PS均为相对估值法（市场法），通过与可比公司比较来估值。'),
    ]):
        questions.append((*q, i))

    # ---- 基础概念 L3: 交易术语 ----
    for i, q in enumerate([
        ('b3_q1', 'L3', 'text', '股票交易中"做多"的含义是？', None,
         '[{"label":"先卖后买，预期下跌","value":"A"},{"label":"先买后卖，预期上涨","value":"B"},{"label":"同时买卖","value":"C"},{"label":"不持有头寸","value":"D"}]',
         'B', '做多即先买入开仓然后卖出平仓，预期价格上涨后获利。'),
        ('b3_q2', 'L3', 'text', '"止损"的含义是？', None,
         '[{"label":"盈利后继续持有","value":"A"},{"label":"亏损达到预定限度时果断卖出","value":"B"},{"label":"下跌时加仓摊平","value":"C"},{"label":"暂停交易等待","value":"D"}]',
         'B', '止损是风险管理手段，在亏损达到可承受范围时果断平仓，防止亏损扩大。'),
        ('b3_q3', 'L3', 'text', '"建仓"是指？', None,
         '[{"label":"全部卖出","value":"A"},{"label":"首次买入建立头寸","value":"B"},{"label":"追加买入","value":"C"},{"label":"部分卖出","value":"D"}]',
         'B', '建仓指首次买入某只股票建立头寸。追加买入叫"加仓"，部分卖出叫"减仓"。'),
        ('b3_q4', 'L3', 'text', '"割肉"通常是指？', None,
         '[{"label":"盈利时卖出","value":"A"},{"label":"亏损状态下忍痛卖出","value":"B"},{"label":"长期持有","value":"C"},{"label":"分红获取收益","value":"D"}]',
         'B', '割肉指股票被套后以低于买入价卖出，实现实际亏损。'),
        ('b3_q5', 'L3', 'text', '"套牢"是指？', None,
         '[{"label":"买入后价格上涨","value":"A"},{"label":"买入后价格下跌，卖出将亏损而被迫持有","value":"B"},{"label":"通过期权锁定收益","value":"C"},{"label":"融券做空获利","value":"D"}]',
         'B', '套牢指买入后价格下跌，卖出会产生亏损，投资者被"套住"无法脱身。'),
        ('b3_q6', 'L3', 'text', '"仓位"指的是？', None,
         '[{"label":"账户现金余额","value":"A"},{"label":"持有股票资金占总资金的比例","value":"B"},{"label":"可用融资额度","value":"C"},{"label":"交易所分配的交易席位","value":"D"}]',
         'B', '仓位反映投入股市的资金比例，"满仓"指全部买入，"半仓"指一半股票一半现金。'),
        ('b3_q7', 'L3', 'text', '"止盈"是指？', None,
         '[{"label":"达到止损线卖出","value":"A"},{"label":"盈利达预期时卖出锁定利润","value":"B"},{"label":"不分盈利继续持有","value":"C"},{"label":"加仓摊低成本","value":"D"}]',
         'B', '止盈与止损相对应，在盈利达预期时卖出锁定利润，避免利润回吐。'),
        ('b3_q8', 'L3', 'text', '以下哪种操作属于"加仓"？', None,
         '[{"label":"首次买入1000股","value":"A"},{"label":"已持有2000股，再买入1000股","value":"B"},{"label":"卖出500股","value":"C"},{"label":"全部卖出","value":"D"}]',
         'B', '加仓指在已有头寸基础上追加买入，在看好的方向上增加仓位。'),
    ]):
        questions.append((*q, i))

    # ---- 基础概念 L4: 估值与选股 ----
    for i, q in enumerate([
        ('b4_q1', 'L4', 'text', '价值投资中"安全边际"指的是？', None,
         '[{"label":"买入价远高于内在价值","value":"A"},{"label":"买入价远低于内在价值","value":"B"},{"label":"买入价等于内在价值","value":"C"},{"label":"与价值无关","value":"D"}]',
         'B', '安全边际指买入价显著低于内在价值，留出容错空间，是价值投资的核心原则。'),
        ('b4_q2', 'L4', 'text', '以下哪项不属于基本面分析的范畴？', None,
         '[{"label":"PE市盈率分析","value":"A"},{"label":"ROE分析","value":"B"},{"label":"K线形态分析","value":"C"},{"label":"行业前景分析","value":"D"}]',
         'C', 'K线形态属于技术分析，基本面分析关注财务指标、行业前景、竞争优势等。'),
        ('b4_q3', 'L4', 'text', 'ROE > 15% 通常被认为？', None,
         '[{"label":"盈利能力很差","value":"A"},{"label":"盈利能力较强","value":"B"},{"label":"负债率过高","value":"C"},{"label":"无意义","value":"D"}]',
         'B', 'ROE > 15% 说明公司用股东投入的资本创造了较好的回报，是优质企业的标志之一。'),
        ('b4_q4', 'L4', 'text', '高PE低PB的股票可能属于？', None,
         '[{"label":"传统银行股","value":"A"},{"label":"高成长科技股","value":"B"},{"label":"亏损股票","value":"C"},{"label":"ST股票","value":"D"}]',
         'B', '高成长科技股因预期未来盈利大增，市场给予高PE；但资产规模小导致PB不高。'),
        ('b4_q5', 'L4', 'text', '股息率（Dividend Yield）的计算公式是？', None,
         '[{"label":"每股股息/每股市价","value":"A"},{"label":"每股市价/每股股息","value":"B"},{"label":"净利润/总市值","value":"C"},{"label":"每股股息/每股收益","value":"D"}]',
         'A', '股息率 = 每股股息/每股市价，反映投资者通过分红获得的现金回报率。'),
        ('b4_q6', 'L4', 'text', '价值投资大师巴菲特最看重的财务指标是？', None,
         '[{"label":"市盈率","value":"A"},{"label":"市净率","value":"B"},{"label":"净资产收益率（ROE）","value":"C"},{"label":"资产负债率","value":"D"}]',
         'C', '巴菲特认为ROE是衡量企业长期竞争力的最重要指标，持续高ROE的企业具有护城河。'),
        ('b4_q7', 'L4', 'text', 'PEG估值法中，G代表？', None,
         '[{"label":"总收益 Gross","value":"A"},{"label":"增长率 Growth","value":"B"},{"label":"商誉 Goodwill","value":"C"},{"label":"治理 Governance","value":"D"}]',
         'B', 'PEG = PE/盈利增长率，G代表盈利增长率，综合考虑估值和成长性。'),
        ('b4_q8', 'L4', 'text', '杜邦分析法将ROE拆解为哪三个因素？', None,
         '[{"label":"销售净利率×资产周转率×权益乘数","value":"A"},{"label":"毛利率×净利率×ROA","value":"B"},{"label":"营收×利润×资产","value":"C"},{"label":"PE×PB×PS","value":"D"}]',
         'A', '杜邦分析：ROE = 销售净利率 × 资产周转率 × 权益乘数，分别反映盈利能力、营运能力和财务杠杆。'),
    ]):
        questions.append((*q, i))

    # ---- 交易法则 T1: 海豚交易法 ----
    for i, q in enumerate([
        ('t1_q1', 'T1', 'text', '海豚交易法的核心思路是？', None,
         '[{"label":"长期持有不动","value":"A"},{"label":"利用回调寻找入场点，快进快出做波段","value":"B"},{"label":"每天全仓买卖","value":"C"},{"label":"只在底部抄底","value":"D"}]',
         'B', '海豚交易法是在上升趋势中的回调位置寻找买点，像海豚一样灵活跳跃的短线波段策略。'),
        ('t1_q2', 'T1', 'text', '海豚交易法的止损位一般设在？', None,
         '[{"label":"买入价任意位置","value":"A"},{"label":"前一波段最低点或关键均线下方","value":"B"},{"label":"不设止损","value":"C"},{"label":"亏损50%时","value":"D"}]',
         'B', '通常设在前一波段低点或关键均线（如MA20）下方，保护本金。'),
        ('t1_q3', 'T1', 'text', '海豚交易法适合什么市场环境？', None,
         '[{"label":"单边下跌市","value":"A"},{"label":"横盘震荡市","value":"B"},{"label":"上升趋势中的回调阶段","value":"C"},{"label":"任何市场环境","value":"D"}]',
         'C', '适用于上升趋势明确时的回调买入，顺势而为，下跌市中不适用。'),
        ('t1_q4', 'T1', 'text', '海豚交易法的止盈策略是？', None,
         '[{"label":"永远不卖","value":"A"},{"label":"盈利达目标位或出现反转信号时卖出","value":"B"},{"label":"等跌回成本价再卖","value":"C"},{"label":"固定持有3天","value":"D"}]',
         'B', '达到目标价位或出现技术反转信号时果断卖出，不贪心。'),
        ('t1_q5', 'T1', 'text', '海豚交易法中"仓位管理"的关键是？', None,
         '[{"label":"每次都满仓","value":"A"},{"label":"分批建仓，控制单笔风险","value":"B"},{"label":"越跌越加仓","value":"C"},{"label":"不需要管理","value":"D"}]',
         'B', '分批建仓、控制仓位，单笔交易不超过总资金的一定比例，避免一次性重仓被套。'),
        ('t1_q6', 'T1', 'text', '海豚交易法的"回调买点"通常出现在？', None,
         '[{"label":"价格连续涨停时","value":"A"},{"label":"上升趋势中价格回落至均线附近","value":"B"},{"label":"价格创新低时","value":"C"},{"label":"横盘不动时","value":"D"}]',
         'B', '在上升趋势中，价格回调至MA10或MA20附近获得支撑时，是海豚交易法的典型买点。'),
        ('t1_q7', 'T1', 'text', '海豚交易法建议单笔交易风险控制在总资金的？', None,
         '[{"label":"50%以上","value":"A"},{"label":"20%-30%","value":"B"},{"label":"2%-5%","value":"C"},{"label":"100%","value":"D"}]',
         'C', '专业交易员建议单笔风险不超过总资金的2%-5%，确保连续亏损也不会伤及本金。'),
        ('t1_q8', 'T1', 'text', '海豚交易法中"卖出的信号"不包括？', None,
         '[{"label":"达到目标盈利位","value":"A"},{"label":"出现顶部反转形态","value":"B"},{"label":"均线系统仍为多头排列","value":"C"},{"label":"跌破止损位","value":"D"}]',
         'C', '均线仍为多头排列说明趋势未变，不是卖出信号。止盈、反转、止损才是卖出依据。'),
    ]):
        questions.append((*q, i))

    # ---- 交易法则 T2: 海龟交易法 ----
    for i, q in enumerate([
        ('t2_q1', 'T2', 'text', '海龟交易法的入场信号是？', None,
         '[{"label":"跌破20日最低价买入","value":"A"},{"label":"突破20日最高价买入","value":"B"},{"label":"MACD金叉买入","value":"C"},{"label":"RSI超卖买入","value":"D"}]',
         'B', '经典海龟入场信号：价格突破过去20个交易日最高价时买入，属于趋势跟踪策略。'),
        ('t2_q2', 'T2', 'text', '海龟交易法的核心理念是？', None,
         '[{"label":"低买高卖","value":"A"},{"label":"截断亏损，让利润奔跑","value":"B"},{"label":"越跌越买","value":"C"},{"label":"每天高频交易","value":"D"}]',
         'B', '"截断亏损，让利润奔跑"——严格止损，趋势正确时持有不动获取大利润。'),
        ('t2_q3', 'T2', 'text', '海龟交易法的头寸规模由什么决定？', None,
         '[{"label":"固定金额买入","value":"A"},{"label":"市场的N值（波动率/ATR）","value":"B"},{"label":"随机决定","value":"C"},{"label":"全部资金买入","value":"D"}]',
         'B', '用ATR（平均真实波幅，即N值）计算头寸规模，波动大的少买，波动小得多买，使风险均等化。'),
        ('t2_q4', 'T2', 'text', '海龟交易法的退出规则是？', None,
         '[{"label":"盈利10%就卖","value":"A"},{"label":"跌破10日最低价卖出","value":"B"},{"label":"持有30天自动卖出","value":"C"},{"label":"不设置退出规则","value":"D"}]',
         'B', '跌破过去10个交易日最低价时卖出，确保趋势反转时及时离场。'),
        ('t2_q5', 'T2', 'text', '海龟交易法在震荡市中的表现如何？', None,
         '[{"label":"表现很好，频繁获利","value":"A"},{"label":"会产生多次假突破信号，连续亏损","value":"B"},{"label":"和趋势市一样好","value":"C"},{"label":"震荡市不能用任何策略","value":"D"}]',
         'B', '趋势跟踪策略在震荡市中会遭遇频繁假突破，导致连续小亏，需耐心等待趋势行情。'),
        ('t2_q6', 'T2', 'text', '海龟交易法的加仓（金字塔加仓）规则是？', None,
         '[{"label":"每次加仓规模和首次相同","value":"A"},{"label":"价格每向有利方向移动0.5N，加仓一个单位","value":"B"},{"label":"价格下跌时加仓","value":"C"},{"label":"不允许多次加仓","value":"D"}]',
         'B', '海龟交易法规定价格每向有利方向移动0.5N（N为ATR），可加仓一个单位，采用金字塔方式。'),
        ('t2_q7', 'T2', 'text', '海龟交易法中ATR（N值）的计算周期通常是？', None,
         '[{"label":"5个交易日","value":"A"},{"label":"10个交易日","value":"B"},{"label":"20个交易日","value":"C"},{"label":"60个交易日","value":"D"}]',
         'C', '海龟交易法使用20日ATR（平均真实波幅）作为波动率衡量标准。'),
        ('t2_q8', 'T2', 'text', '海龟交易法的止损幅度为？', None,
         '[{"label":"固定亏损5%","value":"A"},{"label":"2N（2倍ATR）","value":"B"},{"label":"不设置止损","value":"C"},{"label":"跌破成本价","value":"D"}]',
         'B', '海龟交易法规定止损为2N（2倍平均真实波幅），根据市场波动自动调整止损距离。'),
        ('t2_q9', 'T2', 'text', '海龟交易法中系统1和系统2的区别是？', None,
         '[{"label":"系统1用10日突破，系统2用55日突破","value":"A"},{"label":"系统1用55日突破，系统2用20日突破","value":"B"},{"label":"两个系统完全一样","value":"C"},{"label":"系统1做多，系统2做空","value":"D"}]',
         'A', '海龟系统1为10日突破入场，系统2为20日突破入场，两个系统互补减少假信号。'),
        ('t2_q10', 'T2', 'text', '海龟交易法最大的风险是？', None,
         '[{"label":"趋势行情中赚太多","value":"A"},{"label":"震荡市中频繁止损造成本金缓慢消耗","value":"B"},{"label":"交易手续费过高","value":"C"},{"label":"杠杆爆仓","value":"D"}]',
         'B', '趋势跟踪策略在震荡市中频繁出现假突破，连续止损会逐渐消耗本金，需要有足够的耐心等待趋势行情。'),
    ]):
        questions.append((*q, i))

    # ---- 交易法则 T3: 均线策略 ----
    for i, q in enumerate([
        ('t3_q1', 'T3', 'text', 'MA5上穿MA20形成的信号称为？', None,
         '[{"label":"死叉","value":"A"},{"label":"金叉","value":"B"},{"label":"背离","value":"C"},{"label":"突破","value":"D"}]',
         'B', '短期均线上穿长期均线称为金叉，是看涨信号；下穿称为死叉，是看跌信号。'),
        ('t3_q2', 'T3', 'text', '多头排列指的是？', None,
         '[{"label":"MA5>MA10>MA20>MA60","value":"A"},{"label":"MA5<MA10<MA20<MA60","value":"B"},{"label":"所有均线交叉缠绕","value":"C"},{"label":"均线全部向下","value":"D"}]',
         'A', '多头排列：短期均线在长期均线之上，表示趋势向上，是看涨信号。'),
        ('t3_q3', 'T3', 'text', '均线作为支撑位的含义是？', None,
         '[{"label":"价格不会跌破均线","value":"A"},{"label":"价格回调至均线附近时可能获得支撑反弹","value":"B"},{"label":"均线是固定不变的价格","value":"C"},{"label":"均线等于零","value":"D"}]',
         'B', '均线支撑指价格回调至均线附近时，买方力量可能介入使价格反弹，但不是绝对的。'),
        ('t3_q4', 'T3', 'text', 'EMA（指数移动平均线）相比MA的特点是？', None,
         '[{"label":"对所有数据等权重","value":"A"},{"label":"对近期价格赋予更高权重，反应更灵敏","value":"B"},{"label":"只计算收盘价","value":"C"},{"label":"不需要计算","value":"D"}]',
         'B', 'EMA对近期价格赋予更高权重，相比简单均线MA反应更灵敏，能更快捕捉趋势变化。'),
        ('t3_q5', 'T3', 'text', '"葛兰碧八大法则"主要研究的是？', None,
         '[{"label":"K线形态","value":"A"},{"label":"均线与价格的关系","value":"B"},{"label":"成交量分析","value":"C"},{"label":"宏观经济","value":"D"}]',
         'B', '葛兰碧八大法则研究均线与价格之间的八种买卖关系，是均线交易的经典理论。'),
        ('t3_q6', 'T3', 'text', '价格远离均线后"回归"的原因是？', None,
         '[{"label":"均线有吸引力","value":"A"},{"label":"获利回吐和抄底资金共同作用使价格向均线靠拢","value":"B"},{"label":"交易所干预","value":"C"},{"label":"没有原因","value":"D"}]',
         'B', '价格远离均线后，获利盘卖出+抄底资金买入，供需变化使价格向均线回归。'),
        ('t3_q7', 'T3', 'text', 'MA120和MA250通常被称为？', None,
         '[{"label":"短期均线","value":"A"},{"label":"中期均线","value":"B"},{"label":"长期均线（半年线/年线）","value":"C"},{"label":"超短期均线","value":"D"}]',
         'C', 'MA120≈半年线，MA250≈年线，属于长期均线，用于判断长期趋势方向。'),
        ('t3_q8', 'T3', 'text', '均线交叉策略在震荡市中的主要问题是？', None,
         '[{"label":"收益太高","value":"A"},{"label":"频繁产生虚假金叉/死叉信号","value":"B"},{"label":"均线失效","value":"C"},{"label":"无法计算均线","value":"D"}]',
         'B', '震荡市中均线频繁交叉，产生大量虚假信号，导致连续小亏。均线策略在趋势市中表现更好。'),
    ]):
        questions.append((*q, i))

    # ---- 交易法则 T4: 定投与网格 ----
    for i, q in enumerate([
        ('t4_q1', 'T4', 'text', '基金定投的核心优势是？', None,
         '[{"label":"一次性全部投入收益最高","value":"A"},{"label":"通过分批买入摊平成本，降低择时风险","value":"B"},{"label":"不需要承担任何风险","value":"C"},{"label":"保证盈利","value":"D"}]',
         'B', '定投通过固定时间、固定金额分批买入，在市场波动中自动摊低成本，降低择时风险。'),
        ('t4_q2', 'T4', 'text', '网格交易法适合什么市场环境？', None,
         '[{"label":"单边上涨市","value":"A"},{"label":"单边下跌市","value":"B"},{"label":"横盘震荡市","value":"C"},{"label":"任何环境","value":"D"}]',
         'C', '网格交易在震荡市中通过低吸高抛不断获取差价利润，在单边市中表现较差。'),
        ('t4_q3', 'T4', 'text', '网格交易法的风险在于？', None,
         '[{"label":"收益太低","value":"A"},{"label":"单边行情导致套牢或踏空","value":"B"},{"label":"操作太复杂","value":"C"},{"label":"手续费太高","value":"D"}]',
         'B', '单边下跌时网格会持续买入导致套牢，单边上涨时网格会过早卖完筹码踏空后续涨幅。'),
        ('t4_q4', 'T4', 'text', '定投的"微笑曲线"指的是？', None,
         '[{"label":"价格先跌后涨，定投成本先升后降","value":"A"},{"label":"价格先跌后涨，定投成本先降后升","value":"B"},{"label":"价格一直上涨","value":"C"},{"label":"价格一直下跌","value":"D"}]',
         'B', '微笑曲线：市场先跌后涨，定投在下跌中持续以更低价格买入摊低成本，上涨时获得更好回报。'),
        ('t4_q5', 'T4', 'text', '网格交易法中"网格间距"设置过小的问题是？', None,
         '[{"label":"交易频率低","value":"A"},{"label":"频繁交易，手续费成本高","value":"B"},{"label":"利润空间大","value":"C"},{"label":"没有影响","value":"D"}]',
         'B', '网格间距过小会导致交易频繁，虽然每次获利小，但手续费成本累积可能侵蚀利润。'),
        ('t4_q6', 'T4', 'text', '智能定投（估值定投）相比普通定投的优势是？', None,
         '[{"label":"估值低时多投，估值高时少投","value":"A"},{"label":"固定金额更简单","value":"B"},{"label":"不需要择时","value":"C"},{"label":"保证盈利","value":"D"}]',
         'A', '智能定投根据估值高低调整投入金额：低估多投、高估少投或止盈，进一步提升收益。'),
        ('t4_q7', 'T4', 'text', '定投策略最适合以下哪种标的？', None,
         '[{"label":"个股","value":"A"},{"label":"宽基指数基金（如沪深300ETF）","value":"B"},{"label":"ST股票","value":"C"},{"label":"期货合约","value":"D"}]',
         'B', '宽基指数长期趋势向上且具有波动性，是定投的最佳标的。个股可能退市不适合定投。'),
        ('t4_q8', 'T4', 'text', '网格交易法中，当价格跌破网格下限时应该？', None,
         '[{"label":"继续加仓","value":"A"},{"label":"暂停网格，评估趋势是否改变","value":"B"},{"label":"立即清仓","value":"C"},{"label":"提高网格上限","value":"D"}]',
         'B', '价格跌破网格下限说明可能从震荡转为单边下跌，应暂停网格评估趋势，避免持续套牢。'),
    ]):
        questions.append((*q, i))

    # ---- K线实盘 K1: 单根K线 ----
    for i, q in enumerate([
        ('k1_q1', 'K1', 'image', 'K线实体部分较长、上影线很短、下影线也短，这是？', '/assets/kline/big-yang.svg',
         '[{"label":"十字星","value":"A"},{"label":"大阳线","value":"B"},{"label":"大阴线","value":"C"},{"label":"锤子线","value":"D"}]',
         'B', '大阳线：实体长（收盘远高于开盘），上下影线短，买方力量强劲。'),
        ('k1_q2', 'K1', 'image', '开盘价等于收盘价，几乎没有实体，上下影线较长，这是？', '/assets/kline/doji.svg',
         '[{"label":"大阳线","value":"A"},{"label":"阴线","value":"B"},{"label":"十字星","value":"C"},{"label":"射击之星","value":"D"}]',
         'C', '十字星：开盘≈收盘，实体极小，上下影线长，多空均衡，可能变盘。'),
        ('k1_q3', 'K1', 'text', 'A股市场中，红色K线代表？', None,
         '[{"label":"收盘价低于开盘价","value":"A"},{"label":"收盘价高于开盘价","value":"B"},{"label":"收盘价等于开盘价","value":"C"},{"label":"成交量放大","value":"D"}]',
         'B', 'A股红色K线（阳线）表示收盘价高于开盘价，绿色K线（阴线）表示下跌。'),
        ('k1_q4', 'K1', 'image', '下影线很长的K线（锤子线）通常出现在？', '/assets/kline/hammer.svg',
         '[{"label":"上涨趋势顶部","value":"A"},{"label":"下跌趋势底部，可能反转","value":"B"},{"label":"横盘震荡中","value":"C"},{"label":"成交量萎缩时","value":"D"}]',
         'B', '锤子线在下跌趋势底部出现，长下影线表示价格曾大幅下跌但被买方拉回，是潜在反转信号。'),
        ('k1_q5', 'K1', 'image', '实体很短、上影线很长的K线（射击之星）意味着？', '/assets/kline/shooting-star.svg',
         '[{"label":"买方强势突破","value":"A"},{"label":"卖方压力大，可能回调","value":"B"},{"label":"没有特别含义","value":"C"},{"label":"成交量不足","value":"D"}]',
         'B', '射击之星在上涨趋势中，上影线长说明冲高后被卖方打压，是潜在顶部反转信号。'),
        ('k1_q6', 'K1', 'image', '实体很长且收盘远低于开盘，几乎没有上下影线，这是？', '/assets/kline/big-yin.svg',
         '[{"label":"大阳线","value":"A"},{"label":"十字星","value":"B"},{"label":"大阴线（光脚阴线）","value":"C"},{"label":"T字线","value":"D"}]',
         'C', '大阴线（光脚阴线）：实体长，收盘远低于开盘，几乎无上下影线，表示卖方力量极强。'),
        ('k1_q7', 'K1', 'image', '开盘后大幅下跌，随后被买方拉回至接近开盘价，下影线长、上影线短的K线是？', '/assets/kline/hammer2.svg',
         '[{"label":"射击之星","value":"A"},{"label":"倒锤子线","value":"B"},{"label":"锤子线","value":"C"},{"label":"十字星","value":"D"}]',
         'C', '锤子线特征：实体小（可在顶部），下影线长（至少是实体的2倍），上影线短或无。'),
        ('k1_q8', 'K1', 'image', '价格先上涨后回落再拉升，上影线长、下影线短、实体小在底部的K线是？', '/assets/kline/inverse-hammer.svg',
         '[{"label":"锤子线","value":"A"},{"label":"倒锤子线","value":"B"},{"label":"T字线","value":"C"},{"label":"十字星","value":"D"}]',
         'B', '倒锤子线：实体小在底部，上影线长（至少是实体2倍），下影线短或无，是潜在底部反转信号。'),
        ('k1_q9', 'K1', 'image', '收盘价等于最高价，几乎没有上影线，下影线很长，形似字母"T"，这是？', '/assets/kline/t-line.svg',
         '[{"label":"锤子线","value":"A"},{"label":"倒锤子线","value":"B"},{"label":"T字线","value":"C"},{"label":"一字线","value":"D"}]',
         'C', 'T字线：开盘=收盘=最高价，下影线长。表示开盘后下跌但被买方拉回，是底部支撑信号。'),
        ('k1_q10', 'K1', 'image', '开盘价=收盘价=最高价=最低价，形成一条横线，这是？', '/assets/kline/limit-line.svg',
         '[{"label":"十字星","value":"A"},{"label":"T字线","value":"B"},{"label":"一字线（涨跌停）","value":"C"},{"label":"大阳线","value":"D"}]',
         'C', '一字线通常出现在涨跌停时，开盘即封死涨停或跌停，全天无波动。'),
    ]):
        questions.append((*q, i))

    # ---- K线实盘 K2: K线组合 ----
    for i, q in enumerate([
        ('k2_q1', 'K2', 'image', '第一根长阴线、第二根长阳线，阳线实体完全包住阴线实体，这是？', '/assets/kline/bullish-engulf.svg',
         '[{"label":"吞没形态（看涨）","value":"A"},{"label":"十字星","value":"B"},{"label":"三只乌鸦","value":"C"},{"label":"上升三法","value":"D"}]',
         'A', '看涨吞没：第二根阳线实体完全吞没前一根阴线，是强烈的底部反转信号。'),
        ('k2_q2', 'K2', 'image', '连续三根阴线，每根收盘价都比前一根低，这是？', '/assets/kline/three-crows.svg',
         '[{"label":"红三兵","value":"A"},{"label":"三只乌鸦","value":"B"},{"label":"早晨之星","value":"C"},{"label":"锤子线","value":"D"}]',
         'B', '三只乌鸦：连续三根阴线逐步下跌，每根收盘创新低，表示卖压持续，是看跌信号。'),
        ('k2_q3', 'K2', 'image', '高位出现十字星，随后一根大阴线向下突破，这是？', '/assets/kline/evening-star.svg',
         '[{"label":"早晨之星","value":"A"},{"label":"黄昏之星","value":"B"},{"label":"上升三法","value":"C"},{"label":"看涨吞没","value":"D"}]',
         'B', '黄昏之星：高位十字星+大阴线，是经典的顶部反转形态，说明上涨动能衰竭。'),
        ('k2_q4', 'K2', 'image', '一根大阳线后接三根小阴线，价格不跌破阳线最低点，这是？', '/assets/kline/rising-three.svg',
         '[{"label":"三只乌鸦","value":"A"},{"label":"黄昏之星","value":"B"},{"label":"上升三法","value":"C"},{"label":"下降三法","value":"D"}]',
         'C', '上升三法：大阳线后小阴线回调但不破阳线低点，是趋势休整，后市通常继续上涨。'),
        ('k2_q5', 'K2', 'image', '下跌趋势中先有大阴线，随后出现十字星，再跟一根大阳线，这是？', '/assets/kline/morning-star.svg',
         '[{"label":"黄昏之星","value":"A"},{"label":"早晨之星","value":"B"},{"label":"红三兵","value":"C"},{"label":"三只乌鸦","value":"D"}]',
         'B', '早晨之星：大阴线+十字星+大阳线，出现在下跌底部，是强烈的底部反转信号。'),
        ('k2_q6', 'K2', 'image', '连续三根阳线，每根收盘价都比前一根高，实体逐渐增大，这是？', '/assets/kline/three-soldiers.svg',
         '[{"label":"三只乌鸦","value":"A"},{"label":"红三兵","value":"B"},{"label":"黄昏之星","value":"C"},{"label":"十字星","value":"D"}]',
         'B', '红三兵：连续三根阳线逐步上涨，实体增大，表示买盘持续涌入，是看涨信号。'),
        ('k2_q7', 'K2', 'image', '下跌趋势中一根长阴线后，次日一根阳线深入阴线实体内部超过一半，这是？', '/assets/kline/piercing.svg',
         '[{"label":"看涨吞没","value":"A"},{"label":"刺透形态（斩回线）","value":"B"},{"label":"乌云盖顶","value":"C"},{"label":"十字星","value":"D"}]',
         'B', '刺透形态：长阴线后阳线开盘低于阴线最低点但收盘深入阴线实体超过50%，是底部反转信号。'),
        ('k2_q8', 'K2', 'image', '上涨趋势中一根长阳线后，次日高开低走的大阴线收盘深入阳线实体内部超过一半，这是？', '/assets/kline/dark-cloud.svg',
         '[{"label":"看涨吞没","value":"A"},{"label":"刺透形态","value":"B"},{"label":"乌云盖顶","value":"C"},{"label":"早晨之星","value":"D"}]',
         'C', '乌云盖顶：长阳线后大阴线深入阳线实体超过50%，是顶部反转信号。'),
        ('k2_q9', 'K2', 'image', '一根大阴线后接三根小阳线，价格不跌破阴线最低点，这是？', '/assets/kline/falling-three.svg',
         '[{"label":"上升三法","value":"A"},{"label":"下降三法","value":"B"},{"label":"红三兵","value":"C"},{"label":"三只乌鸦","value":"D"}]',
         'B', '下降三法：大阴线后小阳线反弹但不破阴线低点，是下跌趋势中的休整，后市通常继续下跌。'),
        ('k2_q10', 'K2', 'image', '第二根阴线实体完全吞没前一根阳线实体，这是？', '/assets/kline/bearish-engulf.svg',
         '[{"label":"看涨吞没","value":"A"},{"label":"看跌吞没","value":"B"},{"label":"十字星","value":"C"},{"label":"红三兵","value":"D"}]',
         'B', '看跌吞没：第二根阴线实体完全吞没前一根阳线，是强烈的顶部反转信号。'),
    ]):
        questions.append((*q, i))

    # ---- K线实盘 K3: 趋势形态 ----
    for i, q in enumerate([
        ('k3_q1', 'K3', 'image', '价格先上涨形成左肩，再创新高形成头部，随后回落再反弹但未创新高形成右肩，这是？', '/assets/kline/head-shoulder.svg',
         '[{"label":"双顶形态","value":"A"},{"label":"头肩顶形态","value":"B"},{"label":"三角形整理","value":"C"},{"label":"旗形整理","value":"D"}]',
         'B', '头肩顶：左肩-头部（最高点）-右肩（低于头部），跌破颈线后确认，是看跌信号。'),
        ('k3_q2', 'K3', 'image', '价格两次冲击同一高点后回落，形成两个相近的高点，这是？', '/assets/kline/double-top.svg',
         '[{"label":"双底形态","value":"A"},{"label":"头肩顶","value":"B"},{"label":"双顶形态（M头）","value":"C"},{"label":"楔形","value":"D"}]',
         'C', '双顶（M头）：两次冲击同一高点失败，跌破中间低点（颈线）后确认，是看跌形态。'),
        ('k3_q3', 'K3', 'image', '价格两次跌至同一支撑位后反弹，形成两个相近的低点，这是？', '/assets/kline/double-bottom.svg',
         '[{"label":"双顶形态","value":"A"},{"label":"双底形态（W底）","value":"B"},{"label":"头肩顶","value":"C"},{"label":"三角形","value":"D"}]',
         'B', '双底（W底）：两次跌至同一支撑位，突破中间高点（颈线）后确认，是看涨形态。'),
        ('k3_q4', 'K3', 'image', '价格高点逐步降低、低点逐步抬高，K线被压缩在一个收敛的三角区域内，这是？', '/assets/kline/sym-triangle.svg',
         '[{"label":"上升三角形","value":"A"},{"label":"下降三角形","value":"B"},{"label":"对称三角形整理","value":"C"},{"label":"旗形整理","value":"D"}]',
         'C', '对称三角形：高点降低、低点抬高，多空力量均衡，最终突破方向决定后续走势。'),
        ('k3_q5', 'K3', 'image', '一段大涨后出现小幅回调，回调通道向下倾斜且与上涨趋势平行，这是？', '/assets/kline/bull-flag.svg',
         '[{"label":"楔形","value":"A"},{"label":"牛旗形态","value":"B"},{"label":"头肩底","value":"C"},{"label":"双底","value":"D"}]',
         'B', '牛旗：大涨后的回调通道向下倾斜，是上涨趋势中的短暂休整，通常突破后延续上涨。'),
        ('k3_q6', 'K3', 'image', '上升趋势中，高点在同一水平线上，低点逐步抬高，这是？', '/assets/kline/asc-triangle.svg',
         '[{"label":"下降三角形","value":"A"},{"label":"对称三角形","value":"B"},{"label":"上升三角形","value":"C"},{"label":"楔形","value":"D"}]',
         'C', '上升三角形：高点在水平阻力线上，低点逐步抬高，买方力量在累积，向上突破概率较大。'),
        ('k3_q7', 'K3', 'image', '下跌趋势中，低点在同一水平线上，高点逐步降低，这是？', '/assets/kline/desc-triangle.svg',
         '[{"label":"上升三角形","value":"A"},{"label":"下降三角形","value":"B"},{"label":"对称三角形","value":"C"},{"label":"旗形","value":"D"}]',
         'B', '下降三角形：低点在水平支撑线上，高点逐步降低，卖方力量在累积，向下突破概率较大。'),
        ('k3_q8', 'K3', 'image', '价格高点逐步降低，低点也逐步降低，两条收敛线都向下倾斜，这是？', '/assets/kline/falling-wedge.svg',
         '[{"label":"上升楔形","value":"A"},{"label":"下降楔形","value":"B"},{"label":"旗形","value":"C"},{"label":"三角形","value":"D"}]',
         'B', '下降楔形：高点和低点都逐步降低但收敛，通常出现在下跌趋势中，是潜在的看涨反转信号。'),
        ('k3_q9', 'K3', 'image', '头肩底形态完成后（突破颈线），价格目标的计算方法是？', '/assets/kline/head-shoulder-bottom.svg',
         '[{"label":"从突破点加上头部到颈线的垂直距离","value":"A"},{"label":"从头部价格乘以2","value":"B"},{"label":"没有固定的价格目标","value":"C"},{"label":"从右肩价格除以2","value":"D"}]',
         'A', '头肩底最小价格目标 = 突破点 +（头部到颈线的垂直距离），这是形态的测量目标位。'),
        ('k3_q10', 'K3', 'image', '圆弧形（碟形）形态的特征是？', '/assets/kline/rounding.svg',
         '[{"label":"价格快速上涨后快速下跌","value":"A"},{"label":"价格缓慢筑底后缓慢回升，形成圆弧状","value":"B"},{"label":"价格在窄幅区间反复震荡","value":"C"},{"label":"价格呈锯齿状波动","value":"D"}]',
         'B', '圆弧形：价格缓慢下跌至底部后缓慢回升，形成圆弧状，表示趋势从跌转涨的渐变过程。'),
    ]):
        questions.append((*q, i))

    # ---- K线实盘 K4: 量价分析 ----
    for i, q in enumerate([
        ('k4_q1', 'K4', 'image', '价格上涨但成交量逐步萎缩，这是？', '/assets/kline/vol-divergence.svg',
         '[{"label":"量价配合良好","value":"A"},{"label":"量价背离，上涨动能可能减弱","value":"B"},{"label":"成交量不影响价格","value":"C"},{"label":"趋势将加速","value":"D"}]',
         'B', '量价背离：价格上涨但成交量递减，说明追涨意愿不足，上涨动能可能减弱。'),
        ('k4_q2', 'K4', 'image', '价格上涨且成交量同步放大，这是？', '/assets/kline/vol-confirm.svg',
         '[{"label":"量价背离","value":"A"},{"label":"量价配合良好，趋势健康","value":"B"},{"label":"即将见顶","value":"C"},{"label":"没有特别含义","value":"D"}]',
         'B', '价涨量增是健康的上涨信号，说明有新资金持续流入，趋势延续概率大。'),
        ('k4_q3', 'K4', 'image', '价格下跌时成交量放大，说明？', '/assets/kline/vol-sell.svg',
         '[{"label":"买方力量增强","value":"A"},{"label":"卖压沉重，大量抛售","value":"B"},{"label":"市场在底部吸筹","value":"C"},{"label":"没有影响","value":"D"}]',
         'B', '价跌量增说明卖压沉重，大量资金在抛售，短期内可能继续下跌。'),
        ('k4_q4', 'K4', 'image', '价格长期下跌后出现"放量阳线"（成交量突然放大），可能意味着？', '/assets/kline/vol-bottom.svg',
         '[{"label":"趋势将继续下跌","value":"A"},{"label":"有资金在底部进场抄底","value":"B"},{"label":"主力在出货","value":"C"},{"label":"没有特别含义","value":"D"}]',
         'B', '长期下跌后放量上涨，往往意味着有资金认为价格已到底部区域，开始进场建仓。'),
        ('k4_q5', 'K4', 'image', '"天量天价"指的是？', '/assets/kline/vol-peak.svg',
         '[{"label":"成交量最大时价格往往也处于阶段性高点","value":"A"},{"label":"成交量最大时价格最低","value":"B"},{"label":"成交量和价格无关","value":"C"},{"label":"成交量越小价格越高","value":"D"}]',
         'A', '天量天价：成交量极度放大时，价格往往处于阶段性高点，随后可能回调。'),
        ('k4_q6', 'K4', 'image', '缩量回调到均线附近后企稳，通常意味着？', '/assets/kline/vol-pullback.svg',
         '[{"label":"趋势反转","value":"A"},{"label":"健康的趋势休整，回调后可能继续上涨","value":"B"},{"label":"即将暴跌","value":"C"},{"label":"成交量没有参考价值","value":"D"}]',
         'B', '缩量回调说明抛压不重，到均线附近企稳表示支撑有效，是趋势中的健康休整。'),
        ('k4_q7', 'K4', 'image', 'OBV（能量潮指标）持续上升但价格横盘，说明？', '/assets/kline/obv.svg',
         '[{"label":"资金在持续流出","value":"A"},{"label":"资金在暗中吸筹，可能即将突破","value":"B"},{"label":"指标失效","value":"C"},{"label":"价格会继续横盘","value":"D"}]',
         'B', 'OBV上升说明成交量中买方占优，价格横盘但资金暗中流入，可能即将向上突破。'),
        ('k4_q8', 'K4', 'image', '换手率突然显著放大，可能的原因是？', '/assets/kline/turnover.svg',
         '[{"label":"没有人关注该股票","value":"A"},{"label":"有大资金进出或重大消息面变化","value":"B"},{"label":"股票要退市","value":"C"},{"label":"正常波动没有原因","value":"D"}]',
         'B', '换手率突然放大通常意味着有大资金进场/离场，或者市场对股票的预期发生了重大变化。'),
    ]):
        questions.append((*q, i))

    # ---- K线预测 P1: 下周涨跌预测 ----
    for i, q in enumerate([
        ('p1_q1', 'P1', 'predict', '贵州茅台本周连续放量上涨突破MA20，MACD金叉，请预测下周方向？', '/assets/kline/predict-1.svg',
         '[{"label":"📈 看涨","value":"A"},{"label":"📉 看跌","value":"B"},{"label":"➡️ 横盘","value":"C"}]',
         'A', '放量上涨+突破MA20+MACD金叉，多头信号明确，下周大概率延续上涨。'),
        ('p1_q2', 'P1', 'predict', '宁德时代本周缩量下跌跌破MA5和MA10，RSI持续走低，请预测下周方向？', '/assets/kline/predict-2.svg',
         '[{"label":"📈 看涨","value":"A"},{"label":"📉 看跌","value":"B"},{"label":"➡️ 横盘","value":"C"}]',
         'B', '缩量跌破短期均线+RSI走低，空头占优，下周可能继续回调。'),
        ('p1_q3', 'P1', 'predict', '中国平安本周窄幅震荡成交量萎缩，布林带收窄，请预测下周方向？', '/assets/kline/predict-3.svg',
         '[{"label":"📈 看涨","value":"A"},{"label":"📉 看跌","value":"B"},{"label":"➡️ 横盘","value":"C"}]',
         'C', '窄幅震荡+量缩+布林带收窄，多空均衡，下周大概率继续横盘等待方向选择。'),
        ('p1_q4', 'P1', 'predict', '比亚迪本周出现早晨之星，放量突破前期平台，请预测下周方向？', '/assets/kline/predict-4.svg',
         '[{"label":"📈 看涨","value":"A"},{"label":"📉 看跌","value":"B"},{"label":"➡️ 横盘","value":"C"}]',
         'A', '早晨之星+放量突破平台，多头确立，下周有望延续涨势。'),
        ('p1_q5', 'P1', 'predict', '隆基绿能本周高位出现黄昏之星，大阴线跌破MA20，请预测下周方向？', '/assets/kline/predict-5.svg',
         '[{"label":"📈 看涨","value":"A"},{"label":"📉 看跌","value":"B"},{"label":"➡️ 横盘","value":"C"}]',
         'B', '黄昏之星+跌破MA20，空头信号明确，下周可能加速下跌。'),
        ('p1_q6', 'P1', 'predict', '某股票本周放量站上布林带上轨，RSI超过80进入超买区，请预测下周方向？', '/assets/kline/predict-6.svg',
         '[{"label":"📈 看涨","value":"A"},{"label":"📉 看跌或回调","value":"B"},{"label":"➡️ 横盘","value":"C"}]',
         'B', '突破布林上轨+RSI超买，短期过热，下周大概率回调或横盘消化。'),
        ('p1_q7', 'P1', 'predict', '某股票在底部横盘震荡3周后出现放量小阳线突破MA60，请预测下周方向？', '/assets/kline/predict-7.svg',
         '[{"label":"📈 看涨","value":"A"},{"label":"📉 看跌","value":"B"},{"label":"➡️ 横盘","value":"C"}]',
         'A', '底部横盘后放量突破MA60，是长期筑底结束信号，下周有望启动上涨。'),
        ('p1_q8', 'P1', 'predict', '某股票本周连续十字星震荡，成交量极度萎缩，请预测下周方向？', '/assets/kline/predict-8.svg',
         '[{"label":"📈 看涨","value":"A"},{"label":"📉 看跌","value":"B"},{"label":"➡️ 横盘等待方向选择","value":"C"}]',
         'C', '连续十字星+极度缩量，说明市场在等待催化剂，短期方向不明，大概率继续横盘。'),
    ]):
        questions.append((*q, i))

    # ---- K线预测 P2: 趋势转折预测 ----
    for i, q in enumerate([
        ('p2_q1', 'P2', 'predict', '高位出现黄昏之星+量价背离+RSI超买回落，趋势是否即将反转？', '/assets/kline/trend-1.svg',
         '[{"label":"是，由涨转跌","value":"A"},{"label":"是，由跌转涨","value":"B"},{"label":"否，趋势延续","value":"C"}]',
         'A', '多重顶部信号叠加，趋势很可能由涨转跌。'),
        ('p2_q2', 'P2', 'predict', '底部出现早晨之星+放量突破下降趋势线+MACD底背离，趋势是否即将反转？', '/assets/kline/trend-2.svg',
         '[{"label":"是，由涨转跌","value":"A"},{"label":"是，由跌转涨","value":"B"},{"label":"否，趋势延续","value":"C"}]',
         'B', '多重底部信号叠加，趋势很可能由跌转涨。'),
        ('p2_q3', 'P2', 'predict', '小幅回调未破关键支撑，MA排列仍为多头，量能良好，趋势是否即将反转？', '/assets/kline/trend-3.svg',
         '[{"label":"是，由涨转跌","value":"A"},{"label":"是，由跌转涨","value":"B"},{"label":"否，趋势将延续","value":"C"}]',
         'C', '未破关键支撑+多头排列+量能配合，趋势大概率延续而非反转。'),
        ('p2_q4', 'P2', 'predict', '上涨末端长上影线+量价背离+CCI超买拐头，趋势是否即将反转？', '/assets/kline/trend-4.svg',
         '[{"label":"是，由涨转跌","value":"A"},{"label":"是，由跌转涨","value":"B"},{"label":"否，趋势延续","value":"C"}]',
         'A', '长上影+量价背离+超买拐头，多头动能衰竭，可能由涨转跌。'),
        ('p2_q5', 'P2', 'predict', '十字星震荡但重心仍在MA20之上，量能温和放大，趋势是否即将反转？', '/assets/kline/trend-5.svg',
         '[{"label":"是，由涨转跌","value":"A"},{"label":"是，由跌转涨","value":"B"},{"label":"否，趋势将延续","value":"C"}]',
         'C', '重心在MA20之上+量能放大，未出现明确反转信号。'),
        ('p2_q6', 'P2', 'predict', '下跌趋势中出现放量锤子线+RSI底背离，趋势是否即将反转？', '/assets/kline/trend-6.svg',
         '[{"label":"是，由涨转跌","value":"A"},{"label":"是，由跌转涨","value":"B"},{"label":"否，趋势延续","value":"C"}]',
         'B', '锤子线+RSI底背离，底部买盘介入信号，趋势可能由跌转涨。'),
        ('p2_q7', 'P2', 'predict', '上升趋势中MACD出现顶背离（价格创新高但MACD未创新高），趋势是否即将反转？', '/assets/kline/trend-7.svg',
         '[{"label":"是，由涨转跌","value":"A"},{"label":"是，由跌转涨","value":"B"},{"label":"否，趋势延续","value":"C"}]',
         'A', 'MACD顶背离说明价格上涨但动能在衰减，是潜在的顶部反转信号。'),
        ('p2_q8', 'P2', 'predict', '布林带从上轨收窄转向水平，价格在中轨附近反复震荡，趋势是否即将反转？', '/assets/kline/trend-8.svg',
         '[{"label":"是，由涨转跌","value":"A"},{"label":"是，由跌转涨","value":"B"},{"label":"否，趋势转为横盘震荡","value":"C"}]',
         'C', '布林带收窄水平化+价格在中轨震荡，说明上涨趋势结束，但也不一定会大跌，更可能转为横盘。'),
    ]):
        questions.append((*q, i))

    # ---- K线预测 P3: 支撑压力预测 ----
    for i, q in enumerate([
        ('p3_q1', 'P3', 'predict', '某股票价格在 MA60 附近多次获得支撑反弹，当前再次回调到 MA60，请预测？', '/assets/kline/support-1.svg',
         '[{"label":"大概率获得支撑反弹","value":"A"},{"label":"大概率跌破继续下跌","value":"B"},{"label":"没有规律可循","value":"C"}]',
         'A', 'MA60 作为重要均线多次发挥支撑作用，再次回调到此处时大概率仍有支撑。'),
        ('p3_q2', 'P3', 'predict', '某股票前期在 50 元处形成多次高点（压力位），当前价格接近 50 元，请预测？', '/assets/kline/resist-1.svg',
         '[{"label":"一定能突破 50 元","value":"A"},{"label":"可能遭遇压力需要放量才能突破","value":"B"},{"label":"会立刻大跌","value":"C"}]',
         'B', '前期多次高点形成压力位，价格接近时需要放量才能突破，否则可能遇阻回调。'),
        ('p3_q3', 'P3', 'predict', '某股票跌破前期重要支撑位 30 元且放量，请预测后市？', '/assets/kline/breakdown-1.svg',
         '[{"label":"会立刻反弹回 30 元上方","value":"A"},{"label":"支撑变压力，可能继续下跌","value":"B"},{"label":"横盘不动","value":"C"}]',
         'B', '放量跌破重要支撑位后，原来的支撑位转变为压力位，后市大概率继续下行。'),
        ('p3_q4', 'P3', 'predict', '某股票放量突破前期高点压力位 80 元，请预测后市？', '/assets/kline/breakout-1.svg',
         '[{"label":"立刻大跌回 80 元以下","value":"A"},{"label":"打开上涨空间，可能继续上涨","value":"B"},{"label":"横盘不动","value":"C"}]',
         'B', '放量突破前期压力位后，原来的压力位转变为支撑位，打开上涨空间。'),
        ('p3_q5', 'P3', 'predict', '某股票价格在布林带中轨附近反复震荡，布林带正在收窄，请预测？', '/assets/kline/boll-1.svg',
         '[{"label":"会继续横盘直到布林带开口","value":"A"},{"label":"即将出现方向性突破（上或下）","value":"B"},{"label":"会下跌","value":"C"}]',
         'B', '布林带收窄到极限后通常会出现方向性突破，横盘时间越长突破力度越大。'),
        ('p3_q6', 'P3', 'predict', '某股票在下跌过程中成交量持续萎缩，接近前期低点支撑位，请预测？', '/assets/kline/shrink-1.svg',
         '[{"label":"放量跌破支撑","value":"A"},{"label":"缩量说明卖压衰竭，可能在支撑位企稳","value":"B"},{"label":"横盘不动","value":"C"}]',
         'B', '下跌中量缩说明抛压在减少，接近支撑位时空头力量可能衰竭，有望企稳反弹。'),
    ]):
        questions.append((*q, i))

    # 批量插入题目
    cursor.executemany(
        'INSERT OR IGNORE INTO questions (id, level_id, type, title, image_url, options_json, answer, explanation, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        questions
    )

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")
    print(f"Inserted {len(levels)} levels and {len(questions)} questions")


if __name__ == '__main__':
    init_db()
    seed_levels_and_questions()
