execute if data storage bot:interpreter evaluate.stack[-1].metadata{status:"parameters"} run function bot:interpreter/evaluate/literal/resource/parameters/init
execute unless data storage bot:interpreter evaluate.stack[-1].metadata.status{status:"parameters"} run function bot:interpreter/evaluate/literal/resource/before