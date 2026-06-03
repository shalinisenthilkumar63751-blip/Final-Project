import streamlit as st

from modules.claim_decomposition import decompose_claims
from modules.claim_scoring import score_claims
from modules.claim_verification import verify_claims
from modules.correction_module import correct_claims
from modules.evidence_retrieval import retrieve_evidence
from modules.output_module import display_results
from modules.query_generation import generate_queries


def analyze_summary(summary_text):
    claims = decompose_claims(summary_text)
    analysis_results = []

    for claim in claims:
        search_query = generate_queries(claim)
        evidence_items = retrieve_evidence(claim, search_query)
        verification_result = verify_claims(claim, evidence_items)
        verification_status = verification_result["status"]
        confidence_score = score_claims(
            verification_status,
            verification_result.get("similarity_score", 0.0),
            verification_result.get("best_relevance_score", 0),
        )
        correction_result = correct_claims(claim, verification_status, evidence_items)

        analysis_results.append(
            {
                "claim": claim,
                "query": search_query,
                "evidence": evidence_items,
                "verification": verification_status,
                "verification_reason": verification_result["reason"],
                "score": confidence_score,
                "corrected": correction_result["correction"],
                "output": correction_result["output"],
            }
        )

    return analysis_results

st.set_page_config(page_title="MedVerify", layout="wide")

st.title("Factual Hallucination Detection in Medical Summaries")
st.markdown("---")

summary = st.text_area(
    "Enter Medical Summary:",
    height=200,
    placeholder="e.g., Diabetes is cured by insulin...",
)

if st.button("Analyze Summary"):
    if summary:
        with st.spinner("Processing..."):
            results = analyze_summary(summary)
            display_results(summary, results)
    else:
        st.warning("Please enter a summary first.")






