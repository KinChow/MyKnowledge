---
archive_policy: text-only
attachments:
- filename: web-computer-science-class-and-structure.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:5c6af998ee0a76d6da7baa2f641a0fed6d91bae9e6dff38b1d6fc291da9a475f
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-fb2b18d5f22e
  position:
    end: 110
    start: 46
    type: TextPositionSelector
  quote_sha256: sha256:333f97fc05e2ebd4d172d6db8dbc26499d611221c34b9e11d7b80e65d9591eba
  selector:
    exact: 当位于类成员列表前面时，public 关键字指定这些成员可从任何函数访问。 这适用于声明到下一个访问指示符或类的末尾的所有成员。
    prefix: '[member-list]

      public base-class

      '
    suffix: '

      当位于基类名称前面时，public 关键字指定基类的公共和受保'
    type: TextQuoteSelector
  selector_sha256: sha256:59f6db3796aff18f8edb10a5b5626ad62155cd49260c93b8273993c45e5033d1
  snapshot_sha256: sha256:b9adeaf81ecdc9862dd46b52a9e72e6ddbcd73e74ca9593de8bd40dfa90b6f96
- evidence_id: evidence-8c85a56b407c
  position:
    end: 163
    start: 111
    type: TextPositionSelector
  quote_sha256: sha256:29c56dd5292343706e215913032b95a2346629c52e3e9ae9adb9c12c64c372eb
  selector:
    exact: 当位于基类名称前面时，public 关键字指定基类的公共和受保护成员分别是派生类的公共成员和受保护成员。
    prefix: '数访问。 这适用于声明到下一个访问指示符或类的末尾的所有成员。

      '
    suffix: '

      类中成员的默认访问是私有的。 结构或联合中成员的默认访问是公共'
    type: TextQuoteSelector
  selector_sha256: sha256:42a1e44c3b62ff1806b41924f187bb0e35edd1848cc332fa346dd74d12327265
  snapshot_sha256: sha256:b9adeaf81ecdc9862dd46b52a9e72e6ddbcd73e74ca9593de8bd40dfa90b6f96
- evidence_id: evidence-5cd118805b9e
  position:
    end: 197
    start: 164
    type: TextPositionSelector
  quote_sha256: sha256:b4d6ab8fca6eba3f8873e2c6ebf4493fa9d70d598634490a5a455f58e31f334e
  selector:
    exact: 类中成员的默认访问是私有的。 结构或联合中成员的默认访问是公共的。
    prefix: '指定基类的公共和受保护成员分别是派生类的公共成员和受保护成员。

      '
    suffix: '

      基类的默认访问对于类是私有的，而对于结构是公共的。 联合不能具'
    type: TextQuoteSelector
  selector_sha256: sha256:6a24740d39c44d4690028be33fe03323d3e470497889377fc6395353ba42e4bf
  snapshot_sha256: sha256:b9adeaf81ecdc9862dd46b52a9e72e6ddbcd73e74ca9593de8bd40dfa90b6f96
- evidence_id: evidence-776668d876d8
  position:
    end: 233
    start: 198
    type: TextPositionSelector
  quote_sha256: sha256:996090b970748390fd2e8b1fbf091339eada516d88e769e112b6f046542c8497
  selector:
    exact: 基类的默认访问对于类是私有的，而对于结构是公共的。 联合不能具有基类。
    prefix: '成员的默认访问是私有的。 结构或联合中成员的默认访问是公共的。

      '
    suffix: '

      有关详细信息，请参阅 private、protected、fr'
    type: TextQuoteSelector
  selector_sha256: sha256:2ca5c9e9aaaf814e5081ea5328d2284fd6137a9cd943de661abf42f92881bc62
  snapshot_sha256: sha256:b9adeaf81ecdc9862dd46b52a9e72e6ddbcd73e74ca9593de8bd40dfa90b6f96
extractor: trafilatura/2.2.0
id: web-computer-science-class-and-structure
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/5c6af998ee0a76d6da7baa2f641a0fed6d91bae9e6dff38b1d6fc291da9a475f.html
  sha256: sha256:5c6af998ee0a76d6da7baa2f641a0fed6d91bae9e6dff38b1d6fc291da9a475f
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://learn.microsoft.com/zh-cn/cpp/cpp/public-cpp?view=msvc-170
  url: https://learn.microsoft.com/zh-cn/cpp/cpp/public-cpp?view=msvc-170
schema_version: source/v1
snapshot_sha256: sha256:b9adeaf81ecdc9862dd46b52a9e72e6ddbcd73e74ca9593de8bd40dfa90b6f96
source_type: doc
vault_id: public
---
语法
public:
   [member-list]
public base-class
当位于类成员列表前面时，public 关键字指定这些成员可从任何函数访问。 这适用于声明到下一个访问指示符或类的末尾的所有成员。
当位于基类名称前面时，public 关键字指定基类的公共和受保护成员分别是派生类的公共成员和受保护成员。
类中成员的默认访问是私有的。 结构或联合中成员的默认访问是公共的。
基类的默认访问对于类是私有的，而对于结构是公共的。 联合不能具有基类。
有关详细信息，请参阅 private、protected、friend 以及控制对类成员的访问中的成员访问表。
/clr 专用
在 CLR 类型中，C++ 访问说明符关键字（public、private 和 protected）可能影响与程序集相关的类型和方法的可见性。 有关详细信息，请参阅成员访问控制。
注意
使用 /LN 编译的文件不受此行为的影响。 在这种情况下，所有托管类（公共或私有）都将可见。
 
END /clr 专用
示例
// keyword_public.cpp
class BaseClass {
public:
   int pubFunc() { return 0; }
};
class DerivedClass : public BaseClass {};
int main() {
   BaseClass aBase;
   DerivedClass aDerived;
   aBase.pubFunc();       // pubFunc() is accessible
                          //    from any function
   aDerived.pubFunc();    // pubFunc() is still public in
                          //    derived class
}
另请参阅
              控制对类成员的访问
              关键字