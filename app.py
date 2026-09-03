import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Nykaa Fashion Wishlist Confidence Coach",
    page_icon="💗",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.title("💗 Nykaa Fashion")
st.subheader("Wishlist Confidence Coach")

st.write(
    "An AI-inspired decision-support prototype that helps users "
    "resolve purchase uncertainty before buying a wishlisted fashion item."
)

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("About the MVP")

st.sidebar.write(
    """
This graduation-project prototype focuses on one hypothesis:

Users may add products to their wishlist but delay purchase
because they lack confidence about fit, size and product suitability.
"""
)

st.sidebar.info(
    "Prototype note: Product/review information shown here is "
    "illustrative and does not represent Nykaa Fashion internal data."
)

# -----------------------------
# USER INPUT
# -----------------------------
st.header("1. Tell us about your wishlisted item")

col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input(
        "Product",
        "Linen Wrap Dress"
    )

    category = st.selectbox(
        "Category",
        [
            "Women's Dress",
            "Women's Top",
            "Women's Jeans",
            "Women's Footwear",
            "Men's Shirt",
            "Men's Trousers",
            "Other"
        ]
    )

    price = st.number_input(
        "Price (₹)",
        min_value=0,
        value=2499,
        step=100
    )

with col2:
    size = st.selectbox(
        "Preferred Size",
        ["XS", "S", "M", "L", "XL", "XXL"]
    )

    fit_preference = st.selectbox(
        "Fit Preference",
        [
            "Regular",
            "Relaxed",
            "Slim",
            "Oversized",
            "Not sure"
        ]
    )

    purchase_intent = st.selectbox(
        "How likely are you to purchase?",
        [
            "Very likely",
            "Likely",
            "Not sure",
            "Unlikely"
        ]
    )

st.divider()

# -----------------------------
# REVIEW SIGNALS
# -----------------------------
st.header("2. What are you uncertain about?")

uncertainties = st.multiselect(
    "Select the questions you still have",
    [
        "Will the size fit me?",
        "Is the product true to size?",
        "Will the material look like the photos?",
        "Is the price worth it?",
        "What do other buyers think?",
        "What if I need to return/exchange it?",
        "Is there a better alternative?"
    ],
    default=[
        "Will the size fit me?",
        "What do other buyers think?"
    ]
)

# -----------------------------
# ANALYSIS FUNCTION
# -----------------------------
def calculate_confidence(uncertainties, intent):

    score = 80

    score -= len(uncertainties) * 8

    if intent == "Very likely":
        score += 8
    elif intent == "Likely":
        score += 3
    elif intent == "Not sure":
        score -= 5
    elif intent == "Unlikely":
        score -= 10

    score = max(20, min(score, 95))

    if score >= 75:
        level = "HIGH"
    elif score >= 50:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


# -----------------------------
# ANALYSE BUTTON
# -----------------------------
if st.button(
    "🔍 Check Purchase Confidence",
    type="primary",
    use_container_width=True
):

    score, level = calculate_confidence(
        uncertainties,
        purchase_intent
    )

    st.divider()

    st.header("3. Purchase Confidence")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Confidence Score",
            f"{score}/100"
        )

    with col2:
        st.metric(
            "Confidence Level",
            level
        )

    with col3:
        st.metric(
            "Wishlist Status",
            "High Intent"
        )

    # -----------------------------
    # EXPLANATION
    # -----------------------------
    st.subheader("Why this confidence level?")

    if level == "HIGH":

        st.success(
            f"""
Your confidence to purchase **{product_name}** is relatively high.

You have limited unresolved questions, and your stated purchase
intent is positive.

Recommended action:
**Proceed to purchase after a final check of size and returns.**
"""
        )

    elif level == "MEDIUM":

        st.warning(
            f"""
Your confidence to purchase **{product_name}** is medium.

You still have unresolved questions that may cause you to postpone
the purchase.

Recommended action:
**Resolve the most important uncertainty before purchasing.**
"""
        )

    else:

        st.error(
            f"""
Your confidence to purchase **{product_name}** is low.

Several important questions remain unanswered.

Recommended action:
**Do more research or compare alternatives before purchasing.**
"""
        )

    # -----------------------------
    # UNCERTAINTY BREAKDOWN
    # -----------------------------
    st.subheader("Your unresolved questions")

    if uncertainties:

        for item in uncertainties:
            st.write("🔸", item)

    else:

        st.write(
            "No major uncertainties selected."
        )

    # -----------------------------
    # RECOMMENDATION
    # -----------------------------
    st.subheader("💡 Recommended next action")

    if "Will the size fit me?" in uncertainties:

        st.info(
            "Check size chart + fit-related customer reviews."
        )

    elif "Is the price worth it?" in uncertainties:

        st.info(
            "Compare price with similar saved items before purchasing."
        )

    elif "What do other buyers think?" in uncertainties:

        st.info(
            "Review customer ratings and product-specific feedback."
        )

    else:

        st.info(
            "Your next step should be to resolve the most important "
            "remaining uncertainty before purchasing."
        )

    # -----------------------------
    # PRODUCT DECISION
    # -----------------------------
    st.subheader("🛍️ Decision")

    decision = st.radio(
        "What would you do next?",
        [
            "Buy now",
            "Research more",
            "Compare another wishlist item",
            "Wait"
        ],
        horizontal=True
    )

    st.write(
        f"Your selected next action: **{decision}**"
    )

    # -----------------------------
    # PRODUCT SUMMARY
    # -----------------------------
    st.divider()

    st.subheader("Product Summary")

    summary = pd.DataFrame(
        {
            "Attribute": [
                "Product",
                "Category",
                "Price",
                "Preferred Size",
                "Fit Preference",
                "Purchase Intent"
            ],
            "Value": [
                product_name,
                category,
                f"₹{price:,.0f}",
                size,
                fit_preference,
                purchase_intent
            ]
        }
    )

    st.table(summary)

st.divider()

st.caption(
    "Nykaa Fashion Product Management Graduation Project | "
    "Concept prototype | No internal Nykaa data used"
)
