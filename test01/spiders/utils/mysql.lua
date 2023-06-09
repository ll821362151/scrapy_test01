---
--- Generated by EmmyLua(https://github.com/EmmyLua)
--- Created by DELL.
--- DateTime: 2023-4-27 15:52:54
---
require "luasql.mysql"
env = luasql.mysql()
--连接数据库
conn = env:connect("test", "root", "mysql", "localhost", 3306)
if conn then
    print('success')
end
--设置数据库的编码格式
conn:execute "SET NAMES UTF8"

--执行数据库操作
cur = conn:execute("select * from s_dic")
row = cur:fetch({}, "a")

-- 遍历所有记录并逐一打印
while row do
    for k, v in pairs(row) do
        print(k .. ": " .. v)
    end
    print("------------------------------")
    row = cur:fetch({}, "a")
end


--文件对象的创建
--file = io.open("role.txt", "w+");
--
--while row do
--    var = string.format("%s %s\n", row.id, row.name)
--
--    print(var)
--
--    file:write(var)
--
--    row = cur:fetch(row, "a")
--end

--file:close()  --关闭文件对象
conn:close()  --关闭数据库连接
env:close()   --关闭数据库环境
print(_VERSION)