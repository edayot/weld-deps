data remove storage itemio:main.output Item1
data remove storage itemio:main.output Item2
data modify storage itemio:main.output Item1 set from storage itemio:main.output input
data modify storage itemio:main.output Item2 set from storage itemio:main.output Items[0]
data remove storage itemio:main.output Item1.count
data remove storage itemio:main.output Item1.Slot
data remove storage itemio:main.output Item2.count
data remove storage itemio:main.output Item2.Slot
execute store result score #!same_item itemio.math.output run data modify storage itemio:main.output Item1 set from storage itemio:main.output Item2
execute if score #!same_item itemio.math.output matches 0 run function itemio:v1.2.6/container/output/vanilla/output/process with storage itemio:main.output temp.args_loop_item
