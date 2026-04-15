
#loading block data

$execute unless data $(nbt_items_path) run data modify $(nbt_items_path) set value []
$data modify storage itemio:main.output Items set from $(nbt_items_path)
scoreboard players add #nb_entities itemio.math.output 1

# tellraw @p [{"text":"Items : "},{"nbt":"Items","storage":"itemio:main.output"}]
# tellraw @p [{"text":"ioconfig : "},{"nbt":"ioconfig","storage":"itemio:main.output"}]
