# Semantic Compression Proxy

This project is a lightweight HTTP proxy designed to reduce the amount of data transmitted over the network by compressing incoming payloads before they are forwarded. The tradeoff is intentional: lower bandwidth usage comes at the cost of higher latency because the proxy spends extra time analyzing and compressing the data.

## Project idea

The core concept is simple: a proxy sits in the middle of client-server communication and tries to shrink payloads that are expensive to send. This is particularly useful for environments with limited bandwidth, slow mobile connections, or scenarios where transfer size matters more than raw response time.

In this project, the compression is inspired by compiler design. Instead of treating the payload as plain text, the proxy can analyze the structure of source-like content and exploit semantic redundancy. The goal is to compress code by understanding patterns such as:

- repeated identifiers and declarations
- redundant whitespace and formatting
- common syntactic structures
- code that can be represented more compactly without changing meaning
- language-aware transformations that preserve semantics while reducing size

This makes it a micro-project for exploring the intersection of networking, data compression, and compiler analysis.

## Why this fits a compiler design project

A compiler already performs semantic and syntactic analysis to understand meaning before generating optimized output. This project applies a similar idea to data transmission:

- parse incoming content as structured code or code-like text
- identify redundant or derivable information
- encode it using a smaller, semantically equivalent representation
- decode it on the receiving side when needed

This is not a general-purpose compression engine; it is a focused demonstration of how semantic analysis can be used to compress code more intelligently than standard byte-level compression alone.

## Proxy behavior

The current implementation uses `mitmproxy` to intercept HTTP traffic and log request metadata, response size, and content type. This gives the project a solid foundation for adding compression logic later.

The proxy can be extended to:

- inspect request or response bodies
- detect code-heavy payloads
- apply semantic-aware compression
- measure compression ratio and latency impact
- compare naive compression with semantic compression

## Tradeoff: lower data usage vs. more latency

This project intentionally favors data efficiency over speed.

- Benefits: less network traffic, better use of limited bandwidth, lower cost in mobile or constrained environments
- Cost: extra processing time, higher end-to-end latency, more CPU usage in the proxy

This mirrors a real-world design decision in networking and compiler optimization: sometimes a more expensive transformation is worth it if it saves enough bandwidth.

## Getting started

Install dependencies with `uv` and run the proxy:

```bash
uv run mitmdump -s main.py
```

This starts a local MITM proxy that captures HTTP traffic and logs the size of each response for analysis.

## Future extensions

Possible next steps for the project include:

- semantic compression for source-code payloads
- lightweight syntax-aware tokenization
- JSON or XML payload optimization
- latency and bandwidth benchmarking
- comparison against standard gzip or brotli strategies
- a decoder on the client side to restore the original data

## Summary

This is a micro compiler-design project that treats a proxy as a place where semantic analysis can be applied to reduce payload size. The result is a system that saves network data at the expense of additional latency, making it a useful exploration of optimization tradeoffs in both compiler theory and network design.
