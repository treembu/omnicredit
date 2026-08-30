# -*- coding: utf-8 -*-

import streamlit as st

st.set_page_config(page_title="Pricing", page_icon="\U0001f4bc", layout="wide")

# --- constants ---
TIERS = {
    "Starter": {
        "rate": 1.99,
        "min_fee": 700,
        "range": "300-625 active loans",
        "tagline": "For growing lenders establishing their book"
    },
    "Growth": {
        "rate": 1.39,
        "min_fee": 1_250,
        "range": "625-2,500 active loans",
        "tagline": "For established lenders scaling operations"
    },
    "Enterprise": {
        "rate": None,
        "min_fee": None,
        "range": "2,500+ active loans",
        "tagline": "Enterprise features, white-labelling, custom SLAs, and dedicated support"
    },
}

DISCOUNTS = {
    "Monthly": 0.00,
    "6-month upfront (-6%)": 0.06,
    "12-month upfront (-10%)": 0.10,
}

def monthly_cost(rate: float, min_fee: float, loans: int, disc: float) -> float:
    return max(rate * laons, min_fee) * (1 - disc)
    
def active_tier(loans: int) -> str:
    if loans < 625:
        return "Starter"
    if loans <= 2_500:
        return "Growth"
    return "Enterprise"
    
    
# -- Header --
st.markdown("##### Pricing")
st.title("Straightforward pricing that gets better as you grow")
st.markdown("##### Straightforward pricing based on one thing: your active loan count.")
st.caption("No set-up fees. No per-user charges. Cancel monthly plans anytime.")
st.divider()

# -- Controls --
left, right = st.columns([3, 2])
with left:
    loans = st.slider(
        "How many active loans do you currently manage?",
        min_value = 250,
        max_value=3_500,
        value=500,
        step=25,
    )
with right:
    billing = st.radio("Billing period", list(DISCOUNTS.keys()), index=0)
    
disc = DISCOUNTS[billing]
tier_name = active_tier(loans)

st.divider()

# -- Tier cards --
cols = st.columns(3, gap="medium")

for col, (name, t) in zip(cols, TIERS.items()):
    is_active = name == tier_name
    with col:
        with st.container(border=True):
        
            # Recommended badge
            if is_active:
                label = "\u2605  Most Popular" if name == "Growth" else "\u2713  Your tier"
                st.markdown(f"**{label}**")
                
            st.markdown(f"### {name}")
            st.caption(t["tagline"])
            st.markdown(f"*{t['range']}*")
            st.markdown("---")
        
            if t["rate"] is not None:
                base_monthly = max(t["rate"] * loans, t["min_fee"])
                discounted = base_monthly * (1 - disc)
                annual = discounted * 12
                annual_saving = base_monthly * 12 - annual
                
                st.markdown(f"## ${discounted:,.0f} /mo")
                st.caption(f"${t['rate']:.2f} per active loan - min ${t['min_fee']:,}/mo")
                
                if annual_saving > 0:
                    st.success(f"You save ${annual_saving:,.0f}/yr on this plan")
                    
                st.markdown(f"*~ ${annual:,.0f} billed annually*")
                st.markdown(" ")

                st.button(
                    "Get started ->",
                    key=f"cta_{name}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                )
            
            else:
                st.markdown("## Custom")
                st.caption("Tailore to your loan book, volume, and requirements")
                st.markdown(" ")
                st.button("Book a call ->", key="cta_pro", use_container_width=True, type="primary" if is_active else "secondary")
            
# -- Upfront savings breakdown ---
st.divider()
st.markdown("### 💰 Save by paying upfront")
st.caption(f"Based on your selection: **{loans:,} active loans on {tier_name}**")

if tier_name != "Enterprise":
    t = TIERS[tier_name]
    base = max(t["rate"] * loans, t["min_fee"])
    s1, s2, s3 = st.columns(3)
    
    for col, (period, d) in zip([s1, s2, s3], DISCOUNTS.items()):
        effective = base * (1 - d)
        saving = base * 12 - effective * 12
        with col:
            st.metric(
                label=period.split("  ")[0],  # Strip discount label
                value=f"${effective:,.0f}/mo",
                delta=f"Save ${saving:,.0f}/yr" if saving > 0 else "Standard rate",
                delta_color="normal" if saving > 0 else "off",
            )
else:
    st.info("Contact us for enterprise pricing and commitment options.")

# -- FAQ / fine print --
st.divider()

with st.expander("How is my monthly fee calculated?"):
    st.markdown(
        "Your fee is: **(active loans x rate)** or the **minimum monthly fee** - whichever is higher. \n"
        "Active loans are counted on the last calendar day of each billing month."
    )
    
with st.expander("What counts as an active loan?"):
    st.markdown(
        "Any loan that is open and not fully repaid, written off, or cancelled as at the last day of the month. \n"
        "Loans in arrears are still counted as active."
    )
    
with st.expander("Can I change tiers?"):
    st.markdown(
        "Yes - you can upgrade at any time. Downgrades take effect at the start of the next billing period.  \n"
        "Customers on upfront plans can upgrade mid-term and we'll credit the unused portion."
    )
    
st.divider()
st.caption(
    "All prices in AUD and exclude GST. Upfront discounts apply to the base monthly fee only and cannot be combined with other offers."
)
