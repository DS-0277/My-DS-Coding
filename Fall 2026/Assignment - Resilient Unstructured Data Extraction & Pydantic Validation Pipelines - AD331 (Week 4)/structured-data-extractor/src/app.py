import asyncio

import streamlit as st
from bs4 import BeautifulSoup
from pypdf import PdfReader

from extractor import extract_with_retry


st.set_page_config(
    page_title="Structured Data Extractor",
    layout="wide",
)

st.markdown("""
<style>
    .block-container { max-width: 1180px; padding-top: 2rem; }
    .hero { padding: 1.4rem 1.6rem; border-radius: 14px; background: linear-gradient(120deg, #12233f, #1b5e75); color: white; margin-bottom: 1.4rem; }
    .hero h1 { margin: 0; font-size: 2rem; }
    .hero p { margin: .4rem 0 0; color: #d9edf7; }
    .caption { color: #617085; font-size: .9rem; }
</style>
<div class="hero"><h1>Resilient Invoice Extractor</h1><p>Upload a messy PDF or paste invoice HTML, then inspect the validated data and recovery audit trail.</p></div>
""", unsafe_allow_html=True)


# -----------------------------
# Input section
# -----------------------------

with st.sidebar:
    st.header("Controls")
    reflection_enabled = st.toggle(
        "Enable reflection loop",
        value=True,
        help="Allow up to three extraction attempts, including corrective retries.",
    )
    if st.button("Simulate Edge Case Failure", use_container_width=True):
        st.session_state.simulate_failure = True
    if st.session_state.get("simulate_failure"):
        st.warning("The next extraction will intentionally route to the failure path.")

source_column, paste_column = st.columns(2)
with source_column:
    uploaded_file = st.file_uploader("Upload a messy PDF invoice", type=["pdf"])
with paste_column:
    pasted_text = st.text_area("Or paste raw invoice text / HTML", height=160)


# -----------------------------
# Extract PDF text
# -----------------------------

def extract_pdf_text(file) -> str:
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def normalize_pasted_input(value: str) -> str:
    """Convert pasted HTML to readable source text while preserving plain text."""
    if "<" in value and ">" in value:
        return BeautifulSoup(value, "html.parser").get_text("\n", strip=True)
    return value


# -----------------------------
# Determine input text
# -----------------------------

raw_text = ""

if uploaded_file is not None:
    raw_text = extract_pdf_text(
        uploaded_file
    )

elif pasted_text.strip():
    raw_text = normalize_pasted_input(pasted_text)


# -----------------------------
# Run extraction
# -----------------------------

if st.button("Run Extraction", type="primary", use_container_width=True):

    simulate_failure = st.session_state.pop(
        "simulate_failure",
        False,
    )

    if not raw_text and not simulate_failure:
        st.warning(
            "Please upload a PDF or paste invoice text."
        )

    else:

        if simulate_failure:
            raw_text = (
                "THIS IS INTENTIONALLY INVALID DATA "
                "FOR DLQ TESTING."
            )

        if reflection_enabled:
            max_retries = 3
        else:
            max_retries = 1

        with st.spinner("Extracting invoice data..."):

            result = asyncio.run(
                extract_with_retry(
                    raw_text=raw_text,
                    max_retries=max_retries,
                    simulate_failure=simulate_failure,
                )
            )


        # -----------------------------
        # Side-by-side view
        # -----------------------------

        left_column, right_column = st.columns(2)

        with left_column:
            st.subheader("Raw Document")

            st.text_area(
                "Input",
                raw_text,
                height=400,
            )

        with right_column:
            st.subheader("Validated JSON")

            if result.validated_data:
                st.json(
                    result.validated_data.model_dump(
                        mode="json"
                    )
                )

            else:
                st.error(
                    "No validated invoice was produced."
                )


        # -----------------------------
        # Execution status
        # -----------------------------

        st.subheader("Execution Status")

        if result.execution_status == "SUCCESS":
            st.success(
                "SUCCESS - Invoice validated "
                "on the first attempt."
            )

        elif (
            result.execution_status
            == "REPAIRED_VIA_REFLECTION"
        ):
            st.warning(
                "REPAIRED VIA REFLECTION - "
                "The invoice required correction."
            )

        else:
            st.error(
                "DLQ FAILED - Extraction could "
                "not be repaired."
            )


        # -----------------------------
        # Reconciliation badge
        # -----------------------------

        st.subheader("Reconciliation")

        if result.validated_data:

            invoice = result.validated_data

            calculated_total = (
                sum(
                    item.line_total
                    for item in invoice.line_items
                )
                + invoice.tax_amount
            )

            difference = abs(
                calculated_total
                - invoice.total_amount
            )

            if difference <= 0.02:
                st.success(
                    "Line items and tax match "
                    "the grand total."
                )

            else:
                st.error(
                    "Invoice totals do not reconcile."
                )


        # -----------------------------
        # Audit log
        # -----------------------------

        st.subheader("Audit Log")

        st.write(
            f"Attempts used: {result.attempts_used}"
        )

        if result.error_log:

            for index, error in enumerate(
                result.error_log,
                start=1,
            ):
                with st.expander(
                    f"Validation Error {index}"
                ):
                    st.code(error)

        else:
            st.write(
                "No validation errors occurred."
            )

        if result.corrective_prompts:
            st.markdown("#### Corrective Prompts Dispatched")
            for index, prompt in enumerate(result.corrective_prompts, start=1):
                with st.expander(f"Corrective Prompt {index}"):
                    st.code(prompt, language="text")
