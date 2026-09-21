# Week 6 — Lab 3: Visualization integrity and redesign

**AIDA 2156 | Individual | 5% total | One GitHub/D2L submission**

## Scenario

Northstar Community Clinics is preparing a monthly operations briefing. The
operations manager wants to compare average patient wait time across clinic
sites and decide whether one site needs a process review.

One row in `data/clinic_waits.csv` is one completed patient visit. The data is
fictional.

## Decision question

How do average wait times compare across clinic sites, and what chart design
choices are required for the comparison to be honest and decision-useful?

## Your tasks

1. Confirm the row grain and check missing values in the analysis fields.
2. Calculate a site summary containing count, mean, and median wait time.
3. Create one clear comparison chart with a zero baseline, units, period, and
   an informative title.
4. Include the number of visits for each site so the reader can see the
   denominator.
5. Identify one potential chart-integrity risk or data-context limitation.
6. Write a 150–250 word decision note for the clinic operations manager. Include
   one finding, one practical next step, and one limitation. Do not claim that
   the site causes the observed wait-time difference.

## Required files

Work in your assigned private AIDA 2156 repository. Create this folder there:

```text
week-06-lab-03-chart-integrity/
  analysis/analysis.py
  output/site_wait_summary.csv
  output/wait_time_by_site.png
  output/decision_note.md
```

You may start with `analysis/starter.py`, but rename or copy it to
`analysis/analysis.py` before submitting.

## One submission

1. Make meaningful commits while completing the work.
2. Push the completed Lab 3 folder to your assigned private AIDA 2156
   repository.
3. Submit **one repository link** through the Lab 3 D2L assignment.

The rubric criteria are marking dimensions within one 5% submission. Do not
push work to the instructor Graded Labs repository.
