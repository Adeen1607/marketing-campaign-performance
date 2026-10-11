# Marketing Campaign Performance Analytics

A business-intelligence project for evaluating direct-marketing reach, conversion, contact efficiency, customer segments, and campaign outcomes.

## Business questions

- Which customer segments produce the highest term-deposit conversion?
- Which channels, months, and contact strategies perform best?
- How does repeated contact affect conversion and customer fatigue?
- What is the relationship between call duration and outcome, and why must it not be treated as a pre-contact targeting feature?
- Where should campaign managers concentrate follow-up effort?

## Data source

The project uses the [Bank Marketing dataset from the UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing). It describes direct-marketing phone campaigns conducted by a Portuguese banking institution.

## Deliverables

- official-source data download;
- validated customer-contact fact table;
- campaign, segment, channel, and monthly KPI exports;
- Power BI measures and dashboard specification;
- explicit leakage warning for call duration;
- reproducible tests and documented assumptions.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/download_data.py
python src/build_model.py
pytest
```

## Dashboard pages

1. Campaign executive overview
2. Audience and customer segments
3. Contact-channel performance
4. Conversion funnel and contact frequency
5. Timing and seasonality
6. Data quality and leakage controls

## Interpretation

The target indicates whether a client subscribed after the campaign. Call duration is only known after a call finishes, so it can explain completed campaign outcomes but must not be used as a feature for pre-call targeting. The project reports associations rather than claiming that a channel or customer attribute caused conversion.


## Rebuild the reading edition

```bash
python -m pip install -r requirements-research.txt
python scripts/build_research_site.py
```

This renders saved notebook outputs without rerunning model training or external APIs. To refresh findings, run the analysis commands above first, update `reports/research-findings.md`, and rebuild.

<!-- research-edition:start -->
## Research edition

[Research report and final visual results](research/report.md) · [Browser-ready notebook catalogue](research/notebooks.html)

Fresh execution on 11 October 2026. The **45,211 contact records** contain **5,289 subscriptions**, an observed conversion rate of **11.70%**. Channel rates vary, but selection differences prevent a causal claim that one channel improves conversion. Month categories pool years; the chart is a calendar-month comparison, not a time trend.

| contact | contacts | conversions | conversion_rate |
|---|---|---|---|
| cellular | 29285 | 4369 | 0.1491890046098685 |
| telephone | 2906 | 390 | 0.1342050929112181 |
| unknown | 13020 | 530 | 0.0407066052227342 |



The `research/` folder contains a professional static reading edition. The Pages workflow deploys it after GitHub Pages is enabled with **GitHub Actions** as the publishing source. Intended URL: `https://adeen1607.github.io/marketing-campaign-performance/`. Deployment status must be checked in Actions before treating that address as live.

<!-- research-edition:end -->
