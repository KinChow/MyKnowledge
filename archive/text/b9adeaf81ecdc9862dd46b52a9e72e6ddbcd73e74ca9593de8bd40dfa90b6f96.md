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