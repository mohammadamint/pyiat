#%%
from pyiat.core.impact import Indicator,Dimension,Capital,Impact
# Water
water_depleted = Indicator(
    name = "depleted water",
    type = "negative",
    unit = "m3",
    ex_ante = 1,
    ex_post = 4,
    description = "amount of water depleted"
)

water_quality = Indicator(
    name = "water quality",
    type = "positive",
    unit = "m3",
    ex_ante = 2,
    ex_post = 3,
    description = "amount of water depleted"
)

# Air
co2_intensity = Indicator(
    name = "CO2/kWh emitted",
    type = "negative",
    unit = "CO2/kWh",
    ex_ante= 2,
    ex_post= 4,
)
pm_intensity = Indicator(
    name = "PMI/kWh emitted",
    type = "negative",
    unit = "PMI/kWh",
    ex_ante= 5,
    ex_post= 2,
)
#%%
Water = Dimension("Water",[water_depleted,water_quality])
Air = Dimension("Air",[co2_intensity,pm_intensity])
natural_capital = Capital("Natural Capital",[Water,Air])
#%%
"""Physical"""
distribution = Indicator(
    name = "line distribution",
    type = "positive",
    unit = "kW",
    ex_ante = 1,
    ex_post = 4
)

capacity = Indicator(
    name = "Electricity production",
    type = "positive",
    unit = "kW",
    ex_ante = 1,
    ex_post = 4
)

light = Indicator(
    name = "light quality",
    type = "positive",
    unit = "..",
    ex_ante=2,
    ex_post=5,
)

productive_use = Indicator(
    name = "Productive devices",
    type = "positive",
    unit = "share",
    ex_ante = 1,
    ex_post = 3
)

HeavyInfrastructure = Dimension(name="Heavy Infrastructure",indicators=[distribution,capacity])
LightInfrastructure = Dimension(name="Light Infrastructure",indicators=[light,productive_use])

physical_capital = Capital("Physical Capital",dimensions=[HeavyInfrastructure,LightInfrastructure])

impact = Impact("Total Impact",[natural_capital,physical_capital])

for item in [Water,Air,natural_capital,HeavyInfrastructure,LightInfrastructure,physical_capital,impact]:
    df = item.get_weight_matrix()
    df.iloc[0] = 2
    item.set_weight_matrix(df)

# %%
from pyiat.utils.io import excel_parser

output = excel_parser("Book1.xlsx")
# %%
