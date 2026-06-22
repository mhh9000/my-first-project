#!/usr/bin/env python3
# score_statement.py 公关声明修辞质量打分工具（适配本次12组全新案例体系）
# 理论依据：亚里士多德 Ethos/Pathos/Logos 三要素 + 伯克三大认同理论
# 适用文本：企业公关稿、明星回应、政府/国际组织官方通报
# 总分100，六大评分维度，输出分项得分+评级+优化建议

导入re

类PR语句评分器：
     str, category: str = "企业"):
        """
        :param text: 待打分公关文稿全文
        :param category: 文稿分类 enterprise/celebrity/government
        """
        self.text = text.strip()
        self.category = category
        self.total_score = 0
        self.score_detail = {}
        self.suggestions = []

    def score_ethos(self):
        “维度1 伦理主体可信度 满分15”
        score = 0
        # 分行业可信度关键词库
        ethos_dict = {
            "企业": ["CEO致歉", 全面整改", 配合监管", 第三方检测", 召回", 公开白皮书"],
            “名人”: [“深刻自省”，暂停商务”，公益反思”，全面整改话术审核"],
            "政府": ["行政命令", 监测数据", 独立调查组", 人道救援", WHO监测报告", IAEA评估"]
        }
        keywords = ethos_dict.get(self.category, ethos_dict["enterprise"])
        对于单词 在关键词中：
            如果单词 在自文本:
                score += 2.5
        分数 = 最小值(分数, 15)
        self.score_detail["Ethos 主体可信度(15分)"] = score
        self.total_score += score
        if score < 8:
            self.suggestions.append("【Ethos不足】缺少权威背书、主动担责、第三方佐证等提升可信度表述")

    def score_pathos(self):
        """维度2 Pathos 受众情感共情 满分15"""
        score = 0
        pathos_words = ["致歉", 悲痛", 恐惧", 焦虑", 理解大家担忧", 体恤", 安抚", 共情", 苦难", 平民诉求"]
        for w in pathos_words:
            if w in self.text:
                score += 2.5
        分数 = 最小值(分数, 15)
        self.score_detail["Pathos 情感共情(15分)"] = score
        self.total_score += score
        if score < 8:
            self.suggestions.append("【Pathos不足】未前置情绪安抚，缺少对受众恐惧、悲痛、焦虑的共情表达")

    def score_logos(self):
        """维度3 Logos 事实逻辑论证 满分10"""
        score = 0
        # 时间/数字/分层条款
        if re.search(r"\d{4}|\d+年|\d+份|\d+项", self.text):
            score += 3
        # 分点论证
        if re.search(r"1\.|2\.|3\.|一、|二、", self.text):
            score += 3
        # 报告/数据/政策依据
        if any(x in self.text for x in ["监测报告", 检测数据", 行政命令", IAEA", WHO", 成本明细", MCAS系统"]):
            score += 4
        score = min(score, 10)
        self.score_detail["Logos 事实逻辑(10分)"] = score
        self.total_score += score
        if score < 6:
            self.suggestions.append("【Logos不足】缺少数据、报告、分点措施，论证单薄片面")

    def score_identification(self):
        """维度4 伯克三大认同策略 满分30"""
        score = 0
        # 同情认同：共同价值、大众诉求
        sympathy = ["共同追求安全", 保护隐私", 平价消费", 反对战争", 公共健康"]
        # 对立认同：统一对抗负面事物
        opposite = ["抵制谣言", 防范AI风险", 杜绝安全缺陷", 反对虚假宣传"]
        # 象征认同：行业/公共核心符号
        symbol = ["安全第一", 隐私守护", 人道主义", 全球公共卫生"]
        if any(w in self.text for w in sympathy):
            score += 10
        if any(w in self.text for w in opposite):
            score += 10
        if any(w in self.text for w in symbol):
            score += 10
        score = min(score, 30)
        self.score_detail["伯克认同策略(30分)"] = score
        self.total_score += score
        if score < 15:
            self.suggestions.append("【认同策略不足】未搭建同情/对立/象征认同，无法和受众达成价值共识")

    def score_compliance(self):
        """维度5 合规舆论风险 满分20，扣分制"""
        base = 20
        risk_words = [
            "与我方无关", 都是误会", 我反正信了", 绝对安全无隐患", 完全不会泄露", 强制管控无缓冲"
        ]
        for risk in risk_words:
            if risk in self.text:
                base -= 7
        base = max(base, 0)
        self.score_detail["合规风险得分(20分)"] = base
        self.total_score += base
        if base < 12:
            self.suggestions.append("【合规风险】存在推诿、绝对化、激化对立话术，易引发二次舆情")

    def score_format(self):
        """维度6 文本规范结构 满分10"""
        score = 0
        if len(self.text) > 120:
            score += 5
        if any(x in self.text for x in ["#", "尊敬的", 各位市民", 各位消费者"]):
            score += 5
        score = min(score, 10)
        self.score_detail["文本结构规范(10分)"] = score
        self.total_score += score
        if score < 5:
            self.suggestions.append("【格式不规范】缺少标题、分层结构，篇幅过短表述简略")

    def full_evaluate(self):
        """执行完整打分并输出报告"""
        self.score_ethos()
        self.score_pathos()
        self.score_logos()
        self.score_identification()
        self.score_compliance()
        self.score_format()

        print("=" * 50)
        print("          公关文稿修辞质量打分报告")
        print("=" * 50)
        for k, v in self.score_detail.items():
            print(f"{k:22} | {v} 分")
        print("-" * 50)
        print(f"【文稿总分】 {self.total_score} / 100")
        print("-" * 50)

        # 评级判定
        if self.total_score >= 80:
            level = "优秀：修辞完整，可直接对外发布"
        elif self.total_score >= 60:
            level = "合格：补充共情、数据或认同话术后发布"
        否则:
            level = "不合格：核心修辞要素缺失，建议全文重写"
        print(f"【综合评级】 {level}")

        # 输出优化建议
        if len(self.suggestions) > 0:
            print("\n【优化修改建议】")
            for tip in self.suggestions:
                print(f"- {tip}")
        else:
            print("\n【优化修改建议】无明显缺陷，文稿达标")
        print("=" * 50)
        return self.total_score


# ---------------------- 测试示例（覆盖三类案例） ----------------------
if __name__ == "__main__":
    # 测试1 企业类：Apple AI隐私正面声明
    test_enterprise = """
# Apple Intelligence 隐私安全官方说明
各位用户：
我们充分理解大家对手机私人数据被AI读取的焦虑，在此完整说明端侧AI隐私架构。
1. 所有用户相册、聊天记录仅在本地设备运算，不会上传用于通用大模型训练；
2. 专有云计算采用全链路加密，第三方无法获取原始数据；
3. 官方发布完整隐私白皮书，逐条标注数据采集边界。
保护用户隐私是苹果长期坚守的核心底线，我们和所有用户一样拒绝无边界数据抓取，共同守护数字安全。
"""
    print("【测试案例1：企业正面文稿 - Apple隐私声明】")
    sc1 = PRStatementScorer(test_enterprise, category="enterprise")
    sc1.full_evaluate()
    print("\n\n")

    # 测试2 明星类：李佳琦眉笔负面回应（缺陷稿）
    测试名人 = """
大家好，这次直播发言只是表达不当，没有别的意思，直播间后续会注意话术。
"""
    print("【测试案例2：明星缺陷文稿 - 李佳琦原始道歉】")
    sc2 = PRStatementScorer(test_celebrity, category="celebrity")
    sc2.full_evaluate()
    print("\n\n")

    # 测试3 政府类：WHO全球卫生通报（正面范本）
    test_government = """
# 世界卫生组织2024年全球流行病风险通报
全球各国民众：
我们深知大家对新型病毒感染的恐慌，现将全年全球采样监测数据完整公开。
1. 已建立7大洲常态化病毒采样站点，按月更新传播风险等级；
2. 配套分层次居家、医疗机构防护指南，降低大众感染概率；
我们与全世界共同对抗传染病隐患，守护全球公共卫生安全是本组织核心使命。
"""
    print("【测试案例3：政府正面文稿 - WHO卫生通报】")
    sc3 = PRStatementScorer(test_government, category="government")
