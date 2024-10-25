import streamlit as st
import pandas as pd

# Function to perform calculations
def calculate_chlorine_hcl_hydrogen_costs(caustic_soda_prod, sodium_hypo_prod, liquid_chlorine_prod, stearic_batches, hcl_hydrogen_usage, stearic_hydrogen_usage, power_rate, steam_cost, demin_water_cost, chemical_cost, caustic_soda_sale_price, sodium_hypo_sale_price, hcl_sale_price):
    # Constants for calculations
    chlorine_factor = 0.889
    hypo_chlorine_usage = 0.22
    chlorine_neutralization = 0.017
    hcl_chlorine_usage = 0.32
    in_house_hcl = 0.05
    power_rate_per_ton = 2400.0
    hydrogen_production_percentage = 0.026

    chlorine_production = caustic_soda_prod * chlorine_factor
    chlorine_used_in_hypo = sodium_hypo_prod * hypo_chlorine_usage
    chlorine_neutralized = chlorine_production * chlorine_neutralization
    net_chlorine_available = chlorine_production - chlorine_used_in_hypo - chlorine_neutralized - liquid_chlorine_prod

    hcl_prod = net_chlorine_available / hcl_chlorine_usage
    hcl_in_house = caustic_soda_prod * in_house_hcl
    net_hcl_for_sale = hcl_prod - hcl_in_house

    hydrogen_prod_mt = caustic_soda_prod * hydrogen_production_percentage
    hydrogen_prod_nm3 = hydrogen_prod_mt * 34819 / 3.12

    hydrogen_used_in_hcl = hcl_hydrogen_usage
    hydrogen_used_in_stearic = stearic_hydrogen_usage
    total_hydrogen_usage = hydrogen_used_in_hcl + hydrogen_used_in_stearic
    balance_hydrogen_nm3 = hydrogen_prod_nm3 - total_hydrogen_usage
    balance_waste_percentage = (balance_hydrogen_nm3 / hydrogen_prod_nm3) * 100 if hydrogen_prod_nm3 > 0 else 0

    total_power_used = power_rate_per_ton * caustic_soda_prod
    power_per_ton_caustic_soda = total_power_used / caustic_soda_prod if caustic_soda_prod > 0 else 0

    power_factor = 2380
    steam_factor = 1.37
    dw_factor = 10.50
    caustic_soda_percentage = 2.5 / 100
    caustic_soda_cost = 2.96

    power_cost = round(power_factor * (power_rate / 1000), 2)
    steam_cost_total = round(steam_factor * (steam_cost / 1000), 2)
    dw_cost = round(dw_factor * (demin_water_cost / 1000), 2)
    chemical_cost = round(chemical_cost, 2)

    cost_of_production = round(power_cost + steam_cost_total + dw_cost + chemical_cost, 2)
    caustic_soda_usage_cost = round(cost_of_production * caustic_soda_percentage, 2)
    total_cost_per_ton = round(cost_of_production + caustic_soda_usage_cost, 2)

    total_sales = round((caustic_soda_prod * caustic_soda_sale_price) + (sodium_hypo_prod * sodium_hypo_sale_price) + (net_hcl_for_sale * hcl_sale_price), 2)
    sodium_hypo_cost = round(0.22 * total_cost_per_ton, 2)

    rmc_caustic_soda = round(total_cost_per_ton * caustic_soda_prod, 2)
    rmc_sodium_hypo = sodium_hypo_cost * sodium_hypo_prod
    total_rmc = round(rmc_caustic_soda + rmc_sodium_hypo, 2)

    total_gc = round(total_sales - total_rmc, 2)
    gc_per_kg = round(total_gc / caustic_soda_prod, 2) if caustic_soda_prod > 0 else 0
    gc_percentage = round((total_gc / total_sales) * 100, 2) if total_sales > 0 else 0

    results = {
        "Production": {
            "Chlorine Production (tons/day)": round(chlorine_production, 2),
            "Chlorine Used in Hypo Production (tons)": round(chlorine_used_in_hypo, 2),
            "Chlorine Neutralized (tons)": round(chlorine_neutralized, 2),
            "Net Chlorine Available for HCl (tons)": round(net_chlorine_available, 2),
            "Total HCl Production (tons)": round(hcl_prod, 2),
            "HCl Used In-House (tons)": round(hcl_in_house, 2),
            "Net HCl Available for Sale (tons)": round(net_hcl_for_sale, 2),
            "Hydrogen Production (MT)": round(hydrogen_prod_mt, 2),
            "Hydrogen Production (NM³)": round(hydrogen_prod_nm3, 2),
            "Balance Hydrogen NM³": round(balance_hydrogen_nm3, 2),
            "Balance Hydrogen Waste (%)": round(balance_waste_percentage, 2),
            "Total Power Used (KWH)": round(total_power_used, 2),
            "Power Used per ton Caustic Soda (KWH)": round(power_per_ton_caustic_soda, 2),
        },
        "Power": {
            "Power Cost (Rs/ton)": power_cost,
            "Steam Cost (Rs/ton)": steam_cost_total,
            "Demin Water Cost (Rs/ton)": dw_cost,
            "Other Chemical Costs (Rs/ton)": chemical_cost,
            "Total Cost of Production (Rs/ton)": cost_of_production,
            "Caustic Soda Usage Cost (Rs/ton)": caustic_soda_usage_cost,
            "Total Cost per ton (Rs)": total_cost_per_ton,
            "Sodium Hypo Cost (Rs)": sodium_hypo_cost,
        },
        "Cost": {
            "Sales Total (Rs)": total_sales,
        },
        "RMC": {
            "RMC Caustic Soda (Rs)": rmc_caustic_soda,
            "RMC Sodium Hypochlorite (Rs)": rmc_sodium_hypo,
            "Total RMC (Rs)": total_rmc,
        },
        "GC": {
            "Total GC (Rs)": total_gc,
            "GC per kg (Rs)": gc_per_kg,
            "GC Percentage (%)": gc_percentage,
        }
    }

    return results

# Streamlit app
st.title("NIMIR - Chemical Production Cost Analysis")
st.header("Caustic Soda and By-products Calculator")

# Input fields
caustic_soda_prod = st.number_input("Caustic Soda production in tons (TPD)", min_value=0.0, step=0.1)
sodium_hypo_prod = st.number_input("Sodium Hypochlorite production in tons", min_value=0.0, step=0.1)
liquid_chlorine_prod = st.number_input("Liquid Chlorine production in tons", min_value=0.0, step=0.1)
stearic_batches = st.number_input("Number of Stearic Acid Batches", min_value=0, step=1)

# Cost inputs
power_rate = st.number_input("Power Rate (per unit in Rs)", min_value=0.0, step=0.1)
steam_cost = st.number_input("Steam Cost (per ton in Rs)", min_value=0.0, step=0.1)
demin_water_cost = st.number_input("Demin Water Cost (per m³ in Rs)", min_value=0.0, step=0.1)
chemical_cost = st.number_input("Other Chemical Costs (per ton in Rs)", min_value=0.0, step=0.1)

# Sales prices
caustic_soda_sale_price = st.number_input("Sale Price of Caustic Soda (per ton in Rs)", min_value=0.0, step=0.1)
sodium_hypo_sale_price = st.number_input("Sale Price of Sodium Hypochlorite (per ton in Rs)", min_value=0.0, step=0.1)
hcl_sale_price = st.number_input("Sale Price of HCl (per ton in Rs)", min_value=0.0, step=0.1)

# Button to calculate results
if st.button("Calculate"):
    results = calculate_chlorine_hcl_hydrogen_costs(
        caustic_soda_prod, sodium_hypo_prod, liquid_chlorine_prod, stearic_batches,
        hcl_hydrogen_usage=17228.0, stearic_hydrogen_usage=5400.0,
        power_rate=power_rate, steam_cost=steam_cost, demin_water_cost=demin_water_cost,
        chemical_cost=chemical_cost, caustic_soda_sale_price=caustic_soda_sale_price,
        sodium_hypo_sale_price=sodium_hypo_sale_price, hcl_sale_price=hcl_sale_price
    )
    
    # Display results as tables
    st.subheader("Production Results")
    st.table(pd.DataFrame(results["Production"], index=["Values"]))
    
    st.subheader("Power Costs")
    st.table(pd.DataFrame(results["Power"], index=["Values"]))
    
    st.subheader("Cost Summary")
    st.table(pd.DataFrame(results["Cost"], index=["Values"]))

    st.subheader("RMC Summary")
    st.table(pd.DataFrame(results["RMC"], index=["Values"]))
    
    st.subheader("GC Summary")
    st.table(pd.DataFrame(results["GC"], index=["Values"]))

# Footer
st.markdown("---")
st.markdown("**Developed by mak3.10**")
