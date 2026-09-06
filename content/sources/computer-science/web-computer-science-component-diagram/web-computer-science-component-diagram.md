---
archive_policy: text-only
attachments:
- filename: web-computer-science-component-diagram.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:da656228103edc7c5d65438940faf9e149de9b61e58f87f6be64d4737914a14a
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-6f35d0c7a293
  position:
    end: 278
    start: 246
    type: TextPositionSelector
  quote_sha256: sha256:99164e16aa1d740170ba6adc6d29ddd37bf11ab6dcb39720e2082c98d742cb0e
  selector:
    exact: 使用 PlantUML，您可以使用简单直观的文本描述来创建组件图
    prefix: "t you think!\n    \n    \n组件图\n- 简单："
    suffix: '，无需使用复杂的绘图工具。

      - 集成：PlantUML 可* 与'
    type: TextQuoteSelector
  selector_sha256: sha256:0954e7afb74cf58a107bce8f4ee881ebe6968ae31bc8d3a6db5bdf3af11a2073
  snapshot_sha256: sha256:d2fb54f5bf689d8e5e8531c7189a4bccc287510e81983e2a23222d3bf171e7c9
- evidence_id: evidence-0d168b7dd5c5
  position:
    end: 423
    start: 395
    type: TextPositionSelector
  quote_sha256: sha256:f63763bbc4b2a5b9c74c09b0ffaca79cf3f8930c50f95d19c26b67bb00637401
  selector:
    exact: 组件必须用中括号括起来。component定义一个组件。
    prefix: '讨论、分享和寻求图表帮助的平台，从而培养了一个协作社区。

      组件

      '
    suffix: '

      并且可以用关键字as给组件定义一个别名。

      这个别名可以在稍后定'
    type: TextQuoteSelector
  selector_sha256: sha256:3f7f80c1366a303b84470d917cc6d24112fe5705e6483b99d3ce021cf5905345
  snapshot_sha256: sha256:d2fb54f5bf689d8e5e8531c7189a4bccc287510e81983e2a23222d3bf171e7c9
- evidence_id: evidence-b66f23103eae
  position:
    end: 464
    start: 424
    type: TextPositionSelector
  quote_sha256: sha256:f7ef5e57de46d2ae236f520310c19bb62dc24f45ba32d29d012119ceeed45e79
  selector:
    exact: '并且可以用关键字as给组件定义一个别名。

      这个别名可以在稍后定义关系的时候使用。'
    prefix: '组件

      组件必须用中括号括起来。component定义一个组件。

      '
    suffix: '

      命名例外

      注意，以$ 开头的组件名以后不能隐藏或删除，因为hi'
    type: TextQuoteSelector
  selector_sha256: sha256:3b8c054672af985bc1244c4b700680bf256ae7a41efb76ff95196d0eb6eaf163
  snapshot_sha256: sha256:d2fb54f5bf689d8e5e8531c7189a4bccc287510e81983e2a23222d3bf171e7c9
- evidence_id: evidence-3c6199ce1cd9
  position:
    end: 610
    start: 572
    type: TextPositionSelector
  quote_sha256: sha256:abcf7667067e362a0f28b1ce4531e391ef8bceac9b2115b42ab28fce5b20a878
  selector:
    exact: 'interface关键字来定义接口。

      并且还可以使用关键字as定义一个别名。'
    prefix: '其添加别名或标记。

      接口

      ()来定义(因为这个看起来像个圆)。

      '
    suffix: '

      这个别名可以在稍后定义关系的时候使用。

      基础示例

      ..)、直线'
    type: TextQuoteSelector
  selector_sha256: sha256:e2d55236ca1a664f5f135e7f784f4031f1587058a76fc6f86b50ac19c2cb5789
  snapshot_sha256: sha256:d2fb54f5bf689d8e5e8531c7189a4bccc287510e81983e2a23222d3bf171e7c9
extractor: trafilatura/2.2.0
id: web-computer-science-component-diagram
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/da656228103edc7c5d65438940faf9e149de9b61e58f87f6be64d4737914a14a.html
  sha256: sha256:da656228103edc7c5d65438940faf9e149de9b61e58f87f6be64d4737914a14a
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://plantuml.com/zh/component-diagram
  url: https://plantuml.com/zh/component-diagram
schema_version: source/v1
snapshot_sha256: sha256:d2fb54f5bf689d8e5e8531c7189a4bccc287510e81983e2a23222d3bf171e7c9
source_type: doc
vault_id: public
---
New! Render PlantUML diagrams directly inside GitHub
        with our official browser extension —
        No server. No tokens. No tracking. Zero permissions but clipboard. —
        Try it out and let us know what you think!
    
    
组件图
- 简单：使用 PlantUML，您可以使用简单直观的文本描述来创建组件图，无需使用复杂的绘图工具。
- 集成：PlantUML 可* 与各种工具和平台无缝集成，是开发人员和建筑师的多功能选择。
- 协作：PlantUML 论坛为用户提供了一个讨论、分享和寻求图表帮助的平台，从而培养了一个协作社区。
组件
组件必须用中括号括起来。component定义一个组件。
并且可以用关键字as给组件定义一个别名。
这个别名可以在稍后定义关系的时候使用。
命名例外
注意，以$ 开头的组件名以后不能隐藏或删除，因为hide 和remove 命令会将该名称视为$tag ，而不是组件名。要删除此类组件，必须为其添加别名或标记。
接口
()来定义(因为这个看起来像个圆)。
interface关键字来定义接口。
并且还可以使用关键字as定义一个别名。
这个别名可以在稍后定义关系的时候使用。
基础示例
..)、直线(--)、箭头(-->)的组合进行连接。
使用注释
note left of , note right of ,
note top of , note bottom of
等关键字定义相对于对象位置的注释。
note单独定义注释，然后使用虚线(..)将其连接到其他对象。
WARNING
 This translation need to be updated. 
WARNING
组合组件
- package
- node
- folder
- frame
- cloud
- database
改变箭头方向
--连接，并且连接是竖直的。不过可以使用一个横线或者点设置水平方向的连接，就行这样：
left, right, up
or down改变箭头方向。
-d-, -do-, -down-都是等价的)。
Graphviz(PlantUML的后端引擎)不喜欢这个样子。
使用 UML2 标记
(from v1.2020.13-14), UML2 notation is used.
使用UML1标记符
skinparam componentStyle uml1 可以切换到UML1标记符。
使用矩形符号（去除 UML 符号）
skinparam componentStyle rectangle 命令用来切换到矩形符号 (没有任何 UML 符号).
长描述
可以用方括号"[ ]"在多行添加描述。
不同的颜色表示
在定型组件中使用精灵图
你可以在定型组件中使用精灵图（sprite）。
显示参数
skinparam命令来改变绘图的字体和颜色。
特定皮肤参数
组件样式
- 默认情况下（或使用skinparam componentStyle uml2 ），组件有一个图标。
- 如果您想取消它，只使用矩形图标，可以使用skinparam componentStyle rectangle
隐藏或删除未链接的组件
- hide @unlinked 组件：
- 或remove @unlinked 组件：
隐藏、删除或恢复被标记的组件或通配符
$tags (使用 $ 符号) , 然后单独或者按照标记删除、隐藏或者还原组件.
- hide $tag13 以隐藏组件组件:
- 或者 remove $tag13 以移除组件:
- 或者 remove $tag13 and restore $tag1 以移除一个标记下的组件并还原另一个标记下的组件:
- 或者 remove * and restore $tag1 以移除全部组件并且还原一个被标记的组件:
在组件图上显示JSON数据
简单的例子
端口 [port, portIn, portOut]
port,portin和portout 关键词添加端口。