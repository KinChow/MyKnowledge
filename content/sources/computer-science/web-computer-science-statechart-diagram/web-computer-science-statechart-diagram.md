---
archive_policy: text-only
attachments:
- filename: web-computer-science-statechart-diagram.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:2e94cb4a9eb461c42eed508d6685f1a4e05c844a19b0d39bb6bde71d09dc400a
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-40b9db19760a
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
    suffix: "\n    \n    \n状态图\n- 基于文本的语言：快速定义并可视"
    type: TextQuoteSelector
  selector_sha256: sha256:539d52de8458db18451ea52890222da25e915e1e5754615bbd25610972e40882
  snapshot_sha256: sha256:695e9056ac81b30b507133d0a6a3b4254a5303d7ce8f1a0c5cb7b22b61bbf19a
extractor: trafilatura/2.2.0
id: web-computer-science-statechart-diagram
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/2e94cb4a9eb461c42eed508d6685f1a4e05c844a19b0d39bb6bde71d09dc400a.html
  sha256: sha256:2e94cb4a9eb461c42eed508d6685f1a4e05c844a19b0d39bb6bde71d09dc400a
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://plantuml.com/zh/state-diagram
  url: https://plantuml.com/zh/state-diagram
schema_version: source/v1
snapshot_sha256: sha256:695e9056ac81b30b507133d0a6a3b4254a5303d7ce8f1a0c5cb7b22b61bbf19a
source_type: doc
vault_id: public
---
New! Render PlantUML diagrams directly inside GitHub
        with our official browser extension —
        No server. No tokens. No tracking. Zero permissions but clipboard. —
        Try it out and let us know what you think!
    
    
状态图
- 基于文本的语言：快速定义并可视化状态和转换，无需手动绘图的麻烦。
- 效率与一致性：确保流线型的图表创建和简单的版本控制。
- 多功能性：与各种文档平台集成，并支持多种输出格式。
- 开源和社区支持：由一个强大的社区支持，该社区不断为其改进作出贡献，并提供无价的资源。
普通状态
使用([*])绘制状态图的起点或终点。
-->添加箭头。
简化状态
hide empty description 关键字，渲染一个简单的状态。
复杂状态
state和花括号来定义复杂状态。
内部子状态
子状态间的连接
WARNING
 This translation need to be updated. 
WARNING
长状态名
state来给状态描述较长的状态名，并定义其指代名。
历史状态 [[H], [H*]]
[H] 来表示历史状态， [H*] 表示深层历史状态. 
分支状态 [fork, join]
<<fork>> 和 <<join>> 来表示状态的分叉及合并。
并发状态 [--, ||]
-- or ||作为分隔符来合成并发状态。
水平分隔 --
竖直分隔 ||
WARNING
 This translation need to be updated. 
WARNING
选择结点 [choice]
<<choice>>可以用来表示一个选择结点，表示状态条件。
一个使用版型的完整样例 [start, choice, fork, join, end]
WARNING
 This translation need to be updated. 
WARNING
入口和出口 [entryPoint, exitPoint]
入口结点<<entryPoint>>和出口结点 <<exitPoint>>。
WARNING
 This translation need to be updated. 
WARNING
引脚 [inputPin, outputPin]
引脚结点<<inputPin>>和 <<outputPin>>。
WARNING
 This translation need to be updated. 
WARNING
扩展 [expansionInput, expansionOutput]
扩展结点<<expansionInput>>和 <<expansionOutput>>。
WARNING
 This translation need to be updated. 
WARNING
箭头方向
->定义水平箭头，也可以使用下列格式强制设置箭头方向：
- -down-> (default arrow)
- -right-> or->
- -left->
- -up->
-d-，-down-和-do-是完全等价的)。
Graphviz不喜欢这样。
更改箭头线条的颜色和风格
颜色及风格.
WARNING
 This translation need to be updated. 
WARNING
Change head or tail of arrow line
注释
note left of, note right of, note top of, note bottom of
关键字来定义注释。
WARNING
 This translation need to be updated. 
WARNING
在箭头上添加注释
note on link 关键字来添加注释.
给复杂状态添加注释
颜色
显示参数
skinparam改变字体和颜色。
状态图所有显示参数测试
WARNING
 This translation need to be updated. 
WARNING
Changing style
style.
Change state color and style (inline style)
color or style of individual state using the following notation:
- #color ##[style]color
#color), then line style and line color (##[style]color ).
- #color;line:color;line.[bold|dashed|dotted];text:color
FIXME
 🚩
text:color seems not to be taken into account 
FIXME
别名
alias ，比如。
Display JSON Data on State diagram
Simple example
State description
Style for Nested State Body
Mainframe and frame
Mainframe
You can use global mainframe:
Frame
Or simply local frame:
Specific SkinParameter
By default
Edge Label Style
skinparam  stateDiagramEdgeLabelStyle node to put label on the middle of the arrow, and create a pseudo node.
Mix label defintion
-[node]-> form.