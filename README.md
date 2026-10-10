# Semantic Compression Proxy

A lightweight HTTP/HTTPS proxy that reduces network data usage by optimizing responses before they reach the client. The project explores the trade-off between bandwidth savings, processing overhead, and latency.

## Project Overview

The Semantic Compression Proxy intercepts network traffic and aims to reduce the size of transmitted content through content-aware optimization.

Inspired by compiler design, the project explores how understanding the structure of content can enable more efficient representations.

Potential optimization targets include:

- HTML, CSS, and JavaScript minification
- Redundant whitespace and formatting
- Image optimization
- Repeated or unnecessary content
- Language-aware transformations that preserve semantics

## Experimental Results

Our experiment demonstrated that the proxy can reduce internet data usage by **up to 27%**.

| Metric | Result |
|---|---|
| Maximum observed data reduction | 27% |
| Equivalent data saved per 100 GB transferred | Up to 27 GB |
| Bandwidth utilization reduction | Up to 27% |

The 27% figure represents the maximum observed reduction, not a guaranteed improvement for every website or user. Actual savings depend on the content processed and the optimizations applied.

## Estimated Annual Data and Cost Savings

To estimate the potential real-world impact, we use India's reported average mobile data consumption of approximately **31 GB per month per user in 2025**, as reported by Nokia's Mobile Broadband Index.

Source: [The Economic Times — India's average monthly mobile data usage per user hits 31 GB in 2025](https://economictimes.indiatimes.com/industry/telecom/indias-average-monthly-mobile-data-usage-per-user-hits-31-gb-in-2025/articleshow/129921729.cms)

This corresponds to an estimated annual average of:

**31 GB × 12 = 372 GB per year**

### Percentile estimates

Publicly reported average usage does not provide the individual-user percentile distribution required for this analysis. Therefore, the following estimates use a log-normal distribution calibrated to a mean of 31 GB/month, with a log-space standard deviation of 0.8.

These are illustrative statistical estimates, not observed population percentiles.

Assumptions:
- Average monthly usage: 31 GB
- Annual usage: monthly usage × 12
- Maximum proxy reduction: 27%
- Data cost: ₹8 per GB saved
- Savings assume the same usage pattern and reduction rate throughout the year.

| User percentile | Estimated annual usage | Data saved/year (27%) | Estimated cost saved/year |
|---|---:|---:|---:|
| 25th percentile | 157.5 GB | 42.5 GB | ₹340 |
| 50th percentile (median) | 270.1 GB | 72.9 GB | ₹583 |
| 75th percentile | 463.4 GB | 125.1 GB | ₹1,001 |
| 90th percentile | 753.1 GB | 203.3 GB | ₹1,627 |
| 99th percentile | 1,737.1 GB | 469.0 GB | ₹3,752 |

### Calculation methodology

For each percentile:

- **Annual usage** = estimated monthly usage × 12
- **Annual data saved** = annual usage × 0.27
- **Annual cost saved** = annual data saved × ₹8

For example, a median user consuming approximately 270.1 GB annually would save:

- Data: 270.1 × 0.27 ≈ 72.9 GB/year
- Cost: 72.9 × ₹8 ≈ ₹583/year

**Important:** These figures represent potential savings at the maximum observed reduction. Actual financial savings depend on the user's tariff. For fixed-price plans with unlimited data or prepaid data allowances, reducing usage may not directly reduce the bill.

## Why This Fits a Compiler Design Project

Compilers analyze source code before transforming it into a more efficient representation. This project applies a similar principle to network content:

1. Inspect incoming responses.
2. Identify redundant or compressible content.
3. Apply suitable content transformations.
4. Measure the resulting reduction in transmitted data.
5. Evaluate the trade-off between bandwidth and latency.

Unlike conventional compression that operates primarily on bytes, semantic optimization exploits knowledge of content structure where applicable.

## Proxy Behavior

The implementation uses `mitmproxy` to intercept HTTP/HTTPS traffic and inspect responses.

The proxy can be extended to support:

- Request and response inspection
- Content-type detection
- Response-body optimization
- Compression ratio measurement
- Bandwidth and latency benchmarking
- Comparison with standard compression algorithms

## Trade-offs

The proxy prioritizes data efficiency over minimum latency.

**Benefits**
- Reduced network traffic
- Potential savings on metered data connections
- More efficient use of limited bandwidth
- Lower transfer requirements for supported content

**Costs**
- Additional processing time
- Potentially higher end-to-end latency
- CPU and memory overhead
- HTTPS interception setup and certificate requirements

## Installation Guide — Semantic Compression Proxy

Repository: [ivanrj7j/compressionProxy](https://github.com/ivanrj7j/compressionProxy). The project uses `uv` and `mitmproxy`.&#x20;




### Step 1: Install prerequisites

Install:

- Git: [Download Git](https://git-scm.com/downloads)
- Python: [Download Python](https://www.python.org/downloads/)
- uv: [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

Verify the installations in CMD or PowerShell:

```
git --version
python --version
uv --version
```

### Step 2: Clone the repository

```
git clone https://github.com/ivanrj7j/compressionProxy.git
cd compressionProxy
```

### Step 3: Install dependencies

Run:

```
uv sync
```

This creates the project environment and installs the dependencies defined in `pyproject.toml` and `uv.lock`.

### Step 4: Start the proxy

Run the following command from the repository directory:

```
uv run mitmdump -s main.py
```

The `-s main.py` argument loads the project's proxy addon.

Keep this terminal open while using the proxy.

### Step 5: Configure your browser

1. Open your browser's network or proxy settings.
2. Configure the HTTP proxy as `127.0.0.1` and port `8080`.
3. Open `http://mitm.it` in the browser.
4. Follow the instructions to install the mitmproxy certificate for HTTPS inspection.&#x20;

   [image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

   GitHub



### Step 6: Test the proxy

Visit a few websites through the configured browser and check the terminal output for intercepted traffic and response statistics.

Compare the transferred data with and without the proxy to evaluate the reduction.

### Step 7: Stop the proxy

Press `Ctrl+C` in the terminal.

Security note: HTTPS interception allows the proxy to inspect encrypted traffic. Use it only on devices and connections you are authorized to inspect, and remove the trusted certificate when it is no longer needed.

## Getting Started

Install the dependencies using `uv` and start the proxy:

```bash
uv run mitmdump -s main.py
```

This starts the `mitmproxy` addon, which can intercept traffic and collect response statistics. Configure the client to use the proxy and install its certificate when HTTPS inspection is required.

## Future Work

- Expand semantic optimization for HTML, CSS, and JavaScript.
- Add image optimization and content-type-specific strategies.
- Benchmark against gzip and Brotli.
- Measure latency and CPU overhead.
- Test across different websites and usage patterns.
- Collect a larger experimental dataset to report average and percentile savings with confidence intervals.
- Validate annual savings using real-world user traffic distributions.

## Summary

The Semantic Compression Proxy explores how content-aware optimization can reduce network traffic. Our experiment observed data-usage reductions of up to 27%, suggesting potential bandwidth and cost benefits.

The annual savings estimates illustrate the possible impact at different usage levels, but rely on a modeled percentile distribution and the maximum observed reduction. Further testing is required to establish representative real-world savings.
