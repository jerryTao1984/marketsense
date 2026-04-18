"""
基于海豚交易法则、深度估值Agent、波动率反转与统计套利生成题目
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

def gen_dolphin_questions(cursor):
    questions = {
        'T1': [
            {
                "title": "海豚交易法则被公认为全球交易界几大经典交易系统之一？",
                "options": [
                    {"label": "五大经典系统", "value": "A"},
                    {"label": "八大经典交易系统", "value": "B"},
                    {"label": "十大经典系统", "value": "C"},
                    {"label": "三大经典系统", "value": "D"},
                ],
                "answer": "B",
                "explanation": "海豚交易法则被公认为八大经典交易系统之一，与海龟交易法则、123法则等齐名。"
            },
            {
                "title": "海豚交易法则的哲学理念是什么？",
                "options": [
                    {"label": "预测市场顶部和底部", "value": "A"},
                    {"label": "右侧交易，等待趋势确认后才部署资本", "value": "B"},
                    {"label": "频繁短线交易", "value": "C"},
                    {"label": "长期持有不动", "value": "D"},
                ],
                "answer": "B",
                "explanation": "海豚法则深刻依赖右侧交易哲学，绝对不应试图预测市场的绝对顶部或底部，必须等待趋势确认后才进行交易。"
            },
            {
                "title": "海豚交易法则中，趋势判断期的核心指标是什么？",
                "options": [
                    {"label": "RSI和MACD", "value": "A"},
                    {"label": "MA26和MACD", "value": "B"},
                    {"label": "KD和布林带", "value": "C"},
                    {"label": "布林带和成交量", "value": "D"},
                ],
                "answer": "B",
                "explanation": "趋势判断期内，海豚法则依赖MA26移动平均线和MACD指标来量化市场宏观状态。"
            },
            {
                "title": "海豚法则中，MA26的参数26最初来源于什么？",
                "options": [
                    {"label": "随机测试结果", "value": "A"},
                    {"label": "历史上一个标准月约26个交易日", "value": "B"},
                    {"label": "斐波那契数列", "value": "C"},
                    {"label": "一周交易日的倍数", "value": "D"},
                ],
                "answer": "B",
                "explanation": "在五天工作制广泛采用之前，一个标准日历月通常包含约26个交易日，MA26最初被构建为月度均衡价格的替代指标。"
            },
            {
                "title": "海豚法则第一象限（牛市）的系统条件是什么？",
                "options": [
                    {"label": "价格>MA26，MACD值>信号线>0", "value": "A"},
                    {"label": "价格<MA26，MACD值<信号线<0", "value": "B"},
                    {"label": "价格>MA26，信号线>MACD值>0", "value": "C"},
                    {"label": "价格<MA26，信号线<MACD值<0", "value": "D"},
                ],
                "answer": "A",
                "explanation": "第一象限牛市：价格位于MA26之上，且MACD值>信号线>0，表明市场处于积极的机构资金吸筹状态。"
            },
            {
                "title": "海豚法则第二象限（上升调整）的系统执行授权是什么？",
                "options": [
                    {"label": "积极做多", "value": "A"},
                    {"label": "平仓多头，尝试做空", "value": "B"},
                    {"label": "积极做空", "value": "C"},
                    {"label": "平仓空头，尝试做多", "value": "D"},
                ],
                "answer": "B",
                "explanation": "第二象限：价格>MA26但信号线>MACD值>0，动量减速。系统授权清算多头头寸并尝试战术性做空。"
            },
            {
                "title": "海豚法则第三象限（熊市）的系统条件是什么？",
                "options": [
                    {"label": "价格>MA26，MACD值>信号线>0", "value": "A"},
                    {"label": "价格>MA26，信号线>MACD值>0", "value": "B"},
                    {"label": "价格<MA26，MACD值<信号线<0", "value": "C"},
                    {"label": "价格<MA26，信号线<MACD值<0", "value": "D"},
                ],
                "answer": "C",
                "explanation": "第三象限熊市：价格位于MA26之下，且MACD值<信号线<0，市场处于持续的资金派发状态。"
            },
            {
                "title": "海豚法则中，出入场期使用什么指标来精准锁定入场时机？",
                "options": [
                    {"label": "MACD", "value": "A"},
                    {"label": "MA26", "value": "B"},
                    {"label": "KD随机指标（随机振荡器）", "value": "C"},
                    {"label": "布林带", "value": "D"},
                ],
                "answer": "C",
                "explanation": "海豚法则引入KD随机指标，在微观时间框架上通过金叉/死叉触发实际的市场进入指令。"
            },
        ],
        'T2': [
            {
                "title": "海豚法则中，KD指标的金叉指什么？",
                "options": [
                    {"label": "%K线自上而下穿越%D线", "value": "A"},
                    {"label": "%K线自下而上穿越%D线", "value": "B"},
                    {"label": "%D线穿越MACD线", "value": "C"},
                    {"label": "%K线穿越零轴", "value": "D"},
                ],
                "answer": "B",
                "explanation": "金叉是快速%K线自下而上穿越慢速%D线，是强烈的看涨执行信号。"
            },
            {
                "title": "海豚法则中，MACD默认参数设置是什么？",
                "options": [
                    {"label": "3, 10, 16", "value": "A"},
                    {"label": "12, 26, 9", "value": "B"},
                    {"label": "15, 35, 5", "value": "C"},
                    {"label": "5, 10, 20", "value": "D"},
                ],
                "answer": "B",
                "explanation": "MACD默认参数为12（快速EMA）、26（慢速EMA）、9（信号线EMA），由杰拉德·阿佩尔开发。"
            },
            {
                "title": "海豚法则中，高频极速动量配置的MACD参数是什么？",
                "options": [
                    {"label": "12, 26, 9", "value": "A"},
                    {"label": "3, 10, 16", "value": "B"},
                    {"label": "15, 35, 5", "value": "C"},
                    {"label": "5, 15, 10", "value": "D"},
                ],
                "answer": "B",
                "explanation": "高频剥头皮使用(3, 10, 16)配置，能快速检测订单流微小转变，适合5分钟或15分钟图表。"
            },
            {
                "title": "海豚法则中，KD指标金叉发生在什么区域最理想？",
                "options": [
                    {"label": "中性区域（40-60）", "value": "A"},
                    {"label": "超卖区域（指标值低于20）", "value": "B"},
                    {"label": "超买区域（指标值高于80）", "value": "C"},
                    {"label": "零轴附近", "value": "D"},
                ],
                "answer": "B",
                "explanation": "对于做多授权，KD金叉发生在超卖区域（低于20）最理想，表明局部回调流动性已被完全消耗。"
            },
            {
                "title": "海豚法则中，第四象限（向下调整）的系统条件是什么？",
                "options": [
                    {"label": "价格>MA26，MACD值>信号线>0", "value": "A"},
                    {"label": "价格>MA26，信号线>MACD值>0", "value": "B"},
                    {"label": "价格<MA26，MACD值<信号线<0", "value": "C"},
                    {"label": "价格<MA26，信号线<MACD值<0", "value": "D"},
                ],
                "answer": "D",
                "explanation": "第四象限：价格<MA26但信号线<MACD值<0，下跌速率放缓，系统授权平仓空头并尝试战术性做多。"
            },
            {
                "title": "海豚法则中，宏观抗噪稳健配置的MACD参数是什么？",
                "options": [
                    {"label": "12, 26, 9", "value": "A"},
                    {"label": "3, 10, 16", "value": "B"},
                    {"label": "15, 35, 5", "value": "C"},
                    {"label": "20, 50, 10", "value": "D"},
                ],
                "answer": "C",
                "explanation": "宏观抗噪配置(15, 35, 5)对突然价格冲击有极强抵抗力，适合日线图至周线图，产生极其保守的交易系统。"
            },
            {
                "title": "海豚法则与海龟法则的核心认识论分歧是什么？",
                "options": [
                    {"label": "海龟看重基本面，海豚只看技术", "value": "A"},
                    {"label": "海龟相信突破本身即是趋势，海豚要求多重指标确认趋势", "value": "B"},
                    {"label": "海豚做短线，海龟做长线", "value": "C"},
                    {"label": "没有分歧，两者完全相同", "value": "D"},
                ],
                "answer": "B",
                "explanation": "海龟系统坚信突破本身就是趋势起点，不寻求确认；海豚法则要求等待移动平均线和动量指标形成方向一致性的数学对齐后才确认趋势。"
            },
            {
                "title": "海豚法则的多时间框架分析（MTFA）中，趋势判断期与主交易期的关系是？",
                "options": [
                    {"label": "同一时间框架", "value": "A"},
                    {"label": "比主交易期高一个数量级", "value": "B"},
                    {"label": "比主交易期低一个数量级", "value": "C"},
                    {"label": "没有关系", "value": "D"},
                ],
                "answer": "B",
                "explanation": "趋势判断期比主交易期高出一个数量级的时间框架，用于确定机构订单流的主导方向性偏见。"
            },
        ],
        'T3': [
            {
                "title": "海豚法则中，RSI作为共振过滤器的作用是什么？",
                "options": [
                    {"label": "计算波动率", "value": "A"},
                    {"label": "量化超买超卖，过滤趋势末端的劣质信号", "value": "B"},
                    {"label": "确定止损点", "value": "C"},
                    {"label": "计算仓位大小", "value": "D"},
                ],
                "answer": "B",
                "explanation": "RSI被限制在0-100固定边界内，能判断资产是否处于过度高估或低估状态，配合MACD过滤掉趋势末端的劣质信号。"
            },
            {
                "title": "海豚法则中，MACD零轴代表什么？",
                "options": [
                    {"label": "价格最高点", "value": "A"},
                    {"label": "12-EMA和26-EMA完全相等的数学中性点", "value": "B"},
                    {"label": "成交量最大值", "value": "C"},
                    {"label": "RSI的50中线", "value": "D"},
                ],
                "answer": "B",
                "explanation": "零轴是12-EMA和26-EMA完全相等的数学中性点，MACD值穿越零轴表明短期动量与长期基准发生方向性转换。"
            },
            {
                "title": "海豚法则在横盘震荡市场中的表现如何？",
                "options": [
                    {"label": "表现极佳，胜率高", "value": "A"},
                    {"label": "表现退化，会反复被来回鞭打", "value": "B"},
                    {"label": "不受影响", "value": "C"},
                    {"label": "只会做多不会做空", "value": "D"},
                ],
                "answer": "B",
                "explanation": "在横盘震荡市场中，MA26被拉平，价格无序穿越，MACD在零轴附近缠绕，系统会快速循环四个象限，产生交替的做多/做空信号。"
            },
            {
                "title": "海豚法则中，KD指标的%D线是什么？",
                "options": [
                    {"label": "收盘价在高低范围的百分比", "value": "A"},
                    {"label": "%K线的3期简单移动平均", "value": "B"},
                    {"label": "MACD的信号线", "value": "C"},
                    {"label": "RSI的平滑线", "value": "D"},
                ],
                "answer": "B",
                "explanation": "%D线是%K线的平滑移动平均线，通常采用3期简单移动平均，作为慢速线。"
            },
            {
                "title": "海豚法则中，MACD的直方图（Histogram）代表什么？",
                "options": [
                    {"label": "成交量", "value": "A"},
                    {"label": "MACD值与信号线之间的距离", "value": "B"},
                    {"label": "价格波动幅度", "value": "C"},
                    {"label": "RSI差值", "value": "D"},
                ],
                "answer": "B",
                "explanation": "MACD直方图可视化MACD值与信号线之间的距离，其扩张和收缩提供了动量正在加速或减速的直接视觉证据。"
            },
            {
                "title": "海豚法则中，与埃尔德射线的互补关系是什么？",
                "options": [
                    {"label": "BBP测量多空力量绝对极值，MACD测量二阶变化率", "value": "A"},
                    {"label": "两者完全相同", "value": "B"},
                    {"label": "BBP替代MACD", "value": "C"},
                    {"label": "没有互补关系", "value": "D"},
                ],
                "answer": "A",
                "explanation": "BBP专注于测量多空力量的绝对极值，而海豚的MACD机制专注于这些力量的二阶变化率，两者可结合使用。"
            },
        ],
        'T4': [
            {
                "title": "海豚法则中，出入场期相对于主交易期的时间框架关系是？",
                "options": [
                    {"label": "同一时间框架", "value": "A"},
                    {"label": "高一个数量级", "value": "B"},
                    {"label": "低一个数量级，用于微观执行优化", "value": "C"},
                    {"label": "没有关系", "value": "D"},
                ],
                "answer": "C",
                "explanation": "出入场期比主交易期低一个数量级，用于微观层面的订单执行，优化入场价格和止损位置。"
            },
            {
                "title": "海豚法则中，MACD交叉发生在远离零轴的深度负值区域意味着什么？",
                "options": [
                    {"label": "高确信度的买入信号", "value": "A"},
                    {"label": "高度投机性且容易夭折的试探性底部", "value": "B"},
                    {"label": "趋势极强", "value": "C"},
                    {"label": "应该加仓", "value": "D"},
                ],
                "answer": "B",
                "explanation": "MACD交叉发生在远离零轴的深度负值区域，这是高度投机性且极易夭折的试探性底部信号。"
            },
            {
                "title": "海豚法则中，MACD交叉刚好发生在零轴附近测试时意味着什么？",
                "options": [
                    {"label": "信号很弱", "value": "A"},
                    {"label": "完美的微观回调结束，具有极高入场价值", "value": "B"},
                    {"label": "应该立即平仓", "value": "C"},
                    {"label": "趋势即将结束", "value": "D"},
                ],
                "answer": "B",
                "explanation": "MACD值从上方回撤并精确测试零轴附近的交叉，通常意味着强劲宏观趋势中的完美微观回调已结束，具有极高入场价值。"
            },
            {
                "title": "海豚法则中，短线波段交易的标准时间框架配置是什么？",
                "options": [
                    {"label": "趋势判断期日线图，主交易期4小时，出入场期1小时", "value": "A"},
                    {"label": "趋势判断期4小时图，主交易期1小时，出入场期15分钟", "value": "B"},
                    {"label": "趋势判断期1小时，主交易期15分钟，出入场期5分钟", "value": "C"},
                    {"label": "趋势判断期周线，主交易期日线，出入场期4小时", "value": "D"},
                ],
                "answer": "B",
                "explanation": "短线波段交易：趋势判断期4小时图，主交易期1小时图，出入场期15分钟图。"
            },
            {
                "title": "海豚法则中，与维克多·斯波朗迪的123法则相比，其优势是什么？",
                "options": [
                    {"label": "能捕捉绝对顶部和底部", "value": "A"},
                    {"label": "绝对客观和数字化，易于编程为自动算法", "value": "B"},
                    {"label": "在震荡市场表现更好", "value": "C"},
                    {"label": "没有滞后性", "value": "D"},
                ],
                "answer": "B",
                "explanation": "海豚系统是绝对客观和数字化的，收盘价格要么在MA26之上要么之下，不存在人类解读的灰色地带，易于转为自动化算法。"
            },
        ],
    }

    count = 0
    for level_id, qs in questions.items():
        for i, q in enumerate(qs):
            qid = f"dolphin_{count + 1}"
            count += 1
            insert_q(cursor, qid, level_id, 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=i+1)
    return count

def gen_valuation_questions(cursor):
    questions = {
        'L1': [
            {
                "title": "贝叶斯收缩因子模型主要用于解决什么问题？",
                "options": [
                    {"label": "股价预测", "value": "A"},
                    {"label": "因子动物园中的过拟合和虚假显著性", "value": "B"},
                    {"label": "成交量分析", "value": "C"},
                    {"label": "技术指标计算", "value": "D"},
                ],
                "answer": "B",
                "explanation": "贝叶斯收缩因子模型通过施加结构化先验，在高维数据中防止过拟合，有效识别哪些Alpha信号是噪声或样本过拟合产生的。"
            },
            {
                "title": "Horseshoe Prior（马蹄先验）的特点是什么？",
                "options": [
                    {"label": "均匀压缩所有系数", "value": "A"},
                    {"label": "强烈压缩近零噪声系数，同时保留强信号", "value": "B"},
                    {"label": "只适用于线性回归", "value": "C"},
                    {"label": "无法处理高维数据", "value": "D"},
                ],
                "answer": "B",
                "explanation": "马蹄先验利用重尾的半Cauchy分布，在零点附近有极高密度（压缩噪声），同时尾部极其肥厚（保留强信号）。"
            },
            {
                "title": "Dickinson现金流分类模型通过什么来推断企业生命周期阶段？",
                "options": [
                    {"label": "企业年龄", "value": "A"},
                    {"label": "经营、投资、筹资现金流的正负符号组合", "value": "B"},
                    {"label": "公司规模", "value": "C"},
                    {"label": "股价高低", "value": "D"},
                ],
                "answer": "B",
                "explanation": "Dickinson模型通过分析OCF、ICF、FCF的正负符号组合，将企业动态划分为导入期、成长期、成熟期、动荡期和衰退期。"
            },
            {
                "title": "企业处于成熟期时，现金流模式通常是？",
                "options": [
                    {"label": "OCF<0, ICF<0, FCF>0", "value": "A"},
                    {"label": "OCF>0, ICF<0, FCF>0", "value": "B"},
                    {"label": "OCF>0, ICF<0, FCF<0", "value": "C"},
                    {"label": "OCF<0, ICF>0, FCF+/-", "value": "D"},
                ],
                "answer": "C",
                "explanation": "成熟期：OCF>0（经营产生正现金流），ICF<0（维护性投资），FCF<0（偿还债务、分红或回购）。"
            },
            {
                "title": "成长期企业的核心估值锚点是什么？",
                "options": [
                    {"label": "P/E（市盈率）", "value": "A"},
                    {"label": "P/S（市销率）和PEG", "value": "B"},
                    {"label": "P/B（市净率）", "value": "C"},
                    {"label": "EV/EBITDA", "value": "D"},
                ],
                "answer": "B",
                "explanation": "成长期企业盈利尚未稳定，收入增速是主要矛盾，适合用P/S和PEG作为估值锚点。"
            },
            {
                "title": "成熟期企业的核心估值锚点是什么？",
                "options": [
                    {"label": "P/S（市销率）", "value": "A"},
                    {"label": "P/FCF（市现率）和FCF Yield", "value": "B"},
                    {"label": "PEG", "value": "C"},
                    {"label": "P/B（市净率）", "value": "D"},
                ],
                "answer": "B",
                "explanation": "成熟期企业现金流产出能力是价值核心，适合用P/FCF和自由现金流收益率作为估值锚点。"
            },
        ],
        'L2': [
            {
                "title": "导入期企业的现金流特征是？",
                "options": [
                    {"label": "OCF>0, ICF>0, FCF>0", "value": "A"},
                    {"label": "OCF<0, ICF<0, FCF>0", "value": "B"},
                    {"label": "OCF>0, ICF<0, FCF<0", "value": "C"},
                    {"label": "OCF<0, ICF>0, FCF<0", "value": "D"},
                ],
                "answer": "B",
                "explanation": "导入期：OCF<0（经营亏损），ICF<0（大量研发和开拓支出），FCF>0（依赖外部融资）。"
            },
            {
                "title": "衰退期企业的现金流特征是？",
                "options": [
                    {"label": "OCF>0, ICF<0, FCF<0", "value": "A"},
                    {"label": "OCF<0, ICF<0, FCF>0", "value": "B"},
                    {"label": "OCF<0, ICF>0, FCF可正可负", "value": "C"},
                    {"label": "OCF>0, ICF<0, FCF>0", "value": "D"},
                ],
                "answer": "C",
                "explanation": "衰退期：OCF<0（盈利枯竭），ICF>0（资产变现回笼资金），FCF可正可负。"
            },
            {
                "title": "个股的系统性风险（Beta）在生命周期中呈现什么轨迹？",
                "options": [
                    {"label": "线性上升", "value": "A"},
                    {"label": "线性下降", "value": "B"},
                    {"label": "U型（导入期和衰退期最高，成熟期最低）", "value": "C"},
                    {"label": "倒U型", "value": "D"},
                ],
                "answer": "C",
                "explanation": "Beta在导入期和衰退期最高，在成熟期最低。导入期面临极高风险和不确定性，成熟期拥有稳健的资源基础。"
            },
            {
                "title": "Bayesian Lasso相比传统OLS的优势是什么？",
                "options": [
                    {"label": "计算速度更快", "value": "A"},
                    {"label": "更好处理多重共线性并提高预测R方", "value": "B"},
                    {"label": "不需要数据", "value": "C"},
                    {"label": "只能用于单变量", "value": "D"},
                ],
                "answer": "B",
                "explanation": "贝叶斯Lasso使用拉普拉斯先验，在处理解释变量间多重共线性方面优于OLS，并提高预测收益率的R方。"
            },
            {
                "title": "Spike-and-Slab先验提供什么功能？",
                "options": [
                    {"label": "连续平滑", "value": "A"},
                    {"label": "硬性剔除无效因子的概率支持", "value": "B"},
                    {"label": "增加因子数量", "value": "C"},
                    {"label": "计算波动率", "value": "D"},
                ],
                "answer": "B",
                "explanation": "Spike-and-Slab通过混合分布明确区分无效因子与显著因子，提供硬性剔除的概率支持。"
            },
            {
                "title": "光伏产业中，N型技术相比P型技术的估值优势是什么？",
                "options": [
                    {"label": "没有优势", "value": "A"},
                    {"label": "生产能力倍数应获得20%-40%的溢价", "value": "B"},
                    {"label": "更便宜", "value": "C"},
                    {"label": "产能更大但效率更低", "value": "D"},
                ],
                "answer": "B",
                "explanation": "拥有高效N型（TOPCon/HJT）产能的龙头企业，其生产能力倍数应获得20%-40%的溢价。"
            },
            {
                "title": "深度估值Agent的一票否决机制中，现金流否决权的触发条件是什么？",
                "options": [
                    {"label": "P/E因子得分很高", "value": "A"},
                    {"label": "Dickinson模式从成长期突然退化至衰退期", "value": "B"},
                    {"label": "股价上涨", "value": "C"},
                    {"label": "成交量放大", "value": "D"},
                ],
                "answer": "B",
                "explanation": "即使P/E得分很高，如果检测到OCF持续转负且ICF异常转正，则该标的将被一票否决，防止落入价值陷阱。"
            },
            {
                "title": "光伏产业的产能出清后，各环节稳态净利率有望恢复至什么水平？",
                "options": [
                    {"label": "1%-2%", "value": "A"},
                    {"label": "5%-7%", "value": "B"},
                    {"label": "15%-20%", "value": "C"},
                    {"label": "30%以上", "value": "D"},
                ],
                "answer": "B",
                "explanation": "产能利用率回归正常后，各环节净利率有望恢复至5%-7%的合理水平。"
            },
        ],
        'L3': [
            {
                "title": "贝叶斯顺序EFDR程序主要用于什么？",
                "options": [
                    {"label": "计算移动平均线", "value": "A"},
                    {"label": "从因子动物园中筛选稳健的定价变量", "value": "B"},
                    {"label": "预测股价", "value": "C"},
                    {"label": "计算成交量", "value": "D"},
                ],
                "answer": "B",
                "explanation": "贝叶斯顺序EFDR通过反向测试逻辑验证异常值是否能被因子集合所覆盖，有效识别虚假显著性。"
            },
            {
                "title": "光伏产业中，ELCC指标衡量什么？",
                "options": [
                    {"label": "公司的总利润", "value": "A"},
                    {"label": "新增光伏系统能替代多少传统化石能源装机", "value": "B"},
                    {"label": "公司的负债率", "value": "C"},
                    {"label": "股票的市盈率", "value": "D"},
                ],
                "answer": "B",
                "explanation": "ELCC（有效载荷能力）衡量在既定可靠性标准下，新增光伏系统能够替代多少传统的化石能源装机。"
            },
            {
                "title": "深度估值Agent中，趋势跟踪滤波器的作用是什么？",
                "options": [
                    {"label": "计算财务指标", "value": "A"},
                    {"label": "作为执行辅助，只有基本面价值回归概率>75%且价格站上均线时才建仓", "value": "B"},
                    {"label": "预测利率", "value": "C"},
                    {"label": "计算税收", "value": "D"},
                ],
                "answer": "B",
                "explanation": "趋势跟踪滤波器作为双重校验：只有基本面价值回归概率>75%且价格站上10个月移动平均线时才触发建仓。"
            },
        ],
        'L4': [
            {
                "title": "深度估值Agent的三大代理子系统是什么？",
                "options": [
                    {"label": "买入、卖出、持有代理", "value": "A"},
                    {"label": "数据代理、推断代理、解释代理", "value": "B"},
                    {"label": "财务、技术、宏观代理", "value": "C"},
                    {"label": "短线、中线、长线代理", "value": "D"},
                ],
                "answer": "B",
                "explanation": "数据代理整合异构信息，推断代理执行贝叶斯算法进行递归更新，解释代理将统计分布转化为叙事化建议。"
            },
            {
                "title": "贝叶斯收缩模型在回测中能拦截多少噪声信号？",
                "options": [
                    {"label": "50%", "value": "A"},
                    {"label": "70%", "value": "B"},
                    {"label": "90%以上", "value": "C"},
                    {"label": "100%", "value": "D"},
                ],
                "answer": "C",
                "explanation": "在66,000次历史回测中，仅不到7%的异常值能持续创造Alpha，贝叶斯收缩模型能成功将90%以上的噪声信号拦截。"
            },
        ],
    }

    count = 0
    for level_id, qs in questions.items():
        for i, q in enumerate(qs):
            qid = f"valuation_{count + 1}"
            count += 1
            insert_q(cursor, qid, level_id, 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=i+1)
    return count

def gen_volatility_questions(cursor):
    questions = {
        'T1': [
            {
                "title": "De Bondt和Thaler提出的过度反应假说认为什么？",
                "options": [
                    {"label": "市场完全有效", "value": "A"},
                    {"label": "投资者倾向于将近期趋势线性外推，导致价格偏离合理区间", "value": "B"},
                    {"label": "价格总是等于内在价值", "value": "C"},
                    {"label": "交易量不影响价格", "value": "D"},
                ],
                "answer": "B",
                "explanation": "过度反应假说认为投资者受制于代表性启发式偏差，将近期趋势线性外推至未来，导致价格超越基本面合理区间。"
            },
            {
                "title": "布林带的中轨通常采用什么？",
                "options": [
                    {"label": "20期简单移动平均（SMA）", "value": "A"},
                    {"label": "50期指数移动平均", "value": "B"},
                    {"label": "10期加权移动平均", "value": "C"},
                    {"label": "100期简单移动平均", "value": "D"},
                ],
                "answer": "A",
                "explanation": "布林带中轨通常采用20期SMA，反映资产的中期基础共识价值。"
            },
            {
                "title": "正态分布下，2倍标准差涵盖约多少数据？",
                "options": [
                    {"label": "68.2%", "value": "A"},
                    {"label": "95.4%", "value": "B"},
                    {"label": "99.7%", "value": "C"},
                    {"label": "50%", "value": "D"},
                ],
                "answer": "B",
                "explanation": "正态分布下，2倍标准差涵盖约95.4%的数据，3倍标准差涵盖99.7%。"
            },
            {
                "title": "布林带2σ上轨被突破意味着什么？",
                "options": [
                    {"label": "价格一定继续上涨", "value": "A"},
                    {"label": "统计上属于不到5%概率的小概率事件", "value": "B"},
                    {"label": "成交量一定放大", "value": "C"},
                    {"label": "趋势一定结束", "value": "D"},
                ],
                "answer": "B",
                "explanation": "价格触及2σ布林带上轨意味着该价格行为在统计上属于发生概率不到5%的小概率事件。"
            },
            {
                "title": "金融资产收益率分布的典型特征是？",
                "options": [
                    {"label": "完美正态分布", "value": "A"},
                    {"label": "尖峰厚尾（Leptokurtic and Fat-tailed）", "value": "B"},
                    {"label": "均匀分布", "value": "C"},
                    {"label": "泊松分布", "value": "D"},
                ],
                "answer": "B",
                "explanation": "金融资产收益率具有显著的尖峰厚尾特征，极端价格变动的真实频率远高于正态分布的理论预期。"
            },
            {
                "title": "为什么单纯在2σ处执行逆势反转策略风险很大？",
                "options": [
                    {"label": "因为价格不会回归均值", "value": "A"},
                    {"label": "因为在强劲动量趋势中价格能长期依附并不断刺穿2σ", "value": "B"},
                    {"label": "因为计算太复杂", "value": "C"},
                    {"label": "因为成交量不够", "value": "D"},
                ],
                "answer": "B",
                "explanation": "在强劲单边动量趋势中，价格能长期Riding the Bands（依附并刺穿2σ），在2σ处盲目反转将面临连续止损。"
            },
        ],
        'T2': [
            {
                "title": "R-Breaker策略由谁开发？",
                "options": [
                    {"label": "理查德·丹尼斯", "value": "A"},
                    {"label": "Richard Saidenberg", "value": "B"},
                    {"label": "乔治·莱恩", "value": "C"},
                    {"label": "琳达·拉施克", "value": "D"},
                ],
                "answer": "B",
                "explanation": "R-Breaker策略由Richard Saidenberg在20世纪90年代初开发，长期统治标普500指数期货市场。"
            },
            {
                "title": "R-Breaker策略中，反转卖出线的触发条件是什么？",
                "options": [
                    {"label": "价格直接突破最高价", "value": "A"},
                    {"label": "价格先触及观察卖出线后调头跌破反转线", "value": "B"},
                    {"label": "成交量放大", "value": "C"},
                    {"label": "MACD金叉", "value": "D"},
                ],
                "answer": "B",
                "explanation": "只有当价格先向上触及观察线耗尽多头动能，随后反身向下跌破反转线时，做空信号才被激活。"
            },
            {
                "title": "海龟汤策略由谁提出？",
                "options": [
                    {"label": "理查德·丹尼斯", "value": "A"},
                    {"label": "Linda Raschke", "value": "B"},
                    {"label": "Richard Saidenberg", "value": "C"},
                    {"label": "亚历山大·埃尔德", "value": "D"},
                ],
                "answer": "B",
                "explanation": "海龟汤策略由华尔街顶尖交易员Linda Raschke提出，是对海龟交易法则的反向收割。"
            },
            {
                "title": "海龟汤策略中，假突破做空的信号是什么？",
                "options": [
                    {"label": "价格突破20日新高后持续上涨", "value": "A"},
                    {"label": "价格突破20日新高但迅速回落至先前区间内", "value": "B"},
                    {"label": "价格跌破20日新低", "value": "C"},
                    {"label": "成交量持续放大", "value": "D"},
                ],
                "answer": "B",
                "explanation": "一旦价格突破20日新高但未能维持，迅速回落至先前区间，就构成强烈的假突破做空信号。"
            },
            {
                "title": "R-Breaker策略中，六条线从上到下第三条是什么？",
                "options": [
                    {"label": "突破买入线", "value": "A"},
                    {"label": "观察卖出线", "value": "B"},
                    {"label": "反转卖出线", "value": "C"},
                    {"label": "反转买入线", "value": "D"},
                ],
                "answer": "C",
                "explanation": "从上到下：突破买入线、观察卖出线、反转卖出线、反转买入线、观察买入线、突破卖出线。"
            },
        ],
        'T3': [
            {
                "title": "量价背离中放量滞涨说明什么？",
                "options": [
                    {"label": "趋势极强", "value": "A"},
                    {"label": "散户海量市价买单遭到机构限价卖单的无情吸收与派发", "value": "B"},
                    {"label": "成交量不足", "value": "C"},
                    {"label": "市场正常波动", "value": "D"},
                ],
                "answer": "B",
                "explanation": "高努力低结果现象表明散户涌入的海量市价买单遭到机构被动限价卖单的无情吸收与派发，是均值回归的高确信度信号。"
            },
            {
                "title": "RSI顶背离是指？",
                "options": [
                    {"label": "价格和RSI同时创新高", "value": "A"},
                    {"label": "价格创新高但RSI未能同步创出新高", "value": "B"},
                    {"label": "RSI创新高但价格不涨", "value": "C"},
                    {"label": "价格和RSI同时创新低", "value": "D"},
                ],
                "answer": "B",
                "explanation": "RSI顶背离指价格创出新高但14周期RSI未能同步创出新高，表明上涨速度与加速度已彻底衰竭。"
            },
            {
                "title": "波动率分位数（IVP）<30%意味着？",
                "options": [
                    {"label": "波动率处于历史极高区域", "value": "A"},
                    {"label": "波动率处于过去一年最低30%，市场处于严重的波动率挤压状态", "value": "B"},
                    {"label": "市场极度恐慌", "value": "C"},
                    {"label": "应该立即做空", "value": "D"},
                ],
                "answer": "B",
                "explanation": "IVP<30%表明波动率处于过去一年中最低的30%象限，市场正处于严重的波动率挤压状态，预示巨大方向性动能正在酝酿。"
            },
            {
                "title": "IVP>80%时，价格突破20日新高大概率是什么？",
                "options": [
                    {"label": "真突破，应该追涨", "value": "A"},
                    {"label": "假突破，情绪的最后一次绝望宣泄", "value": "B"},
                    {"label": "趋势极强", "value": "C"},
                    {"label": "应该持有不动", "value": "D"},
                ],
                "answer": "B",
                "explanation": "在IVP>80%的高波动狂热后期，价格刺穿极值的突破极大概率是情绪的最后一次绝望宣泄，属于典型假突破。"
            },
            {
                "title": "IVP极低时发生的价格突破，应该采取什么策略？",
                "options": [
                    {"label": "均值回归反转策略", "value": "A"},
                    {"label": "趋势跟踪顺势突破策略", "value": "B"},
                    {"label": "做空策略", "value": "C"},
                    {"label": "不操作", "value": "D"},
                ],
                "answer": "B",
                "explanation": "IVP极低时代表深度波动率挤压的终结，是真突破概率极高的情况，应该采用趋势跟踪而非均值回归策略。"
            },
            {
                "title": "波动率反转策略的止损应该设置在哪里？",
                "options": [
                    {"label": "不设止损", "value": "A"},
                    {"label": "极其严苛地设置在当日极值高点上方", "value": "B"},
                    {"label": "设置在中轨下方", "value": "C"},
                    {"label": "设置在5%止损", "value": "D"},
                ],
                "answer": "B",
                "explanation": "止损位必须极其严苛地设置在当日形成的极值高点上方，距离入场位仅毫厘之差，以保障非对称的盈亏比。"
            },
        ],
        'T4': [
            {
                "title": "高阶统计套利反转模型中，四大共振要素是什么？",
                "options": [
                    {"label": "价格、成交量、MACD、RSI", "value": "A"},
                    {"label": "宏观体制、空间极值、流动性清扫、动能衰竭", "value": "B"},
                    {"label": "开盘价、收盘价、最高价、最低价", "value": "C"},
                    {"label": "支撑位、压力位、均线、趋势线", "value": "D"},
                ],
                "answer": "B",
                "explanation": "四大要素：宏观状态门控（IVP极高）、空间极值定位（刺穿3σ和R-Breaker观察线）、流动性清扫（越过20日新高）、内生动能审查（量价背离和RSI衰竭）。"
            },
            {
                "title": "均值收敛退出机制中，常规的高效退出逻辑是什么？",
                "options": [
                    {"label": "持有不动等待新趋势", "value": "A"},
                    {"label": "价格触及布林中轨或RSI回归到中性50水平线附近平仓", "value": "B"},
                    {"label": "等待价格创新低", "value": "C"},
                    {"label": "加仓持有", "value": "D"},
                ],
                "answer": "B",
                "explanation": "当价格触及布林中轨或RSI修复回归到中性50水平线附近时执行平仓，不应贪婪期望均值修复会演变成反向新趋势。"
            },
            {
                "title": "De Bondt和Thaler发现输家组合的均值回归呈现什么特征？",
                "options": [
                    {"label": "对称性", "value": "A"},
                    {"label": "非对称性，输家向上修复跑赢市场的幅度远大于赢家向下修复的幅度", "value": "B"},
                    {"label": "没有回归", "value": "C"},
                    {"label": "回归幅度相同", "value": "D"},
                ],
                "answer": "B",
                "explanation": "均值回归呈现高度非对称性，前期输家向上修复跑赢市场的幅度远大于前期赢家向下修复跑输市场的幅度。"
            },
        ],
    }

    count = 0
    for level_id, qs in questions.items():
        for i, q in enumerate(qs):
            qid = f"vol_{count + 1}"
            count += 1
            insert_q(cursor, qid, level_id, 'text', q['title'], q['options'], q['answer'], q['explanation'], sort_order=i+1)
    return count

if __name__ == "__main__":
    conn = get_db()
    cursor = conn.cursor()

    print("生成海豚交易法题目...")
    dolphin_count = gen_dolphin_questions(cursor)
    print(f"OK 海豚交易法: {dolphin_count} 题")

    print("生成深度估值Agent题目...")
    valuation_count = gen_valuation_questions(cursor)
    print(f"OK 深度估值Agent: {valuation_count} 题")

    print("生成波动率反转题目...")
    vol_count = gen_volatility_questions(cursor)
    print(f"OK 波动率反转: {vol_count} 题")

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM questions")
    total = cursor.fetchone()[0]
    print(f"\nTotal: {total} 题")

    cursor.execute("SELECT level_id, COUNT(*) FROM questions GROUP BY level_id ORDER BY level_id")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} 题")

    conn.close()
