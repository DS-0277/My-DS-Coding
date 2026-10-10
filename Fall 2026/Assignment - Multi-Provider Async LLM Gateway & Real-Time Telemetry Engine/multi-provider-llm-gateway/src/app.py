import asyncio

import streamlit as st

from gateway import (
    GatewayAuthenticationError,
    GatewayProviderError,
    GatewayRateLimitError,
    UnifiedLLMGateway,
)
from pricing import PRICING_PER_MILLION_TOKENS


st.set_page_config(
    page_title="Multi-Provider LLM Gateway",
    page_icon="🤖",
    layout="wide",
)


@st.cache_resource
def get_gateway() -> UnifiedLLMGateway:
    return UnifiedLLMGateway()


async def run_stream(
    prompt: str,
    model: str,
    temperature: float,
):
    gateway = get_gateway()

    response_text = ""
    final_telemetry = None

    async for chunk in gateway.stream(
        prompt=prompt,
        model=model,
        temperature=temperature,
    ):
        if chunk.is_final:
            final_telemetry = chunk.telemetry
        else:
            response_text += chunk.delta_text
            yield response_text, final_telemetry

    yield response_text, final_telemetry


def run_async_stream(
    prompt: str,
    model: str,
    temperature: float,
):
    async def collect_results():
        results = []

        async for response_text, telemetry in run_stream(
            prompt=prompt,
            model=model,
            temperature=temperature,
        ):
            results.append((response_text, telemetry))

        return results

    return asyncio.run(collect_results())


st.title("Multi-Provider Async LLM Gateway")
st.write(
    "Select an LLM provider model, enter a prompt, and view streaming output with telemetry."
)

with st.sidebar:
    st.header("Settings")

    model = st.selectbox(
        "Model",
        options=list(PRICING_PER_MILLION_TOKENS.keys()),
    )

    provider = PRICING_PER_MILLION_TOKENS[model]["provider"]

    st.write(f"Provider: `{provider}`")

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
    )

    st.divider()

    st.subheader("Telemetry")

    ttft_box = st.empty()
    speed_box = st.empty()
    input_tokens_box = st.empty()
    output_tokens_box = st.empty()
    total_tokens_box = st.empty()
    cost_box = st.empty()


prompt = st.text_area(
    "Prompt",
    value="Explain artificial intelligence in simple terms.",
    height=150,
)

submit = st.button("Run Prompt")

response_area = st.empty()

if submit:
    if not prompt.strip():
        st.error("Please enter a prompt.")

    else:
        try:
            response_area.markdown("")

            results = run_async_stream(
                prompt=prompt,
                model=model,
                temperature=temperature,
            )

            latest_text = ""
            final_telemetry = None

            for response_text, telemetry in results:
                latest_text = response_text
                final_telemetry = telemetry
                response_area.markdown(latest_text)

            if final_telemetry is not None:
                ttft_box.metric(
                    "TTFT",
                    f"{final_telemetry.ttft_ms:.2f} ms",
                )

                speed_box.metric(
                    "Tokens / second",
                    f"{final_telemetry.tokens_per_second:.2f}",
                )

                input_tokens_box.metric(
                    "Prompt tokens",
                    final_telemetry.input_tokens,
                )

                output_tokens_box.metric(
                    "Completion tokens",
                    final_telemetry.output_tokens,
                )

                total_tokens_box.metric(
                    "Total tokens",
                    final_telemetry.total_tokens,
                )

                cost_box.metric(
                    "Cost",
                    f"${final_telemetry.total_cost_usd:.6f}",
                )

        except GatewayAuthenticationError as error:
            st.error(str(error))

        except GatewayRateLimitError as error:
            st.error(str(error))

        except GatewayProviderError as error:
            st.error(str(error))

        except ValueError as error:
            st.error(str(error))