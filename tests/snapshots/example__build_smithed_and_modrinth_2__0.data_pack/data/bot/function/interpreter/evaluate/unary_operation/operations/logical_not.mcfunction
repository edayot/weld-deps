data modify storage bot:interpreter evaluate.operation.result set value {type: "literal", variant: "boolean", value: false}
execute if score $value bot.interpreter matches 0 run data modify storage bot:interpreter evaluate.operation.result.value set value true