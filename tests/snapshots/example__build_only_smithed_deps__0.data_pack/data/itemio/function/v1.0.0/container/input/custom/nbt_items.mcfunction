$execute unless data $(nbt_items_path) run data modify $(nbt_items_path) set value []
$data modify storage itemio:main.input Items set from $(nbt_items_path)
scoreboard players add #nb_entities itemio.math.input 1
