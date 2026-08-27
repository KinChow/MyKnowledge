---
archive_policy: text-only
confidentiality: public
domain: computer-science
extractor: utf8/1
id: random
local:
  file_sha256: sha256:4ea26b575bdeaea4a04fcc46bd3e7cb968069eb87495ec271344eb66337156b9
  path_ref: local-sidecar:public/random
media_type: text/markdown
origin: external
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:4ea26b575bdeaea4a04fcc46bd3e7cb968069eb87495ec271344eb66337156b9
source_type: local-file
vault_id: public
---
# 随机数

## 随机数的生成

使用当前时间作为随机数生成器的种子，这样可以保证每次运行程序时都会生成不同的随机数序列。
然后定义了一个 `std::uniform_int_distribution` 对象，用于生成1到100之间的随机数，然后使用 `distribution(generator)` 方法来生成随机数。



```c++
#include <iostream>
#include <random>
#include <chrono>

int main()
{
	// 使用当前时间作为种子
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::mt19937 generator(seed);
    std::uniform_int_distribution<int> distribution(1, 100);  // 生成1到100之间的随机整数
    // 生成10个随机数
    for (int i = 0; i < 10; i++) {
        int random_number = distribution(generator);
    	std::cout << random number << " ";
    }
    return 0;   
}
```



