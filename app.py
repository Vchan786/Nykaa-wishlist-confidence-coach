import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nykaa Fashion Wishlist Confidence Coach",
    page_icon="💗",
    layout="wide"
)

st.title("💗 Nykaa Fashion")
st.subheader("Wishlist Confidence Coach")

st.write(
    "An AI-assisted decision-support prototype that helps high-intent "
    "wishlist shoppers resolve price and product-confidence barriers before purchasing."
)

st.info(
    "Research-backed prototype: exploratory research (survey n=10 + interviews n=5). "
    "Product, price and review signals shown below are illustrative and do not represent live Nykaa data."
)

st.divider()

st.sidebar.header("About the MVP")
st.sidebar.write(
    """This MVP addresses the research-backed problem hypothesis:

High-intent wishlist shoppers postpone purchasing because they lack timely price and
product-confidence signals such as discounts, fit/quality information, reviews and decision support."""
)

st.sidebar.markdown("### Research signals")
st.sidebar.write("💰 Price/discount was a major purchase blocker.")
st.sidebar.write("👗 Fit/quality/returns created purchase uncertainty.")
st.sidebar.write("⭐ Reviews and social proof influenced confidence.")
st.sidebar.write("🔄 Many shoppers compare other apps/sites.")
st.sidebar.write("⏰ Generic reminders were not consistently effective.")
st.sidebar.caption("Concept prototype | No internal Nykaa data or live product API used")

st.header("1. Select your wishlisted item")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Product", "Linen Wrap Dress")
    category = st.selectbox(
        "Category",
        ["Women's Dress", "Women's Top", "Women's Jeans", "Women's Footwear",
         "Men's Shirt", "Men's Trousers", "Other"]
    )
    price = st.number_input("Current Price (₹)", min_value=0, value=2499, step=100)

with col2:
    size = st.selectbox("Preferred Size", ["XS", "S", "M", "L", "XL", "XXL"])
    fit_preference = st.selectbox(
        "Fit Preference", ["Regular", "Relaxed", "Slim", "Oversized", "Not sure"]
    )
    purchase_intent = st.selectbox(
        "How likely are you to purchase?",
        ["Very likely", "Likely", "Not sure", "Unlikely"]
    )

st.divider()

st.header("2. Product signals")
st.caption(
    "These signals are simulated for the MVP demonstration. "
    "A production version would connect to real product/review/price APIs."
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    rating = st.slider("Illustrative rating", 1.0, 5.0, 4.2, 0.1)
with c2:
    review_count = st.number_input("Illustrative review count", min_value=0, value=128, step=10)
with c3:
    discount = st.slider("Illustrative discount (%)", 0, 70, 10, 5)
with c4:
    stock_status = st.selectbox("Illustrative stock signal", ["In stock", "Low stock", "Out of stock"])

st.divider()

st.header("3. What are you uncertain about?")

uncertainties = st.multiselect(
    "Select the questions you still have",
    [
        "Will the size fit me?",
        "Is the product true to size?",
        "Will the material look like the photos?",
        "Is the price worth it?",
        "Should I wait for a discount?",
        "What do other buyers think?",
        "What if I need to return/exchange it?",
        "Is there a better alternative?",
        "Am I buying this because I really need it?"
    ],
    default=[
        "Will the size fit me?",
        "What do other buyers think?",
        "Is the price worth it?"
    ]
)

def calculate_confidence(uncertainties, intent, rating, review_count, discount, stock_status):
    score = 78
    score -= len(uncertainties) * 6

    if intent == "Very likely":
        score += 10
    elif intent == "Likely":
        score += 5
    elif intent == "Not sure":
        score -= 5
    elif intent == "Unlikely":
        score -= 12

    if rating >= 4.3:
        score += 5
    elif rating < 3.5:
        score -= 6

    if review_count >= 100:
        score += 3
    elif review_count < 20:
        score -= 3

    if discount >= 20:
        score += 5
    elif discount == 0 and (
        "Is the price worth it?" in uncertainties or
        "Should I wait for a discount?" in uncertainties
    ):
        score -= 5

    if stock_status == "Low stock":
        score += 2
    elif stock_status == "Out of stock":
        score -= 8

    score = max(20, min(score, 95))

    if score >= 75:
        level = "HIGH"
    elif score >= 50:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level

def get_recommendation(uncertainties, discount, stock_status):
    if ("Will the size fit me?" in uncertainties or
        "Is the product true to size?" in uncertainties):
        return "Check Fit & Size", "Review the size chart and fit-related customer reviews before purchasing."

    if ("What do other buyers think?" in uncertainties or
        "Will the material look like the photos?" in uncertainties):
        return "Check Reviews", "Read product-specific reviews, especially comments about material, fit and real-life appearance."

    if ("Should I wait for a discount?" in uncertainties or
        "Is the price worth it?" in uncertainties):
        if discount < 15:
            return "Consider Waiting", "Price is still an unresolved blocker. In this prototype, waiting for a relevant offer may be more appropriate."
        return "Buy Now", "The current illustrative discount reduces the price barrier. Complete a final fit/return check before purchasing."

    if "Is there a better alternative?" in uncertainties:
        return "Compare Alternatives", "Compare this item with other saved items on price, fit, quality and reviews before deciding."

    if stock_status == "Low stock":
        return "Buy Now", "The illustrative stock signal is low. If confidence is already high, consider completing the purchase after a final check."

    return "Buy Now", "Your major uncertainties are relatively limited. Complete a final size and return-policy check."

def get_reasons(uncertainties, discount, rating, review_count):
    reasons = []

    if "Is the price worth it?" in uncertainties or "Should I wait for a discount?" in uncertainties:
        reasons.append(
            "Current price is an unresolved barrier." if discount < 15
            else "Current illustrative discount reduces price friction."
        )

    if "Will the size fit me?" in uncertainties or "Is the product true to size?" in uncertainties:
        reasons.append("Fit/size confidence still needs validation.")

    if "What do other buyers think?" in uncertainties or "Will the material look like the photos?" in uncertainties:
        reasons.append(
            "Review signals provide useful product confidence."
            if rating >= 4.0 and review_count >= 50
            else "More social proof may be needed."
        )

    if "Is there a better alternative?" in uncertainties:
        reasons.append("Comparison may delay the purchase decision.")

    return reasons or ["Few major purchase barriers were selected."]

if st.button("🔍 Analyse My Purchase Confidence", type="primary", use_container_width=True):

    score, level = calculate_confidence(
        uncertainties, purchase_intent, rating, review_count, discount, stock_status
    )
    recommendation, recommendation_detail = get_recommendation(
        uncertainties, discount, stock_status
    )
    reasons = get_reasons(uncertainties, discount, rating, review_count)

    st.divider()
    st.header("4. Purchase Confidence")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Confidence Score", f"{score}/100")
    with m2:
        st.metric("Confidence Level", level)
    with m3:
        st.metric("Purchase Intent", purchase_intent)

    st.subheader("Why is my confidence at this level?")
    for reason in reasons:
        st.write("🔸", reason)

    st.subheader("💡 Recommended next action")
    if recommendation == "Buy Now":
        st.success(f"**{recommendation}**")
    elif recommendation == "Consider Waiting":
        st.warning(f"**{recommendation}**")
    else:
        st.info(f"**{recommendation}**")
    st.write(recommendation_detail)

    st.subheader("🔎 Decision-support signals")
    e1, e2 = st.columns(2)

    with e1:
        st.write("**Price signal**")
        if discount >= 20:
            st.success(f"Illustrative discount: {discount}%")
        elif discount > 0:
            st.info(f"Illustrative discount: {discount}%")
        else:
            st.warning("No illustrative discount currently shown.")

        st.write("**Product confidence**")
        st.write(f"Rating: ⭐ {rating}/5")
        st.write(f"Reviews: {review_count}")

    with e2:
        st.write("**Fit context**")
        st.write(f"Preferred size: **{size}**")
        st.write(f"Fit preference: **{fit_preference}**")
        st.write("**Availability**")
        st.write(f"Illustrative stock status: **{stock_status}**")

    st.subheader("🛍️ Your decision")
    decision = st.radio(
        "What would you do next?",
        ["Buy now", "Check fit / size", "Check reviews",
         "Wait for a better price", "Compare alternatives"],
        horizontal=True
    )
    st.write(f"Your selected next action: **{decision}**")

    st.divider()
    st.subheader("Product Summary")

    summary = pd.DataFrame({
        "Attribute": [
            "Product", "Category", "Current Price", "Preferred Size",
            "Fit Preference", "Purchase Intent", "Illustrative Discount",
            "Illustrative Rating", "Illustrative Reviews", "Illustrative Stock"
        ],
        "Value": [
            product_name, category, f"₹{price:,.0f}", size, fit_preference,
            purchase_intent, f"{discount}%", f"{rating}/5", review_count, stock_status
        ]
    })
    st.table(summary)

    st.subheader("📊 Product experiment signal")
    st.write(
        "For a production experiment, these interactions would be logged as decision-support events."
    )
    events = pd.DataFrame({
        "Event": ["Coach viewed", "Confidence calculated", "Recommendation shown", "Decision selected"],
        "Status": ["Yes", "Yes", recommendation, decision]
    })
    st.table(events)

st.divider()
st.caption(
    "Nykaa Fashion Product Management Graduation Project | "
    "AI-assisted concept prototype | Exploratory research n=10 survey + n=5 interviews | "
    "No internal Nykaa data used"
)
