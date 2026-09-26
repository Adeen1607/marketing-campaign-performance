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
