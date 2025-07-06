# 图书馆管理系统建模例子

## 需求分析

* 借阅者的基本业务功能
  * 支持查询、借阅、续借、预约/撤销、归还图书
  * 支持查询历史借阅记录，缴纳罚款
  * 不同类型的借阅者（如：老师、学生）一次借阅的书本数量和最大借阅时长限制可以不同
* 图书管理员的基本业务功能
  * 支持图书出借、图书归还、图书预约的处理
  * 支持收取罚款
* 系统管理员的基本业务功能
  * 支持添加、删除、修改图书信息
  * 支持添加、删除、修改借阅者信息
* 身份认证系统
  * 系统管理员和图书管理员需要进行身份认证才能操作
  * 借阅者除查询图书信息无需登录认证以外，其他操作需要登录认证才能操作



## 建立模型

从系统的不同视角对图书管理系统进行软件建模：

1. 从交互视角（对应UML4+1视图中的用例视图）建立用例模型（用例图）。
2. 从结构化视角（对应UML4+1视图中的逻辑视图）建立静态模型（类图）。
3. 从行为视角（对应UML4+1视图中的行为视图）建立动态模型（序列图、活动图、状态图）。



### 用例图

在图书管理系统中，参与者有借阅者、图书管理员和系统管理员。

#### 借阅者

![use case diagram 1](example.assets/use-case-diagram1.png)

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
actor 借阅者 as Borrower
actor 教师 as Teacher
actor 学生 as Student

Teacher --|> Borrower
Student --|> Borrower

(登录系统) as (UC1)
(查询图书) as (UC2)
(借阅图书) as (UC3)
(归还图书) as (UC4)
(预约图书) as (UC5)
(缴纳罚款) as (UC6)

Borrower --> (UC1)
Borrower --> (UC2)
Borrower --> (UC3)
Borrower --> (UC4)
Borrower --> (UC5)
(UC3) -up.> (UC2) : include
(UC4) -up.> (UC2) : include
(UC5) -down.> (UC2) : include
(UC4) <. (UC6) : extend

@enduml
```



#### 图书管理员

![use case diagram 2](example.assets/use-case-diagram2.png)

```plantuml
@startuml
actor 图书管理员 as Admin

(把图书从系统借出) as (UC1)
(把图书归还到系统) as (UC2)
(查询图书借阅信息) as (UC3)
(检查借阅者账户) as (UC4)
(预约图书) as (UC5)
(收取罚款) as (UC6)
(记录图书借出日志) as (UC7)
(记录图书归还日志) as (UC8)

Admin -right--> (UC1)
Admin -left--> (UC2)
Admin -down--> (UC3)
Admin -up--> (UC5)
(UC1) -down.> (UC4) : include
(UC1) -down.> (UC7) : include
(UC2) -down.> (UC8) : include
(UC3) -right.> (UC7) : include
(UC3) -down.> (UC8) : include

(UC1) <. (UC5) : extend
(UC2) <. (UC6) : extend

@enduml
```



### 类图

```mermaid
classDiagram
	class Borrower {
		+int userID
		+string userName
		+string email
		+int maxNumAllowed
		+BorrowedInfo record
		+Reservation reservedBook
		+setMaxNum() void
		+findBook(string) void
		+borrowBook(string) void
		+returnBook(string) void
		+reserveBook(string) void
	}
    class Teacher {
		+int teacherID
		+setMaxNum() void
	}
	class Student {
		+int studentID
		+setMaxNum() void
	}
	class BorrowerInterface {
		<<interface>>
		+borrowBook(string) void
		+returnBook(string) void
		+reserveBook(string) void
	}
	class BorrowedInfo {
	 	+list~Loan~ borrowedBook
	}
	class Loan {
		+int borrowedID
		+Date borrowDate
		+float needPayMoney
		+Item item
		+payMoney() void
		+destory() void
	}
	class Item {
		+int id
		+string barCode
		+destory() void
	}
	class Reservation {
		+int borrowerID
		+Date reserveDate
		+string reserveBookName
		+destory() void
	}
	class Title {
		+string barCode
		+string bookName
		+string bookAuthor
		+int totalNumber
		+int reserveNumber
		+int borrowNumber
		+int allowedNumber
		+create() Item
		+reserved() Item
	}
	Borrower ..|> BorrowerInterface
	Teacher --|> Borrower
	Student --|> Borrower
	Borrower ..> Title
	Borrower --> Reservation
	Borrower --> BorrowedInfo
	BorrowedInfo "1" o-- "0..n" Loan
	Loan "1" *-- Item
```



### 序列图



### 活动图



### 状态图