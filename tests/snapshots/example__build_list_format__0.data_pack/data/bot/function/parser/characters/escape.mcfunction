execute if data storage bot:parser current.escape{status:"current"} run data merge storage bot:parser {current:{escape:{escaped:false,status:"none"}}}
execute if data storage bot:parser current.escape{status:"new"} run data modify storage bot:parser current.escape.status set value "current"
execute if data storage bot:parser {current:{value:"\\",escape:{escaped:false}}} run data modify storage bot:parser current merge value {escape:{escaped:true,status:"new"},consumed:true,flags:["escape","meta"]}