function itemio:v1.2.6/container/hopper_v2/extract_top
execute positioned ~1 ~ ~ run summon marker ~ ~ ~ {data: {itemio: {ioconfig: {input_side: "west"}}}, Tags: ["itemio.transfer.destination", "itemio.transfer.destination.temp", "itemio.summoned"]}
scoreboard players set #max_output_count itemio.io 1
data remove storage itemio:io filters
data remove storage itemio:io input
data modify storage itemio:io output_side set value "east"
function #itemio:calls/transfer
kill @e[tag=itemio.transfer.destination.temp]
