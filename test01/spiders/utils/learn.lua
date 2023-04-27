--package.path = "F:\\Demo\\Scrapy\\test01\\test01\\spiders\\utils/?.lua"
--local module = require("module")
--module.func3()
print(package.path)
local a = 0

repeat
    a = a + 1
    print(a)
until a > 2

function max(num1, num2)
    if num1 > num2 then
        print('max is num1:', num1)
    else
        print('max is num2:', num2)
    end
end

print(max(234, 34))
s, e = string.find("www.runoob.com", "runoob")
print(s, e)

function maximum (a)
    local mi = 1             -- 最大值索引
    local m = a[mi]          -- 最大值
    for i, val in ipairs(a) do
        if val > m then
            mi = i
            m = val
        end
    end
    return m, mi
end

print(maximum({ 8, 10, 23, 12, 5 }))

function average(...)
    result = 0
    local arg = { ... }    --> arg 为一个表，局部变量
    for i, v in ipairs(arg) do
        result = result + v
    end
    print("总共传入 " .. #arg .. " 个数")
    return result / #arg
end

print("平均值为", average(10, 5, 3, 4, 5, 6, 34, 564, 23, 3, 5))

function f(...)
    a = select(4, ...)  -->从第三个位置开始，变量 a 对应右边变量列表的第一个参数
    print(a)
    print(select(3, ...)) -->打印所有列表参数
end

f(0, 1, 2, 3, 4, 5)
print(3 ^ 2)
a = 5
b = 2

print(a - b + b)
b = '\a'
b = 'hello world'
print(string.upper(b))
print(string.lower(b))
print(string.gsub(b, 'e', 'fd'))
print(string.find(b, 'or'))
print(string.len(b))
print(#b)
print(string.rep(b, 3))
array = { "Google", "Runoob" }

for key, value in ipairs(array)
do
    print(key, value)
end

function myfunction ()
   n = n/nil
end

function myerrorhandler( err )
   print( "ERROR:", err )
end

status = xpcall( myfunction, myerrorhandler )
print( status)











