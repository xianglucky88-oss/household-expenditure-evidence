# 家庭支出调查数据

主子方向为数仓与数据湖。调查团队需要把购物日记、合住分摊、自产消费和补充访谈转换成口径一致的家庭消费事实。基础数据可用几个虚构家庭的访谈表和账本，验证价格、时间、户内分摊和样本代表性的处理。

这是可运行的最小数据基线，只实现下表列明的能力。金额使用整数分，样例家庭均为虚构。补访均值不作抽样权重校正。

| 数据链 | 基线能力 | 离线样例 | 可核验结果 |
|---|---|---|---|
| `beneficiary-lines` | 按购物条目的实际受益家庭归属整行金额，不猜未确认的家庭。 | [输入](examples/beneficiary-lines.json) | [结果](tests/expected/beneficiary-lines.json) |
| `reference-period` | 用消费日而非录入日归入调查期间并单列消费日不明的金额。 | [输入](examples/reference-period.json) | [结果](tests/expected/reference-period.json) |
| `home-production` | 按自用单位与明确可比的单位价形成非现金消费估值。 | [输入](examples/home-production.json) | [结果](tests/expected/home-production.json) |
| `bundle-bridge` | 保留组合收费原分类，将有明细支持的金额桥接到新分类。 | [输入](examples/bundle-bridge.json) | [结果](tests/expected/bundle-bridge.json) |
| `followup-coverage` | 对比同一抽样组的完整日记与补访加入后的可用金额和样本数。 | [输入](examples/followup-coverage.json) | [结果](tests/expected/followup-coverage.json) |

## 运行

在仓库根目录使用 Python 3.11 及以上版本，无需安装运行依赖：

```sh
python3 -m household_expenditure_evidence beneficiary-lines examples/beneficiary-lines.json
python3 -m household_expenditure_evidence beneficiary-lines examples/beneficiary-lines.json --sqlite facts.sqlite
python3 -m unittest discover -s tests -v
```

每个输入文件包含 `records` 数组，记录的 `id` 在批内唯一。各数据链校验自己的业务字段，输出按 `fact_id` 标识的事实。起止范围若无另行说明均为左闭右开；日期、深度、金额和持续时间等单位由字段标明。

加上 `--sqlite` 时，`runs` 表保存规范化的来源 JSON 与 SHA-256，`facts` 表保存同一批次的事实。原样重放不新增事实；写入失败回滚整批。既有数据库不会被自动改写为不同版本的处理结果。JSON 接口和入库只是数据处理的运行入口，不是仓库的业务主体。
