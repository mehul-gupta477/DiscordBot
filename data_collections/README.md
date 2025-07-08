# Data-Collections Documentation

## Purpose

This directory of the project focuses on how data is collected and managed. Data is extracted from various sources using automated scripts via our YAML GitHub Workflows. Once gathered, the data is  formatted and stored into our `runningCSV.csv`, making it easy for our data-processing sub-team to utilize.

In this document you will understand how our data is stored after being extracted from these various sources. This document is mainly for our data-processing sub-team to understand our storage containers.

## RunningCSV Format

Below is how the `runningCSV.csv` file is formatted

| Type | Title | Description | whenDate | pubDate | Location | link | entryDate
| --- | --- | --- | --- | --- | --- | --- | --- |
| An indicator to seperate what type of career development data this is. The options are [Event, Job, Internship] | The title of the Event, Job or Internship. These can vary in meaning depending on the type. Please read on for clarification. | The Description of the Event, Job, or Internship. These can vary in meaning depending on the type. Please read on for clarification. | The whenDate is mostly for Events as to when the event is. If the whenDate is specified for Internships or Jobs, it's the deadline to apply for said job. | pubDate is specified as the Event, Job, or Internship's published date on the data source's website. | The Location of the Event, Job, or Internship. | The embed link to the Event, Job, or Internship Page | The Date that the Item (Job,Internship, or Job) was extracted and stored into our system.

