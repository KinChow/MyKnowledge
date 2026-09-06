---
archive_policy: text-only
attachments:
- filename: web-computer-science-use-case-diagram.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:dbd6cb5062092d6c51df7a97023a5c394fb561bcd24771b0e016e82d7841f29e
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-e446160d9a06
  position:
    end: 226
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:fe005f3b52795844f887ac25ae514fb1aece4d1ad06ce5f27830a72ba440632d
  selector:
    exact: "New! Render PlantUML diagrams directly inside GitHub\n        with our
      official browser extension —\n        No server. No tokens. No tracking. Zero
      permissions but clipboard. —\n        Try it out and let us know what you think!"
    prefix: ''
    suffix: "\n    \n    \n用例图\n- 文本输入，图形输出。 用几行代"
    type: TextQuoteSelector
  selector_sha256: sha256:acd85497d87faafb015dc9eb50793862765d8b9a1f00778bf5c3a631812f9da9
  snapshot_sha256: sha256:5d4caaee9ff531777b6b95a971e9d43f687eb63ff46bba978e3779bfc6df8738
extractor: trafilatura/2.2.0
id: web-computer-science-use-case-diagram
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/dbd6cb5062092d6c51df7a97023a5c394fb561bcd24771b0e016e82d7841f29e.html
  sha256: sha256:dbd6cb5062092d6c51df7a97023a5c394fb561bcd24771b0e016e82d7841f29e
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://plantuml.com/zh/use-case-diagram
  url: https://plantuml.com/zh/use-case-diagram
schema_version: source/v1
snapshot_sha256: sha256:5d4caaee9ff531777b6b95a971e9d43f687eb63ff46bba978e3779bfc6df8738
source_type: doc
vault_id: public
---
New! Render PlantUML diagrams directly inside GitHub
        with our official browser extension —
        No server. No tokens. No tracking. Zero permissions but clipboard. —
        Try it out and let us know what you think!
    
    
用例图
- 文本输入，图形输出。 用几行代码定义参与者、用例和关系。
- 易于重构。 重命名一个参与者或移动一个用例，只需修改一行文本。
- 融入您的代码仓库。 图与所记录的代码并排存放，纳入版本管理。
用例
用例是用小括号括起来的（因为两个 小括号看起来像一个椭圆）。usecase 关键字来定义一个
用例。
你可以用as 关键字来定义一个别名。
这个别名将在以后定义关系时使用。
角色
actor 关键字来定义一个行为体。
一个别名可以使用as 关键字来指定，并且可以在以后代替行为体的名称，例如在定义关系时使用。
改变角色的样式
- 用户头像样式：skinparam actorStyle awesome
- 透明人样式：skinparam actorStyle hollow
火柴人 默认
用户头像
透明人
用例描述
- -- （横线）
- .. （虚线）
- == （双横线）
- __ （下划线）
WARNING
 This translation need to be updated. 
WARNING
使用包
rectangle来改变包的外观。
基础示例
-->连接角色和用例。
-越多，箭头越长。
通过在箭头定义的后面加一个冒号及文字的方式来添加标签。
User并没有定义，而是直接拿来当做一个角色使用。
继承
<|--符号表示。
使用注释
note left of , note right of ,
note top of , note bottom of等关键字给一个对象添加注释。
note关键字来定义，然后用..连接其他对象。
构造类型
<<
 和 >> 来定义角色或者用例的构造类型。
改变箭头方向
-- ，并且是垂直方向的。
可以通过像这样放一个破折号（或点）来使用水平链接。
left,right,up
或down 关键字来改变箭头方向。
-d- ，而不是
-down- ）
或两个第一个字符(-do-)。
Graphviz通常在没有
调整的情况下给出良好的结果。
left to right direction参数。
分割图示
newpage关键字将图示分解为多个页面。
从左向右方向
left to right direction命令改变图示方向。
显示参数
skinparam改变字体和颜色。
WARNING
 This translation need to be updated. 
WARNING
完整样例
业务用例
/ 来制作业务用例。
业务用例
商业行为者
改变箭头的颜色和样式（内联样式）
颜色或样式。
- #color;line.[bold|dashed|dotted];text:color
改变元素的颜色和样式（内联样式）
颜色或样式。
- #[color|back:color];line:color;line.[bold|dashed|dotted];text:color