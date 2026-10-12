# open-wheel-size

独立维护的车辆轮圈与轮胎参考目录，用于研究、比较和工具开发，明确区分市场、车型年和前后轴。

**DATA RELEASE BLOCKED：当前仅提供工具、结构定义和文档，公开车辆记录为零。**
完整的私有研究 v1 尚未发布。现有来源文件的复制权限标记不能直接决定独立记录事实的再分发权；
目前缺少针对这些结构化事实的公开发布依据评估。详见 [覆盖统计](COVERAGE.md)。

本项目属于 wheel-size 参考目录类别的独立替代项目，与 Wheel-Size.com 及车辆制造商无官方关系，
不是其镜像或 API 兼容克隆。中文别名不代表中国市场配置；名义胎宽不代表实测胎宽。
已知原厂尺寸也不代表改装适配、安全性或制动系统间隙得到确认。

从 Releases 下载并解压后，可完全离线运行（Python 3.9+，无需额外依赖）：

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 examples/query.py
python3 scripts/release.py --output dist
```

层级为平台/代际 → 市场/年份/版本 → 原厂套装 → 前后轴。尺寸使用数值，单位为英寸、毫米或百分比。
未知值为 null，不得改为零；不适用与冲突状态单独保留。配置参考年份不能自动视为车型年。

原创代码、结构定义和文档采用 MIT；权利范围内的数据整理贡献采用 CC BY 4.0。
当前空数据发布不授予第三方文档或未公开车辆记录的权利。详见 [NOTICE.md](NOTICE.md)。
公开发布资格、技术审核、下游应用发布资格和 Garage 支持分别判断；不会自动推广至生产应用。
更正及来源权利问题请使用 issue 模板，不要公开私人信息。完整说明见 [英文 README](README.md)。
