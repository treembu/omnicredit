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
st.markdown("##### Pay upfront and save up to 10% - or go month-to-month with no lock-in.")
st.caption("No set-up fees. No per-user charges. Cancel monthly plans anytime.")
st.divider()

# -- Controls --
st.markdown("**How would you like to be billed?**")
billing = st.radio(
    "Billing period",
    list(DISCOUNTS.keys()),
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)

loans = st.slider(
    "How many active loans do you currently manage?",
    min_value = 250,
    max_value=3_500,
    value=500,
    step=25,
)
    
disc = DISCOUNTS[billing]
tier_name = active_tier(loans)

if disc > 0:
    t_current = TIERS[tier_name]
    if t_current["rate"] is not None:
        base = max(t_current["rate"] * loans, t_current["min_fee"])
        saving = base * 12 - base * (1 - disc) * 12
        st.success(
            f"💰 At your current loan count, paying {'6-monthly' if disc == 0.06 else 'annually'} "
            f"saves you **${saving:,.0f}/year** (${saving/12:,.0f}/month) on the {tier_name} plan."
        )

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
                    st.success(f"Save ${annual_saving:,.0f}/yr")
                    st.markdown(
                        f"<h2 style='margin:0;'>${discounted:,.0f} "
                        f"<span style='font-size:16px; color:#888;text-decoration:line-through;'>"
                        f"${base_monthly:,.0f}</span> /mo</h2>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(f"## ${discounted:,.0f} /mo")
                    
                    st.caption(f"${t['rate']:.2f} per active loan \xb7 min ${t['min_fee']:,}/mo")    
                    st.markdown(f"*~ ${annual:,.0f} billed annually*")
                    st.markdown(" ")

                    st.button(
                        "Get started \u2192",
                        key=f"cta_{name}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary",
                    )
            
            else:
                st.markdown("## Custom")
                st.caption("Tailored to your loan book, volume, and requirements")
                st.markdown(" ")
                st.button("Book a call \u2192", key="cta_pro", use_container_width=True, type="primary" if is_active else "secondary")
            
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
        is_selected = period == billing
        label = ("\u2713  " if is_selected else "") + period.split("  ")[0]  # Strip discount label
        with col:
            st.metric(
                label=label,
                value=f"${effective:,.0f} /mo",
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
