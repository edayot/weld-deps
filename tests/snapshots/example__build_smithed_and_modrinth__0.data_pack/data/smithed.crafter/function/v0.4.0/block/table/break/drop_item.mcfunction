kill @e[type=item, nbt={Item: {id: "minecraft:barrel", count: 1}}, limit=1, sort=nearest, distance=..3]
execute if entity @s[tag=smithed.default] run loot spawn ~ ~ ~ loot smithed.crafter:blocks/table
execute if entity @s[tag=!smithed.default] run function #smithed.crafter:event/break
