<｜begin▁of▁sentence｜>###### tags: `hexschool` `javascript`
# Javascript 核心篇

## 純值、物件型別
https://courses.hexschool.com/courses/202049/lectures/3080860
### 純值 (primitive)
* string
* number
* boolean
* undefined
* null
* Symbol(ES6)
### 物件 (object)
* array
* object
* function
* Date

### 練習1
#### 答案：
```
1.string
2.number
3.object(是陣列)
4.number
5.object
6.object
7.boolean
```
#### 解惑：
`typeof null` 會是 object 是 JavaScript 長期以來的已知錯誤。
在 JavaScript 最初的實現中，JavaScript 中的值是由一個表示類型的標籤和實際資料值表示的。物件的類型標籤是 0。由於 null 代表的是空指針（大多數平台下值為 0x00），因此，null 的類型標籤也成為了 0，typeof null 就錯誤的返回了 "object"。 

## 記憶體存放方式與傳參考、傳值概念
[記憶體](https://courses.hexschool.com/courses/202049/lectures/3080862)
[JS 執行環境與作用域](https://courses.hexschool.com/courses/202049/lectures/3080864)
[函式與區域、全域變數](https://courses.hexschool.com/courses/202049/lectures/3080871)
### 練習 2
```
function callSomeone(person){
  var person = '小明';
  var someone = '杰哥';
  return person + ' 打給 ' + someone;
}
callSomeone('小華');
```
執行完callSomeone('小華')，person的值為？
#### 答案：小明
#### 解惑：
當呼叫函式並帶入參數時，例如 `callSomeone('小華')`，這個動作會將引數 `'小華'` 傳入函式，並將該值賦予函式內定義的參數 `person`。

函式內部的運作如下：
- `var person = '小明';`：這行程式碼會重新宣告一個區域變數 `person`，並將其設為 `'小明'`。這會**覆蓋**先前從參數得到的 `'小華'`。

因此，在執行完這行程式碼後，`person` 的值變為 `'小明'`。所以答案為 `'小明'`。

### 練習 3
```
var family = '媽媽';
function callFamily(){
  var family = '爸爸';
  console.log(family);
}
callFamily();
console.log(family);
```
執行結果？
#### 答案：
```
爸爸
媽媽
```
#### 解惑：
變數有分全域與區域
函式內的 family 因為是用 var family，所以雖然全域已經有 family 變數了，但這是在函式內宣告，所以屬於函式內的區域變數，因此當呼叫函式印出 family 時，結果會是區域的 family (爸爸)

而第二行 console.log(family) 是在全域下執行的，因此印出全域的 family (媽媽)

### 練習 4
```
var person = '小明';
function callSomeone(someone){
  someone = '杰哥';
  return person + ' 打給 ' + someone;
}
callSomeone('小華');
console.log(person);
console.log(someone);
```
執行結果？
#### 答案：
小明
Uncaught ReferenceError: someone is not defined
#### 解惑：
person 是全域變數，值為小明
函式 callSomeone(someone) 裡面的 someone 雖然被賦值為杰哥，但是是區域變數，所以只有在函式內才能取用，因此印出時會出錯

### 練習 5
```
var a = '杰哥';
function callSomeone(){
  var a = '小明';
  function callHey(){
    return a + ' 打給 阿偉';
  }
  return callHey();
}
callSomeone();
```
執行結果？
#### 答案：小明 打給 阿偉
#### 解惑：
雖然 callHey() 函式內沒有宣告 a，但 callHey() 會先看自己的區域有沒有 a，沒有的話會往上一層的區域找，找到 callSomeone() 函式內有宣告 var a = '小明'，所以會印出小明，而不是全域的杰哥。

### 練習 6
```
var a = '杰哥';
function callSomeone(){
  function callHey(){
    return a + ' 打給 阿偉';
  }
  var a = '小明';
  return callHey();
}
callSomeone();
```
執行結果？
#### 答案：小明 打給 阿偉
#### 解惑：
不論 var a 宣告在哪裡，只要是在函式內，就會在函式的一開始被建立，因此在 callHey() 執行時，a 已經被宣告了，雖然還未被賦值，但在執行 `return a + ' 打給 阿偉';` 時，a 已被宣告為 `undefined`，但因為後續的賦值 `var a = '小明';` 是在 callHey 被呼叫之前執行的，所以 callHey 內部的 a 會參照到已更新的值 '小明'。

然而，這題的重點在於**變數提升**的概念：在 callSomeone 函式內部，`var a` 會被提升到函式的頂部，但**賦值** (`= '小明'`) 不會提升。因此，在 callHey 被呼叫時，a 已經被賦值為 `'小明'` 了。

所以結果是 `'小明 打給 阿偉'`。

### 練習 7
```
var a = '杰哥';
function callSomeone(){
  function callHey(){
    return a + ' 打給 阿偉';
  }
  return callHey();
  var a = '小明';
}
callSomeone();
```
執行結果？
#### 答案：杰哥 打給 阿偉
#### 解惑：
callHey() 內沒有變數 a，因此往上一層的 callSomeone() 函式尋找，但因為 `var a = '小明'` 在 `return callHey();` 之後才宣告，且 return 後面的程式碼不會被執行，所以 callHey() 在 callSomeone() 函式內找不到變數 a，因此再往全域尋找，最後印出杰哥。

### 練習 8
```
var a = '杰哥';
function callSomeone(){
  a = '小明';
  function callHey(){
    return a + ' 打給 阿偉';
  }
  return callHey();
  var a = '阿緯';
}
callSomeone();
```
執行結果？
#### 答案：小明 打給 阿偉
#### 解惑：
callHey() 內沒有變數 a，因此往上一層的 callSomeone() 函式尋找。callSomeone() 函式內有 `a = '小明'`，因為這裡沒有使用 `var` 宣告，所以這個 `a` 會是全域變數嗎？不是，因為函式內部還有另一個 `var a = '阿緯'` 宣告（雖然在 return 後面不會執行，但變數提升會讓 `a` 在函式頂部被宣告為區域變數）。

所以 `a = '小明'` 這裡的 `a` 會被視為區域變數（因為有變數提升的宣告），而不是修改全域的 `a`。因此 callHey() 內的 `a` 會取到區域變數 `a` 的值 `'小明'`。

### 練習 9
```
var a = '杰哥';
function callSomeone(){
  a = '小明';
  function callHey(){
    return a + ' 打給 阿偉';
  }
  return callHey();
}
callSomeone();
```
執行結果？
#### 答案：小明 打給 阿偉
#### 解惑：
callHey() 內沒有變數 a，因此往上一層的 callSomeone() 函式尋找。callSomeone() 函式內有 `a = '小明'`，因為這裡沒有使用 `var` 宣告，所以這個 `a` 會被視為全域變數（因為函式內部沒有宣告 `var a`，所以會往外層找，找到全域的 `a` 並修改它）。

因此 callHey() 內的 `a` 會取到全域變數 `a` 的值 `'小明'`。

### 練習 10
```
var a = '杰哥';
function callSomeone(){
  var a = '小明';
  function callHey(){
    a = '阿緯';
    return a + ' 打給 阿偉';
  }
  return callHey();
}
callSomeone();
console.log(a);
```
執行結果？
#### 答案：
阿緯 打給 阿偉
杰哥
#### 解惑：
callHey() 內沒有宣告 a，但有一行 `a = '阿緯'`，所以會往上一層的 callSomeone() 函式尋找是否有變數 a，找到 `var a = '小明'`，因此將 callSomeone() 函式內的 a 從小明改為阿緯，所以印出「阿緯 打給 阿偉」。

最後印出全域的 a，結果是杰哥。

### 練習 11
```
var a = '杰哥';
function callSomeone(){
  var a = '小明';
  function callHey(){
    var a = '阿緯';
    return a + ' 打給 阿偉';
  }
  return callHey();
}
callSomeone();
console.log(a);
```
執行結果？
#### 答案：
阿緯 打給 阿偉
杰哥
#### 解惑：
callHey() 內有宣告 `var a = '阿緯'`，所以是區域變數，return 時會印出「阿緯 打給 阿偉」。

最後印出全域的 a，結果是杰哥。

### 練習 12
```
var person = '小明';
function callSomeone(person){
  return person + ' 打給 ' + someone;
  var someone = '杰哥';
}
callSomeone('阿緯');
```
執行結果？
#### 答案：
Uncaught ReferenceError: someone is not defined
#### 解惑：
函式內的變數 someone 有宣告但沒有被賦值，所以是 undefined，但因為 return 在 someone 宣告之前，所以 someone 在 return 時尚未被宣告，因此會出現錯誤。

### 練習 13
```
var person = '小明';
function callSomeone(person){
  var someone = '杰哥';
  return person + ' 打給 ' + someone;
}
callSomeone('阿緯');
console.log(person);
```
執行結果？
#### 答案：
阿緯 打給 杰哥
小明
#### 解惑：
函式 callSomeone(person) 的參數 person 會接收傳入的值 '阿緯'，因此 return 時印出「阿緯 打給 杰哥」。

最後印出全域的 person，結果是小明。

### 練習 14
```
var person = '小明';
function callSomeone(person){
  var someone = '杰哥';
  return person + ' 打給 ' + someone;
  var person = '漂亮阿姨'
}
callSomeone('阿緯');
```
執行結果？
#### 答案：
阿緯 打給 杰哥
#### 解惑：
雖然函式內有 `var person = '漂亮阿姨'`，但因為在 return 之後，所以不會執行，因此 person 的值仍然是傳入的 '阿緯'。

### 練習 15
```
var person = '小明';
function callSomeone(person){
  var someone = '杰哥';
  var person = '漂亮阿姨'
  return person + ' 打給 ' + someone;
}
callSomeone('阿緯');
```
執行結果？
#### 答案：
漂亮阿姨 打給 杰哥
#### 解惑：
函式內有 `var person = '漂亮阿姨'`，這會覆蓋掉參數 person 的值，因此 return 時 person 的值是 '漂亮阿姨'。

### 練習 16
```
var person = '小明';
function callSomeone(person){
  var someone = '杰哥';
  person = '漂亮阿姨';
  return person + ' 打給 ' + someone;
}
callSomeone('阿緯');
```
執行結果？
#### 答案：
漂亮阿姨 打給 杰哥
#### 解惑：
函式內有 `person = '漂亮阿姨'`，這會修改參數 person 的值，因此 return 時 person 的值是 '漂亮阿姨'。

### 練習 17
```
var family = {
  name: '小明家'
}
function callFamily(family){
  family.name = '小華家';
  return family
}
callFamily(family);
console.log(family);
```
執行結果？
#### 答案：
{name: "小華家"}
#### 解惑：
`family` 是一個物件，在傳入函式時，傳遞的是物件的參考（reference），所以函式內修改 `family.name` 會影響到外層的物件。

### 練習 18
```
var family = {
  name: '小明家'
}
function callFamily(family){
  family = {
    name: '小華家'
  }
  return family
}
callFamily(family);
console.log(family);
```
執行結果？
#### 答案：
{name: "小明家"}
#### 解惑：
在函式內，`family` 被重新賦值為一個新的物件 `{ name: '小華家' }`，這並不會影響外層的 `family` 物件，因為這裡的 `family` 參數現在指向了一個新的物件。

### 練習 19
```
var family = {
  name: '小明家',
  members: {
    father: '爸爸',
    mom: '媽媽',
    children: 3
  }
}
function callFamily(family){
  family.members = {
    father: '爸爸',
    mom: '媽媽'
  }
  return family
}
callFamily(family);
console.log(family);
```
執行結果？
#### 答案：
{name: "小明家", members: {father: "爸爸", mom: "媽媽"}}
#### 解惑：
`family` 是一個物件，傳入函式後，`family.members` 被重新賦值為一個新的物件 `{ father: '爸爸', mom: '媽媽' }`，這會影響外層的 `family` 物件，因為 `family.members` 是物件內的一個屬性。

### 練習 20
```
var family = {
  name: '小明家',
  members: {
    father: '爸爸',
    mom: '媽媽',
    children: 3
  }
}
function callFamily(family){
  family.members.children = 2;
  return family
}
callFamily(family);
console.log(family);
```
執行結果？
#### 答案：
{name: "小明家", members: {father: "爸爸", mom: "媽媽", children: 2}}
#### 解惑：
`family.members.children` 被修改為 `2`，這會影響外層的物件。

### 練習 21
```
var family = {
  name: '小明家',
  members: {
    father: '爸爸',
    mom: '媽媽',
    children: 3
  }
}
function callFamily(family){
  family = {
    name: '小華家',
    members: {
      father: '老爸',
      mom: '老媽'
    }
  }
  return family
}
callFamily(family);
console.log(family);
```
執行結果？
#### 答案：
{name: "小明家", members: {father: "爸爸", mom: "媽媽", children: 3}}
#### 解惑：
在函式內，`family` 被重新賦值為一個新的物件，這並不會影響外層的 `family` 物件。

### 練習 22
```
var family = {
  name: '小明家',
  members: {
    father: '爸爸',
    mom: '媽媽',
    children: 3
  }
}
function callFamily(family){
  family.members = {
    father: '老爸',
    mom: '老媽'
  }
  family = {
    name: '小華家'
  }
  return family
}
callFamily(family);
console.log(family);
```
執行結果？
#### 答案：
{name: "小明家", members: {father: "老爸", mom: "老媽"}}
#### 解惑：
首先，`family.members` 被重新賦值為 `{ father: '老爸', mom: '老媽' }`，這會影響外層的物件。然後 `family` 被重新賦值為 `{ name: '小華家' }`，但這不會影響外層的 `family`，因為現在 `family` 指向一個新的物件。

### 練習 23
```
var a = {
  family: '小明家'
}
var b = a;
b.family = '小華家';
console.log(a);
```
執行結果？
#### 答案：
{family: "小華家"}
#### 解惑：
`b = a` 是將 `b` 指向 `a` 所指向的物件，所以修改 `b.family` 會影響到 `a.family`。

### 練習 24
```
var a = {
  family: '小明家'
}
var b = a;
b = {
  family: '小華家'
}
console.log(a);
```
執行結果？
#### 答案：
{family: "小明家"}
#### 解惑：
`b = { family: '小華家' }` 是將 `b` 指向一個新的物件，這不會影響 `a`。

### 練習 25
```
var a = {
  family: '小明家'
}
var b = a;
b.family = '小華家';
var c = {
  family: '小華家'
}
console.log(a === b);
console.log(a === c);
console.log(b === c);
```
執行結果？
#### 答案：
true
false
false
#### 解惑：
- `a === b`：`a` 和 `b` 指向同一個物件，所以是 `true`。
- `a === c`：`a` 和 `c` 指向不同的物件，所以是 `false`。
- `b === c`：`b` 和 `c` 指向不同的物件，所以是 `false`。

### 練習 26
```
var a = {
  family: '小明家'
}
var b = a;
a.family = '杰哥';
a = {
  family: '小華家'
}
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
{family: "小華家"}
{family: "杰哥"}
#### 解惑：
- `b = a`：`b` 指向 `a` 所指向的物件。
- `a.family = '杰哥'`：修改 `a` 指向的物件的 `family` 屬性為 `'杰哥'`，所以 `b` 也會看到這個變化。
- `a = { family: '小華家' }`：`a` 指向一個新的物件，但 `b` 仍然指向原來的物件。

### 練習 27
```
var a = {
  family: '小明家'
}
var b = {
  family: '小明家'
}
console.log(a === b);
```
執行結果？
#### 答案：
false
#### 解惑：
`a` 和 `b` 雖然內容相同，但它們是不同的物件，所以 `===` 比較的是參考，結果為 `false`。

### 練習 28
```
var a = 1;
var b = a;
b = 2;
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
1
2
#### 解惑：
`a` 是純值，`b = a` 是複製值，所以修改 `b` 不會影響 `a`。

### 練習 29
```
var a = 1;
var b = a;
b = 2;
a = 3;
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
3
2
#### 解惑：
`a` 和 `b` 是獨立的變數，修改一個不會影響另一個。

### 練習 30
```
var a = {
  family: '小明家'
}
var b = a;
b.family = '杰哥';
a = {
  family: '小華家'
}
b = a;
b.family = '漂亮阿姨';
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
{family: "漂亮阿姨"}
{family: "漂亮阿姨"}
#### 解惑：
- `b = a`：`b` 指向 `a` 所指向的物件。
- `b.family = '杰哥'`：修改 `a` 指向的物件的 `family` 屬性為 `'杰哥'`。
- `a = { family: '小華家' }`：`a` 指向一個新的物件。
- `b = a`：`b` 指向 `a` 所指向的新物件。
- `b.family = '漂亮阿姨'`：修改 `a` 指向的新物件的 `family` 屬性為 `'漂亮阿姨'`。

所以 `a` 和 `b` 最後都指向同一個物件 `{ family: '漂亮阿姨' }`。

### 練習 31
```
var a = {
  family: '小明家'
}
var b = a;
b.family = '杰哥';
a = {
  family: '小華家'
}
b = a;
a.family = '漂亮阿姨';
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
{family: "漂亮阿姨"}
{family: "漂亮阿姨"}
#### 解惑：
與上題類似，最後 `a` 和 `b` 指向同一個物件，且 `family` 被修改為 `'漂亮阿姨'`。

### 練習 32
```
var a = {
  family: '小明家'
}
var b = a;
b = {
  family: '小華家'
}
b.family = '杰哥';
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
{family: "小明家"}
{family: "杰哥"}
#### 解惑：
- `b = a`：`b` 指向 `a` 所指向的物件。
- `b = { family: '小華家' }`：`b` 指向一個新的物件。
- `b.family = '杰哥'`：修改 `b` 指向的新物件的 `family` 屬性。

所以 `a` 仍然指向原來的物件 `{ family: '小明家' }`，`b` 指向新的物件 `{ family: '杰哥' }`。

### 練習 33
```
var a = {
  family: '小明家'
}
var b = a;
a.family = '杰哥';
b = {
  family: '小華家'
}
a = b;
b.family = '漂亮阿姨';
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
{family: "漂亮阿姨"}
{family: "漂亮阿姨"}
#### 解惑：
- `b = a`：`b` 指向 `a` 所指向的物件。
- `a.family = '杰哥'`：修改 `a` 指向的物件的 `family` 屬性為 `'杰哥'`，所以 `b` 也會看到這個變化。
- `b = { family: '小華家' }`：`b` 指向一個新的物件。
- `a = b`：`a` 指向 `b` 所指向的新物件。
- `b.family = '漂亮阿姨'`：修改 `b` 指向的新物件的 `family` 屬性為 `'漂亮阿姨'`，所以 `a` 也會看到這個變化。

所以 `a` 和 `b` 最後都指向同一個物件 `{ family: '漂亮阿姨' }`。

### 練習 34
```
var a = {
  family: '小明家'
}
var b = a;
a.family = '杰哥';
b = {
  family: '小華家'
}
a = b;
a.family = '漂亮阿姨';
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
{family: "漂亮阿姨"}
{family: "漂亮阿姨"}
#### 解惑：
同上題，最後 `a` 和 `b` 指向同一個物件，且 `family` 被修改為 `'漂亮阿姨'`。

### 練習 35
```
var a = {
  family: '小明家'
}
var b = a;
a.family = '杰哥';
a = {
  family: '小華家'
}
b = a;
a.family = '漂亮阿姨';
console.log(a);
console.log(b);
```
執行結果？
#### 答案：
{family: "漂亮阿姨"}
{family: "漂亮阿姨"}
#### 解惑：
同上題，最後 `a` 和 `b` 指向同一個物件，且 `family` 被修改為 `'漂亮阿姨'`。

## 總結
這些練習題涵蓋了 JavaScript 中變數作用域、純值與物件的傳值/傳參考、變數提升等核心概念。理解這些概念對於掌握 JavaScript 的運作機制非常重要。