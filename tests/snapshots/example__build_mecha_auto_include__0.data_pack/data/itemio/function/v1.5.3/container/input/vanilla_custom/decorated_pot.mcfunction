
data remove storage itemio:main.input ItemUnique
data modify storage itemio:main.input ItemUnique set from block ~ ~ ~ item

function itemio:v1.5.3/container/input/vanilla_custom/single_item/main

data modify block ~ ~ ~ item set from storage itemio:main.input ItemUnique
