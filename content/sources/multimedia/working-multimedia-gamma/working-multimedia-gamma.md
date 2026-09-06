---
archive_policy: text-only
confidentiality: public
domain: multimedia
evidence_items:
- evidence_id: evidence-568bb0bf2131
  position:
    end: 62
    start: 47
    type: TextPositionSelector
  quote_sha256: sha256:d242905aa489aaf05cf274535684dfbfe0c1f3ed6ee87da50340cd56b7981a1a
  selector:
    exact: 输入亮度与输出亮度的非线性变换
    prefix: 'Gamma


      Gamma：一种数学变换。


      Gamma矫正：


      '
    suffix: '，一般写作：

      $$

      L_{out} = L_{in}^{1/\g'
    type: TextQuoteSelector
  selector_sha256: sha256:005f0c7928ad643a8200ee6ff245d5f20fed3bf4f17eb91a3efbe672cd941079
  snapshot_sha256: sha256:2066e10c0dc51753812aaab9bbfad47285485c3c90a0c6d177deae7ba66f0b05
extractor: personal-note/1
id: working-multimedia-gamma
media_type: text/markdown
origin: personal
read_status: retrieved
retrieval:
  acquisition: personal-note
schema_version: source/v1
snapshot_sha256: sha256:2066e10c0dc51753812aaab9bbfad47285485c3c90a0c6d177deae7ba66f0b05
source_type: personal-note
vault_id: public
---
# gamma

## 什么是Gamma

Gamma：一种数学变换。

Gamma矫正：

输入亮度与输出亮度的非线性变换，一般写作：
$$
L_{out} = L_{in}^{1/\gamma}
$$
或显示侧 $V_{out} = V_{in}^{\gamma}$（编码/解码的 gamma 互为倒数）。常见的 gamma 值：sRGB 编码约 1/2.2（解码 2.2），BT.709 编码约 0.45（解码 2.4 近似）。

## Gamma与人的视觉非线性

韦伯理论（韦伯-费希纳定律）：

即感觉的差别阈限随原来刺激量的变化而变化，而且表现为一定的规律性——人眼对亮度的感知近似对数/幂函数：暗部对亮度差异更敏感，亮部差异不易察觉。因此把更多编码比特分配给暗部（而非线性平均分配），可以在有限位深下让人眼感知的量化误差更均匀，这就是 gamma 编码的生理基础。

### Gamma与系统

存储、传输、显示图像的带宽有限。

通过Gamma矫正，将更多的存储分配给暗区，配合人眼的非线性。

Gamma的效果由Encoding及Display共同决定。

- **编码侧（Encoding）**：相机/内容侧对线性场景光做幂次压缩（如 1/2.2），把暗部细节用更多码值保存，减少暗部量化带（banding）。
- **传输/存储**：在 8bit/10bit 有限位深下，gamma 编码使暗部量化更密、亮部更疏，匹配人眼灵敏度。
- **显示侧（Display）**：显示器按解码 gamma（约 2.2）展开，恢复近似线性亮度。
- **端到端**：编码与解码 gamma 需匹配（系统 gamma 近似 1），否则画面偏亮/偏暗或对比度异常；ICC/色彩管理正是为了协调各环节 gamma 与色域。

## 参考
- Gamma 校正与人眼视觉：https://en.wikipedia.org/wiki/Gamma_correction
- 韦伯定律：https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law
- sRGB 传输函数：https://en.wikipedia.org/wiki/SRGB
