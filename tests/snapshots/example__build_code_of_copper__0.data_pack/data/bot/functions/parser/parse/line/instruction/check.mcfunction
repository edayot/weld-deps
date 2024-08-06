data modify storage bot:helpers/registry key set from storage bot:parser current.value
function bot:helpers/registry/init

execute if data storage bot:helpers/registry output.exact run data modify storage bot:parser stack[-1].instruction set from storage bot:helpers/registry output.exact

execute unless data storage bot:helpers/registry output.matches[] run data modify storage bot:parser stack[-1].metadata.no_matches set value true

execute unless data storage bot:parser current{flags:["whitespace"]} run data modify storage bot:parser stack[-1].value append from storage bot:parser current.value

data modify storage bot:parser current.consumed set value true