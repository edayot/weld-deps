data modify storage bot:interpreter evaluate.operation.result set value {type: "literal", variant: "boolean", value: false}
execute store result storage bot:interpreter evaluate.operation.result.value byte 1 if score .a bot.interpreter >= .b bot.interpreter
